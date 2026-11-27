import math

# Metodo de Paso Estandar (FGV) - Rect, Trap y Triang
def r4(x):
    return round(x, 4)

def r3(x):
    return round(x, 3)

def bisecc(fn, a, b):
    fa = fn(a)
    for _ in range(65):
        m = 0.5 * (a + b)
        fm = fn(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return 0.5 * (a + b)

def ped_unid():
    u = input("Unidades (1=SI m, 2=Ing ft): ")
    if u == "2":
        return 32.2, 1.49, "ft", "ft3/s", "ft/s"
    return 9.81, 1.0, "m", "m3/s", "m/s"

def ped_canal(uL, uQ):
    print("Seccion: Rect(z=0), Trap(b>0,z>0), Triang(b=0,z>0)")
    b = float(input("Base b (0=triang): "))
    z = float(input("Talud z (0=rect): "))
    Q = float(input("Caudal Q (" + uQ + "): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    if b < 0 or z < 0 or (b == 0 and z == 0) or Q <= 0 or n <= 0:
        return None
    return b, z, Q, n, S0

def geom(b, z, y):
    A = (b + z * y) * y
    P = b + 2.0 * y * math.sqrt(1.0 + z * z)
    return A, P, A / P, b + 2.0 * z * y

def eq_ecuaciones(b, z):
    if z == 0:
        print("Geometria Rect (b=", b, "): A=b*y | P=b+2*y | R=A/P | T=b")
    elif b == 0:
        print("Geometria Triang (z=", z, "): A=z*y^2 | P=2*y*sqrt(1+z^2) | R=A/P | T=2*z*y")
    else:
        print("Geometria Trap (b=", b, ", z=", z, "): A=(b+z*y)*y | P=b+2*y*sqrt(1+z^2) | R=A/P | T=b+2*z*y")
    print("Critico: Q^2*T/(g*A^3)=1 | Normal: A*R^(2/3)=Q*n/(Cm*sqrt(S0))")
    print("V=Q/A | E=y+V^2/(2*g) | H=z+E | Sf=(V*n/(Cm*R^(2/3)))^2")
    print("Paso Estandar: H2 = H1 - Sfm*dx, Sfm=(Sf1+Sf2)/2, hf=Sfm*dx")

def calc_yc(Q, b, z, g):
    def f(y):
        A, _, _, T = geom(b, z, y)
        return (Q * Q * T) / (g * A * A * A) - 1.0
    ys = 1.0
    while f(ys) > 0:
        ys *= 2.0
    return bisecc(f, 1e-6, ys)

def calc_yn(Q, n, S0, b, z, Cm):
    if S0 <= 0:
        return None
    Zr = (Q * n) / (Cm * math.sqrt(S0))
    def f(y):
        A, _, R, _ = geom(b, z, y)
        return A * (R ** (2.0 / 3.0)) - Zr
    ys = 1.0
    while f(ys) < 0:
        ys *= 2.0
    return bisecc(f, 1e-6, ys)

def props(b, z, y, Q, n, g, Cm):
    A, P, R, _ = geom(b, z, y)
    V = Q / A
    E = y + (V * V) / (2.0 * g)
    Sf = ((V * n) / (Cm * (R ** (2.0 / 3.0)))) ** 2
    return A, P, R, V, E, Sf

def mom_M(Q, b, z, y, g):
    A = (b + z * y) * y
    return (Q * Q) / (g * A) + y * y * (0.5 * b + (z * y) / 3.0)

def secuente(Q, b, z, y1, yc, g):
    M1 = mom_M(Q, b, z, y1, g)
    if y1 >= yc:
        return yc
    ys = yc * 2.0
    while mom_M(Q, b, z, ys, g) < M1:
        ys *= 2.0
    return bisecc(lambda y: mom_M(Q, b, z, y, g) - M1, yc, ys)

def paso_estandar(b, z, Q, n, S0, g, Cm, y1, dx, yc, sub):
    _, _, _, _, E1, Sf1 = props(b, z, y1, Q, n, g, Cm)
    def F(y):
        _, _, _, _, E2, Sf2 = props(b, z, y, Q, n, g, Cm)
        return E2 - E1 - (S0 - 0.5 * (Sf1 + Sf2)) * dx
    Fc = F(yc)
    if sub:
        if dx < 0 and Fc > 0:
            return None
        ys = max(y1 * 1.5, yc * 1.5)
        while (F(ys) < 0 if dx < 0 else F(ys) * Fc > 0):
            ys *= 2.0
            if ys > 1e4:
                return None
        return bisecc(F, yc, ys)
    if dx > 0 and Fc > 0:
        return None
    yi = min(y1 * 0.5, yc * 0.5) if dx > 0 else 1e-5
    if dx > 0:
        while F(yi) < 0:
            yi *= 0.5
            if yi < 1e-6:
                return None
    elif F(yi) * Fc > 0:
        return None
    return bisecc(F, yi, yc)

def op_perfil_est():
    print("\n=== 1. Paso Estandar (N tramos) ===\nHalla y(x) conociendo dx y S0.")
    g, Cm, uL, uQ, uV = ped_unid()
    dat = ped_canal(uL, uQ)
    if dat is None:
        print("Datos invalidos.")
        return
    b, z, Q, n, S0 = dat
    y1 = float(input("Tirante inicial y1 (" + uL + "): "))
    L = float(input("Longitud total L (" + uL + "): "))
    N = int(input("Numero de tramos N: "))
    sent = input("Sentido (1=Aguas abajo, 2=Arriba): ")
    z0 = float(input("Cota fondo inicial z0 (0=ref): "))
    det = input("Mostrar (1=Tabla, 2=Detalle): ")
    if y1 <= 0 or L <= 0 or N < 1:
        print("Datos invalidos.")
        return
    yc = calc_yc(Q, b, z, g)
    yn = calc_yn(Q, n, S0, b, z, Cm)
    sub = y1 >= yc
    dx = (L / N) if sent == "1" else -(L / N)
    print("\n--- PROCEDIMIENTO PASO ESTANDAR ---")
    eq_ecuaciones(b, z)
    print("yc =", r4(yc), uL, "| yn =", r4(yn) if yn else "N/A")
    print("Regimen:", "Subcritico" if sub else "Supercritico", "| dx = +-L/N =", r3(dx), uL)
    x, zc, ya = 0.0, z0, y1
    p1 = props(b, z, ya, Q, n, g, Cm)
    H1 = zc + p1[4]
    if det != "2":
        print(" x  |  z_f  |   y   |   H   |  Sf")
        print(r3(x), "|", r3(zc), "|", r3(ya), "|", r3(H1), "|", round(p1[5], 5))
    for i in range(1, N + 1):
        ynx = paso_estandar(b, z, Q, n, S0, g, Cm, ya, dx, yc, sub)
        if ynx is None:
            print("AVISO: El perfil alcanzo yc antes del tramo", i)
            return
        x, z2 = x + dx, zc - S0 * dx
        p2 = props(b, z, ynx, Q, n, g, Cm)
        H2, Sfm = z2 + p2[4], 0.5 * (p1[5] + p2[5])
        hf = Sfm * dx
        if det == "2":
            print("\n--- Tramo", i, "x =", r3(x), uL, "---")
            print("z1=", r3(zc), "| E1=y1+V1^2/2g=", r4(p1[4]), "| H1=z1+E1=", r4(H1), "| Sf1=", round(p1[5], 6))
            print("z2 = z1 - S0*dx =", r3(z2), "-> y2 =", r4(ynx), uL)
            print("A2=", r3(p2[0]), "| P2=", r3(p2[1]), "| R2=A2/P2=", r3(p2[2]), "| V2=Q/A2=", r3(p2[3]), uV)
            print("E2 = y2+V2^2/2g =", r4(p2[4]), "| Sf2 = (V2*n/(Cm*R2^(2/3)))^2 =", round(p2[5], 6))
            print("Sfm = (Sf1+Sf2)/2 =", round(Sfm, 6), "| hf = Sfm*dx =", r4(hf))
            print("Verif: H2 = z2+E2 =", r4(H2), "| H1 - hf =", r4(H1 - hf))
            if i < N:
                input("[Enter sig tramo...]")
        else:
            print(r3(x), "|", r3(z2), "|", r3(ynx), "|", r3(H2), "|", round(p2[5], 5))
        ya, zc, p1, H1 = ynx, z2, p2, H2
    print("\nTirante final en x =", r3(x), ": y =", r4(ya), uL)

def op_un_tramo():
    print("\n=== 2. Un Tramo con Cotas z1, z2 ===")
    g, Cm, uL, uQ, uV = ped_unid()
    b = float(input("Base b (0=triang): "))
    z = float(input("Talud z (0=rect): "))
    Q = float(input("Caudal Q (" + uQ + "): "))
    n = float(input("Rugosidad n: "))
    z1 = float(input("Cota fondo z1 (" + uL + "): "))
    z2 = float(input("Cota fondo z2 (" + uL + "): "))
    L = float(input("Distancia L (" + uL + "): "))
    sent = input("2 esta (1=Aguas abajo, 2=Arriba): ")
    y1 = float(input("Tirante conocido y1 (" + uL + "): "))
    if b < 0 or z < 0 or (b == 0 and z == 0) or Q <= 0 or n <= 0 or L <= 0 or y1 <= 0:
        print("Datos invalidos.")
        return
    dx = L if sent == "1" else -L
    S0 = (z1 - z2) / dx
    yc = calc_yc(Q, b, z, g)
    p1 = props(b, z, y1, Q, n, g, Cm)
    H1 = z1 + p1[4]
    y2 = paso_estandar(b, z, Q, n, S0, g, Cm, y1, dx, yc, y1 >= yc)
    print("\n--- PROCEDIMIENTO ---")
    eq_ecuaciones(b, z)
    print("S0 = (z1 - z2)/dx =", round(S0, 6), "| yc =", r4(yc), uL)
    print("Secc 1: A1=", r3(p1[0]), "| R1=A1/P1=", r3(p1[2]), "| V1=Q/A1=", r3(p1[3]), uV)
    print("  E1 = y1+V1^2/2g =", r4(p1[4]), "| H1 = z1+E1 =", r4(H1), uL, "| Sf1 =", round(p1[5], 6))
    if y2 is None:
        print("No hay solucion en la misma rama (alcanza yc).")
        return
    p2 = props(b, z, y2, Q, n, g, Cm)
    H2, Sfm = z2 + p2[4], 0.5 * (p1[5] + p2[5])
    print("Secc 2: -> y2 =", r4(y2), uL, "| A2 =", r3(p2[0]), "| R2 = A2/P2 =", r3(p2[2]))
    print("  V2 = Q/A2 =", r3(p2[3]), uV, "| E2 = y2+V2^2/2g =", r4(p2[4]), "| Sf2 =", round(p2[5], 6))
    print("Sfm = (Sf1+Sf2)/2 =", round(Sfm, 6), "| hf = Sfm*dx =", r4(Sfm * dx))
    print("Verif: H2 = z2+E2 =", r4(H2), "| H1 - Sfm*dx =", r4(H1 - Sfm * dx))

def op_ubicar_resalto():
    print("\n=== 3. Ubicar Resalto (M3 + M2) ===\nSupercritico (x=0) vs Subcritico (x=L).")
    g, Cm, uL, uQ, _ = ped_unid()
    dat = ped_canal(uL, uQ)
    if dat is None:
        print("Datos invalidos.")
        return
    b, z, Q, n, S0 = dat
    L = float(input("Longitud canal L (" + uL + "): "))
    y0 = float(input("y aguas arriba (x=0, <yc): "))
    yL = float(input("y aguas abajo (x=L, 0=yc): "))
    N = int(input("Tramos N (ej 10 o 20): "))
    yc = calc_yc(Q, b, z, g)
    yn = calc_yn(Q, n, S0, b, z, Cm)
    yL = yc * 1.001 if yL <= 0 else yL
    dx = L / N
    ysup, yseq, ysub = [None] * (N + 1), [None] * (N + 1), [None] * (N + 1)
    ysup[0], yseq[0] = y0, secuente(Q, b, z, y0, yc, g)
    for i in range(1, N + 1):
        if ysup[i - 1] is not None:
            ysup[i] = paso_estandar(b, z, Q, n, S0, g, Cm, ysup[i - 1], dx, yc, False)
            if ysup[i] is not None:
                yseq[i] = secuente(Q, b, z, ysup[i], yc, g)
    ysub[N] = yL
    for i in range(N - 1, -1, -1):
        if ysub[i + 1] is not None:
            ysub[i] = paso_estandar(b, z, Q, n, S0, g, Cm, ysub[i + 1], -dx, yc, True)
    print("\n--- ECUACIONES Y TABLA ---")
    eq_ecuaciones(b, z)
    print("Secuente: M(y_seq)=M(y_sup), M = Q^2/(gA) + y^2*(b/2 + z*y/3)")
    print("yc =", r4(yc), "| yn =", r4(yn) if yn else "N/A", "| dx =", r3(dx), uL)
    print("  x  | y_sup | y_seq | y_sub")
    xr = None
    for i in range(N + 1):
        s1 = r3(ysup[i]) if ysup[i] else "yc"
        s2 = r3(yseq[i]) if ysup[i] else "yc"
        s3 = r3(ysub[i]) if ysub[i] else "yc"
        print(r3(i * dx), "|", s1, "|", s2, "|", s3)
        if i > 0 and xr is None and ysup[i] and ysup[i - 1] and ysub[i] and ysub[i - 1]:
            d0, d1 = yseq[i - 1] - ysub[i - 1], yseq[i] - ysub[i]
            if d0 * d1 <= 0 and abs(d1 - d0) > 1e-9:
                f = d0 / (d0 - d1)
                xr = (i - 1 + f) * dx
                ya = ysup[i - 1] + f * (ysup[i] - ysup[i - 1])
                yd = ysub[i - 1] + f * (ysub[i] - ysub[i - 1])
    print("\n--- UBICACION DEL RESALTO ---")
    if xr is not None:
        print("Cruce y_seq(x) = y_sub(x) -> Resalto en x =", r3(xr), uL, "desde x=0")
        print("y antes (sup) =", r4(ya), uL, "| y despues (sub) =", r4(yd), uL)
    elif ysub[0] and yseq[0] < ysub[0]:
        print("Resalto sumergido / pegado a compuerta (x=0).")
    else:
        print("Resalto barrido (sale del canal, x > L).")

def menu():
    print("=== Metodo de Paso Estandar ===\n1. Perfil en N tramos (dx, S0)")
    print("2. Un tramo con cotas (z1, z2)\n3. Ubicar resalto (M3 + M2 en L)")
    op = input("Opcion (1-3): ")
    try:
        if op == "1":
            op_perfil_est()
        elif op == "2":
            op_un_tramo()
        elif op == "3":
            op_ubicar_resalto()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

menu()
