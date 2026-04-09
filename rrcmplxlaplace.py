pi = 3.141592653589793

def factorial(n):
    if n < 0:
        return None
    result = 1
    i = 1
    while i <= n:
        result = result * i
        i = i + 1
    return result

def absval(x):
    if x < 0:
        return -x
    return x

def is_close(a, b):
    return absval(a - b) < 0.0000001

def fmt(x):
    if is_close(x, int(x)):
        return str(int(x))
    s = str(x)
    return s

def line():
    print("----------------------------------")

def sqrt_newton(x):
    if x < 0:
        return None
    if x == 0:
        return 0
    guess = x
    i = 0
    while i < 20:
        guess = 0.5 * (guess + x / guess)
        i = i + 1
    return guess

def quad_discriminant(a, b, c):
    return b * b - 4 * a * c

def factor_quadratic(a, b, c):
    d = quad_discriminant(a, b, c)
    if d < 0:
        return None
    root_d = sqrt_newton(d)
    r1 = (-b + root_d) / (2 * a)
    r2 = (-b - root_d) / (2 * a)
    return (r1, r2)

def inverse_basic_power_shift():
    line()
    print("Inverse Laplace for repeated-pole forms")
    print("1 -> A/(s-a)")
    print("2 -> A/(s-a)^2")
    print("3 -> A/(s-a)^3")
    print("4 -> A/(s-a)^n")
    ch = input("Choice: ")

    if ch == "1":
        A = float(input("A = "))
        a = float(input("a = "))
        print("")
        print("L^-1{A/(s-a)} = A e^(at)")
        print("f(t) = " + fmt(A) + "e^(" + fmt(a) + "t)")
    elif ch == "2":
        A = float(input("A = "))
        a = float(input("a = "))
        print("")
        print("Use L^-1{1/(s-a)^2} = t e^(at)")
        print("f(t) = " + fmt(A) + " t e^(" + fmt(a) + "t)")
    elif ch == "3":
        A = float(input("A = "))
        a = float(input("a = "))
        print("")
        print("Use L^-1{1/(s-a)^3} = (t^2/2)e^(at)")
        print("f(t) = (" + fmt(A) + "/2) t^2 e^(" + fmt(a) + "t)")
    elif ch == "4":
        A = float(input("A = "))
        a = float(input("a = "))
        n = int(input("n = "))
        print("")
        print("Use L^-1{1/(s-a)^n} = t^(n-1)e^(at)/(n-1)!")
        print("f(t) = (" + fmt(A) + "/" + fmt(factorial(n - 1)) + ") t^" + fmt(n - 1) + " e^(" + fmt(a) + "t)")
    line()

def partial_fraction_distinct_linear():
    line()
    print("Partial fractions: (m s + n) / ((s-r1)(s-r2))")
    m = float(input("m = "))
    n = float(input("n = "))
    r1 = float(input("r1 = "))
    r2 = float(input("r2 = "))

    if is_close(r1, r2):
        print("These are repeated poles. Use the repeated-pole menu instead.")
        line()
        return

    A = (m * r1 + n) / (r1 - r2)
    B = (m * r2 + n) / (r2 - r1)

    print("")
    print("We write")
    print("(m s + n)/((s-r1)(s-r2)) = A/(s-r1) + B/(s-r2)")
    print("")
    print("A =", fmt(A))
    print("B =", fmt(B))
    print("")
    print("Inverse Laplace:")
    print("f(t) = " + fmt(A) + "e^(" + fmt(r1) + "t) + " + fmt(B) + "e^(" + fmt(r2) + "t)")
    line()

def partial_fraction_repeated_linear():
    line()
    print("Partial fractions: (m s + n) / (s-r)^2")
    m = float(input("m = "))
    n = float(input("n = "))
    r = float(input("r = "))

    A = m
    B = m * r + n

    print("")
    print("We write")
    print("(m s + n)/(s-r)^2 = A/(s-r) + B/(s-r)^2")
    print("")
    print("Match coefficients:")
    print("m s + n = A(s-r) + B = As - Ar + B")
    print("So A = m and B = mr + n")
    print("")
    print("A =", fmt(A))
    print("B =", fmt(B))
    print("")
    print("Inverse Laplace:")
    print("f(t) = " + fmt(A) + "e^(" + fmt(r) + "t) + " + fmt(B) + " t e^(" + fmt(r) + "t)")
    line()

def inverse_rational_quadratic():
    line()
    print("Inverse Laplace of (m s + n)/(a s^2 + b s + c)")
    print("This version handles:")
    print("1 -> distinct real roots")
    print("2 -> repeated real root")
    print("")
    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))
    m = float(input("numerator coefficient m = "))
    n = float(input("numerator constant n = "))

    d = quad_discriminant(a, b, c)
    print("")
    print("Discriminant =", fmt(d))

    if d < -0.0000001:
        print("This script version does not handle complex roots in this menu.")
        line()
        return

    roots = factor_quadratic(a, b, c)
    r1 = roots[0]
    r2 = roots[1]

    if is_close(r1, r2):
        r = r1
        print("Repeated pole detected at s =", fmt(r))
        print("")
        print("Since denominator = a(s-r)^2, first divide numerator by a.")
        mm = m / a
        nn = n / a
        A = mm
        B = mm * r + nn
        print("Equivalent form:")
        print("(" + fmt(m) + "s + " + fmt(n) + ")/(" + fmt(a) + "(s-" + fmt(r) + ")^2)")
        print("= (" + fmt(mm) + "s + " + fmt(nn) + ")/(s-" + fmt(r) + ")^2")
        print("")
        print("A =", fmt(A))
        print("B =", fmt(B))
        print("")
        print("f(t) = " + fmt(A) + "e^(" + fmt(r) + "t) + " + fmt(B) + " t e^(" + fmt(r) + "t)")
    else:
        print("Distinct poles detected:")
        print("r1 =", fmt(r1))
        print("r2 =", fmt(r2))
        print("")
        den_scale = a
        mm = m / den_scale
        nn = n / den_scale
        A = (mm * r1 + nn) / (r1 - r2)
        B = (mm * r2 + nn) / (r2 - r1)
        print("Equivalent form:")
        print("(" + fmt(m) + "s + " + fmt(n) + ")/(" + fmt(a) + "(s-" + fmt(r1) + ")(s-" + fmt(r2) + "))")
        print("= (" + fmt(mm) + "s + " + fmt(nn) + ")/((s-" + fmt(r1) + ")(s-" + fmt(r2) + "))")
        print("")
        print("A =", fmt(A))
        print("B =", fmt(B))
        print("")
        print("f(t) = " + fmt(A) + "e^(" + fmt(r1) + "t) + " + fmt(B) + "e^(" + fmt(r2) + "t)")
    line()

def solve_Y():
    line()
    print("Solve for Y(s):")
    print("y'' + 2y' + y = e^(5t), y(0)=0, y'(0)=2")
    print("")
    print("Step 1: Laplace transforms")
    print("L{y''} = s^2Y - sy(0) - y'(0)")
    print("L{y'} = sY - y(0)")
    print("L{y} = Y")
    print("L{e^(5t)} = 1/(s-5)")
    print("")
    print("Step 2: Substitute")
    print("(s^2Y - 2) + 2(sY) + Y = 1/(s-5)")
    print("")
    print("Step 3: Combine Y terms")
    print("(s^2 + 2s + 1)Y - 2 = 1/(s-5)")
    print("")
    print("Step 4: Solve for Y(s)")
    print("Y(s) = (1/(s-5) + 2)/(s+1)^2")
    print("Y(s) = (2s - 9)/((s-5)(s+1)^2)")
    print("")
    print("Notice: (s+1)^2 is a repeated pole.")
    print("That is valid. It just means inverse Laplace must use repeated-pole formulas.")
    line()

def convolution():
    line()
    print("Convolution problem:")
    print("Y(s) = 1/((s-3)(s+5))")
    print("")
    print("Step 1:")
    print("L^-1{1/(s-3)} = e^(3t)")
    print("L^-1{1/(s+5)} = e^(-5t)")
    print("")
    print("Step 2: Convolution")
    print("y(t) = integral from 0 to t of e^(3u)e^(-5(t-u)) du")
    print("")
    print("Step 3: Result")
    print("y(t) = (e^(3t) - e^(-5t))/8")
    line()

def piecewise():
    line()
    print("Rewrite piecewise function:")
    print("f(t)=4 for 0<t<2")
    print("f(t)=-8+4t for t>2")
    print("")
    print("Step 1: Unit step form")
    print("f(t)=4 - 4U(t-2) + 4(t-2)U(t-2)")
    print("")
    print("Step 2: Laplace transform")
    print("F(s)=4/s - 4e^(-2s)/s + 4e^(-2s)/s^2")
    line()

def inverse_shift():
    line()
    print("Inverse Laplace with exponential shift")
    print("1 -> 1/s + e^(-2s)(1/s - 3)")
    print("2 -> custom A/s + e^(-a s)(B/s + C)")
    print("3 -> custom A/s + e^(-a s)(B/(s-r))")
    ch = input("Choice: ")

    if ch == "1":
        print("")
        print("F(s)=1/s + e^(-2s)(1/s - 3)")
        print("")
        print("L^-1{1/s}=1")
        print("L^-1{1/s - 3}=1 - 3delta(t)")
        print("Apply shift:")
        print("f(t)=1 + U(t-2) - 3delta(t-2)")
    elif ch == "2":
        A = float(input("A = "))
        a = float(input("shift a = "))
        B = float(input("B = "))
        C = float(input("C = "))
        print("")
        print("L^-1{A/s} = " + fmt(A))
        print("L^-1{B/s + C} = " + fmt(B) + " + " + fmt(C) + "delta(t)")
        print("Apply shift:")
        print("f(t) = " + fmt(A) + " + " + fmt(B) + "U(t-" + fmt(a) + ") + " + fmt(C) + "delta(t-" + fmt(a) + ")")
    elif ch == "3":
        A = float(input("A = "))
        a = float(input("shift a = "))
        B = float(input("B = "))
        r = float(input("r = "))
        print("")
        print("L^-1{A/s} = " + fmt(A))
        print("L^-1{B/(s-r)} = " + fmt(B) + "e^(" + fmt(r) + "t)")
        print("Apply shift:")
        print("f(t) = " + fmt(A) + " + " + fmt(B) + "U(t-" + fmt(a) + ")e^(" + fmt(r) + "(t-" + fmt(a) + "))")
    line()

def spring():
    line()
    print("Solve spring DE:")
    print("y'' + 16y = 10delta(t-4pi)")
    print("y(0)=0, y'(0)=2")
    print("")
    print("Step 1: Laplace")
    print("(s^2Y - 2) + 16Y = 10e^(-4pi s)")
    print("")
    print("Step 2:")
    print("Y(s) = (10e^(-4pi s)+2)/(s^2+16)")
    print("")
    print("Step 3: Inverse")
    print("L^-1{2/(s^2+16)} = (1/2)sin(4t)")
    print("L^-1{10e^(-4pi s)/(s^2+16)} = (5/2)U(t-4pi)sin(4(t-4pi))")
    print("")
    print("y(t) = (1/2)sin(4t) + (5/2)U(t-4pi)sin(4(t-4pi))")
    line()

def laplace_table():
    line()
    print("Laplace table:")
    print("1 -> t^n")
    print("2 -> e^(at)")
    print("3 -> sin(at)")
    print("4 -> cos(at)")
    print("5 -> t^n e^(at)")
    ch = input("Choice: ")

    if ch == "1":
        n = int(input("n = "))
        print("L{t^n} = " + fmt(factorial(n)) + "/s^" + fmt(n + 1))
    elif ch == "2":
        a = float(input("a = "))
        print("L{e^(at)} = 1/(s-" + fmt(a) + ")")
    elif ch == "3":
        a = float(input("a = "))
        print("L{sin(at)} = " + fmt(a) + "/(s^2+" + fmt(a * a) + ")")
    elif ch == "4":
        a = float(input("a = "))
        print("L{cos(at)} = s/(s^2+" + fmt(a * a) + ")")
    elif ch == "5":
        n = int(input("n = "))
        a = float(input("a = "))
        print("L{t^n e^(at)} = " + fmt(factorial(n)) + "/(s-" + fmt(a) + ")^" + fmt(n + 1))
    line()

def inverse_table():
    line()
    print("Inverse Laplace table:")
    print("1 -> 1/(s-a)")
    print("2 -> 1/(s-a)^2")
    print("3 -> 1/(s-a)^3")
    print("4 -> 1/(s-a)^n")
    print("5 -> a/(s^2+a^2)")
    print("6 -> s/(s^2+a^2)")
    ch = input("Choice: ")

    if ch == "1":
        a = float(input("a = "))
        print("L^-1{1/(s-a)} = e^(" + fmt(a) + "t)")
    elif ch == "2":
        a = float(input("a = "))
        print("L^-1{1/(s-a)^2} = t e^(" + fmt(a) + "t)")
    elif ch == "3":
        a = float(input("a = "))
        print("L^-1{1/(s-a)^3} = (t^2/2)e^(" + fmt(a) + "t)")
    elif ch == "4":
        a = float(input("a = "))
        n = int(input("n = "))
        print("L^-1{1/(s-a)^n} = t^" + fmt(n - 1) + "e^(" + fmt(a) + "t)/" + fmt(factorial(n - 1)))
    elif ch == "5":
        a = float(input("a = "))
        print("L^-1{" + fmt(a) + "/(s^2+" + fmt(a * a) + ")} = sin(" + fmt(a) + "t)")
    elif ch == "6":
        a = float(input("a = "))
        print("L^-1{s/(s^2+" + fmt(a * a) + ")} = cos(" + fmt(a) + "t)")
    line()

def run_examples():
    solve_Y()
    convolution()
    piecewise()
    inverse_shift()
    spring()

def menu():
    while True:
        print("")
        print("Laplace Solver")
        print("1 Solve Y(s) example")
        print("2 Convolution example")
        print("3 Piecewise -> unit step")
        print("4 Inverse Laplace with shift")
        print("5 Spring impulse example")
        print("6 Laplace table")
        print("7 Inverse Laplace table")
        print("8 Inverse repeated-pole basic forms")
        print("9 Partial fractions, distinct poles")
        print("10 Partial fractions, repeated pole")
        print("11 Inverse rational quadratic")
        print("12 Run all worksheet examples")
        print("13 Quit")

        c = input("Select: ")

        if c == "1":
            solve_Y()
        elif c == "2":
            convolution()
        elif c == "3":
            piecewise()
        elif c == "4":
            inverse_shift()
        elif c == "5":
            spring()
        elif c == "6":
            laplace_table()
        elif c == "7":
            inverse_table()
        elif c == "8":
            inverse_basic_power_shift()
        elif c == "9":
            partial_fraction_distinct_linear()
        elif c == "10":
            partial_fraction_repeated_linear()
        elif c == "11":
            inverse_rational_quadratic()
        elif c == "12":
            run_examples()
        elif c == "13":
            break
        else:
            print("Invalid")

menu()
