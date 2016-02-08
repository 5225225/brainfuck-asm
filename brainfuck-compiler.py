import sys

TMP_VARS = 4

MAX_MEM_SIZE = 256

# XXX PROGRAMS GETTING INPUT **MUST** HAVE NEWLINE AT END XXX

def convert(instr, converter):
    out = ""
    for ch in instr:
        if ch in converter:
            out += converter[ch]

    return out

def simplify(prog):
    while "<>" in prog or "><" in prog:
        prog = prog.replace("<>", "")
        prog = prog.replace("><", "")
    return prog


def escapes(text):
    inpt = list(text)
    out = ""
    while inpt:
        ch = inpt.pop(0)
        if ch == "\\":
            esccode = inpt.pop(0)
            if esccode == "n":
                out += "\n"
            if esccode == "\\":
                out += "\\"
            if esccode == "\s":
                out += " "
        else:
            out += ch
    return out

def runfunc(cmd, args):
    global variables
    global varcounter
    global out

    if cmd == "var":
        variables[args[0]] = varcounter
        varcounter += 1

    if cmd == "space":
        varcounter += int(args[0])

    if cmd == "litprint":
        lit = escapes(" ".join(args))
        curr = 0
        for ch in lit:
            delta = ord(ch) - curr
            if delta > 0:
                out += "+"*abs(delta)
            if delta < 0:
                out += "-"*abs(delta)
            if delta == 0:
                pass
            out += "."
            curr = ord(ch)
        runfunc("zero", ["tmp_litprint"])

    if cmd == "strlit":
        variables[args[0]] = varcounter
        lit = escapes(" ".join(args[1:]))
        out += ">"
        out += ">"*varcounter
        for ch in lit:
            out += "+"*ord(ch)
            out += ">"

        out += "<"*len(lit)
        out += "<"*varcounter
        out += "<"


        varcounter += len(lit) + 2

    if cmd == "str":
        variables[args[0]] = varcounter
        strlen = int(args[1])
        out += ">"
        out += ">"*varcounter
        for ch in range(strlen):
            out += "+"
            out += ">"

        out += "<"*strlen
        out += "<"*varcounter
        out += "<"


        varcounter += strlen + 2



    if cmd == "split2":
        source, var1, var2 = args

        source = variables[source]
        var1 = variables[var1]
        var2 = variables[var2]

        _ = """
            Go to source
            While source is not 0
              decrement source by one
              go to var1
              increment var1 by one
              go to var2
              increment var2 by one
              go to source
        """

        out += ">" * source

        out += "["

        out += "-"

        
        out += "<" * source

        out += ">" * var1
        out += "+"
        out += "<" * var1

        out += ">" * var2
        out += "+"
        out += "<" * var2

        out += ">" * source

        out += "]"

        out += "<" * source

    if cmd == "move":
        source, dest = args

        source = variables[source]
        dest = variables[dest]

        _ = """
            Go to source
            While source is not 0
                decrement source by one
                go to dest
                increment dest by one
        """

        out += ">" * source

        out += "["

        out += "-"

        out += "<" * source

        out += ">" * dest

        out += "+"

        out += "<" * dest

        out += ">" * source

        out += "]"


        out += "<"*source

    if cmd == "copy":
        x, y = args
        runfunc("split2", [x, "tmp_0", "tmp_1"])
        runfunc("move", ["tmp_0", x])
        runfunc("move", ["tmp_1", y])

    if cmd == "inc":
        var, count = args
        vc = variables[var]

        out += ">"*vc

        out += "+"*int(count)

        out += "<"*vc

    if cmd == "dec":
        var, count = args
        vc = variables[var]

        out += ">"*vc

        out += "-"*int(count)

        out += "<"*vc

    if cmd == "break":
        out += "#"

    if cmd == "add":
        x, y = args

        runfunc("copy", [y, "tmp_2"])
        runfunc("move", ["tmp_2", x])

    if cmd == "mult":
        x, y = args

        runfunc("copy", [y, "tmp_3"])
        runfunc("dec", ["tmp_3", "1"])
        runfunc("while", ["tmp_3"])
        runfunc("add", [x, x])
        runfunc("dec", ["tmp_3", "1"])
        runfunc("end_while", ["tmp_3"])



    if cmd == "putch":
        x = variables[args[0]]

        out += ">"*x
        out += "."
        out += "<"*x

    if cmd == "getch":
        x = variables[args[0]]

        out += ">"*x
        out += ","
        out += "<"*x

    if cmd == "while":
        x = variables[args[0]]

        out += ">"*x

        out += "["

        out += "<"*x

    if cmd == "end_while":
        x = variables[args[0]]
        out += ">"*x
        out += "]"
        out += "<"*x

    if cmd == "if":
        x = args[0]
        n = 0
        while "if_cond{}".format(n) in variables:
            n += 1

        runfunc("var", ["if_cond{}".format(n)])

        runfunc("copy", [x, "if_cond{}".format(n)])

        out += ">"*variables["if_cond{}".format(n)]

        out += "["
        out += "<"*variables["if_cond{}".format(n)]

        runfunc("zero", ["if_cond{}".format(n)])

    if cmd == "end_if":
        n = 0
        while "if_cond{}".format(n) in variables:
            n += 1
        cond = variables["if_cond{}".format(n-1)]
        out += ">"*cond
        out += "]"
        out += "<"*cond



    if cmd == "sub":
        x, y = args
        xv = variables[x]
        yv = variables[y]
        runfunc("copy", [y, "tmp_2"])
        

        out += ">" * yv

        out += "[-"

        out += "<" * yv

        out += ">" * xv

        out += "-"

        out += "<" * xv

        out += ">" * yv

        out += "]"


        out += "<" * yv

        runfunc("move", ["tmp_2", y])

    if cmd == "zero":
        x = args[0]
        x = variables[x]

        out += ">"*x
        out += "[-]"
        out += "<"*x

    if cmd == "print":
        s = variables[args[0]]
        out += ">"*s
        out += ">"
        out += "[.>]"
        out += "<"
        out += "[<]"
        out += "<"*s


    if cmd == "read":
        s = variables[args[0]]
        eof = 10
        try:
            eof = int(args[1])
        except IndexError:
            pass

        out += ">"*s

        out += ">"


        out += ",{}[{}>,{}]".format("-"*eof, "+"*eof, "-"*eof)


        
        out += "<"


        out += "[<]"
        out += "<"*s


variables = {}
varcounter = 0
indents = 0
indent_width = 4

for x in range(TMP_VARS):
    runfunc("var", ["tmp_{}".format(x+0)])
runfunc("var", ["if_cond{}".format(x+0)])

runfunc("var", ["tmp_litprint"])

out = "\n"

linenum = 1
for line in sys.stdin.readlines():
    line = line.strip()
    if line:
        cmd, *args = line.split()
        try:
            if cmd == "end_while" or cmd == "end_if":
                indents -= 1
            out += " "*indent_width*indents
            runfunc(cmd, args)
            out += ": {}\n".format(line)

            if cmd == "while" or cmd == "if":
                indents += 1

        except KeyError as e:
            print("Unknown Variable name: {}".format(str(e)))
            print("Line {}".format(linenum))
            raise e
            sys.exit(1)
        except ValueError:
            print("Not enough arguments")
            print("Line {}".format(linenum))
            sys.exit(1)
        if varcounter >= MAX_MEM_SIZE:
            print("Over Memory Usage")
            print("Line {}".format(linenum))
            sys.exit(1)
    linenum += 1

out = simplify(out)
print(out)
