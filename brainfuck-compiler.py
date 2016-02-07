import sys

TMP_VARS = 3

MAX_MEM_SIZE = 256

# XXX PROGRAMS GETTING INPUT **MUST** HAVE NEWLINE AT END XXX

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
        out += ">"*s

        out += ">"


        out += ",----------[++++++++++>,----------]"


        
        out += "<"


        out += "[<]"
        out += "<"*s


variables = {}
varcounter = 0

for x in range(TMP_VARS):
    runfunc("var", ["tmp_{}".format(x+0)])

out = ""

linenum = 1
for line in sys.stdin.readlines():
    line = line.strip()
    if line:
        cmd, *args = line.split()
        try:
            runfunc(cmd, args)
        except KeyError as e:
            print("Unknown Variable name: {}".format(str(e)))
            print("Line {}".format(linenum))
            sys.exit(1)
        if varcounter >= MAX_MEM_SIZE:
            print("Over Memory Usage")
            print("Line {}".format(linenum))
            sys.exit(1)
    linenum += 1

print(out)
