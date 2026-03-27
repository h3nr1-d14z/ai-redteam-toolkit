# Vulnerable API Lab

A deliberately vulnerable REST + GraphQL API built with Python Flask for practicing API security testing techniques.

> **WARNING**: This application is intentionally insecure. Never deploy it on a public network or in production.

## Quick Start

```bash
# Start the lab
docker compose up --build -d

# Verify it's running
curl http://localhost:5000/

# Stop the lab
docker compose down -v
```

The API will be available at `http://localhost:5000` and PostgreSQL at `localhost:5432`.

## Default Credentials

| Username | Password   | Role  |
|----------|------------|-------|
| admin    | admin123   | admin |
| alice    | password1  | user  |
| bob      | letmein    | user  |
| carol    | carol2024  | user  |

## Endpoints

| Method | Endpoint           | Auth Required | Description          |
|--------|--------------------|---------------|----------------------|
| POST   | /api/login         | No            | Get JWT token        |
| GET    | /api/users         | Yes           | List all users       |
| GET    | /api/users/\<id\>  | Yes           | Get user by ID       |
| POST   | /api/users         | No            | Register new user    |
| PUT    | /api/users/\<id\>  | Yes           | Update user          |
| GET    | /api/posts         | No            | List all posts       |
| POST   | /api/posts         | Yes           | Create a post        |
| GET    | /api/search?q=     | Yes           | Search users         |
| GET    | /graphql           | No            | GraphQL endpoint     |

## Authentication

```bash
# Login to get a token
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password1"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Use the token
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/users
```

## Vulnerabilities to Find

There are **10 intentional vulnerabilities** in this lab. Each is marked with a `[VULN-XX]` comment in the source code.

| #  | Vulnerability                  | Difficulty | Endpoint             | Hint                                       |
|----|--------------------------------|------------|----------------------|--------------------------------------------|
| 01 | CORS Wildcard                  | Easy       | All /api/*           | Check response headers                     |
| 02 | Weak JWT Secret                | Easy       | /api/login           | Try cracking the token with common secrets |
| 03 | API Key Leaked in Headers      | Easy       | All responses        | Inspect response headers carefully         |
| 04 | No Rate Limiting on Login      | Easy       | /api/login           | Try brute-forcing with a wordlist          |
| 05 | Excessive Data Exposure        | Easy       | /api/users           | Look at what fields are returned           |
| 06 | IDOR                           | Medium     | /api/users/\<id\>    | Access another user's data with your token |
| 07 | Mass Assignment                | Medium     | POST/PUT /api/users  | Send extra fields in the JSON body         |
| 08 | SQL Injection                  | Medium     | /api/search?q=       | Classic string-based SQLi                  |
| 09 | No Input Validation            | Easy       | /api/posts           | Submit unexpected content/lengths          |
| 10 | GraphQL Introspection Enabled  | Medium     | /graphql             | Run an introspection query                 |

## Exercise Suggestions

### Beginner
1. Use `curl` or Burp Suite to inspect all response headers. What sensitive data is leaked?
2. Log in as `alice`, then try to read `admin`'s profile at `/api/users/1`.
3. Register a new user with `role=admin` in the JSON body.

### Intermediate
4. Crack the JWT secret using `hashcat` or `jwt_tool`.
5. Exploit the SQL injection on `/api/search?q=` to dump all user passwords.
6. Use GraphQL introspection to discover the full schema and extract sensitive data.

### Advanced
7. Chain multiple vulnerabilities: SQLi to get admin creds, forge a JWT, escalate to admin role.
8. Write a Python script that brute-forces the login endpoint.
9. Build an automated scanner that detects all 10 vulnerabilities.

## Tools

Recommended tools for testing this lab:

- **curl / httpie** -- manual API requests
- **Burp Suite** -- proxy and intercept
- **jwt_tool** -- JWT analysis and cracking
- **sqlmap** -- automated SQL injection
- **GraphQL Voyager / InQL** -- GraphQL introspection
- **ffuf / wfuzz** -- fuzzing and brute force
- **Postman** -- API exploration

## Cleanup

```bash
docker compose down -v
```

This removes all containers and the PostgreSQL data volume.
