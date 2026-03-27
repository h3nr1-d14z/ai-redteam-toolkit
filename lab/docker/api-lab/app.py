"""
Vulnerable API Lab — AI RedTeam Toolkit
Deliberately insecure REST + GraphQL API. DO NOT deploy in production.
Vulnerabilities marked with [VULN-XX] comments.
"""
import os, jwt, datetime, psycopg2, psycopg2.extras
from functools import wraps
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

# [VULN-01] CORS Wildcard — allows any origin to make authenticated requests
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# [VULN-02] Weak JWT Secret — trivially brute-forceable
JWT_SECRET = os.environ.get("JWT_SECRET", "secret123")

# [VULN-03] Hardcoded API Key leaked in response headers
API_KEY = os.environ.get("API_KEY", "sk-live-vuln-lab-key-do-not-use-in-prod")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://apiuser:apipass123@db:5432/apilab")

# --- Database helpers ---

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(DATABASE_URL)
        g.db.autocommit = True
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL, email VARCHAR(200),
            role VARCHAR(20) DEFAULT 'user', ssn VARCHAR(20) DEFAULT '000-00-0000',
            created_at TIMESTAMP DEFAULT NOW())""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users(id),
            title VARCHAR(300), body TEXT, created_at TIMESTAMP DEFAULT NOW())""")
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (username, password, email, role, ssn) VALUES
            ('admin','admin123','admin@vuln-lab.local','admin','123-45-6789'),
            ('alice','password1','alice@vuln-lab.local','user','987-65-4321'),
            ('bob','letmein','bob@vuln-lab.local','user','111-22-3333'),
            ('carol','carol2024','carol@vuln-lab.local','user','444-55-6666')""")
        cur.execute("""
            INSERT INTO posts (user_id, title, body) VALUES
            (1,'Welcome','Welcome to the vulnerable API lab!'),
            (2,'Hello','This is Alice''s first post.'),
            (3,'Test','Bob checking in.')""")
    cur.close(); conn.close()

# --- Auth helpers ---

def create_token(user_id, username, role):
    payload = {"user_id": user_id, "username": username, "role": role,
               "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")  # [VULN-02]

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token required"}), 401
        try:
            g.current_user = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

@app.after_request
def add_headers(response):
    response.headers["X-API-Key"] = API_KEY       # [VULN-03] API key in every response
    response.headers["X-Powered-By"] = "VulnLabAPI/1.0"
    return response

def _serialize(rows):
    """Convert datetime fields for JSON serialization."""
    for r in (rows if isinstance(rows, list) else [rows]):
        if "created_at" in r: r["created_at"] = str(r["created_at"])
    return rows

# --- Routes ---

@app.route("/")
def index():
    return jsonify({"name": "Vulnerable API Lab", "version": "1.0.0",
        "endpoints": ["POST /api/login","GET /api/users","GET /api/users/<id>",
            "POST /api/users","PUT /api/users/<id>","GET /api/posts",
            "POST /api/posts","GET /api/search?q=","GET /graphql"]})

# [VULN-04] No rate limiting on login — brute force possible
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, username, password, role FROM users WHERE username=%s AND password=%s",
                (data.get("username",""), data.get("password","")))
    user = cur.fetchone(); cur.close()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_token(user["id"], user["username"], user["role"])
    return jsonify({"token": token, "user_id": user["id"], "role": user["role"]})

# [VULN-05] Excessive Data Exposure — returns password & SSN for ALL users
# [VULN-06] IDOR — any authenticated user can access any user record by ID
@app.route("/api/users", methods=["GET"])
@token_required
def list_users():
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users ORDER BY id")  # [VULN-05] SELECT * exposes sensitive cols
    users = cur.fetchall(); cur.close()
    return jsonify(_serialize(users))

@app.route("/api/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """[VULN-06] IDOR — no check that requesting user owns this record."""
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone(); cur.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(_serialize(user))

# [VULN-07] Mass Assignment — client can set `role` to escalate privileges
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    role = data.get("role", "user")  # [VULN-07] Role from user input, no restriction
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("INSERT INTO users (username,password,email,role,ssn) VALUES (%s,%s,%s,%s,%s) RETURNING *",
                    (username, password, data.get("email",""), role, data.get("ssn","000-00-0000")))
        new_user = cur.fetchone(); cur.close()
        return jsonify(_serialize(new_user)), 201
    except psycopg2.errors.UniqueViolation:
        cur.close()
        return jsonify({"error": "Username already exists"}), 409

@app.route("/api/users/<int:user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    """[VULN-06] IDOR + [VULN-07] Mass assignment on update."""
    data = request.get_json(force=True, silent=True) or {}
    fields, values = [], []
    for col in ("username","password","email","role","ssn"):
        if col in data:
            fields.append(f"{col}=%s"); values.append(data[col])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(user_id)
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(f"UPDATE users SET {','.join(fields)} WHERE id=%s RETURNING *", values)
    updated = cur.fetchone(); cur.close()
    if not updated:
        return jsonify({"error": "User not found"}), 404
    return jsonify(_serialize(updated))

# [VULN-08] SQL Injection — user input concatenated into query
@app.route("/api/search", methods=["GET"])
@token_required
def search():
    q = request.args.get("q", "")
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = f"SELECT id,username,email,role FROM users WHERE username LIKE '%{q}%'"  # [VULN-08]
    try:
        cur.execute(query); results = cur.fetchall()
    except Exception as e:
        results = {"sql_error": str(e), "query": query}
    cur.close()
    return jsonify(results)

# [VULN-09] No input validation on posts — no length/content checks, stored XSS possible
@app.route("/api/posts", methods=["GET"])
def list_posts():
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT p.*,u.username FROM posts p JOIN users u ON p.user_id=u.id ORDER BY p.id")
    posts = cur.fetchall(); cur.close()
    return jsonify(_serialize(posts))

@app.route("/api/posts", methods=["POST"])
@token_required
def create_post():
    """[VULN-09] No sanitization or length check on title/body."""
    data = request.get_json(force=True, silent=True) or {}
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("INSERT INTO posts (user_id,title,body) VALUES (%s,%s,%s) RETURNING *",
                (g.current_user["user_id"], data.get("title",""), data.get("body","")))
    post = cur.fetchone(); cur.close()
    return jsonify(_serialize(post)), 201

# --- [VULN-10] GraphQL with introspection enabled ---

class UserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    role = graphene.String()
    password = graphene.String()   # [VULN-05] Sensitive fields in GraphQL schema
    ssn = graphene.String()

class PostType(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.Int()
    title = graphene.String()
    body = graphene.String()

def _gql_query(sql):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql); rows = cur.fetchall(); cur.close(); conn.close()
    return rows

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    all_posts = graphene.List(PostType)

    def resolve_all_users(self, info):
        return [UserType(**u) for u in _gql_query("SELECT * FROM users")]

    def resolve_user(self, info, id):
        rows = _gql_query(f"SELECT * FROM users WHERE id={id}")
        return UserType(**rows[0]) if rows else None

    def resolve_all_posts(self, info):
        return [PostType(**p) for p in _gql_query("SELECT * FROM posts")]

schema = graphene.Schema(query=Query)
# [VULN-10] Introspection enabled — full schema discoverable
app.add_url_rule("/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

# --- Entrypoint ---

if __name__ == "__main__":
    print("[*] Initializing database..."); init_db()
    print("[*] Vulnerable API Lab running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
