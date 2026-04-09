def fmt(x):
    if abs(x - round(x)) < 1e-10:
        return str(int(round(x)))
    s = "{:.10f}".format(x).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s

def trim(p):
    while len(p) > 1 and abs(p[-1]) < 1e-12:
        p.pop()
    return p

def poly_add(p, q):
    n = max(len(p), len(q))
    r = [0.0] * n
    for i in range(len(p)):
        r[i] += p[i]
    for i in range(len(q)):
        r[i] += q[i]
    return trim(r)

def poly_sub(p, q):
    n = max(len(p), len(q))
    r = [0.0] * n
    for i in range(len(p)):
        r[i] += p[i]
    for i in range(len(q)):
        r[i] -= q[i]
    return trim(r)

def poly_mul(p, q):
    r = [0.0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            r[i + j] += p[i] * q[j]
    return trim(r)

def poly_scale(p, c):
    return trim([c * x for x in p])

def poly_eval(p, x):
    total = 0.0
    xp = 1.0
    for c in p:
        total += c * xp
        xp *= x
    return total

def poly_deriv(p):
    if len(p) <= 1:
        return [0.0]
    r = [0.0] * (len(p) - 1)
    for i in range(1, len(p)):
        r[i - 1] = i * p[i]
    return trim(r)

def poly_div_linear(p, r):
    # divide p(s) by (s-r)
    n = len(p) - 1
    if n < 1:
        return [0.0], p[0]
    q = [0.0] * n
    q[n - 1] = p[n]
    for i in range(n - 1, 0, -1):
        q[i - 1] = p[i] + r * q[i]
    rem = p[0] + r * q[0]
    return trim(q), rem

def poly_to_string(p):
    parts = []
    for i in range(len(p) - 1, -1, -1):
        c = p[i]
        if abs(c) < 1e-12:
            continue

        sign = "+" if c > 0 else "-"
        a = abs(c)

        if i == 0:
            term = fmt(a)
        elif i == 1:
            if abs(a - 1.0) < 1e-12:
                term = "s"
            else:
                term = fmt(a) + "*s"
        else:
            if abs(a - 1.0) < 1e-12:
                term = "s^" + str(i)
            else:
                term = fmt(a) + "*s^" + str(i)

        parts.append((sign, term))

    if not parts:
        return "0"

    out = ""
    if parts[0][0] == "-":
        out += "-"
    out += parts[0][1]

    for sign, term in parts[1:]:
        out += " " + sign + " " + term

    return out

def factor_poly_from_root_mult(root, mult):
    p = [1.0]
    factor = [-root, 1.0]
    for _ in range(mult):
        p = poly_mul(p, factor)
    return trim(p)

def build_G_terms():
    terms = []
    m = int(input("How many forcing terms in g(t)? "))
    print("Enter each forcing term as c*e^(r*t).")
    print("For a constant C, enter c = C and r = 0.")
    for i in range(m):
        print("Term " + str(i + 1))
        c = float(input("c = "))
        r = float(input("r = "))
        terms.append((c, r))
    return terms

def G_string(terms):
    if len(terms) == 0:
        return "0"
    parts = []
    for c, r in terms:
        if abs(r) < 1e-12:
            parts.append(fmt(c))
        else:
            parts.append(fmt(c) + "*e^(" + fmt(r) + "*t)")
    return " + ".join(parts)

def G_laplace_string(terms):
    if len(terms) == 0:
        return "0"
    parts = []
    for c, r in terms:
        parts.append(fmt(c) + "/(s-" + fmt(r) + ")")
    return " + ".join(parts)

def count_mults(values):
    roots = []
    mults = []
    for x in values:
        found = False
        for i in range(len(roots)):
            if abs(x - roots[i]) < 1e-10:
                mults[i] += 1
                found = True
                break
        if not found:
            roots.append(x)
            mults.append(1)
    return roots, mults

def gaussian_elimination(A, b):
    n = len(b)

    for col in range(n):
        pivot = col
        for r in range(col + 1, n):
            if abs(A[r][col]) > abs(A[pivot][col]):
                pivot = r

        if abs(A[pivot][col]) < 1e-12:
            raise ValueError("System is singular or nearly singular")

        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            b[col], b[pivot] = b[pivot], b[col]

        piv = A[col][col]
        for j in range(col, n):
            A[col][j] /= piv
        b[col] /= piv

        for r in range(n):
            if r != col:
                factor = A[r][col]
                if abs(factor) > 1e-12:
                    for j in range(col, n):
                        A[r][j] -= factor * A[col][j]
                    b[r] -= factor * b[col]

    return b

def partial_fractions_repeated(num, roots, mults):
    # We want:
    # num/den = sum A_{i,k}/(s-r_i)^k
    # with k = 1..m_i
    #
    # Multiply by den:
    # num = sum A_{i,k} * den/(s-r_i)^k
    #
    # Solve by coefficient matching.

    den = [1.0]
    for i in range(len(roots)):
        den = poly_mul(den, factor_poly_from_root_mult(roots[i], mults[i]))

    basis = []
    labels = []

    for i in range(len(roots)):
        r = roots[i]
        m = mults[i]
        for k in range(1, m + 1):
            piece = den[:]
            for _ in range(k):
                piece, rem = poly_div_linear(piece, r)
            basis.append(trim(piece))
            labels.append((r, k))

    n_unknowns = len(basis)
    deg_max = max(len(den) - 2, len(num) - 1)
    if deg_max + 1 < n_unknowns:
        deg_max = n_unknowns - 1

    A = []
    b = []

    for power in range(n_unknowns):
        row = []
        for piece in basis:
            row.append(piece[power] if power < len(piece) else 0.0)
        A.append(row)
        b.append(num[power] if power < len(num) else 0.0)

    coeffs = gaussian_elimination(A, b)

    result = []
    for i in range(len(coeffs)):
        result.append((coeffs[i], labels[i][0], labels[i][1]))
    return result

def pf_string(pf):
    parts = []
    for A, r, k in pf:
        denom = "(s-" + fmt(r) + ")"
        if k > 1:
            denom += "^" + str(k)
        parts.append(fmt(A) + "/" + denom)
    if len(parts) == 0:
        return "0"
    return " + ".join(parts)

def time_term_from_pf(A, r, k):
    # L^-1{ A / (s-r)^k } = A * t^(k-1)/(k-1)! * e^(r t)
    fact = 1
    for i in range(2, k):
        fact *= i

    coef = A / fact

    if k == 1:
        if abs(r) < 1e-12:
            return fmt(A)
        return fmt(A) + "*e^(" + fmt(r) + "*t)"

    power = k - 1
    tpart = "t^" + str(power) if power > 1 else "t"
    if abs(r) < 1e-12:
        return fmt(coef) + "*" + tpart
    return fmt(coef) + "*" + tpart + "*e^(" + fmt(r) + "*t)"

def solution_string_from_pf(pf):
    parts = []
    for A, r, k in pf:
        parts.append(time_term_from_pf(A, r, k))
    if len(parts) == 0:
        return "0"
    return " + ".join(parts)

def build_rational_first_order(a, y0, forcing):
    # y' + a y = g(t)
    # (sY - y0) + aY = G
    # Y = (G + y0)/(s+a)

    sys_den = [a, 1.0]
    total_num = [y0]
    total_den = sys_den[:]

    raw_poles = [-a]

    for c, r in forcing:
        total_num = poly_add(poly_mul(total_num, [-r, 1.0]), poly_scale(total_den, c))
        total_den = poly_mul(total_den, [-r, 1.0])
        raw_poles.append(r)

    return trim(total_num), trim(total_den), raw_poles

def build_rational_second_order(a, b, y0, y1, forcing):
    # y'' + a y' + b y = g(t)
    # (s^2Y - s y0 - y1) + a(sY - y0) + bY = G
    # Y = [G + s y0 + y1 + a y0] / (s^2 + a s + b)

    disc = a * a - 4.0 * b
    if disc < -1e-12:
        print("This version only handles real poles.")
        return None, None, None

    if abs(disc) < 1e-12:
        r = -a / 2.0
        raw_poles = [r, r]
    else:
        sqrt_disc = disc ** 0.5
        r1 = (-a + sqrt_disc) / 2.0
        r2 = (-a - sqrt_disc) / 2.0
        raw_poles = [r1, r2]

    base_num = [y1 + a * y0, y0]
    base_den = [b, a, 1.0]

    total_num = base_num[:]
    total_den = base_den[:]

    for c, r in forcing:
        total_num = poly_add(poly_mul(total_num, [-r, 1.0]), poly_scale(total_den, c))
        total_den = poly_mul(total_den, [-r, 1.0])
        raw_poles.append(r)

    return trim(total_num), trim(total_den), raw_poles

def print_repeated_pole_info(roots, mults):
    print("Pole structure:")
    for i in range(len(roots)):
        if mults[i] == 1:
            print("root " + fmt(roots[i]) + " with multiplicity 1")
        else:
            print("root " + fmt(roots[i]) + " with multiplicity " + str(mults[i]))

def main():
    print("IVP SOLVER WITH REPEATED POLES")
    print("1: y' + a y = g(t), y(0)=y0")
    print("2: y'' + a y' + b y = g(t), y(0)=y0, y'(0)=y1")
    mode = int(input("Mode: "))

    if mode == 1:
        a = float(input("a = "))
        y0 = float(input("y0 = "))
        forcing = build_G_terms()

        print("")
        print("STEP 1: Write the ODE")
        print("y' + " + fmt(a) + "y = " + G_string(forcing))

        print("")
        print("STEP 2: Take Laplace transforms")
        print("L{y'} = sY - y0")
        print("(sY - " + fmt(y0) + ") + " + fmt(a) + "Y = " + G_laplace_string(forcing))

        num, den, raw_poles = build_rational_first_order(a, y0, forcing)

        print("")
        print("STEP 3: Solve for Y(s)")
        print("Y(s) = (" + poly_to_string(num) + ")/(" + poly_to_string(den) + ")")

        roots, mults = count_mults(raw_poles)
        print("")
        print("STEP 4: Identify poles")
        print_repeated_pole_info(roots, mults)

        print("")
        print("STEP 5: Partial fractions")
        pf = partial_fractions_repeated(num, roots, mults)
        print("Y(s) = " + pf_string(pf))

        print("")
        print("STEP 6: Inverse Laplace")
        y = solution_string_from_pf(pf)
        print("y(t) = " + y)

    elif mode == 2:
        a = float(input("a = "))
        b = float(input("b = "))
        y0 = float(input("y0 = "))
        y1 = float(input("y1 = "))
        forcing = build_G_terms()

        print("")
        print("STEP 1: Write the ODE")
        print("y'' + " + fmt(a) + "y' + " + fmt(b) + "y = " + G_string(forcing))

        print("")
        print("STEP 2: Take Laplace transforms")
        print("L{y''} = s^2Y - s*y0 - y1")
        print("L{y'} = sY - y0")
        print("(s^2Y - s*" + fmt(y0) + " - " + fmt(y1) + ") + " + fmt(a) + "(sY - " + fmt(y0) + ") + " + fmt(b) + "Y = " + G_laplace_string(forcing))

        num, den, raw_poles = build_rational_second_order(a, b, y0, y1, forcing)
        if num is None:
            return

        print("")
        print("STEP 3: Solve for Y(s)")
        print("Y(s) = (" + poly_to_string(num) + ")/(" + poly_to_string(den) + ")")

        roots, mults = count_mults(raw_poles)
        print("")
        print("STEP 4: Identify poles")
        print_repeated_pole_info(roots, mults)

        print("")
        print("STEP 5: Partial fractions")
        pf = partial_fractions_repeated(num, roots, mults)
        print("Y(s) = " + pf_string(pf))

        print("")
        print("STEP 6: Inverse Laplace")
        y = solution_string_from_pf(pf)
        print("y(t) = " + y)

    else:
        print("Unsupported mode.")

main()
