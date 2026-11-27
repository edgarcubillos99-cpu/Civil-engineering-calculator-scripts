import math

# Flujo Gradualmente Variado (FGV): Perfiles, Lago-Canal y Resalto
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

def ped_sec():
    print("Seccion: Rect(z=0), Trap(b>0,z>0), Triang(b=0,z>0)")
    b = float(input("Base b (0=triang): "))
    z = float(input("Talud z (0=rect): "))
    if b < 0 or z < 0 or (b == 0 and z == 0):
        return None, None
    return b, z

def geom(b, z, y):
    A = (b + z * y) * y
    P = b + 2.0 * y * math.sqrt(1.0 + z * z)
    T = b + 2.0 * z * y
    return A, P, A / P, T, A / T

def eq_geom(b, z):
    if z == 0:
        print("Seccion Rectangular (b=", b, "):\n  A=b*y | P=b+2*y | T=b | R=A/P | D=A/T")
    elif b == 0:
        print("Seccion Triangular (z=", z, "):\n  A=z*y^2 | P=2*y*sqrt(1+z^2) | T=2*z*y | R=A/P | D=A/T")
    else:
        print("Seccion Trapezoidal (b=", b, ", z=", z, "):\n  A=(b+z*y)*y | P=b+2*y*sqrt(1+z^2) | T=b+2*z*y | R=A/P | D=A/T")

def calc_yc(Q, b, z, g):
    def f(y):
        A, _, _, T, _ = geom(b, z, y)
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
        A, _, R, _, _ = geom(b, z, y)
        return A * (R ** (2.0 / 3.0)) - Zr
    ys = 1.0
    while f(ys) < 0:
        ys *= 2.0
    return bisecc(f, 1e-6, ys)

def calc_sf(Q, n, A, R, Cm):
    return (((Q / A) * n) / (Cm * (R ** (2.0 / 3.0)))) ** 2

def mom_M(Q, b, z, y, g):
    A = (b + z * y) * y
    yA = y * y * (0.5 * b + (z * y) / 3.0)
    return (Q * Q) / (g * A) + yA, yA

def op_clasificar():
    print("\n=== 1. Clasificar Perfil FGV ===\nHalla yc, yn, Sc, perfil y dy/dx.")
    g, Cm, uL, uQ, uV = ped_unid()
    b, z = ped_sec()
    if b is None:
        print("Seccion invalida.")
        return
    Q = float(input("Caudal Q (" + uQ + "): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0 (<=0 perm): "))
    y = float(input("Tirante y (" + uL + ", 0=omitir): "))
    if Q <= 0 or n <= 0 or y < 0:
        print("Datos invalidos.")
        return
    yc = calc_yc(Q, b, z, g)
    Ac, Pc, Rc, Tc, Dc = geom(b, z, yc)
    Vc = Q / Ac
    Ec = yc + (Vc * Vc) / (2.0 * g)
    Sc = calc_sf(Q, n, Ac, Rc, Cm)
    print("\n--- PROCEDIMIENTO ---")
    eq_geom(b, z)
    print("\nPaso 1: Condicion critica (Fr=1)")
    print("Ec: Q^2*T/(g*A^3) = 1" + ("  => yc = ((Q/b)^2/g)^(1/3)" if z == 0 else ""))
    print("-> yc =", r4(yc), uL, "| Ac =", r4(Ac), "| Tc =", r4(Tc), "| Rc =", r4(Rc))
    print("Vc = Q/Ac =", r4(Vc), uV, "(o sqrt(g*Dc))")
    print("Emin = yc + Vc^2/(2*g) =", r4(Ec), uL)
    print("Sc = (Vc*n / (Cm*Rc^(2/3)))^2 =", round(Sc, 6))
    yn = calc_yn(Q, n, S0, b, z, Cm)
    print("\nPaso 2: Tirante normal yn (Manning)")
    print("Ec: Q = (Cm/n)*A*R^(2/3)*sqrt(S0)")
    if S0 > 0:
        An, Pn, Rn, _, _ = geom(b, z, yn)
        Zr = (Q * n) / (Cm * math.sqrt(S0))
        print("Factor sec: A*R^(2/3) = Q*n/(Cm*sqrt(S0)) =", r4(Zr))
        print("-> yn =", r4(yn), uL, "| An =", r4(An), "| Pn =", r4(Pn), "| Rn =", r4(Rn))
        print("Vn = Q/An =", r4(Q / An), uV)
    else:
        print("S0 <= 0: No existe flujo uniforme (no hay yn).")
    if S0 < 0:
        tp, desc = "A", "Adversa (S0 < 0)"
    elif S0 == 0:
        tp, desc = "H", "Horizontal (S0 = 0)"
    elif abs(yn - yc) / yc < 1e-3:
        tp, desc = "C", "Critica (yn = yc)"
    elif yn > yc:
        tp, desc = "M", "Suave / Mild (yn > yc)"
    else:
        tp, desc = "S", "Fuerte / Steep (yn < yc)"
    print("\nPaso 3: Tipo de pendiente ->", tp, ":", desc)
    if y <= 0:
        return
    A, P, R, T, D = geom(b, z, y)
    V = Q / A
    Fr = V / math.sqrt(g * D)
    Sf = calc_sf(Q, n, A, R, Cm)
    zn = "2"
    if tp in ("H", "A") and y < yc:
        zn = "3"
    elif tp == "C":
        zn = "1" if y > yc else "3"
    elif tp == "M":
        zn = "1" if y > yn else ("3" if y < yc else "2")
    elif tp == "S":
        zn = "1" if y > yc else ("3" if y < yn else "2")
    print("\nPaso 4: Analisis en y =", r4(y), uL)
    print("A =", r4(A), "| P =", r4(P), "| R = A/P =", r4(R), "| D = A/T =", r4(D))
    print("V = Q/A =", r4(V), uV, "| E = y + V^2/(2*g) =", r4(y + V * V / (2.0 * g)), uL)
    print("Fr = V/sqrt(g*D) =", r4(Fr), "| Sf = (V*n/(Cm*R^(2/3)))^2 =", round(Sf, 6))
    print("-> Perfil:", tp + zn)
    if abs(1.0 - Fr * Fr) > 1e-6:
        dydx = (S0 - Sf) / (1.0 - Fr * Fr)
        tend = "Remanso (y crece)" if dydx > 0 else "Abatimiento (y baja)"
        print("dy/dx = (S0 - Sf)/(1 - Fr^2) =", round(dydx, 6), "->", tend)
    print("Subcritico: calcular AGUAS ARRIBA" if Fr < 1.0 else ("Supercritico: calcular AGUAS ABAJO" if Fr > 1.0 else "Flujo critico (control)."))

def op_lago_canal():
    print("\n=== 2. Problema Lago-Canal ===\nHalla Q, yn y yc dada energia Eup.")
    g, Cm, uL, uQ, uV = ped_unid()
    b, z = ped_sec()
    if b is None:
        print("Seccion invalida.")
        return
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    Eup = float(input("Energia lago Eup (" + uL + "): "))
    if n <= 0 or Eup <= 0:
        print("Datos invalidos.")
        return
    print("\n--- PROCEDIMIENTO ---")
    eq_geom(b, z)
    print("\nPaso 1: Sistema Energia + Manning")
    print("Eup = y + V^2/(2*g)  => V = sqrt(2*g*(Eup - y))")
    print("Manning: V = (Cm/n)*R^(2/3)*sqrt(S0) | Continuidad: Q = A*V")
    es_suave = False
    if S0 > 0:
        def f_m(y):
            _, _, R, _, _ = geom(b, z, y)
            return (Cm / n) * (R ** (2.0 / 3.0)) * math.sqrt(S0) - math.sqrt(2.0 * g * (Eup - y))
        yn = bisecc(f_m, 1e-6, Eup - 1e-6)
        An, _, Rn, _, _ = geom(b, z, yn)
        Vn = math.sqrt(2.0 * g * (Eup - yn))
        Q = An * Vn
        yc = calc_yc(Q, b, z, g)
        print("\nPaso 2: Ensayo pendiente Suave (y = yn en entrada)")
        print("Igualando (Cm/n)*R^(2/3)*sqrt(S0) = sqrt(2*g*(Eup-yn)):")
        print("-> yn =", r4(yn), uL, "| An =", r4(An), "| Rn =", r4(Rn))
        print("Vn = sqrt(2*g*(Eup-yn)) =", r4(Vn), uV, "| Q = An*Vn =", r3(Q), uQ)
        print("hv = Vn^2/(2*g) = Eup - yn =", r4(Eup - yn), uL)
        print("\nPaso 3: Verificacion con yc (Q^2*T/(g*A^3) = 1)")
        print("-> yc =", r4(yc), uL)
        if yn > yc:
            es_suave = True
            print("Como yn > yc -> CONFIRMA Perfil M (Suave, canal largo).")
    if not es_suave:
        print("yn <= yc (o S0<=0) -> Control CRITICO en la entrada!")
        print("\nPaso 4: Condicion critica (Fr=1 => Vc^2/(2g) = Dc/2 = Ac/(2*Tc))")
        print("Ec: Eup = yc + Ac/(2*Tc)")
        def f_c(y):
            A, _, _, T, _ = geom(b, z, y)
            return y + A / (2.0 * T) - Eup
        yc = bisecc(f_c, 1e-6, Eup)
        Ac, _, _, Tc, Dc = geom(b, z, yc)
        Vc = math.sqrt(g * Dc)
        Q = Ac * Vc
        print("-> yc =", r4(yc), uL, "| Ac =", r4(Ac), "| Tc =", r4(Tc))
        print("Vc = sqrt(g*Ac/Tc) =", r4(Vc), uV, "| Q = Ac*Vc =", r3(Q), uQ)
        print("hv = Vc^2/(2*g) = Eup - yc =", r4(Eup - yc), uL)
        if S0 > 0:
            yn = calc_yn(Q, n, S0, b, z, Cm)
            print("Manning A*R^(2/3)=Q*n/(Cm*sqrt(S0)) -> yn =", r4(yn), uL, "(yn < yc -> Perfil S2)")

def op_resalto():
    print("\n=== 3. Tirante Secuente / Resalto ===\nM = Q^2/(gA) + y_bar*A (Rect/Trap/Triang)")
    g, Cm, uL, uQ, uV = ped_unid()
    b, z = ped_sec()
    if b is None:
        print("Seccion invalida.")
        return
    Q = float(input("Caudal Q (" + uQ + "): "))
    y1 = float(input("Tirante conocido y1 (" + uL + "): "))
    if Q <= 0 or y1 <= 0:
        print("Datos invalidos.")
        return
    yc = calc_yc(Q, b, z, g)
    A1, _, _, T1, D1 = geom(b, z, y1)
    V1 = Q / A1
    Fr1 = V1 / math.sqrt(g * D1)
    E1 = y1 + (V1 * V1) / (2.0 * g)
    M1, yA1 = mom_M(Q, b, z, y1, g)
    print("\n--- PROCEDIMIENTO ---")
    eq_geom(b, z)
    print("\nPaso 1: Seccion conocida y1 =", r4(y1), uL)
    print("Critico Q^2*T/(g*A^3)=1 -> yc =", r4(yc), uL)
    print("A1 =", r4(A1), "| D1 = A1/T1 =", r4(D1), "| V1 = Q/A1 =", r4(V1), uV)
    print("Fr1 = V1/sqrt(g*D1) =", r4(Fr1), "| Fr1^2 =", r4(Fr1 * Fr1))
    print("E1 = y1 + V1^2/(2*g) =", r4(E1), uL)
    print("\nPaso 2: Funcion Momentum M = Q^2/(g*A) + y_bar*A")
    print("y_bar*A1 = y1^2*(b/2 + z*y1/3) =", r4(yA1))
    print("-> M1 = Q^2/(g*A1) + y_bar*A1 =", r4(M1))
    if abs(Fr1 - 1.0) < 1e-4:
        print("Flujo critico: y2 = y1 = yc.")
        return
    def f_M(y):
        return mom_M(Q, b, z, y, g)[0] - M1
    if y1 < yc:
        ys = yc * 2.0
        while f_M(ys) < 0:
            ys *= 2.0
        y2 = bisecc(f_M, yc, ys)
        tipo = "Subcritico (aguas abajo)"
    else:
        y2 = bisecc(f_M, 1e-6, yc)
        tipo = "Supercritico (aguas arriba)"
    A2, _, _, T2, D2 = geom(b, z, y2)
    V2 = Q / A2
    Fr2 = V2 / math.sqrt(g * D2)
    E2 = y2 + (V2 * V2) / (2.0 * g)
    print("\nPaso 3: Tirante secuente y2 (" + tipo + ")")
    if z == 0:
        print("Belanger: y2 = (y1/2)*(sqrt(1 + 8*Fr1^2) - 1)")
    else:
        print("Igualando M(y2) = Q^2/(g*A2) + y_bar2*A2 = M1 =", r4(M1))
    print("-> y2 =", r4(y2), uL, "| V2 = Q/A2 =", r4(V2), uV, "| Fr2 = V2/sqrt(g*D2) =", r4(Fr2))
    print("E2 = y2 + V2^2/(2*g) =", r4(E2), uL)
    print("Perdida dE = |E1 - E2| =", r4(abs(E1 - E2)), uL)

def menu():
    print("=== Flujo Gradualmente Variado ===\n1. Clasificar perfil (yc, yn, dy/dx)")
    print("2. Problema Lago-Canal (Eup -> Q,yn)\n3. Tirante secuente / Resalto (M)")
    op = input("Opcion (1-3): ")
    try:
        if op == "1":
            op_clasificar()
        elif op == "2":
            op_lago_canal()
        elif op == "3":
            op_resalto()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

menu()
