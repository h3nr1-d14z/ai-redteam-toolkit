Build ROP chain for: $ARGUMENTS

1. **Gadget discovery**: Extract gadgets from binary and linked libraries using ROPgadget/ropper
2. **Categorize gadgets**: Map useful gadgets — pop/ret, mov, xchg, syscall/int 0x80, write primitives
3. **Chain strategy**: Determine goal — mprotect+shellcode, execve("/bin/sh"), system("/bin/sh"), or sigreturn
4. **Address resolution**: Handle ASLR — find info leak, use PLT/GOT entries, ret2libc with known offsets
5. **Build chain**: Construct gadget chain with proper stack alignment, handle null bytes
6. **Test**: Verify chain in debugger step-by-step, fix alignment and register state issues
7. **Document**: Save chain with annotated comments explaining each gadget purpose

Tools: ROPgadget, ropper, pwntools, GDB+pwndbg/GEF, one_gadget
Save to `exploitation/rop-chains/<target>-rop.py`
