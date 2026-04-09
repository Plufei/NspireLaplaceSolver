# step_laplace_poly.py
# TI-Nspire CX II CAS compatible
# Solves Laplace transforms of the form P(t)*U(t-a)
# where P(t) is any polynomial

def factorial(n):
    r = 1
    i = 2
    while i <= n:
        r = r * i
        i = i + 1
    return r

def comb(n, r):
    if r < 0 or r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def poly_eval(coeffs, x):
    # coeffs in ascending powers:
    # [c0, c1, c2, ...] means c0 + c1*x + c2*x^2 + ...
    total = 0
    p = 1
    i = 0
    while i < len(coeffs):
        total = total + coeffs[i] * p
        p = p * x
        i = i + 1
    return total

def poly_to_string(coeffs, var):
    # Makes readable polynomial string
    s = ""
    i = len(coeffs) - 1
    first = 1
    while i >= 0:
        c = coeffs[i]
        if c != 0:
            # sign
            if first:
                if c < 0:
                    s = s + "-"
            else:
                if c < 0:
                    s = s + " - "
                else:
                    s = s + " + "

            ac = c
            if ac < 0:
                ac = -ac

            # term body
            if i == 0:
                s = s + str(ac)
            elif i == 1:
                if ac == 1:
                    s = s + var
                else:
                    s = s + str(ac) + "*" + var
            else:
                if ac == 1:
                    s = s + var + "^" + str(i)
                else:
                    s = s + str(ac) + "*" + var + "^" + str(i)

            first = 0
        i = i - 1

    if s == "":
        s = "0"
    return s

def shifted_coeffs(coeffs, a):
    # Rewrites P(t) as Q(u+a), then expresses in powers of u=(t-a)
    # Input coeffs represent P(t)
    # Output coeffs represent Q(u) = P(u+a)
    n = len(coeffs) - 1
    out = []
    i = 0
    while i <= n:
        out.append(0)
        i = i + 1

    k = 0
    while k <= n:
        ck = coeffs[k]
        j = 0
        while j <= k:
            out[j] = out[j] + ck * comb(k, j) * (a ** (k - j))
            j = j + 1
        k = k + 1

    return out

def laplace_poly_string(coeffs):
    # L{c0 + c1*u + c2*u^2 + ...}
    # = c0/s + c1/s^2 + 2!*c2/s^3 + ...
    parts = []
    i = 0
    while i < len(coeffs):
        c = coeffs[i]
        if c != 0:
            num = c * factorial(i)
            denpow = i + 1

            if denpow == 1:
                part = str(num) + "/s"
            else:
                part = str(num) + "/s^" + str(denpow)
            parts.append(part)
        i = i + 1

    if len(parts) == 0:
        return "0"

    # join with signs cleaned up
    result = ""
    i = 0
    while i < len(parts):
        p = parts[i]
        if i == 0:
            result = p
        else:
            if p[0] == "-":
                result = result + " - " + p[1:]
            else:
                result = result + " + " + p
        i = i + 1
    return result

def main():
    print("Laplace of P(t)*U(t-a)")
    print("")
    print("Enter polynomial P(t) by coefficients.")
    print("Example: P(t)=2t^2-5t+7")
    print("degree = 2, then c0=7, c1=-5, c2=2")
    print("")

    deg = int(input("Degree of P(t): "))
    coeffs = []
    i = 0
    while i <= deg:
        coeffs.append(float(input("Coefficient c" + str(i) + ": ")))
        i = i + 1

    a = float(input("Shift a in U(t-a): "))

    print("")
    print("Step 1: Original function")
    print("f(t) = (" + poly_to_string(coeffs, "t") + ")*U(t-" + str(a) + ")")
    print("")

    newc = shifted_coeffs(coeffs, a)

    print("Step 2: Rewrite P(t) in terms of u = t-a")
    print("Then t = u + " + str(a))
    print("So P(t) = P(u+" + str(a) + ")")
    print("Q(u) = " + poly_to_string(newc, "u"))
    print("")
    print("Hence")
    print("f(t) = Q(t-" + str(a) + ")*U(t-" + str(a) + ")")
    print("f(t) = (" + poly_to_string(newc, "(t-" + str(a) + ")") + ")*U(t-" + str(a) + ")")
    print("")

    g = laplace_poly_string(newc)

    print("Step 3: Laplace of Q(u)")
    print("L{Q(u)} = " + g)
    print("")

    print("Step 4: Apply second shifting theorem")
    print("L{Q(t-a)U(t-a)} = e^(-a*s)L{Q(t)}")
    print("")
    print("Final answer:")
    print("F(s) = e^(-" + str(a) + "*s)*(" + g + ")")

main()
