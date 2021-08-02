#!/usr/bin/python3

from sys import stdout
import tb
import json

def run(source_filename, input_filename=None, in_state_filename=None, out_state_filename = None):
    print(f"run source: {source_filename}, input: {input_filename}, in state: {in_state_filename}, out state: {out_state_filename}")
    input_file = open(input_filename, 'r') if input_filename else sys.stdin
    if in_state_filename:
        (vars, stack, line_number, raw_lines) = import_state(in_state_filename)
        tiny_basic = tb.TinyBasic(input_file, sys.stdout, vars, stack, line_number, raw_lines)
    elif source_filename:
        with open(source_filename, 'r') as file:
            raw_lines = file.readlines()
        tiny_basic = tb.TinyBasic(input_file, sys.stdout, {}, [], 0, raw_lines)
    try:
        tiny_basic.parse_all()
        tiny_basic.run()
    except EOFError: # not enough input, so we stop here for now
        export_state(tiny_basic, out_state_filename)
        print(f"written state to {out_state_filename}")
    except Exception as e:
        print("ERROR: {}".format(e), file=sys.stderr)


def import_state(filename):
    with open(filename, 'r') as file:
        raw_data = file.readline()
    json_data = json.loads(raw_data)
    return (json_data["vars"], json_data["stack"], json_data["line"], json_data["prog"])


def export_state(tiny_basic, filename):
    raw_lines = []
    lines_numbers = sorted(tiny_basic.memory.keys())
    for line_number in lines_numbers:
        statement = tiny_basic.memory[line_number]
        raw_lines.append(f"{line_number} {statement}\n")
    export = { "vars" : tiny_basic.vars, "stack": tiny_basic.stack, "line": tiny_basic.line_number, "prog": raw_lines }
    export_json = json.dumps(export)
    with open(filename, 'w') as file:
        file.write(export_json)


def main(argv):
    print("Tiny Basic v0.1")
    source_file = None
    input_file = None
    in_state_file = None
    out_state_file = None
    while argv:
        arg = argv.pop(0)
        if arg == "-input":
            input_file = argv.pop(0)
        elif arg == "-in_state":
            in_state_file = argv.pop(0)
        elif arg == "-out_state":
            out_state_file = argv.pop(0)
        else:
            if source_file == None: source_file = arg
            else: raise Exception(f"don't know how to handle {arg}")        
    run(source_file, input_file, in_state_file, out_state_file)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
