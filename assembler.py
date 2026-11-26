# assembler.py - Hack Assembler (Nand2Tetris Capstone, Part B)
# Roll no 2501730501 -> K = 01 -> K mod 3 = 1
# Extra feature: galat line par crash nahi hoga, "Line N: invalid instruction" print hoga.
#
# Usage:  python3 assembler.py Box.asm      (Box.hack ban jayegi)

import sys


# ---------------- Tables ----------------

COMP = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "!D":  "0001101",
    "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101",
}

DEST = {
    "":    "000", "M":   "001", "D":   "010", "MD":  "011",
    "A":   "100", "AM":  "101", "AD":  "110", "AMD": "111",
}

JUMP = {
    "":    "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}

SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    SYMBOLS["R" + str(i)] = i


class AsmError(Exception):
    """Ek galat line ke liye error."""
    pass


# ---------------- Helpers ----------------

def clean(line):
    """Comment aur spaces hata do."""
    line = line.split("//")[0]
    return line.replace(" ", "").replace("\t", "").strip()


def to_binary(n):
    return format(n, "016b")


def encode_c(instr):
    """C-instruction: dest=comp;jump"""
    dest, jump = "", ""
    comp = instr

    if "=" in comp:
        dest, comp = comp.split("=", 1)
    if ";" in comp:
        comp, jump = comp.split(";", 1)

    if dest not in DEST:
        raise AsmError("invalid dest '" + dest + "'")
    if comp not in COMP:
        raise AsmError("invalid instruction")
    if jump not in JUMP:
        raise AsmError("invalid jump '" + jump + "'")

    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


# ---------------- Main ----------------

def assemble(path):
    # ----- First reading: comments/blank lines hatao, labels note karo -----
    instructions = []       # (source line number, instruction text)
    errors = []
    rom_address = 0

    with open(path) as f:
        for line_no, raw in enumerate(f, start=1):
            text = clean(raw)

            if text == "":
                continue

            if text.startswith("("):
                if not text.endswith(")") or len(text) < 3:
                    errors.append("Line " + str(line_no) + ": invalid label")
                    continue
                label = text[1:-1]
                SYMBOLS[label] = rom_address
                continue

            instructions.append((line_no, text))
            rom_address += 1

    # ----- Second reading: har line ko 16 bits mein badlo -----
    next_var = 16
    output = []

    for line_no, text in instructions:
        try:
            if text.startswith("@"):
                value = text[1:]

                if value == "":
                    raise AsmError("invalid instruction")

                if value.isdigit():
                    number = int(value)
                    if number > 32767:
                        raise AsmError("number too big")
                else:
                    if value not in SYMBOLS:
                        SYMBOLS[value] = next_var
                        next_var += 1
                    number = SYMBOLS[value]

                output.append(to_binary(number))
            else:
                output.append(encode_c(text))

        except AsmError as e:
            errors.append("Line " + str(line_no) + ": " + str(e))

    # ----- Errors ho to print karo, crash mat karo -----
    if errors:
        for e in errors:
            print(e)
        print(str(len(errors)) + " error(s) found. .hack file nahi bani.")
        return

    out_path = path.rsplit(".", 1)[0] + ".hack"
    with open(out_path, "w") as f:
        f.write("\n".join(output) + "\n")

    print("Done: " + out_path + " (" + str(len(output)) + " instructions)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py File.asm")
    else:
        assemble(sys.argv[1])
