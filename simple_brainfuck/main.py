import sys
import time
from typing import Optional

def default_in_hook(memory_status:dict[int, int]) -> int:
    try:
        return ord(sys.stdin.read(1)) % 256
    except:
        return 255

def default_output_book(memory_status:dict[int, int], c:int):
    print(chr(c), end="")

def char_category(c:str) -> int:
    if c == "+" or c == '-': # add or sub
        return 1
    elif c == "<" or c == ">": # move ptr
        return 2
    elif c == "[":
        return 3
    elif c == "]":
        return 4
    elif c == ",":
        return 5
    elif c == ".":
        return 6
    else:
        return 0 # comment category

def count_char(s:str, c:str) -> int:
    ans = 0
    for c_now in s:
        if c_now == c:
            ans += 1
    return ans

def safe_get(mem:dict[int, int], ptr:int) -> int:
    if ptr < 0:
        raise ValueError("Tape pointer out of bound.")
    if mem.get(ptr) is None:
        mem[ptr] = 0
    return mem[ptr]

def safe_set(mem:dict[int, int], ptr:int, val_now:int):
    if ptr < 0:
        raise ValueError("Tape pointer out of bound.")
    mem[ptr] = val_now % 256

def safe_add(mem:dict[int, int], ptr:int, val_now:int):
    if ptr < 0:
        raise ValueError("Tape pointer out of bound.")
    new_val = (safe_get(mem, ptr) + val_now) % 256
    mem[ptr] = new_val

def serialize_status(mem:dict[int, int]):
    max_index_set = max([
        key 
        for key in mem if mem[key] != 0
    ])
    return [
        mem.get(i, 0)
        for i in range(max_index_set + 1)
    ]

# return meory status, and time
def run(
        bf_program:str, 
        in_hook=default_in_hook, 
        out_hook=default_output_book, 
        show_memory=False, 
        show_time=False,
        initial_memory:Optional[dict[int, int]]=None) -> tuple[dict, float]:
    
    if not isinstance(bf_program, str):
        raise TypeError("Brainfuck program must be a string.")

    program_arr = []
    for c_now in bf_program:
        category_now = char_category(c_now)
        if category_now != 0:
            program_arr.append((category_now, c_now))

            # 最后两个元素具有相同 category
            if (
                len(program_arr) >= 2 and 
                program_arr[-2][0] == program_arr[-1][0] and
                program_arr[-2][0] in [1, 2]
            ):
                new_cat = program_arr[-2][0]
                new_str = program_arr[-2][1] + program_arr[-1][1]
                program_arr.pop()
                program_arr.pop()
                program_arr.append((new_cat, new_str))
    
    # 统计元素的出现次数
    for i in range(len(program_arr)):
        now_cat, now_val = program_arr[i]
        if now_cat == 1:
            program_arr[i] = (now_cat, count_char(now_val, "+") - count_char(now_val, "-"))
        elif now_cat == 2:
            program_arr[i] = (now_cat, count_char(now_val, ">") - count_char(now_val, "<"))

    # 匹配中括号
    match_pos = {}
    pos_stack = []
    for i in range(len(program_arr)):
        if program_arr[i][1] == "[":
            pos_stack.append(i)
        elif program_arr[i][1] == "]":
            if len(pos_stack) == 0:
                raise ValueError("Unexpected right bracket.")
            match_pos[i] = pos_stack[-1]
            match_pos[pos_stack.pop()] = i
    if len(pos_stack) != 0:
        raise ValueError("Unclosed bracket exists.")
    
    begin_time = time.time()
    ptr = 0

    # 初始化内存空间
    if initial_memory is None:
        mem = dict()
    else:
        mem = initial_memory # 使用旧的内存空间

    program_ptr = 0
    while program_ptr < len(program_arr):
        cat_now, val_now = program_arr[program_ptr]
        if cat_now == 1:
            safe_add(mem, ptr, val_now)
            program_ptr += 1
        elif cat_now == 2:
            ptr += val_now
            program_ptr += 1
        elif val_now == ",":
            safe_set(mem, ptr, in_hook(mem))
            program_ptr += 1
        elif val_now == ".":
            out_hook(mem, safe_get(mem, ptr))
            program_ptr += 1
        elif val_now == "[":
            if safe_get(mem, ptr) == 0:
                program_ptr = match_pos[program_ptr] + 1
            else:
                program_ptr += 1
        elif val_now == "]":
            if safe_get(mem, ptr) != 0:
                program_ptr = match_pos[program_ptr] + 1
            else:
                program_ptr += 1
        else:
            print(cat_now, val_now)
            raise AssertionError()
    end_time = time.time()
    
    if show_memory:
        print(f"Array status: ptr = {ptr}, {serialize_status(mem)}")

    if show_time:
        print(f"Time cost: {end_time - begin_time:.6f}s")

    return mem, end_time - begin_time
