def absval(x):
    if x < 0:
        return -x
    return x

def is_close(a, b):
    return absval(a - b) < 0.0000001

def fmt(x):
    if is_close(x, int(x)):
        return str(int(x))
    return str(x)

def line():
    print("----------------------------------")

def sqrt_newton(x):
    if x < 0:
        return None
    if x == 0:
        return 0
    g = x
    i = 0
    while i < 30:
        g = 0.5 * (g + x / g)
        i = i + 1
    return g

def factor_quadratic(a, b, c):
    d = b * b - 4 * a * c
    if d < 0:
        return None
    root_d = sqrt_newton(d)
    r1 = (-b + root_d) / (2 * a)
    r2 = (-b - root_d) / (2 * a)
    return (r1, r2)

def solve_ypp_byp_delta():
    line()
    print("Solve y'' + b y' = A delta(t-a)")
    print("with y(0)=y0 and y'(0)=v0")
    print("")

    b = float(input("b = "))
    A = float(input("A = "))
    a = float(input("impulse time a = "))
    y0 = float(input("y(0) = "))
    v0 = float(input("y'(0) = "))

    if is_close(b, 0):
        print("")
        print("This case becomes y'' = A delta(t-a).")
        print("This script menu does not handle b = 0.")
        line()
        return

    print("")
    print("STEP 1: Take Laplace transforms")
    print("L{y''} = s^2Y - s y0 - v0")
    print("L{y'} = sY - y0")
    print("L{delta(t-a)} = e^(-as)")
    print("")
    print("(s^2Y - " + fmt(y0) + "s - " + fmt(v0) + ") + " + fmt(b) + "(sY - " + fmt(y0) + ") = " + fmt(A) + "e^(-" + fmt(a) + "s)")
    print("")

    print("STEP 2: Solve for Y(s)")
    print("(s^2 + " + fmt(b) + "s)Y = " + fmt(A) + "e^(-" + fmt(a) + "s) + " + fmt(y0) + "s + " + fmt(v0 + b * y0))
    print("")
    print("Y(s) = (" + fmt(A) + "e^(-" + fmt(a) + "s) + " + fmt(y0) + "s + " + fmt(v0 + b * y0) + ")/(s(s+" + fmt(b) + "))")
    print("")

    print("STEP 3: Split Y(s)")
    print("Y(s) = (" + fmt(y0) + "s + " + fmt(v0 + b * y0) + ")/(s(s+" + fmt(b) + ")) + " + fmt(A) + "e^(-" + fmt(a) + "s)/(s(s+" + fmt(b) + "))")
    print("")

    P = (v0 + b * y0) / b
    Q = y0 - P

    print("STEP 4: Partial fractions for the initial-condition part")
    print("(" + fmt(y0) + "s + " + fmt(v0 + b * y0) + ")/(s(s+" + fmt(b) + ")) = P/s + Q/(s+" + fmt(b) + ")")
    print("P = " + fmt(P))
    print("Q = " + fmt(Q))
    print("")
    print("So")
    print("y_ic(t) = " + fmt(P) + " + " + fmt(Q) + "e^(-" + fmt(b) + "t)")
    print("")

    print("STEP 5: Invert the impulse part")
    print("1/(s(s+" + fmt(b) + ")) = (1/" + fmt(b) + ")(1/s - 1/(s+" + fmt(b) + "))")
    print("")
    print("So")
    print("y_delta(t) = (" + fmt(A) + "/" + fmt(b) + ")U(t-" + fmt(a) + ")(1 - e^(-" + fmt(b) + "(t-" + fmt(a) + ")))")
    print("")

    print("STEP 6: Final answer")
    print("y(t) = " + fmt(P) + " + " + fmt(Q) + "e^(-" + fmt(b) + "t) + (" + fmt(A) + "/" + fmt(b) + ")U(t-" + fmt(a) + ")(1 - e^(-" + fmt(b) + "(t-" + fmt(a) + ")))")
    line()

def solve_ypp_byp_cy_delta():
    line()
    print("Solve y'' + b y' + c y = A delta(t-a)")
    print("with y(0)=y0 and y'(0)=v0")
    print("")

    b = float(input("b = "))
    c = float(input("c = "))
    A = float(input("A = "))
    a = float(input("impulse time a = "))
    y0 = float(input("y(0) = "))
    v0 = float(input("y'(0) = "))

    print("")
    print("STEP 1: Take Laplace transforms")
    print("L{y''} = s^2Y - s y0 - v0")
    print("L{y'} = sY - y0")
    print("L{y} = Y")
    print("L{delta(t-a)} = e^(-as)")
    print("")
    print("(s^2Y - " + fmt(y0) + "s - " + fmt(v0) + ") + " + fmt(b) + "(sY - " + fmt(y0) + ") + " + fmt(c) + "Y = " + fmt(A) + "e^(-" + fmt(a) + "s)")
    print("")

    print("STEP 2: Solve for Y(s)")
    print("(s^2 + " + fmt(b) + "s + " + fmt(c) + ")Y = " + fmt(A) + "e^(-" + fmt(a) + "s) + " + fmt(y0) + "s + " + fmt(v0 + b * y0))
    print("")
    print("Y(s) = (" + fmt(A) + "e^(-" + fmt(a) + "s) + " + fmt(y0) + "s + " + fmt(v0 + b * y0) + ")/(s^2 + " + fmt(b) + "s + " + fmt(c) + ")")
    print("")

    d = b * b - 4 * c
    print("STEP 3: Check the denominator")
    print("Discriminant = b^2 - 4c = " + fmt(d))
    print("")

    if d < -0.0000001:
        print("This version handles real-root cases only.")
        print("If the discriminant is negative, the roots are complex.")
        line()
        return

    roots = factor_quadratic(1, b, c)
    r1 = roots[0]
    r2 = roots[1]

    if is_close(r1, r2):
        r = r1
        print("Repeated root detected: s = " + fmt(r))
        print("")
        print("Denominator = (s-" + fmt(r) + ")^2")
        print("")
        print("STEP 4: General inverse-Laplace structure")
        print("The initial-condition part and impulse part must be rewritten using")
        print("A/(s-r) + B/(s-r)^2")
        print("")
        print("Useful formulas:")
        print("L^-1{1/(s-r)} = e^(rt)")
        print("L^-1{1/(s-r)^2} = t e^(rt)")
        print("L^-1{e^(-as)/(s-r)} = U(t-a)e^(r(t-a))")
        print("L^-1{e^(-as)/(s-r)^2} = U(t-a)(t-a)e^(r(t-a))")
        print("")
        print("So the final answer will be of the form")
        print("y(t) = C1 e^(" + fmt(r) + "t) + C2 t e^(" + fmt(r) + "t) + U(t-" + fmt(a) + ")(D1 e^(" + fmt(r) + "(t-" + fmt(a) + ")) + D2 (t-" + fmt(a) + ")e^(" + fmt(r) + "(t-" + fmt(a) + ")))")
        line()
        return

    print("Distinct real roots detected")
    print("r1 = " + fmt(r1))
    print("r2 = " + fmt(r2))
    print("Denominator = (s-" + fmt(r1) + ")(s-" + fmt(r2) + ")")
    print("")

    print("STEP 4: Split Y(s) into initial and impulse parts")
    print("Y(s) = (" + fmt(y0) + "s + " + fmt(v0 + b * y0) + ")/((s-" + fmt(r1) + ")(s-" + fmt(r2) + ")) + " + fmt(A) + "e^(-" + fmt(a) + "s)/((s-" + fmt(r1) + ")(s-" + fmt(r2) + "))")
    print("")

    m = y0
    n = v0 + b * y0

    C1 = (m * r1 + n) / (r1 - r2)
    C2 = (m * r2 + n) / (r2 - r1)

    D1 = A / (r1 - r2)
    D2 = A / (r2 - r1)

    print("STEP 5: Partial fractions for the initial-condition part")
    print("(" + fmt(m) + "s + " + fmt(n) + ")/((s-" + fmt(r1) + ")(s-" + fmt(r2) + ")) = C1/(s-" + fmt(r1) + ") + C2/(s-" + fmt(r2) + ")")
    print("C1 = " + fmt(C1))
    print("C2 = " + fmt(C2))
    print("")
    print("So")
    print("y_ic(t) = " + fmt(C1) + "e^(" + fmt(r1) + "t) + " + fmt(C2) + "e^(" + fmt(r2) + "t)")
    print("")

    print("STEP 6: Partial fractions for the impulse part")
    print(fmt(A) + "/((s-" + fmt(r1) + ")(s-" + fmt(r2) + ")) = D1/(s-" + fmt(r1) + ") + D2/(s-" + fmt(r2) + ")")
    print("D1 = " + fmt(D1))
    print("D2 = " + fmt(D2))
    print("")
    print("Apply the shift theorem")
    print("y_delta(t) = " + fmt(D1) + "U(t-" + fmt(a) + ")e^(" + fmt(r1) + "(t-" + fmt(a) + ")) + " + fmt(D2) + "U(t-" + fmt(a) + ")e^(" + fmt(r2) + "(t-" + fmt(a) + "))")
    print("")

    print("STEP 7: Final answer")
    print("y(t) = " + fmt(C1) + "e^(" + fmt(r1) + "t) + " + fmt(C2) + "e^(" + fmt(r2) + "t) + " + fmt(D1) + "U(t-" + fmt(a) + ")e^(" + fmt(r1) + "(t-" + fmt(a) + ")) + " + fmt(D2) + "U(t-" + fmt(a) + ")e^(" + fmt(r2) + "(t-" + fmt(a) + "))")
    line()

def menu():
    while True:
        print("")
        print("Universal Impulse ODE Solver")
        print("1 Solve y'' + b y' = A delta(t-a)")
        print("2 Solve y'' + b y' + c y = A delta(t-a)")
        print("3 Quit")

        ch = input("Select: ")

        if ch == "1":
            solve_ypp_byp_delta()
        elif ch == "2":
            solve_ypp_byp_cy_delta()
        elif ch == "3":
            break
        else:
            print("Invalid")

menu()
