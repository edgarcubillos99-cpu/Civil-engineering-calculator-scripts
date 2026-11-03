import math

# Diseno de canales en flujo uniforme
FT_M = 0.3048
FT3_M3 = 0.0283168466
G = 9.81

def r4(x):
    return round(x, 4)

def r2(x):
    return round(x, 2)

def borde_libre(Q):
    if Q < 0.75:
        return 0.45
    if Q < 1.50:
        return 0.60
    if Q <= 85.0:
        return 0.75
    return 0.90

def geom_trap(b, y, m):
    rm = math.sqrt(1.0 + m * m)
    A = (b + m * y) * y
    P = b + 2.0 * y * rm
    R = A / P
    return A, P, R, A * (R ** (2.0 / 3.0)), rm

def resolver_b(Z, y, m):
    if m > 0 and Z <= geom_trap(0.0, y, m)[3]:
        return 0.0
    bi, bs = 1e-6, 1.0
    while geom_trap(bs, y, m)[3] < Z:
        bs = bs * 2.0
        if bs > 1e6:
            return None
    i = 0
    while i < 60:
        bm = 0.5 * (bi + bs)
        if geom_trap(bm, y, m)[3] < Z:
            bi = bm
        else:
            bs = bm
        i = i + 1
    return 0.5 * (bi + bs)

def fin_hidr(Q, n, S0, b, y, m, A, R, V, p_num):
    T = b + 2.0 * m * y
    D = A / T
    Fr = V / math.sqrt(G * D)
    Qv = (1.0 / n) * A * (R ** (2.0 / 3.0)) * math.sqrt(S0)
    BL = borde_libre(Q)
    H = y + BL
    reg = "Subcritico (Fr<1)"
    if abs(Fr - 1.0) < 1e-4:
        reg = "Critico (Fr=1)"
    elif Fr > 1.0:
        reg = "Supercritico (Fr>1)"
    print("\nPaso", p_num, ": Froude, Verif. y BL")
    print("T = b + 2*z*y =", r4(T), "m (", r2(T), "m)")
    print("D = A/T =", r4(D), "m, Fr =", r4(Fr))
    print("Regimen:", reg, "\nQ verif =", r4(Qv), "m3/s")
    print("BL (Tabla 9-1) =", r2(BL), "m, H =", r4(H), "m")
    print("Ancho sup. total =", r4(b + 2.0 * m * H), "m")

def op_vel_permisible():
    print("\n=== 1. Vel. Max. Permisible ===\nDisena b, y, T, BL y H (V <= Vmax).")
    u = input("Unidades (1=SI m, 2=ft): ")
    if u not in ("1", "2"):
        print("Opcion invalida.")
        return
    Qi = float(input("Caudal Q: "))
    Vi = float(input("Vel. max V: "))
    Q, V = Qi, Vi
    if u == "2":
        Q, V = Qi * FT3_M3, Vi * FT_M
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    m = float(input("Talud z o m [H:V]: "))
    if Q <= 0 or V <= 0 or n <= 0 or S0 <= 0 or m < 0:
        print("Datos invalidos.")
        return
    rm = math.sqrt(1.0 + m * m)
    Cm = 2.0 * rm - m
    A = Q / V
    R = ((V * n) / math.sqrt(S0)) ** 1.5
    P = A / R
    print("\n--- PROCEDIMIENTO ---\nPaso 1: Parametros")
    if u == "2":
        print("1ft=0.3048m, 1ft3/s=0.028317m3/s")
    print("Q =", r4(Q), "m3/s, V =", r4(V), "m/s\nPaso 2: A = Q/V =", r4(A), "m2")
    print("R = (V*n/sqrt(S0))^(3/2) =", r4(R), "m\nPaso 3: P = A/R =", r4(P), "m")
    if u == "2":
        print("ft: A=", r4(Qi / Vi), "R=", r4(R / FT_M), "P=", r4(P / FT_M))
    print("\nPaso 4: Sistema A y P (Cuadratica)")
    print("b = P - 2*y*sqrt(1+z^2) = P -", r4(2.0 * rm), "* y")
    disc = P * P - 4.0 * Cm * A
    print("Cm*y^2 - P*y + A = 0  (Cm =", r4(Cm), ")\nDisc = P^2 - 4*Cm*A =", r4(disc))
    if disc < 0:
        print("Disc < 0: Aumente z o reduzca V.")
        return
    rd = math.sqrt(disc)
    y1, y2 = (P - rd) / (2.0 * Cm), (P + rd) / (2.0 * Cm)
    b1, b2 = P - 2.0 * y1 * rm, P - 2.0 * y2 * rm
    print("Raiz 1: y1 =", r4(y1), "m -> b1 =", r4(b1), "m")
    print("Raiz 2: y2 =", r4(y2), "m -> b2 =", r4(b2), "m")
    yd, bd = y1, b1
    if b1 < 0:
        yd, bd = y2, b2
    if bd < 0:
        print("Ambas raices dan b < 0.")
        return
    print("Se adopta raiz con b > 0:\n-> y =", r4(yd), "m (", r2(yd), "m)")
    print("-> b =", r4(bd), "m (", r2(bd), "m)")
    if u == "2":
        print("En ft: y =", r4(yd / FT_M), "ft, b =", r4(bd / FT_M), "ft")
        Rf = ((Vi * n) / (1.49 * math.sqrt(S0))) ** 1.5
        Pf = (Qi / Vi) / Rf
        df = Pf * Pf - 4.0 * Cm * (Qi / Vi)
        if df >= 0:
            yf = (Pf - math.sqrt(df)) / (2.0 * Cm)
            bf = Pf - 2.0 * yf * rm
            print("[ku=1.49: y=", round(yf, 3), "ft, b=", round(bf, 3), "ft]")
    fin_hidr(Q, n, S0, bd, yd, m, A, R, V, 5)

def op_seccion_optima():
    print("\n=== 2. Seccion Hidr. Optima ===\nMinimo P (R = y/2): z=0 (Rect),")
    print("z=-1 (Opt 60 gr) o z>0 (Trap).")
    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    mi = float(input("Talud z (0=rect, -1=opt): "))
    if Q <= 0 or n <= 0 or S0 <= 0:
        print("Datos invalidos.")
        return
    m = mi
    if mi < 0:
        m = 1.0 / math.sqrt(3.0)
    rm = math.sqrt(1.0 + m * m)
    cb, cA = 2.0 * (rm - m), 2.0 * rm - m
    Zr = (Q * n) / math.sqrt(S0)
    cm = cA * (0.5 ** (2.0 / 3.0))
    y = (Zr / cm) ** (3.0 / 8.0)
    b, A, P, R = cb * y, cA * y * y, 2.0 * cA * y, 0.5 * y
    V = Q / A
    print("\n--- PROCEDIMIENTO ---\nPaso 1: Deduccion dP/dy = 0 (A cte)")
    print("b/y = 2*(sqrt(1+z^2)-z) =", r4(cb), "| R/y = 0.5")
    if mi < 0:
        print("Talud opt dP/dz=0: z=1/sqrt(3) =", r4(m), "\nAngulo = 60 gr, T/b = 2.0")
    print("b =", r4(cb), "* y, A =", r4(cA), "* y^2\nP =", r4(2.0 * cA), "* y, R = 0.5 * y")
    print("Paso 2: A*R^(2/3) = Q*n/sqrt(S0) =", r4(Zr))
    print(r4(cm), "* y^(8/3) =", r4(Zr), "\nPaso 3: -> y =", r4(y), "m (", r2(y), "m)")
    print("-> b =", r4(b), "m (", r2(b), "m)\nA =", r4(A), "m2, P =", r4(P), "m")
    print("R = y/2 =", r4(R), "m, V =", r4(V), "m/s")
    fin_hidr(Q, n, S0, b, y, m, A, R, V, 4)

def op_fuerza_tractiva():
    print("\n=== 3. Fuerza Tractiva ===\n0.76 * gamma * y * S0 = K * tau_p")
    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    m = float(input("Talud m [H:V]: "))
    tp = float(input("tau_p perm. (N/m2): "))
    pd = float(input("Ang. reposo phi (gr, 0=coh): "))
    fs = float(input("Factor sinuos. (0=1.0): "))
    if Q <= 0 or n <= 0 or S0 <= 0 or m <= 0 or tp <= 0:
        print("Datos invalidos.")
        return
    if fs <= 0:
        fs = 1.0
    tpc = tp * fs
    tr = math.atan(1.0 / m)
    td = math.degrees(tr)
    K = 1.0
    if pd > 0:
        if td >= pd:
            print("Error: theta >= phi (inestable).")
            return
        pr = math.radians(pd)
        K = math.sqrt(1.0 - (math.sin(tr) ** 2) / (math.sin(pr) ** 2))
    tl = K * tpc
    y = tl / (0.76 * 9810.0 * S0)
    Zr = (Q * n) / math.sqrt(S0)
    b = resolver_b(Zr, y, m)
    if b is None:
        print("No se pudo converger b.")
        return
    A, _, R, _, _ = geom_trap(b, y, m)
    V = Q / A
    tf = 9810.0 * y * S0
    est = "CUMPLE"
    if tf > tpc * 1.001:
        est = "NO CUMPLE"
    print("\n--- PROCEDIMIENTO ---\nPaso 1: tau_p corr =", r4(tpc), "N/m2")
    print("Paso 2: theta =", r2(td), "gr, K =", r4(K))
    print("        tau_p(lados) = K*tau_p =", r4(tl), "N/m2")
    print("Paso 3: -> y =", r4(y), "m (", r2(y), "m)\nPaso 4: A*R^(2/3) =", r4(Zr))
    print("-> b =", r4(b), "m (", r2(b), "m)\nA =", r4(A), "m2, V =", r4(V), "m/s")
    print("tau_fondo =", round(tf, 3), "N/m2 ->", est)
    fin_hidr(Q, n, S0, b, y, m, A, R, V, 5)

def menu():
    print("=== Diseno de Canales ===\n1. Vel. Max. Permisible")
    print("2. Secc. Hidr. Optima (Rect/Trap)\n3. Fuerza Tractiva")
    op = input("Opcion (1-3): ")
    try:
        if op == "1":
            op_vel_permisible()
        elif op == "2":
            op_seccion_optima()
        elif op == "3":
            op_fuerza_tractiva()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

menu()
