# Custom Language to RISC-V Assembly Compiler

A full-fledged multi-phase compiler written in Python that translates a custom high-level imperative programming language (case++) into executable RISC-V Assembly.

## Features and Compiler Pipeline

- Lexical Analysis (Lexer):
  - Tokenizes identifiers, keywords, multi-character operators, and numerical constants.
  - Handles single-line and multi-line comments with error reporting.
- Syntax and Semantic Analysis (Parser):
  - Implemented using Recursive Descent Parsing.
  - Supports complex control-flow structures (if/else, while, switchcase, forcase, incase, untilcase).
  - Function declarations with support for recursion and parameter passing modes (in / inout).
- Intermediate Code Generation (IR / Quads):
  - Generates 4-tuples (Quads) for intermediate representation.
  - Employs Backpatching algorithms for jump target resolution in conditional statements and loops.
- Symbol Table Management:
  - Hierarchical scope tracking for nested functions.
  - Calculates variable offsets and activation record frame lengths.
- Final Code Generation (RISC-V Assembly):
  - Target Architecture: RISC-V.
  - Implements runtime stack frame layout utilizing sp (Stack Pointer), fp (Frame Pointer), and gp (Global Pointer).
  - Static Links (gnlvcode) implementation for non-local variable access across nested function scopes.
  - Standard environment I/O handling via RISC-V system calls (ecall).

## Tech Stack

- Language: Python 3
- Target Architecture: RISC-V Assembly
- Tools and Simulators: RARS / MARS RISC-V Simulator

## How to Run

1. Generate Assembly from source code:
   python compiler_phase3.py example_program.c++

2. Generated Output Files:
   - out.int: Intermediate Code (Quads)
   - out.symb: Symbol Table log per scope
   - out.asm: Final RISC-V Assembly code

3. Execution:
   Load out.asm into a RISC-V Simulator (such as RARS) and execute.
```
