import math

# Flujo uniforme - Ecuacion de Manning
def r4(x):
    return round(x, 4)

def geom_trap(b, y, m):
    raiz = math.sqrt(1.0 + m * m)
    A = (b + m * y) * y
    P = b + 2.0 * y * raiz
    R = A / P
    return A, P, R, A * (R ** (2.0 / 3.0)), raiz

def resolver_b(Z_obj, y, m):
    if m > 0 and Z_obj <= geom_trap(0.0, y, m)[3]:
        return 0.0
    b_inf, b_sup = 1e-6, 1.0
    while geom_trap(b_sup, y, m)[3] < Z_obj:
        b_sup = b_sup * 2.0
        if b_sup > 1e6:
            return None
    i = 0
    while i < 60:
        b_med = 0.5 * (b_inf + b_sup)
        if geom_trap(b_med, y, m)[3] < Z_obj:
            b_inf = b_med
        else:
            b_sup = b_med
        i = i + 1
    return 0.5 * (b_inf + b_sup)

def resolver_y(Z_obj, b, m):
    y_inf, y_sup = 1e-6, 1.0
    while geom_trap(b, y_sup, m)[3] < Z_obj:
        y_sup = y_sup * 2.0
        if y_sup > 1e6:
            return None
    i = 0
    while i < 60:
        y_med = 0.5 * (y_inf + y_sup)
        if geom_trap(b, y_med, m)[3] < Z_obj:
            y_inf = y_med
        else:
            y_sup = y_med
        i = i + 1
    return 0.5 * (y_inf + y_sup)

def op_hallar_b():
    print("\n=== 1. Hallar Ancho b ===")
    print("Calcula el ancho b dados Q, n,\nS0, yn y talud m (0=rectang).")
    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    yn = float(input("Tirante yn (m): "))
    m = float(input("Talud m (0=rect): "))
    if Q <= 0 or n <= 0 or S0 <= 0 or yn <= 0 or m < 0:
        print("Datos invalidos.")
        return
    raiz_s = math.sqrt(S0)
    Z_req = (Q * n) / raiz_s
    raiz_m = math.sqrt(1.0 + m * m)
    print("\n--- PROCEDIMIENTO ---\nPaso 1: Geometria en fn de b")
    if m == 0:
        print("A = b*yn =", r4(yn), "* b\nP = b + 2*yn = b +", r4(2.0 * yn))
    else:
        print("A = (b +", r4(m * yn), ") *", r4(yn))
        print("P = b +", r4(2.0 * yn * raiz_m))
    print("R = A / P\n\nPaso 2: Ec. de Manning")
    print("Q = (1/n) * A * R^(2/3) * S0^(1/2)")
    print("A * R^(2/3) = (Q*n)/sqrt(S0) =", r4(Z_req))
    print("\nPaso 3: Planteo y despeje de b")
    print("Como R = A/P => A^(5/3)/P^(2/3) =", r4(Z_req))
    if m == 0:
        print("(", r4(yn), "*b)^(5/3)/(b+", r4(2.0 * yn), ")^(2/3)=", r4(Z_req), sep="")
    b = resolver_b(Z_req, yn, m)
    if b is None or b <= 0:
        print("No hay solucion con b > 0.")
        return
    A, P, R, Z, _ = geom_trap(b, yn, m)
    print("-> b =", r4(b), "m\n\nPaso 4: Verificacion")
    print("A =", r4(A), "m2, P =", r4(P), "m")
    print("R =", r4(R), "m, V =", r4(Q / A), "m/s")
    print("Q calc =", r4((1.0 / n) * Z * raiz_s), "m3/s")

def op_relacion_qy():
    print("\n=== 2. Relacion sin n ni S0 ===")
    print("En un mismo canal, n y S0 son\nconstantes: K = sqrt(S0)/n = Q/Z")
    print("a) Halla Q2 para y2 | b) y3 para Q3")
    b = float(input("Ancho base b (m): "))
    m = float(input("Talud m (0=rect): "))
    Q1 = float(input("Caudal base Q1 (m3/s): "))
    y1 = float(input("Tirante base y1 (m): "))
    y2 = float(input("Nuevo tirante y2 (m): "))
    Q3 = float(input("Nuevo Q3 (0 = Q1/2): "))
    if b < 0 or m < 0 or (b == 0 and m == 0) or Q1 <= 0 or y1 <= 0:
        print("Datos base invalidos.")
        return
    if Q3 <= 0:
        Q3 = 0.5 * Q1
    A1, P1, R1, Z1, _ = geom_trap(b, y1, m)
    K = Q1 / Z1
    print("\n--- PROCEDIMIENTO ---\nPaso 1: Condicion inicial (1)")
    print("A1 =", r4(A1), "m2, P1 =", r4(P1), "m")
    print("R1 = A1/P1 =", r4(R1), "m, Z1 =", r4(Z1))
    print("K = sqrt(S0)/n = Q1/Z1 =", round(K, 5))
    if y2 > 0:
        A2, P2, R2, Z2, _ = geom_trap(b, y2, m)
        Q2 = K * Z2
        print("\nPaso 2: a) Q2 para y2 =", y2, "m")
        print("A2 =", r4(A2), "m2, P2 =", r4(P2), "m")
        print("R2 =", r4(R2), "m, Z2 =", r4(Z2))
        print("Q2 = K * Z2 = Q1 * (Z2 / Z1)")
        print("-> Q2 =", r4(Q2), "m3/s, V2 =", r4(Q2 / A2), "m/s")
    Z3_req = Q3 / K
    y3 = resolver_y(Z3_req, b, m)
    print("\nPaso 3: b) y3 para Q3 =", r4(Q3), "m3/s")
    print("Factor req Z3 = Q3 / K =", r4(Z3_req))
    print("Ec: A(y3)^(5/3) / P(y3)^(2/3) =", r4(Z3_req))
    if y3 is not None:
        A3, _, R3, _, _ = geom_trap(b, y3, m)
        print("-> y3 =", r4(y3), "m")
        print("Comp: A3 =", r4(A3), "m2, R3 =", r4(R3), "m")

def op_hallar_y():
    print("\n=== 3. Hallar Tirante yn ===\nCalcula yn dados Q, n, S0, b y m.")
    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    b = float(input("Ancho base b (m): "))
    m = float(input("Talud m (0=rect): "))
    if Q <= 0 or n <= 0 or S0 <= 0 or b < 0 or m < 0 or (b == 0 and m == 0):
        print("Datos invalidos.")
        return
    Z_req = (Q * n) / math.sqrt(S0)
    yn = resolver_y(Z_req, b, m)
    if yn is None:
        print("No se encontro solucion.")
        return
    A, P, R, _, _ = geom_trap(b, yn, m)
    print("\n--- PROCEDIMIENTO ---")
    print("Paso 1: A*R^(2/3) = Q*n/sqrt(S0) =", r4(Z_req))
    print("Paso 2: A(yn)^(5/3) / P(yn)^(2/3) =", r4(Z_req))
    print("Paso 3: -> yn =", r4(yn), "m")
    print("A =", r4(A), "m2, P =", r4(P), "m")
    print("R =", r4(R), "m, V =", r4(Q / A), "m/s")

def op_calcular_q():
    print("\n=== 4. Calcular Q y V ===")
    b = float(input("Ancho base b (m): "))
    yn = float(input("Tirante yn (m): "))
    m = float(input("Talud m (0=rect): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    if b < 0 or yn <= 0 or m < 0 or (b == 0 and m == 0) or n <= 0 or S0 <= 0:
        print("Datos invalidos.")
        return
    A, P, R, _, _ = geom_trap(b, yn, m)
    V = (1.0 / n) * (R ** (2.0 / 3.0)) * math.sqrt(S0)
    print("\n--- PROCEDIMIENTO ---")
    print("Paso 1: A =", r4(A), "m2, P =", r4(P), "m, R =", r4(R), "m")
    print("Paso 2: V = (1/n) * R^(2/3) * S0^(1/2)")
    print("-> V =", r4(V), "m/s, Q =", r4(A * V), "m3/s")

def menu():
    print("=== Flujo Uniforme Manning ===\n1. Hallar base b\n2. Relacion sin n ni S0")
    print("3. Hallar tirante normal yn\n4. Calcular Q y V directo")
    op = input("Opcion (1-4): ")
    try:
        if op == "1":
            op_hallar_b()
        elif op == "2":
            op_relacion_qy()
        elif op == "3":
            op_hallar_y()
        elif op == "4":
            op_calcular_q()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

menu()
