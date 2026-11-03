import math

# Flujo uniforme - Ecuacion de Manning
# Soluciona Paso a Paso:
# 1. Ancho b dados Q, n, S0, yn, m
# 2. Relacion Q-y sin conocer n ni S0
# 3. Tirante normal yn dados Q, n, S0, b, m
# 4. Caudal Q y velocidad V directos


def geom_trap(b, y, m):
    raiz = math.sqrt(1.0 + m * m)
    A = (b + m * y) * y
    P = b + 2.0 * y * raiz
    R = A / P
    Z = A * (R ** (2.0 / 3.0))
    return A, P, R, Z, raiz


def resolver_b(Z_obj, y, m):
    # Resuelve A(b)*R(b)^(2/3) = Z_obj para b > 0
    if m > 0:
        z0 = geom_trap(0.0, y, m)[3]
        if Z_obj <= z0:
            return 0.0
    b_inf = 1e-6
    b_sup = 1.0
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
    # Resuelve A(y)*R(y)^(2/3) = Z_obj para y > 0
    y_inf = 1e-6
    y_sup = 1.0
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
    print("")
    print("=== 1. Hallar Ancho b ===")
    print("Descripcion del ejercicio:")
    print("Calcula el ancho de base b")
    print("de un canal en flujo uniforme")
    print("conociendo Q, n, S0, yn y m")
    print("(use m=0 si es rectangular).")
    print("--------------------------")

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

    print("")
    print("--- PROCEDIMIENTO ---")
    print("Paso 1: Geometria en fn de b")
    if m == 0:
        print("Canal rectangular (m=0):")
        print("A = b * yn =", round(yn, 4), "* b")
        print("P = b + 2*yn = b +", round(2.0 * yn, 4))
    else:
        print("Canal trapezoidal:")
        print("A = (b +", round(m * yn, 4), ") *", round(yn, 4))
        print("P = b +", round(2.0 * yn * raiz_m, 4))
    print("R = A / P")

    print("")
    print("Paso 2: Ec. de Manning")
    print("Q = (1/n) * A * R^(2/3) * S0^(1/2)")
    print("Despejando factor de seccion:")
    print("A * R^(2/3) = (Q * n) / sqrt(S0)")
    print("A * R^(2/3) = (", Q, "*", n, ")")
    print("              / sqrt(", S0, ")")
    print("A * R^(2/3) =", round(Z_req, 5))

    print("")
    print("Paso 3: Planteo y despeje de b")
    print("Como R = A / P, entonces:")
    print("A^(5/3) / P^(2/3) =", round(Z_req, 5))
    if m == 0:
        print("(", round(yn, 3), "*b)^(5/3) / (b+", round(2.0 * yn, 3), ")^(2/3)", sep="")
        print("=", round(Z_req, 5))

    b = resolver_b(Z_req, yn, m)
    if b is None or b <= 0:
        print("No hay solucion con b > 0.")
        return

    A, P, R, Z, _ = geom_trap(b, yn, m)
    V = Q / A
    Q_ver = (1.0 / n) * Z * raiz_s

    print("Resolviendo para b:")
    print("-> b =", round(b, 4), "m")

    print("")
    print("Paso 4: Verificacion")
    print("A =", round(A, 4), "m2")
    print("P =", round(P, 4), "m")
    print("R =", round(R, 4), "m")
    print("V = Q/A =", round(V, 4), "m/s")
    print("Q calc =", round(Q_ver, 4), "m3/s")


def op_relacion_qy():
    print("")
    print("=== 2. Relacion sin n ni S0 ===")
    print("Descripcion del ejercicio:")
    print("En un mismo canal, n y S0 son")
    print("constantes, por lo que:")
    print("K = sqrt(S0)/n = Q / (A*R^(2/3))")
    print("es constante para todo tirante.")
    print("a) Halla Q2 para una altura y2")
    print("b) Halla y3 para un caudal Q3")
    print("-------------------------------")

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

    A1, P1, R1, Z1, raiz_m = geom_trap(b, y1, m)
    K = Q1 / Z1

    print("")
    print("--- PROCEDIMIENTO ---")
    print("Paso 1: Condicion inicial (1)")
    print("A1 = (b + m*y1)*y1 =", round(A1, 4), "m2")
    print("P1 = b + 2*y1*sqrt(1+m^2)")
    print("P1 =", round(P1, 4), "m")
    print("R1 = A1/P1 =", round(R1, 4), "m")
    print("Z1 = A1*R1^(2/3) =", round(Z1, 4))
    print("Constante del canal K:")
    print("K = sqrt(S0)/n = Q1 / Z1")
    print("K =", round(Q1, 3), "/", round(Z1, 4), "=", round(K, 5))

    if y2 > 0:
        A2, P2, R2, Z2, _ = geom_trap(b, y2, m)
        Q2 = K * Z2
        V2 = Q2 / A2
        print("")
        print("Paso 2: a) Q2 para y2 =", y2, "m")
        print("A2 = (b + m*y2)*y2 =", round(A2, 4), "m2")
        print("P2 =", round(P2, 4), "m")
        print("R2 = A2/P2 =", round(R2, 4), "m")
        print("Z2 = A2*R2^(2/3) =", round(Z2, 4))
        print("Q2 = K * Z2 = Q1 * (Z2 / Z1)")
        print("-> Q2 =", round(Q2, 4), "m3/s")
        print("   V2 =", round(V2, 4), "m/s")

    Z3_req = Q3 / K
    y3 = resolver_y(Z3_req, b, m)

    print("")
    print("Paso 3: b) y3 para Q3 =", round(Q3, 4), "m3/s")
    print("Factor requerido Z3 = A3*R3^(2/3):")
    print("Z3 = Q3 / K =", round(Z3_req, 4))
    print("Ec: A(y3)^(5/3) / P(y3)^(2/3) =", round(Z3_req, 4))
    if y3 is not None:
        A3, P3, R3, _, _ = geom_trap(b, y3, m)
        print("Resolviendo para y3:")
        print("-> y3 =", round(y3, 4), "m")
        print("Comp: A3 =", round(A3, 4), "m2, R3 =", round(R3, 4), "m")


def op_hallar_y():
    print("")
    print("=== 3. Hallar Tirante yn ===")
    print("Descripcion del ejercicio:")
    print("Calcula la profundidad normal yn")
    print("dados Q, n, S0, ancho b y talud m.")
    print("----------------------------")

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
    V = Q / A

    print("")
    print("--- PROCEDIMIENTO ---")
    print("Paso 1: Factor de seccion")
    print("A * R^(2/3) = (Q * n) / sqrt(S0)")
    print("A * R^(2/3) =", round(Z_req, 5))
    print("")
    print("Paso 2: Ecuacion en funcion de yn")
    print("[(b + m*yn)*yn]^(5/3)")
    print(" / [b + 2*yn*sqrt(1+m^2)]^(2/3)")
    print(" =", round(Z_req, 5))
    print("")
    print("Paso 3: Solucion y verificacion")
    print("-> yn =", round(yn, 4), "m")
    print("A =", round(A, 4), "m2")
    print("P =", round(P, 4), "m")
    print("R =", round(R, 4), "m")
    print("V =", round(V, 4), "m/s")


def op_calcular_q():
    print("")
    print("=== 4. Calcular Q y V ===")
    print("Descripcion del ejercicio:")
    print("Calcula caudal Q y velocidad V")
    print("con la ecuacion de Manning.")
    print("-------------------------")

    b = float(input("Ancho base b (m): "))
    yn = float(input("Tirante yn (m): "))
    m = float(input("Talud m (0=rect): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))

    if b < 0 or yn <= 0 or m < 0 or (b == 0 and m == 0) or n <= 0 or S0 <= 0:
        print("Datos invalidos.")
        return

    A, P, R, Z, _ = geom_trap(b, yn, m)
    V = (1.0 / n) * (R ** (2.0 / 3.0)) * math.sqrt(S0)
    Q = A * V

    print("")
    print("--- PROCEDIMIENTO ---")
    print("Paso 1: Propiedades geometricas")
    print("A = (b + m*yn)*yn =", round(A, 4), "m2")
    print("P = b + 2*yn*sqrt(1+m^2) =", round(P, 4), "m")
    print("R = A / P =", round(R, 4), "m")
    print("")
    print("Paso 2: Velocidad y Caudal")
    print("V = (1/n) * R^(2/3) * S0^(1/2)")
    print("-> V =", round(V, 4), "m/s")
    print("Q = A * V")
    print("-> Q =", round(Q, 4), "m3/s")


def menu():
    print("=== Flujo Uniforme Manning ===")
    print("1. Hallar base b")
    print("2. Relacion sin n ni S0")
    print("3. Hallar tirante normal yn")
    print("4. Calcular Q y V directo")

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
