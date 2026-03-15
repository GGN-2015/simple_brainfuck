import json
import sys
import os
import traceback

from . import run

def main():
    argv_list = json.loads(json.dumps(sys.argv[1:]))

    filename_list = []
    show_time = False
    show_memory = False
    for item in argv_list:
        if item in ["--show-time", "-t"]:
            show_time = True
        elif item in ["--show-memory", "-m"]:
            show_memory = True
        else:
            filename_list.append(item)

    if len(filename_list) == 0:
        print("simple_brainfuck: CLI interface, Ctrl+C to exit")
        running =True
        mem = dict()
        while running:
            try:
                cmd = input(">>> ").strip()
                run(cmd, show_memory=True, show_time=True, initial_memory=mem)
            except KeyboardInterrupt:
                print("Bye.")
                running = False

            except Exception:
                traceback.print_exc()
        return
        
    if len(filename_list) != 1:
        raise ValueError("Please select exact one file.")
    
    if not os.path.isfile(filename_list[0]):
        raise FileNotFoundError(filename_list[0])
    
    with open(filename_list[0], "r") as fp:
        bf_program = fp.read()
    run(bf_program, show_memory=show_memory, show_time=show_time)

main()
