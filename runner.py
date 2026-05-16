import os
import sys
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter

def run_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    tokens = Tokenizer(code).tokenize()
    program = Parser(tokens).parse()
    Interpreter().run(program)

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
        return

    for file in os.listdir():
        if file.endswith(".hb"):
            print(f"[HB] {file}")
            run_file(file)

if __name__ == "__main__":
    main()
