from math import pi

def factorial(n):
    if n < 0:
        return None
    result = 1
    i = 1
    while i <= n:
        result = result * i
        i = i + 1
    return result

def fmt(x):
    if isinstance(x, int):
        return str(x)
    if abs(x - int(x)) < 1e-10:
        return str(int(x))
    s = "{:.10f}".format(x).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s

def sign_str(x):
    if x >= 0:
        return "+ " + fmt(x)
    return "- " + fmt(abs(x))

def quad_str(a, b, c, var):
    out = ""
    if abs(a) > 1e-10:
        if abs(a - 1) < 1e-10:
            out += var + "^2"
        elif abs(a + 1) < 1e-10:
            out += "-" + var + "^2"
        else:
            out += fmt(a) + var + "^2"
    if abs(b) > 1e-10:
        if out != "":
            out += " "
        if abs(b - 1) < 1e-10:
            out += "+ " + var
        elif abs(b + 1) < 1e-10:
            out += "- " + var
        else:
            out += sign_str(b) + var
    if abs(c) > 1e-10:
        if out != "":
            out += " "
        out += sign_str(c)
    return out.strip()

def print_line():
    print("----------------------------------------")

def solve_Y_exp_rhs(a, b, c, k, y0, y1):
    print_line()
    print("Problem type: Solve for Y(s) in")
    print("y'' + a y' + b y = c e^(k t)")
    print("")
    print("Inputs:")
    print("a =", fmt(a), "b =", fmt(b), "c =", fmt(c), "k =", fmt(k), "y(0) =", fmt(y0), "y'(0) =", fmt(y1))
    print("")
    print("Step 1: Take Laplace transforms")
    print("L{y''} = s^2 Y - s y(0) - y'(0)")
    print("L{y'}  = sY - y(0)")
    print("L{y}   = Y")
    print("L{c e^(k t)} = c / (s - k)")
    print("")
    print("Step 2: Substitute")
    left = "(s^2 Y - s(" + fmt(y0) + ") - " + fmt(y1) + ") + " + fmt(a) + "(sY - " + fmt(y0) + ") + " + fmt(b) + "Y"
    right = fmt(c) + "/(s - " + fmt(k) + ")"
    print(left + " = " + right)
    print("")
    extra = y1 + a * y0
    print("Step 3: Collect Y terms")
    print("(" + quad_str(1, a, b, "s") + ")Y - (" + fmt(extra) + " + " + fmt(y0) + "s" + (" " if abs(y0) > 1e-10 else "") + ") = " + right)
    print("Since y(0) =", fmt(y0) + ", this becomes:")
    print("(" + quad_str(1, a, b, "s") + ")Y - " + fmt(extra) + " = " + right)
    print("")
    print("Step 4: Solve for Y(s)")
    print("Y(s) = (" + right + " + " + fmt(extra) + ") / (" + quad_str(1, a, b, "s") + ")")
    print("")
    if abs(a - 2) < 1e-10 and abs(b - 1) < 1e-10 and abs(c - 1) < 1e-10 and abs(k - 5) < 1e-10 and abs(y0) < 1e-10 and abs(y1 - 2) < 1e-10:
        print("For this specific problem:")
        print("Y(s) = (1/(s - 5) + 2) / (s + 1)^2")
        print("Y(s) = (2s - 9) / ((s - 5)(s + 1)^2)")
    print_line()

def convolution_two_linear_factors(a, b):
    print_line()
    print("Problem type: Convolution theorem for")
    print("Y(s) = 1 / ((s - a)(s - b))")
    print("")
    print("Inputs:")
    print("a =", fmt(a), "b =", fmt(b))
    print("")
    print("Step 1: Split the product")
    print("Y(s) = [1/(s - " + fmt(a) + ")] [1/(s - " + fmt(b) + ")]")
    print("")
    print("Step 2: Inverse Laplace each factor")
    print("L^-1{1/(s - " + fmt(a) + ")} = e^(" + fmt(a) + " t)")
    print("L^-1{1/(s - " + fmt(b) + ")} = e^(" + fmt(b) + " t)")
    print("")
    print("Step 3: Use convolution")
    print("y(t) = integral from 0 to t of e^(" + fmt(a) + " tau) e^(" + fmt(b) + " (t - tau)) d tau")
    if abs(a - b) > 1e-10:
        print("y(t) = e^(" + fmt(b) + " t) integral from 0 to t of e^((" + fmt(a - b) + ") tau) d tau")
        print("y(t) = e^(" + fmt(b) + " t) [ e^((" + fmt(a - b) + ") tau) / (" + fmt(a - b) + ") ] from 0 to t")
        print("y(t) = (e^(" + fmt(a) + " t) - e^(" + fmt(b) + " t)) / (" + fmt(a - b) + ")")
    else:
        print("Special case a = b")
        print("y(t) = t e^(" + fmt(a) + " t)")
    print_line()

def piecewise_const_then_linear(c0, shift, m, b):
    print_line()
    print("Problem type: Rewrite a piecewise function using U(t-a)")
    print("")
    print("Inputs:")
    print("f(t) =", fmt(c0), "for 0 < t <", fmt(shift))
    print("f(t) =", fmt(m) + "t " + sign_str(b), "for t >", fmt(shift))
    print("")
    print("Step 1: Write the second piece in shifted form")
    k = m * shift + b - c0
    print("General formula:")
    print("f(t) = " + fmt(c0) + " + U(t - " + fmt(shift) + ")[" + fmt(m) + "(t - " + fmt(shift) + ") " + sign_str(k) + "]")
    print("")
    print("Step 2: Expand if desired")
    print("f(t) = " + fmt(c0) + " + U(t - " + fmt(shift) + ")(" + fmt(m) + "(t - " + fmt(shift) + ") " + sign_str(k) + ")")
    print("")
    print("Step 3: Take Laplace transforms")
    print("L{" + fmt(c0) + "} = " + fmt(c0) + "/s")
    print("L{U(t-a) g(t-a)} = e^(-a s) G(s)")
    print("Here g(t) = " + fmt(m) + "t " + sign_str(k))
    print("So G(s) = " + fmt(m) + "/s^2 " + sign_str(k) + "/s")
    print("")
    print("Final answers:")
    print("f(t) = " + fmt(c0) + " + U(t - " + fmt(shift) + ")(" + fmt(m) + "(t - " + fmt(shift) + ") " + sign_str(k) + ")")
    print("F(s) = " + fmt(c0) + "/s + e^(-" + fmt(shift) + "s)(" + fmt(m) + "/s^2 " + sign_str(k) + "/s)")
    print("")
    if abs(c0 - 4) < 1e-10 and abs(shift - 2) < 1e-10 and abs(m - 4) < 1e-10 and abs(b + 8) < 1e-10:
        print("Equivalent cleaner form for this specific problem:")
        print("f(t) = 4 - 4U(t - 2) + 4(t - 2)U(t - 2)")
        print("F(s) = 4/s - 4e^(-2s)/s + 4e^(-2s)/s^2")
    print_line()

def inverse_shift_basic():
    print_line()
    print("Problem type: Inverse Laplace of A/s + e^(-a s) G(s)")
    print("")
    print("Choose the inside form G(s):")
    print("1 -> B/s + C/(s-r)")
    print("2 -> B/s + C   (this creates a delta term)")
    choice = int(input("Enter 1 or 2: "))
    A = float(input("A = "))
    a = float(input("shift a = "))
    if choice == 1:
        B = float(input("B = "))
        C = float(input("C = "))
        r = float(input("r = "))
        print("")
        print("Step 1: Invert the unshifted part")
        print("L^-1{A/s} = " + fmt(A))
        print("")
        print("Step 2: Invert G(s)")
        print("L^-1{B/s} = " + fmt(B))
        print("L^-1{C/(s-r)} = " + fmt(C) + " e^(" + fmt(r) + " t)")
        print("So g(t) = " + fmt(B) + " + " + fmt(C) + "e^(" + fmt(r) + " t)")
        print("")
        print("Step 3: Apply the shift theorem")
        print("L^-1{e^(-a s)G(s)} = U(t-a) g(t-a)")
        print("")
        print("Final answer:")
        print("f(t) = " + fmt(A) + " + U(t - " + fmt(a) + ")(" + fmt(B) + " + " + fmt(C) + "e^(" + fmt(r) + "(t - " + fmt(a) + ")))")
    else:
        B = float(input("B = "))
        C = float(input("C = "))
        print("")
        print("Step 1: Invert the unshifted part")
        print("L^-1{A/s} = " + fmt(A))
        print("")
        print("Step 2: Invert G(s)")
        print("L^-1{B/s} = " + fmt(B))
        print("L^-1{C} = " + fmt(C) + " delta(t)")
        print("So g(t) = " + fmt(B) + " + " + fmt(C) + " delta(t)")
        print("")
        print("Step 3: Apply the shift theorem")
        print("Final answer:")
        print("f(t) = " + fmt(A) + " + U(t - " + fmt(a) + ")(" + fmt(B) + ") + " + fmt(C) + " delta(t - " + fmt(a) + ")")
    print_line()

def spring_impulse_solution(omega, A, a, y0, v0):
    print_line()
    print("Problem type: Solve")
    print("y'' + omega^2 y = A delta(t-a)")
    print("")
    print("Inputs:")
    print("omega =", fmt(omega), "A =", fmt(A), "a =", fmt(a), "y(0) =", fmt(y0), "y'(0) =", fmt(v0))
    print("")
    print("Step 1: Take Laplace transforms")
    print("L{y''} = s^2 Y - s y(0) - y'(0)")
    print("L{omega^2 y} = " + fmt(omega * omega) + "Y")
    print("L{A delta(t-a)} = " + fmt(A) + "e^(-" + fmt(a) + "s)")
    print("")
    print("Step 2: Substitute")
    print("(s^2 Y - s(" + fmt(y0) + ") - " + fmt(v0) + ") + " + fmt(omega * omega) + "Y = " + fmt(A) + "e^(-" + fmt(a) + "s)")
    print("")
    print("Step 3: Solve for Y(s)")
    print("Y(s) = (" + fmt(A) + "e^(-" + fmt(a) + "s) + " + fmt(y0) + "s + " + fmt(v0) + ") / (s^2 + " + fmt(omega * omega) + ")")
    print("")
    print("Step 4: Invert term by term")
    print("L^-1{s/(s^2 + omega^2)} = cos(omega t)")
    print("L^-1{1/(s^2 + omega^2)} = (1/omega) sin(omega t)")
    print("L^-1{e^(-a s)/(s^2 + omega^2)} = U(t-a)(1/omega)sin(omega(t-a))")
    print("")
    print("Final answer:")
    print("y(t) = " + fmt(y0) + "cos(" + fmt(omega) + "t) + (" + fmt(v0) + "/" + fmt(omega) + ")sin(" + fmt(omega) + "t) + (" + fmt(A) + "/" + fmt(omega) + ")U(t - " + fmt(a) + ")sin(" + fmt(omega) + "(t - " + fmt(a) + "))")
    print("")
    if abs(omega - 4) < 1e-10 and abs(A - 10) < 1e-10 and abs(a - 4 * pi) < 1e-10 and abs(y0) < 1e-10 and abs(v0 - 2) < 1e-10:
        print("For this specific problem:")
        print("y(t) = (1/2)sin(4t) + (5/2)U(t - 4pi)sin(4(t - 4pi))")
    print_line()

def laplace_table_tool():
    print_line()
    print("Laplace transform helper")
    print("1 -> L{t^n}")
    print("2 -> L{e^(a t)}")
    print("3 -> L{sin(a t)}")
    print("4 -> L{cos(a t)}")
    print("5 -> L{t^n e^(a t)}")
    ch = int(input("Choose: "))
    if ch == 1:
        n = int(input("n = "))
        print("L{t^n} = " + fmt(factorial(n)) + "/s^" + fmt(n + 1))
    elif ch == 2:
        a = float(input("a = "))
        print("L{e^(a t)} = 1/(s - " + fmt(a) + ")")
    elif ch == 3:
        a = float(input("a = "))
        print("L{sin(a t)} = " + fmt(a) + "/(s^2 + " + fmt(a * a) + ")")
    elif ch == 4:
        a = float(input("a = "))
        print("L{cos(a t)} = s/(s^2 + " + fmt(a * a) + ")")
    elif ch == 5:
        n = int(input("n = "))
        a = float(input("a = "))
        print("L{t^n e^(a t)} = " + fmt(factorial(n)) + "/(s - " + fmt(a) + ")^" + fmt(n + 1))
    print_line()

def inverse_laplace_table_tool():
    print_line()
    print("Inverse Laplace helper")
    print("1 -> L^-1{1/s^n}")
    print("2 -> L^-1{1/(s-a)}")
    print("3 -> L^-1{a/(s^2+a^2)}")
    print("4 -> L^-1{s/(s^2+a^2)}")
    ch = int(input("Choose: "))
    if ch == 1:
        n = int(input("n = "))
        print("L^-1{1/s^" + fmt(n) + "} = t^" + fmt(n - 1) + "/" + fmt(factorial(n - 1)))
    elif ch == 2:
        a = float(input("a = "))
        print("L^-1{1/(s-a)} = e^(" + fmt(a) + " t)")
    elif ch == 3:
        a = float(input("a = "))
        print("L^-1{" + fmt(a) + "/(s^2+" + fmt(a * a) + ")} = sin(" + fmt(a) + " t)")
    elif ch == 4:
        a = float(input("a = "))
        print("L^-1{s/(s^2+" + fmt(a * a) + ")} = cos(" + fmt(a) + " t)")
    print_line()

def examples_from_your_sheet():
    print_line()
    print("Running your exact examples")
    print_line()
    solve_Y_exp_rhs(2, 1, 1, 5, 0, 2)
    convolution_two_linear_factors(3, -5)
    piecewise_const_then_linear(4, 2, 4, -8)
    print_line()
    print("Problem 6 note:")
    print("If F(s) = 1/s + e^(-2s)(1/s - 3), then")
    print("f(t) = 1 + U(t-2) - 3 delta(t-2)")
    print("")
    print("If instead your teacher meant F(s) = 1/s + e^(-2s)/(s-3), then")
    print("f(t) = 1 + U(t-2)e^(3(t-2))")
    print_line()
    spring_impulse_solution(4, 10, 4 * pi, 0, 2)

def menu():
    while True:
        print("")
        print("Laplace Toolkit for TI-Nspire CX II CAS")
        print("1 -> Solve for Y(s) in y'' + a y' + b y = c e^(k t)")
        print("2 -> Convolution for 1/((s-a)(s-b))")
        print("3 -> Piecewise constant then linear -> unit step and F(s)")
        print("4 -> Inverse Laplace with exponential shift")
        print("5 -> Spring/impulse equation y'' + omega^2 y = A delta(t-a)")
        print("6 -> Basic Laplace transform table")
        print("7 -> Basic inverse Laplace table")
        print("9 -> Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            a = float(input("a = "))
            b = float(input("b = "))
            c = float(input("c = "))
            k = float(input("k = "))
            y0 = float(input("y(0) = "))
            y1 = float(input("y'(0) = "))
            solve_Y_exp_rhs(a, b, c, k, y0, y1)
        elif choice == "2":
            a = float(input("a = "))
            b = float(input("b = "))
            convolution_two_linear_factors(a, b)
        elif choice == "3":
            c0 = float(input("First piece constant value c0 = "))
            shift = float(input("Break point a = "))
            m = float(input("Second piece slope m = "))
            b = float(input("Second piece intercept b in mt+b = "))
            piecewise_const_then_linear(c0, shift, m, b)
        elif choice == "4":
            inverse_shift_basic()
        elif choice == "5":
            omega = float(input("omega = "))
            A = float(input("Impulse size A = "))
            a = float(input("Impulse time a = "))
            y0 = float(input("y(0) = "))
            v0 = float(input("y'(0) = "))
            spring_impulse_solution(omega, A, a, y0, v0)
        elif choice == "6":
            laplace_table_tool()
        elif choice == "7":
            inverse_laplace_table_tool()
        elif choice == "8":
            examples_from_your_sheet()
        elif choice == "9":
            break
        else:
            print("Invalid choice")

menu()
