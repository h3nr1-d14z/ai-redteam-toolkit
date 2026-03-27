# Ghidra Cheatsheet

## Project Setup
```
File > New Project > Non-Shared Project > select directory
File > Import File > select binary
Double-click binary in project window to open CodeBrowser
Analysis Options dialog > select all analyzers > Analyze

# Batch import
File > Batch Import > select directory with multiple binaries
```

## Navigation Shortcuts
```
G             Go to address (enter hex address)
Ctrl+E        Edit the current field
Ctrl+L        Go to label/symbol
Ctrl+Shift+E  Show symbol table
L             Rename label/function/variable
;             Add comment (end-of-line)
Ctrl+;        Add plate comment (before function)
Enter         Follow reference/jump
Alt+Left      Navigate back
Alt+Right     Navigate forward
Space         Toggle listing/decompiler view
```

## Listing (Disassembly) View
```
D             Disassemble at cursor
C             Clear code (turn back to undefined bytes)
P             Create function at cursor
F             Create function from selection
T             Set data type at cursor
B             Set to byte
W             Set to word (2 bytes)
'             Set to char/string
Ctrl+Shift+A  Auto-create ASCII string

# Array
Right-click > Data > Create Array > set element count

# Pointer
Right-click > Data > pointer
```

## Decompiler View
```
# View decompiled C code
Window > Decompile (or press Space to toggle)

Ctrl+E        Edit function signature (rename, change params, return type)
L             Rename variable
Ctrl+L        Retype variable
;             Add comment
/             Set comment on current line
Tab           Toggle between decompiler and listing

# Improve decompilation
- Rename variables (L) to understand data flow
- Retype variables (Ctrl+L) to fix casts and pointer types
- Edit function signature (Ctrl+E) to fix param count and types
- Create structures and apply them to pointers
```

## Function Analysis
```
# Create function
P                         Create function at address
Right-click > Function > Create Function

# Edit function
Right-click > Function > Edit Function Signature
  - Change name, return type, calling convention
  - Add/modify parameters

# View call graph
Right-click > References > Show Call Trees
Window > Function Call Graph

# Cross-references (XRefs)
Right-click > References > Show References to (incoming)
Right-click > References > Show References from (outgoing)
Ctrl+Shift+F    Find references to selection

# List all functions
Window > Symbol Table > Filter by type: Function
Window > Function Manager
```

## Data Types and Structures
```
# Create structure
Window > Data Type Manager > right-click archive > New > Structure
  - Add fields: name, type, size
  - Apply to memory: select bytes > right-click > Data > Choose Data Type

# Edit existing structure
Double-click structure in Data Type Manager
Add/remove/modify fields

# Import C header
File > Parse C Source > add .h file > Parse
  - Automatically creates structures, enums, typedefs

# Apply structure to pointer in decompiler
Ctrl+L on variable > select structure type
Right-click pointer > Retype Variable

# Common type mappings
byte      = uint8_t
word      = uint16_t
dword     = uint32_t
qword     = uint64_t
pointer   = void* (or specific type*)
```

## Search
```
Search > Memory                     Search bytes/strings in memory
Search > Program Text               Search disassembly text
Search > For Strings               Find all strings in binary
Search > For Scalars               Find specific numeric values
Search > For Instruction Patterns  Find instruction sequences

# Search for bytes
Search > Memory > hex string: "48 89 e5" (push rbp pattern)
Search > Memory > string: "password"

# Search for strings
Window > Defined Strings > filter

# Search for function by name
Ctrl+Shift+E > filter by name

# Search for XRefs to an address
Right-click address > References > Show References to
```

## Scripting (Python/Java)
```python
# Ghidra Python (Jython) - run via Script Manager (Window > Script Manager)

# Get current program
program = getCurrentProgram()

# Get current address
addr = currentAddress

# Get function at address
func = getFunctionAt(addr)
func = getFunctionContaining(addr)

# List all functions
fm = currentProgram.getFunctionManager()
for func in fm.getFunctions(True):  # True = forward
    print(func.getName(), func.getEntryPoint())

# Find function by name
func = getGlobalFunctions("main")[0]

# Get cross-references
from ghidra.program.model.symbol import ReferenceManager
refMgr = currentProgram.getReferenceManager()
refs = refMgr.getReferencesTo(addr)
for ref in refs:
    print(ref.getFromAddress(), ref.getReferenceType())

# Read memory
mem = currentProgram.getMemory()
value = mem.getInt(addr)
data = bytearray(64)
mem.getBytes(addr, data)

# Search for bytes
from ghidra.program.model.mem import MemoryAccessException
results = findBytes(None, "48 89 e5", 100)  # find up to 100 matches

# Rename function
func.setName("my_function_name", ghidra.program.model.symbol.SourceType.USER_DEFINED)

# Set comment
setEOLComment(addr, "my comment")
setPlateComment(addr, "function description")

# Get decompiled code
from ghidra.app.decompiler import DecompInterface
decomp = DecompInterface()
decomp.openProgram(currentProgram)
results = decomp.decompileFunction(func, 60, monitor)
print(results.getDecompiledFunction().getC())
```

## Analysis Tips
```
# Identify encryption
Search for known constants:
  - AES S-box: 0x63, 0x7c, 0x77, 0x7b
  - SHA-256: 0x6a09e667
  - MD5: 0x67452301
  - CRC32: 0xEDB88320
Window > Script Manager > FindCrypt (if installed)

# Identify string obfuscation
Look for XOR loops: xor reg, constant in a loop
Look for decode functions called before string use
Set breakpoints in debugger to see decoded strings

# Fix wrong analysis
Select bytes > C (clear) > D (re-disassemble)
Select bytes > P (create function) if function not recognized
Edit > Tool Options > Analysis > re-run specific analyzers

# Compare binaries (BinDiff/Diaphora)
Export both binaries from Ghidra as BinExport
Use BinDiff to compare functions between versions
Identify patched functions for vulnerability research
```

## Useful Plugins and Extensions
```
# Install via File > Install Extensions or manually

ghidra-scripts       Community scripts collection
FindCrypt            Identify cryptographic constants
GhidraDec           Additional decompiler improvements
BinExport           Export for BinDiff comparison
SVD-Loader          Load ARM SVD files for peripheral names
Ghidra2Frida        Generate Frida hooks from Ghidra
```

## Common Workflows
```
# Malware analysis
1. Import binary, run auto-analysis
2. Check strings (Window > Defined Strings) for IOCs
3. Check imports for suspicious APIs (network, file, process, registry)
4. Find main/entry and trace execution flow
5. Identify C2 configuration decryption
6. Document all findings with comments

# Vulnerability research
1. Import binary and patched version
2. BinDiff to find changed functions
3. Analyze changed function for vulnerability details
4. Map input path to vulnerable code
5. Determine exploitability

# CTF reverse engineering
1. Import, analyze, find main
2. Look for flag checks, string comparisons
3. Trace validation logic
4. Extract constraints and solve (Z3 or manual)
```
