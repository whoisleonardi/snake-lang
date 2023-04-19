#!/usr/bin/env python3

import sys
import subprocess

iota_counter = 0

def iota(reset = False):
    global iota_counter

    if reset: iota_counter = 0

    result = iota_counter
    iota_counter += 1
    return result

OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota()

def push(x):
    return (OP_PUSH, x)

def plus():
    return (OP_PLUS, )

def minus():
    return (OP_MINUS, )

def dump():
    return (OP_DUMP, )

def simulate_program(program: list):
    stack = []

    for operator in program:
        assert COUNT_OPS == 4, 'Exhaustive handling of operations in simulation'

        if operator[0] == OP_PUSH:
            stack.append(operator[1])

        elif operator[0] == OP_PLUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(x + y)

        elif operator[0] == OP_MINUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(y - x)

        elif operator[0] == OP_DUMP:
            x = stack.pop()
            print(x)

        else:
            assert False, 'unreachable'

def compile_program(program, out_file_path):
    with open(out_file_path, "w") as out:
        # Push code in assembly
        out.write('segment .text\n')
        out.write('global _start\n')
        out.write('_start:\n')

        for operation in program:
            # Push code in assembly
            if operation[0] == OP_PUSH:
                out.write(f'    ;;-- push {operation[1]} --\n')
                out.write(f'    push{operation[1]}\n')

            elif operation[0] == OP_PLUS:
                out.write(f'    ;;-- plus {operation[1]} --\n')
                out.write(f'    ;;-- Not implemented --\n')

        out.write('    mov rax, 60\n')
        out.write('    mov rdi, 0\n')
        out.write('    syscall\n')

# Unhardcode program
program = [
    push(34),
    push(35),
    plus(),
    dump(),
    push(500),
    push(80),
    minus(),
    dump(),
]

def usage_mode():
    """
    Usage: snake <SUBCOMMAND> [ARGS]

    SUBCOMMANDS:
    ssp  --->  Simulate the program
    scp  --->  Compile the program
    """

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(usage_mode.__doc__)
        print('ERROR: no subcommand is proiveded')
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == 'ssp':
        simulate_program(program)

    elif subcommand == 'scp':
        compile_program(program, 'test/test.asm')
        subprocess.call(['nasm', '-felf64', 'test/test.asm'])
        subprocess.call(['ld', '-o', 'test/output', 'test/test.o'])

    else:
        print(usage_mode.__doc__)
        print(f'\nERROR!: unknown subcommand: \"{subcommand}\"')
        exit(1)
