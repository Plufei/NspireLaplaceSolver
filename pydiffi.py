from math import sqrt, exp, cos, sin
import cmath

def clean_num(n):
    if abs(n - round(n)) < 1e-10:
        return str(int(round(n)))
    s = "{:.10f}".format(n).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s

def clean_complex(z):
    a = z.real
    b = z.imag
    if abs(b) < 1e-10:
        return clean_num(a)
    if abs(a) < 1e-10:
        if abs(b - 1) < 1e-10:
            return "i"
        if abs(b + 1) < 1e-10:
            return "-i"
        return clean_num(b) + "i"
    sign = "+" if b >= 0 else "-"
    bi = abs(b)
    if abs(bi - 1) < 1e-10:
        imag_part = "i"
    else:
        imag_part = clean_num(bi) + "i"
    return clean_num(a) + sign + imag_part

def strip_spaces(s):
    out = ""
    for ch in s:
        if ch != " ":
            out += ch
    return out

def parse_linear_term(expr, target):
    i = expr.find(target)
    if i == -1:
        return 0.0
    left = expr[:i]
    j = len(left) - 1
    while j >= 0 and (left[j].isdigit() or left[j] == "." or left[j] == "-"):
        j -= 1
    coef = left[j+1:]
    if coef == "" or coef == "+":
        return 1.0
    if coef == "-":
        return -1.0
    return float(coef)

def parse_constant_coeff_1st(eq):
    # expected form: y'+ay=0
    eq = strip_spaces(eq)
    parts = eq.split("=")
    if len(parts) != 2:
        return None
    left = parts[0]
    right = parts[1]
    if right != "0":
        return None
    if "y'" not in left or "y" not in left:
        return None

    i = left.find("y'")
    rest = left[i+2:]
    if rest == "":
        a = 0.0
    else:
        k = rest.find("y")
        if k == -1:
            return None
        coef = rest[:k]
        if coef == "" or coef == "+":
            a = 1.0
        elif coef == "-":
            a = -1.0
        else:
            a = float(coef)
    return a

def parse_constant_coeff_2nd(eq):
    # expected form: y''+ay'+by=0
    eq = strip_spaces(eq)
    parts = eq.split("=")
    if len(parts) != 2:
        return None
    left = parts[0]
    right = parts[1]
    if right != "0":
        return None
    if "y''" not in left:
        return None

    left = left.replace("y''", "")
    a = 0.0
    b = 0.0

    if "y'" in left:
        i = left.find("y'")
        before = left[:i]
        left2 = left[i+2:]
        if before == "" or before == "+":
            a = 1.0
        elif before == "-":
            a = -1.0
        else:
            a = float(before)
    else:
        left2 = left

    if "y" in left2:
        i = left2.find("y")
        before = left2[:i]
        if before == "" or before == "+":
            b = 1.0
        elif before == "-":
            b = -1.0
        else:
            b = float(before)

    return a, b

def solve_first_order(a, x0, y0):
    lines = []
    lines.append("Detected form: y' + ay = 0")
    lines.append("a = " + clean_num(a))
    lines.append("")
    lines.append("Step 1: Rewrite the equation")
    lines.append("y' = -ay")
    lines.append("y' = -" + clean_num(a) + "y")
    lines.append("")
    lines.append("Step 2: Separate variables")
    lines.append("(1/y) dy = -" + clean_num(a) + " dx")
    lines.append("")
    lines.append("Step 3: Integrate both sides")
    lines.append("ln|y| = -" + clean_num(a) + "x + C")
    lines.append("")
    lines.append("Step 4: Solve for y")
    lines.append("y = Ce^(-" + clean_num(a) + "x)")
    lines.append("General solution: y = Ce^(-" + clean_num(a) + "x)")
    lines.append("")
    lines.append("Step 5: Apply the initial condition")
    lines.append("Given y(" + clean_num(x0) + ") = " + clean_num(y0))
    C = y0 * exp(a * x0)
    lines.append(clean_num(y0) + " = C e^(-" + clean_num(a) + "(" + clean_num(x0) + "))")
    lines.append("C = " + clean_num(C))
    lines.append("")
    lines.append("Final solution:")
    lines.append("y = " + clean_num(C) + "e^(-" + clean_num(a) + "x)")
    return "\n".join(lines)

def solve_second_order(a, b, x0, y0, yp0):
    lines = []
    lines.append("Detected form: y'' + ay' + by = 0")
    lines.append("a = " + clean_num(a))
    lines.append("b = " + clean_num(b))
    lines.append("")
    lines.append("Step 1: Form the characteristic equation")
    lines.append("r^2 + " + clean_num(a) + "r + " + clean_num(b) + " = 0")
    D = a*a - 4*b
    lines.append("Discriminant: D = a^2 - 4b = " + clean_num(D))
    lines.append("")

    if D > 1e-10:
        lines.append("Step 2: Since D > 0, there are two distinct real roots")
        r1 = (-a + sqrt(D)) / 2.0
        r2 = (-a - sqrt(D)) / 2.0
        lines.append("r1 = " + clean_num(r1))
        lines.append("r2 = " + clean_num(r2))
        lines.append("")
        lines.append("General solution:")
        lines.append("y = C1 e^(" + clean_num(r1) + "x) + C2 e^(" + clean_num(r2) + "x)")
        lines.append("")
        lines.append("Step 3: Differentiate")
        lines.append("y' = " + clean_num(r1) + "C1 e^(" + clean_num(r1) + "x) + " + clean_num(r2) + "C2 e^(" + clean_num(r2) + "x)")
        lines.append("")
        lines.append("Step 4: Apply initial conditions")
        e1 = exp(r1 * x0)
        e2 = exp(r2 * x0)
        A11 = e1
        A12 = e2
        A21 = r1 * e1
        A22 = r2 * e2
        det = A11*A22 - A12*A21
        C1 = (y0*A22 - A12*yp0) / det
        C2 = (A11*yp0 - y0*A21) / det
        lines.append("y(" + clean_num(x0) + ") = " + clean_num(y0))
        lines.append("y'(" + clean_num(x0) + ") = " + clean_num(yp0))
        lines.append("C1 = " + clean_num(C1))
        lines.append("C2 = " + clean_num(C2))
        lines.append("")
        lines.append("Final solution:")
        lines.append("y = " + clean_num(C1) + "e^(" + clean_num(r1) + "x) + " + clean_num(C2) + "e^(" + clean_num(r2) + "x)")

    elif abs(D) <= 1e-10:
        lines.append("Step 2: Since D = 0, there is one repeated real root")
        r = -a / 2.0
        lines.append("r = " + clean_num(r))
        lines.append("")
        lines.append("General solution:")
        lines.append("y = (C1 + C2 x)e^(" + clean_num(r) + "x)")
        lines.append("")
        lines.append("Step 3: Differentiate")
        lines.append("y' = [C2 + " + clean_num(r) + "(C1 + C2 x)]e^(" + clean_num(r) + "x)")
        lines.append("")
        lines.append("Step 4: Apply initial conditions")
        er = exp(r * x0)
        C1 = y0 / er - 0
        C2 = (yp0 / er) - r * C1 - r * 0
        C2 = C2 / (1 + r * x0 - r * x0)
        # Better direct system:
        # y(x0)= (C1 + C2 x0)e^(rx0)=y0
        # y'(x0)= (C2 + r(C1 + C2 x0))e^(rx0)=yp0
        S1 = y0 / er
        S2 = yp0 / er
        C2 = S2 - r * S1
        C1 = S1 - C2 * x0
        lines.append("y(" + clean_num(x0) + ") = " + clean_num(y0))
        lines.append("y'(" + clean_num(x0) + ") = " + clean_num(yp0))
        lines.append("C1 = " + clean_num(C1))
        lines.append("C2 = " + clean_num(C2))
        lines.append("")
        lines.append("Final solution:")
        lines.append("y = (" + clean_num(C1) + " + " + clean_num(C2) + "x)e^(" + clean_num(r) + "x)")

    else:
        lines.append("Step 2: Since D < 0, the roots are complex")
        alpha = -a / 2.0
        beta = sqrt(-D) / 2.0
        lines.append("r = " + clean_num(alpha) + " ± " + clean_num(beta) + "i")
        lines.append("")
        lines.append("General solution:")
        lines.append("y = e^(" + clean_num(alpha) + "x)[C1 cos(" + clean_num(beta) + "x) + C2 sin(" + clean_num(beta) + "x)]")
        lines.append("")
        lines.append("Step 3: Differentiate")
        lines.append("y' = e^(" + clean_num(alpha) + "x)[(" + clean_num(alpha) + "C1 + " + clean_num(beta) + "C2)cos(" + clean_num(beta) + "x) + (" + clean_num(alpha) + "C2 - " + clean_num(beta) + "C1)sin(" + clean_num(beta) + "x)]")
        lines.append("")
        lines.append("Step 4: Apply initial conditions")
        ea = exp(alpha * x0)
        c = cos(beta * x0)
        s = sin(beta * x0)

        A11 = ea * c
        A12 = ea * s
        A21 = ea * (alpha * c - beta * s)
        A22 = ea * (alpha * s + beta * c)
        det = A11*A22 - A12*A21
        C1 = (y0*A22 - A12*yp0) / det
        C2 = (A11*yp0 - y0*A21) / det

        lines.append("y(" + clean_num(x0) + ") = " + clean_num(y0))
        lines.append("y'(" + clean_num(x0) + ") = " + clean_num(yp0))
        lines.append("C1 = " + clean_num(C1))
        lines.append("C2 = " + clean_num(C2))
        lines.append("")
        lines.append("Final solution:")
        lines.append("y = e^(" + clean_num(alpha) + "x)[" + clean_num(C1) + "cos(" + clean_num(beta) + "x) + " + clean_num(C2) + "sin(" + clean_num(beta) + "x)]")

    return "\n".join(lines)

def main():
    print("Differential Equation Step Solver")
    print("Supported forms:")
    print("1) y' + ay = 0")
    print("2) y'' + ay' + by = 0")
    print("")

    eq = input("Enter equation: ")
    eq = strip_spaces(eq)

    if "y''" in eq:
        parsed = parse_constant_coeff_2nd(eq)
        if parsed is None:
            print("Could not parse the equation.")
            print("Use a form like y''+25y=0 or y''+4y'+13y=0")
            return
        a, b = parsed
        x0 = float(input("Enter x0 for y(x0): "))
        y0 = float(input("Enter y(x0): "))
        yp0 = float(input("Enter y'(x0): "))
        print("")
        print(solve_second_order(a, b, x0, y0, yp0))

    elif "y'" in eq:
        parsed = parse_constant_coeff_1st(eq)
        if parsed is None:
            print("Could not parse the equation.")
            print("Use a form like y'+3y=0")
            return
        a = parsed
        x0 = float(input("Enter x0 for y(x0): "))
        y0 = float(input("Enter y(x0): "))
        print("")
        print(solve_first_order(a, x0, y0))

    else:
        print("Unsupported equation type.")
        print("Use y'+ay=0 or y''+ay'+by=0")

main()
