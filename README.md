# simple_brainfuck
a very simple brainfuck interpreter.

## Install

```bash
pip install simple-brainfuck
```

## Python Usage

```python
import simple_brainfuck

# simple usage
bf_program = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
mem, time_cost = simple_brainfuck.run(bf_program)

# run with input, output hook
# through memory_status，you can access the program memory space
def input_hook(memory_status:dict[int, int]) -> int:
    import sys
    return ord(sys.stdin.read(1)) % 256
def output_book(memory_status:dict[int, int], c:int):
    print(chr(c), end="")
simple_brainfuck.run(bf_program, input_hook=input_hook, output_hook=output_hook)

# run program, finally output the memory statue
simple_brainfuck.run(bf_program, show_memory=True)

# run program, finally output time cost
# time cost does not include preprocessing time, just program running time
simple_brainfuck.run(bf_program, show_time=True)
```

## CLI Usage

```bash
# run file as program
python3 -m simple_brainfuck <filepath.bf>

# run file, output time cost
python3 -m simple_brainfuck <filepath.bf> --show-time
python3 -m simple_brainfuck <filepath.bf> -t

# run file, output final memory status
python3 -m simple_brainfuck <filepath.bf> --show-memory
python3 -m simple_brainfuck <filepath.bf> -m
```
