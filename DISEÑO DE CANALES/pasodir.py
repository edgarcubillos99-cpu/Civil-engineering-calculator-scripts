import math

# Metodo de Paso Directo (FGV) - Rect, Trap y Triang
def r4(x):
    return round(x, 4)

def r3(x):
    return round(x, 3)

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
    rz = math.sqrt(1.0 + z * z)
    A = (b + z * y) * y
    P = b + 2.0 * y * rz
    R = A / P
    T = b + 2.0 * z * y
    return A, P, R, T

def eq_ecuaciones(b, z):
    if z == 0:
        print("Geometria Rect (b=", b, "): A=b*y | P=b+2*y | R=A/P | T=b")
    elif b == 0:
        print("Geometria Triang (z=", z, "): A=z*y^2 | P=2*y*sqrt(1+z^2) | R=A/P | T=2*z*y")
    else:
        print("Geometria Trap (b=", b, ", z=", z, "): A=(b+z*y)*y | P=b+2*y*sqrt(1+z^2) | R=A/P | T=b+2*z*y")
    print("Critico: Q^2*T/(g*A^3)=1 | Normal: A*R^(2/3)=Q*n/(Cm*sqrt(S0))")
    print("Energia: V=Q/A | hv=V^2/(2*g) | E=y+hv | Sf=(V*n/(Cm*R^(2/3)))^2")
    print("Paso Directo: dE=E2-E1 | Sfm=(Sf1+Sf2)/2 | dx=dE/(S0-Sfm)")

def calc_yc(Q, b, z, g):
    yi, ys = 1e-6, 1.0
    while True:
        A, _, _, T = geom(b, z, ys)
        if (Q * Q * T) / (g * A * A * A) <= 1.0:
            break
        ys = ys * 2.0
    i = 0
    while i < 65:
        ym = 0.5 * (yi + ys)
        A, _, _, T = geom(b, z, ym)
        if (Q * Q * T) / (g * A * A * A) > 1.0:
            yi = ym
        else:
            ys = ym
        i = i + 1
    return 0.5 * (yi + ys)

def calc_yn(Q, n, S0, b, z, Cm):
    if S0 <= 0:
        return None
    Zr = (Q * n) / (Cm * math.sqrt(S0))
    yi, ys = 1e-6, 1.0
    while True:
        A, _, R, _ = geom(b, z, ys)
        if A * (R ** (2.0 / 3.0)) >= Zr:
            break
        ys = ys * 2.0
    i = 0
    while i < 65:
        ym = 0.5 * (yi + ys)
        A, _, R, _ = geom(b, z, ym)
        if A * (R ** (2.0 / 3.0)) < Zr:
            yi = ym
        else:
            ys = ym
        i = i + 1
    return 0.5 * (yi + ys)

def props(b, z, y, Q, n, g, Cm):
    A, P, R, T = geom(b, z, y)
    V = Q / A
    E = y + (V * V) / (2.0 * g)
    Sf = ((V * n) / (Cm * (R ** (2.0 / 3.0)))) ** 2
    Fr = V / math.sqrt(g * A / T)
    return A, P, R, V, E, Sf, Fr

def tipo_perfil(S0, yn, yc, ym):
    if S0 < 0:
        tp = "A"
    elif S0 == 0:
        tp = "H"
    elif abs(yn - yc) / yc < 1e-3:
        tp = "C"
    elif yn > yc:
        tp = "M"
    else:
        tp = "S"
    zn = "2"
    if tp in ("H", "A"):
        if ym < yc:
            zn = "3"
    elif tp == "C":
        zn = "1" if ym > yc else "3"
    elif tp == "M":
        if ym > yn:
            zn = "1"
        elif ym < yc:
            zn = "3"
    else:
        if ym > yc:
            zn = "1"
        elif ym < yn:
            zn = "3"
    return tp + zn

def imp_paso(idx, y1, y2, p1, p2, S0, uL, uV):
    A1, P1, R1, V1, E1, Sf1, _ = p1
    A2, P2, R2, V2, E2, Sf2, _ = p2
    dE = E2 - E1
    Sfm = 0.5 * (Sf1 + Sf2)
    den = S0 - Sfm
    if abs(den) < 1e-12:
        print("Error: S0 = Sfm (flujo uniforme).")
        return None
    dx = dE / den
    print("\n--- Paso", idx, ": y1=", r4(y1), "-> y2=", r4(y2), uL, "---")
    print("Secc 1: A=", r3(A1), "| P=", r3(P1), "| R=A/P=", r3(R1))
    print("  V1=Q/A1=", r3(V1), uV, "| hv1=V1^2/2g=", r4(E1 - y1), "| E1=y1+hv1=", r4(E1))
    print("  Sf1=(V1*n/(Cm*R1^(2/3)))^2=", round(Sf1, 6))
    print("Secc 2: A=", r3(A2), "| P=", r3(P2), "| R=A/P=", r3(R2))
    print("  V2=Q/A2=", r3(V2), uV, "| hv2=V2^2/2g=", r4(E2 - y2), "| E2=y2+hv2=", r4(E2))
    print("  Sf2=(V2*n/(Cm*R2^(2/3)))^2=", round(Sf2, 6))
    print("dE = E2 - E1 =", r4(dE))
    print("Sfm = (Sf1 + Sf2)/2 =", round(Sfm, 6))
    print("S0 - Sfm =", round(den, 6))
    sent = "aguas abajo (+)" if dx >= 0 else "aguas arriba (-)"
    print("-> dx = dE/(S0 - Sfm) =", r3(dx), uL, sent)
    return dx

def op_un_paso():
    print("\n=== 1. Un Paso Directo Detallado ===")
    print("Calcula dx entre y1 y y2 con todo\nel desarrollo y sus ecuaciones.")
    g, Cm, uL, uQ, uV = ped_unid()
    dat = ped_canal(uL, uQ)
    if dat is None:
        print("Datos invalidos.")
        return
    b, z, Q, n, S0 = dat
    y1 = float(input("Tirante inicial y1 (" + uL + "): "))
    y2 = float(input("Tirante final y2 (" + uL + "): "))
    if y1 <= 0 or y2 <= 0 or y1 == y2:
        print("Tirantes invalidos.")
        return
    yc = calc_yc(Q, b, z, g)
    yn = calc_yn(Q, n, S0, b, z, Cm)
    pf = tipo_perfil(S0, yn, yc, 0.5 * (y1 + y2))
    print("\n--- PROCEDIMIENTO ---")
    eq_ecuaciones(b, z)
    print("yc =", r4(yc), uL, "| yn =", r4(yn) if yn else "N/A", "| Perfil:", pf)
    p1 = props(b, z, y1, Q, n, g, Cm)
    p2 = props(b, z, y2, Q, n, g, Cm)
    dx = imp_paso(1, y1, y2, p1, p2, S0, uL, uV)
    if dx is not None:
        print("Distancia |dx| =", r3(abs(dx)), uL)

def op_perfil():
    print("\n=== 2. Perfil Completo Paso Directo ===")
    print("Calcula x acumulada desde y_ini a\ny_fin en N pasos (dy uniforme).")
    g, Cm, uL, uQ, uV = ped_unid()
    dat = ped_canal(uL, uQ)
    if dat is None:
        print("Datos invalidos.")
        return
    b, z, Q, n, S0 = dat
    yi = float(input("Tirante inicial y_ini (" + uL + "): "))
    yf = float(input("Tirante final y_fin (" + uL + "): "))
    N = int(input("Numero de pasos N: "))
    det = input("Mostrar (1=Tabla, 2=Detalle): ")
    if yi <= 0 or yf <= 0 or yi == yf or N < 1:
        print("Datos invalidos.")
        return
    yc = calc_yc(Q, b, z, g)
    yn = calc_yn(Q, n, S0, b, z, Cm)
    pf = tipo_perfil(S0, yn, yc, 0.5 * (yi + yf))
    print("\n--- ECUACIONES Y RESULTADOS ---")
    eq_ecuaciones(b, z)
    print("yc =", r4(yc), uL, "| yn =", r4(yn) if yn else "N/A", "| Perfil:", pf)
    print("dy = (yf - yi)/N =", r4((yf - yi) / N), uL, "| (+)abajo (-)arriba")
    if (yi < yc < yf) or (yf < yc < yi):
        print("AVISO: El rango cruza yc! Divida en tramos.")
    dy = (yf - yi) / N
    x = 0.0
    y1 = yi
    p1 = props(b, z, y1, Q, n, g, Cm)
    if det != "2":
        print(" i |   y   |   E   |   dx   |  x_ac")
        print(" 0 |", r3(y1), "|", r3(p1[4]), "|  0.0  |  0.0")
    i = 1
    while i <= N:
        y2 = yi + i * dy
        p2 = props(b, z, y2, Q, n, g, Cm)
        if det == "2":
            dx = imp_paso(i, y1, y2, p1, p2, S0, uL, uV)
            if dx is None:
                return
            x = x + dx
            print("x_ac = x_ant + dx =", r3(x), uL)
            if i < N:
                input("[Enter sig paso...]")
        else:
            dE = p2[4] - p1[4]
            Sfm = 0.5 * (p1[5] + p2[5])
            den = S0 - Sfm
            if abs(den) < 1e-12:
                print("Error: S0=Sfm en paso", i)
                return
            dx = dE / den
            x = x + dx
            print(i, "|", r3(y2), "|", r3(p2[4]), "|", r3(dx), "|", r3(x))
        y1 = y2
        p1 = p2
        i = i + 1
    print("\nLongitud total |x| =", r3(abs(x)), uL)
    if x < 0:
        print("Direccion: AGUAS ARRIBA (x =", r3(x), uL, ")")
    else:
        print("Direccion: AGUAS ABAJO (x =", r3(x), uL, ")")

def menu():
    print("=== Metodo de Paso Directo ===\n1. Un paso detallado (y1 -> y2)")
    print("2. Perfil completo (N pasos)")
    op = input("Opcion (1-2): ")
    try:
        if op == "1":
            op_un_paso()
        elif op == "2":
            op_perfil()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

menu()
