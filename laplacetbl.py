def factorial(n):
    if n < 0:
        raise ValueError("factorial undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fmt(x):
    if abs(x - round(x)) < 1e-10:
        return str(int(round(x)))
    s = "{:.10f}".format(x).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s

def power_str(base, n):
    if n == 1:
        return base
    return "(" + base + ")^" + str(n)

def laplace_term():
    print("Choose Laplace term type:")
    print("1: c*t^n*e^(a*t)")
    print("2: c*e^(a*t)*sin(k*t)")
    print("3: c*e^(a*t)*cos(k*t)")
    print("4: c*e^(a*t)*sinh(k*t)")
    print("5: c*e^(a*t)*cosh(k*t)")
    typ = int(input("Type: "))

    if typ == 1:
        c = float(input("c = "))
        n = int(input("n = "))
        a = float(input("a = "))
        coef = c * factorial(n)
        den = power_str("s-" + fmt(a) if a != 0 else "s", n + 1)

        print("")
        print("TERM:")
        if a == 0:
            print("f(t) = " + fmt(c) + "*t^" + str(n))
            print("Use L{t^n} = n!/s^(n+1)")
        else:
            print("f(t) = " + fmt(c) + "*t^" + str(n) + "*e^(" + fmt(a) + "*t)")
            print("Use shift rule: L{e^(a*t)f(t)} = F(s-a)")
            print("Base: L{t^n} = n!/s^(n+1)")
            print("So: L{t^n*e^(a*t)} = n!/(s-a)^(n+1)")

        print("Multiply by " + fmt(c))
        print("Result: " + fmt(coef) + "/" + den)
        return fmt(coef) + "/" + den

    elif typ == 2:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))
        num = c * k
        shift = "s-" + fmt(a) if a != 0 else "s"
        den = "(" + shift + ")^2+" + fmt(k * k)

        print("")
        print("TERM:")
        print("f(t) = " + fmt(c) + "*e^(" + fmt(a) + "*t)*sin(" + fmt(k) + "*t)")
        print("Use L{sin(k*t)} = k/(s^2+k^2)")
        print("Shift by a: replace s with s-a")
        print("Then multiply by " + fmt(c))
        print("Result: " + fmt(num) + "/(" + den + ")")
        return fmt(num) + "/(" + den + ")"

    elif typ == 3:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))
        shift = "s-" + fmt(a) if a != 0 else "s"

        print("")
        print("TERM:")
        print("f(t) = " + fmt(c) + "*e^(" + fmt(a) + "*t)*cos(" + fmt(k) + "*t)")
        print("Use L{cos(k*t)} = s/(s^2+k^2)")
        print("Shift by a: replace s with s-a")
        print("Then multiply by " + fmt(c))
        print("Result: " + fmt(c) + "*(" + shift + ")/((" + shift + ")^2+" + fmt(k * k) + ")")
        return fmt(c) + "*(" + shift + ")/((" + shift + ")^2+" + fmt(k * k) + ")"

    elif typ == 4:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))
        num = c * k
        shift = "s-" + fmt(a) if a != 0 else "s"
        den = "(" + shift + ")^2-" + fmt(k * k)

        print("")
        print("TERM:")
        print("f(t) = " + fmt(c) + "*e^(" + fmt(a) + "*t)*sinh(" + fmt(k) + "*t)")
        print("Use L{sinh(k*t)} = k/(s^2-k^2)")
        print("Shift by a: replace s with s-a")
        print("Then multiply by " + fmt(c))
        print("Result: " + fmt(num) + "/(" + den + ")")
        return fmt(num) + "/(" + den + ")"

    elif typ == 5:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))
        shift = "s-" + fmt(a) if a != 0 else "s"

        print("")
        print("TERM:")
        print("f(t) = " + fmt(c) + "*e^(" + fmt(a) + "*t)*cosh(" + fmt(k) + "*t)")
        print("Use L{cosh(k*t)} = s/(s^2-k^2)")
        print("Shift by a: replace s with s-a")
        print("Then multiply by " + fmt(c))
        print("Result: " + fmt(c) + "*(" + shift + ")/((" + shift + ")^2-" + fmt(k * k) + ")")
        return fmt(c) + "*(" + shift + ")/((" + shift + ")^2-" + fmt(k * k) + ")"

    else:
        print("Unsupported type.")
        return ""

def inverse_term():
    print("Choose inverse Laplace term type:")
    print("1: c/(s-a)^n")
    print("2: c*k/((s-a)^2+k^2)")
    print("3: c*(s-a)/((s-a)^2+k^2)")
    print("4: c*k/((s-a)^2-k^2)")
    print("5: c*(s-a)/((s-a)^2-k^2)")
    typ = int(input("Type: "))

    if typ == 1:
        c = float(input("c = "))
        a = float(input("a = "))
        n = int(input("n = "))

        print("")
        print("TERM:")
        print("F(s) = " + fmt(c) + "/(s-" + fmt(a) + ")^" + str(n))
        print("Use L^-1{1/(s-a)^n} = t^(n-1)e^(a*t)/(n-1)!")

        coef = c / factorial(n - 1)
        if n == 1:
            print("Since n = 1, this is just " + fmt(c) + "*e^(" + fmt(a) + "*t)")
            return fmt(c) + "*e^(" + fmt(a) + "*t)"
        else:
            print("Coefficient becomes " + fmt(c) + "/(" + str(factorial(n - 1)) + ") = " + fmt(coef))
            print("Result: " + fmt(coef) + "*t^" + str(n - 1) + "*e^(" + fmt(a) + "*t)")
            return fmt(coef) + "*t^" + str(n - 1) + "*e^(" + fmt(a) + "*t)"

    elif typ == 2:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))

        print("")
        print("TERM:")
        print("F(s) = " + fmt(c) + "*" + fmt(k) + "/((s-" + fmt(a) + ")^2+" + fmt(k * k) + ")")
        print("Use L^-1{k/((s-a)^2+k^2)} = e^(a*t)sin(k*t)")
        print("Multiply by " + fmt(c))
        return fmt(c) + "*e^(" + fmt(a) + "*t)*sin(" + fmt(k) + "*t)"

    elif typ == 3:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))

        print("")
        print("TERM:")
        print("F(s) = " + fmt(c) + "*(s-" + fmt(a) + ")/((s-" + fmt(a) + ")^2+" + fmt(k * k) + ")")
        print("Use L^-1{(s-a)/((s-a)^2+k^2)} = e^(a*t)cos(k*t)")
        print("Multiply by " + fmt(c))
        return fmt(c) + "*e^(" + fmt(a) + "*t)*cos(" + fmt(k) + "*t)"

    elif typ == 4:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))

        print("")
        print("TERM:")
        print("F(s) = " + fmt(c) + "*" + fmt(k) + "/((s-" + fmt(a) + ")^2-" + fmt(k * k) + ")")
        print("Use L^-1{k/((s-a)^2-k^2)} = e^(a*t)sinh(k*t)")
        print("Multiply by " + fmt(c))
        return fmt(c) + "*e^(" + fmt(a) + "*t)*sinh(" + fmt(k) + "*t)"

    elif typ == 5:
        c = float(input("c = "))
        a = float(input("a = "))
        k = float(input("k = "))

        print("")
        print("TERM:")
        print("F(s) = " + fmt(c) + "*(s-" + fmt(a) + ")/((s-" + fmt(a) + ")^2-" + fmt(k * k) + ")")
        print("Use L^-1{(s-a)/((s-a)^2-k^2)} = e^(a*t)cosh(k*t)")
        print("Multiply by " + fmt(c))
        return fmt(c) + "*e^(" + fmt(a) + "*t)*cosh(" + fmt(k) + "*t)"

    else:
        print("Unsupported type.")
        return ""

def main():
    print("STEP-BY-STEP LAPLACE TOOL")
    print("1: Laplace transform")
    print("2: Inverse Laplace transform")
    mode = int(input("Mode: "))

    n = int(input("How many terms are in the sum? "))
    results = []

    print("")
    for i in range(n):
        print("----- Term " + str(i + 1) + " -----")
        if mode == 1:
            results.append(laplace_term())
        else:
            results.append(inverse_term())
        print("")

    print("FINAL ANSWER:")
    ans = ""
    for i in range(len(results)):
        if i == 0:
            ans = results[i]
        else:
            ans += " + " + results[i]
    print(ans)

main()
