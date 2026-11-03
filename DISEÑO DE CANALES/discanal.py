import math

# Diseno de canales en flujo uniforme
# Incluye borde libre (Tabla 9-1 Ranga Raju),
# numero de Froude y verificacion de Manning:
# 1. Metodo Velocidad Maxima Permisible (Punto 3 + PDF 1)
# 2. Metodo Seccion Hidraulicamente Optima (Punto 4 + Rect/Trap optimo)
# 3. Metodo Esfuerzo Cortante / Fuerza Tractiva (PDF 2)

FT_A_M = 0.3048
FT3_A_M3 = 0.0283168466
G = 9.81


def borde_libre_ranga(Q_m3s):
    # Tabla 9-1 (Ranga Raju, 1983)
    if Q_m3s < 0.75:
        return 0.45, "< 0.75 m3/s"
    if Q_m3s < 1.50:
        return 0.60, "0.75 a 1.5 m3/s"
    if Q_m3s <= 85.0:
        return 0.75, "1.5 a 85 m3/s"
    return 0.90, "> 85 m3/s"


def regimen_froude(Fr):
    if abs(Fr - 1.0) < 1e-4:
        return "Critico (Fr = 1)"
    if Fr < 1.0:
        return "Subcritico (Fr < 1)"
    return "Supercritico (Fr > 1)"


def geom_trap(b, y, m):
    raiz = math.sqrt(1.0 + m * m)
    A = (b + m * y) * y
    P = b + 2.0 * y * raiz
    R = A / P
    Z = A * (R ** (2.0 / 3.0))
    return A, P, R, Z, raiz


def resolver_b(Z_obj, y, m):
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


def op_vel_permisible():
    print("")
    print("=== 1. Vel. Max. Permisible ===")
    print("Descripcion del ejercicio:")
    print("Disena la seccion (b, y, T, BL, H)")
    print("de un canal erosionable para que")
    print("trabaje a la velocidad maxima")
    print("permisible V (Guia PDF 1), y")
    print("verifica Froude y Manning.")
    print("Ref Pto 3: unid=2 (ft), n=0.021,")
    print("Q=74 ft3/s, V=2.80 ft/s,")
    print("z=2.0, S0=0.0009")
    print("-------------------------------")

    unid = input("Unidades (1=SI m, 2=ft): ")
    if unid not in ("1", "2"):
        print("Opcion de unidad invalida.")
        return

    if unid == "1":
        Q_in = float(input("Caudal Q (m3/s): "))
        V_in = float(input("Vel. max V (m/s): "))
        Q = Q_in
        V = V_in
    else:
        Q_in = float(input("Caudal Q (ft3/s): "))
        V_in = float(input("Vel. max V (ft/s): "))
        Q = Q_in * FT3_A_M3
        V = V_in * FT_A_M

    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    m = float(input("Talud z o m [H:V]: "))

    if Q <= 0 or V <= 0 or n <= 0 or S0 <= 0 or m < 0:
        print("Datos invalidos.")
        return

    raiz_m = math.sqrt(1.0 + m * m)
    Cm = 2.0 * raiz_m - m

    print("")
    print("--- PROCEDIMIENTO (PDF 1) ---")
    print("Paso 1: Parametros y unidades")
    if unid == "2":
        print("Convirtiendo de pies (ft) a SI:")
        print("1 ft = 0.3048 m")
        print("1 ft3/s = 0.028317 m3/s")
        print("Q =", Q_in, "ft3/s =", round(Q, 4), "m3/s")
        print("V =", V_in, "ft/s =", round(V, 4), "m/s")
    else:
        print("Q =", round(Q, 4), "m3/s, V =", round(V, 4), "m/s")
    print("n =", n, ", S0 =", S0, ", z =", m)

    # Paso 2: R por Manning y A por continuidad
    R = ((V * n) / math.sqrt(S0)) ** 1.5
    A = Q / V

    print("")
    print("Paso 2: Area A y Radio hidr. R")
    print("De continuidad: A = Q / V")
    print("A =", round(A, 4), "m2", end="")
    if unid == "2":
        print(" (", round(A / (FT_A_M * FT_A_M), 4), "ft2)")
    else:
        print("")
    print("De Manning: V = (1/n)*R^(2/3)*S0^(1/2)")
    print("R = (V * n / sqrt(S0))^(3/2)")
    print("R =", round(R, 4), "m", end="")
    if unid == "2":
        print(" (", round(R / FT_A_M, 4), "ft)")
    else:
        print("")

    # Paso 3: Perimetro mojado P
    P = A / R
    print("")
    print("Paso 3: Perimetro mojado P")
    print("P = A / R =", round(P, 4), "m", end="")
    if unid == "2":
        print(" (", round(P / FT_A_M, 4), "ft)")
    else:
        print("")

    # Paso 4: Sistema A y P -> cuadratica en y
    print("")
    print("Paso 4: Despeje de tirante y y base b")
    print("P = b + 2*y*sqrt(1+z^2)")
    print("=> b = P -", round(2.0 * raiz_m, 4), "* y")
    print("Sustituyendo b en A = (b + z*y)*y:")
    print("Cm * y^2 - P * y + A = 0")
    print("con Cm = 2*sqrt(1+z^2) - z =", round(Cm, 4))

    disc = P * P - 4.0 * Cm * A
    print("Discriminante = P^2 - 4*Cm*A =", round(disc, 4))
    if disc < 0:
        print("Discriminante < 0: No existe")
        print("seccion trapezoidal para ese R.")
        print("Aumente z o reduzca V.")
        return

    raiz_d = math.sqrt(disc)
    y1 = (P - raiz_d) / (2.0 * Cm)
    b1 = P - 2.0 * y1 * raiz_m
    y2 = (P + raiz_d) / (2.0 * Cm)
    b2 = P - 2.0 * y2 * raiz_m

    print("Raiz 1: y1 =", round(y1, 4), "m -> b1 =", round(b1, 4), "m")
    print("Raiz 2: y2 =", round(y2, 4), "m -> b2 =", round(b2, 4), "m")

    if b1 >= 0:
        y_dis = y1
        b_dis = b1
    elif b2 >= 0:
        y_dis = y2
        b_dis = b2
    else:
        print("Ambas raices dan b < 0.")
        return

    print("Se adopta la raiz con b > 0:")
    print("-> y =", round(y_dis, 4), "m (", round(y_dis, 2), "m)", end="")
    if unid == "2":
        print(" [", round(y_dis / FT_A_M, 4), "ft]")
    else:
        print("")
    print("-> b =", round(b_dis, 4), "m (", round(b_dis, 2), "m)", end="")
    if unid == "2":
        print(" [", round(b_dis / FT_A_M, 4), "ft]")
    else:
        print("")

    if unid == "2":
        # Nota usando ku = 1.49 directo en pies
        R_ft = ((V_in * n) / (1.49 * math.sqrt(S0))) ** 1.5
        A_ft = Q_in / V_in
        P_ft = A_ft / R_ft
        d_ft = P_ft * P_ft - 4.0 * Cm * A_ft
        if d_ft >= 0:
            y_ft = (P_ft - math.sqrt(d_ft)) / (2.0 * Cm)
            b_ft = P_ft - 2.0 * y_ft * raiz_m
            print("[Nota con ku=1.49 en ft:")
            print(" R=", round(R_ft, 3), "ft, P=", round(P_ft, 3), "ft,", sep="")
            print(" y=", round(y_ft, 3), "ft, b=", round(b_ft, 3), "ft]", sep="")

    # Paso 5: Espejo T, Froude, Manning y Borde libre
    T_agua = b_dis + 2.0 * m * y_dis
    D_hid = A / T_agua
    Fr = V / math.sqrt(G * D_hid)
    Q_ver = (1.0 / n) * A * (R ** (2.0 / 3.0)) * math.sqrt(S0)
    BL, rango_q = borde_libre_ranga(Q)
    H = y_dis + BL
    T_tot = b_dis + 2.0 * m * H

    print("")
    print("Paso 5: Froude, Verificacion y BL")
    print("Ancho sup. T = b + 2*z*y =", round(T_agua, 4), "m")
    print("Prof. hidr. D = A / T =", round(D_hid, 4), "m")
    print("Froude Fr = V / sqrt(g*D) =", round(Fr, 4))
    print("Regimen:", regimen_froude(Fr))
    print("Q verif (Manning) =", round(Q_ver, 4), "m3/s")
    print("Borde libre BL (Tabla 9-1) =", round(BL, 2), "m")
    print("Altura total H = y + BL =", round(H, 4), "m")
    print("Ancho sup. total =", round(T_tot, 4), "m")


def op_seccion_optima():
    print("")
    print("=== 2. Seccion Hidr. Optima ===")
    print("Descripcion del ejercicio:")
    print("Disena el canal de minimo")
    print("perimetro mojado P para un A")
    print("(donde siempre R = y / 2):")
    print("- z = 0  -> Rectangular optimo")
    print("- z = -1 -> Trapezoidal con talud")
    print("            optimo z=1/sqrt(3) (60 gr)")
    print("- z > 0  -> Trapezoidal con z fijo")
    print("Ref Pto 4: n=0.015, Q=7 m3/s,")
    print("S0=0.0006, z=1.25")
    print("-------------------------------")

    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    m_in = float(input("Talud z (0=rect, -1=opt): "))

    if Q <= 0 or n <= 0 or S0 <= 0:
        print("Datos invalidos.")
        return

    es_talud_opt = False
    if m_in < 0:
        m = 1.0 / math.sqrt(3.0)
        es_talud_opt = True
    else:
        m = m_in

    raiz_m = math.sqrt(1.0 + m * m)
    cb = 2.0 * (raiz_m - m)
    cA = 2.0 * raiz_m - m
    Z_req = (Q * n) / math.sqrt(S0)
    coef_man = cA * (0.5 ** (2.0 / 3.0))

    y = (Z_req / coef_man) ** (3.0 / 8.0)
    b = cb * y
    A = cA * y * y
    P = 2.0 * cA * y
    R = 0.5 * y
    V = Q / A
    T_agua = b + 2.0 * m * y
    D_hid = A / T_agua
    Fr = V / math.sqrt(G * D_hid)
    Q_ver = (1.0 / n) * A * (R ** (2.0 / 3.0)) * math.sqrt(S0)

    BL, rango_q = borde_libre_ranga(Q)
    H = y + BL
    T_tot = b + 2.0 * m * H

    print("")
    print("--- PROCEDIMIENTO ---")
    print("Paso 1: Deduccion y rel. optimas")
    print("De A = (b + z*y)*y => b = A/y - z*y")
    print("P = A/y + (2*sqrt(1+z^2) - z)*y")
    print("Minimizando dP/dy = 0 (con A cte):")
    if m == 0:
        print("Caso rectangular (z = 0):")
        print("-> Relacion b/y = 2  (b = 2*y)")
        print("-> A = 2*y^2, P = 4*y")
        print("-> Relacion R/y = A/(P*y) = 1/2 = 0.5")
    elif es_talud_opt:
        print("Minimizando tambien dP/dz = 0:")
        print("-> Talud optimo z = 1/sqrt(3) =", round(m, 4))
        print("-> Angulo theta = atan(1/z) = 60.0 gr")
        print("-> Relacion b/y = 2/sqrt(3) =", round(cb, 4))
        print("-> Relacion T/b = 2.0 (medio hexagono)")
        print("-> A = sqrt(3)*y^2 =", round(cA, 4), "* y^2")
        print("-> P = 2*sqrt(3)*y =", round(2.0 * cA, 4), "* y")
        print("-> Relacion R/y = 1/2 = 0.5")
    else:
        ang = math.degrees(math.atan(1.0 / m))
        print("Para z =", round(m, 4), "(ang =", round(ang, 2), "gr):")
        print("-> Relacion b/y = 2*(sqrt(1+z^2)-z)")
        print("   b/y =", round(cb, 4), "=> b =", round(cb, 4), "* y")
        print("-> A = (2*sqrt(1+z^2)-z)*y^2 =", round(cA, 4), "* y^2")
        print("-> P =", round(2.0 * cA, 4), "* y")
        print("-> Relacion R/y = 1/2 = 0.5")

    print("")
    print("Paso 2: Sustitucion en Manning")
    print("A * R^(2/3) = (Q * n) / sqrt(S0)")
    print("Factor req =", round(Z_req, 4))
    print("(", round(cA, 4), "*y^2) * (0.5*y)^(2/3) =", round(Z_req, 4), sep="")
    print(round(coef_man, 4), "* y^(8/3) =", round(Z_req, 4))

    print("")
    print("Paso 3: Dimensiones y Hidraulica")
    print("y = (", round(Z_req, 4), "/", round(coef_man, 4), ")^(3/8)")
    print("-> y =", round(y, 4), "m (", round(y, 2), "m)")
    print("-> b =", round(b, 4), "m (", round(b, 2), "m)")
    print("-> T =", round(T_agua, 4), "m (", round(T_agua, 2), "m)")
    print("A =", round(A, 4), "m2, P =", round(P, 4), "m")
    print("R = y/2 =", round(R, 4), "m")
    print("V = Q/A =", round(V, 4), "m/s")

    print("")
    print("Paso 4: Froude, Verificacion y BL")
    print("Prof. hidr. D = A / T =", round(D_hid, 4), "m")
    print("Froude Fr = V / sqrt(g*D) =", round(Fr, 4))
    print("Regimen:", regimen_froude(Fr))
    print("Q verif (Manning) =", round(Q_ver, 4), "m3/s")
    print("BL (Tabla 9-1) =", round(BL, 2), "m")
    print("H = y + BL =", round(H, 4), "m")
    print("Ancho sup. total =", round(T_tot, 4), "m")


def op_fuerza_tractiva():
    print("")
    print("=== 3. Fuerza Tractiva (PDF 2) ===")
    print("Descripcion del ejercicio:")
    print("Disena por esfuerzo cortante")
    print("permisible tau_p (N/m2):")
    print("1) Corrige tau_p por factor K")
    print("   de talud: K=sqrt(1-sin2(t)/sin2(phi))")
    print("2) Iguala a 0.76*gamma*y*S0 y halla y")
    print("3) Halla ancho b por Manning")
    print("4) Verifica fondo, Froude y BL")
    print("----------------------------------")

    Q = float(input("Caudal Q (m3/s): "))
    n = float(input("Rugosidad n: "))
    S0 = float(input("Pendiente S0: "))
    m = float(input("Talud m [H:V]: "))
    tau_p = float(input("tau_p perm. (N/m2): "))
    phi_deg = float(input("Ang. reposo phi (gr, 0=coh): "))
    fsin = float(input("Factor sinuos. (0=1.0): "))

    if Q <= 0 or n <= 0 or S0 <= 0 or m <= 0 or tau_p <= 0:
        print("Datos invalidos.")
        return
    if fsin <= 0:
        fsin = 1.0

    gamma = 9810.0
    tau_pc = tau_p * fsin
    theta_rad = math.atan(1.0 / m)
    theta_deg = math.degrees(theta_rad)

    print("")
    print("--- PROCEDIMIENTO (PDF 2) ---")
    print("Paso 1: Esfuerzo admisible base")
    print("tau_p corr = tau_p * f_sin")
    print("tau_p corr =", round(tau_pc, 4), "N/m2")

    print("")
    print("Paso 2: Factor K en taludes")
    print("theta = atan(1/m) =", round(theta_deg, 2), "grados")
    if phi_deg > 0:
        if theta_deg >= phi_deg:
            print("Error: theta >= phi (talud inestable).")
            return
        phi_rad = math.radians(phi_deg)
        K = math.sqrt(1.0 - (math.sin(theta_rad) ** 2) / (math.sin(phi_rad) ** 2))
        print("K = sqrt(1 - sin^2(theta)/sin^2(phi))")
        print("K =", round(K, 4))
    else:
        K = 1.0
        print("Material cohesivo: K = 1.0")

    tau_lados = K * tau_pc
    print("tau_p(lados) = K * tau_p =", round(tau_lados, 4), "N/m2")

    print("")
    print("Paso 3: Despeje del tirante y")
    print("0.76 * gamma * y * S0 = tau_p(lados)")
    y = tau_lados / (0.76 * gamma * S0)
    print("-> y =", round(y, 4), "m")

    print("")
    print("Paso 4: Ancho b por Manning")
    Z_req = (Q * n) / math.sqrt(S0)
    print("A * R^(2/3) = Q*n/sqrt(S0) =", round(Z_req, 4))
    b = resolver_b(Z_req, y, m)
    if b is None:
        print("No se pudo converger b.")
        return
    if b == 0.0:
        print("Nota: Con b=0 (triangular) ya")
        print("supera el caudal requerido.")
    print("-> b =", round(b, 4), "m")

    A, P, R, _, _ = geom_trap(b, y, m)
    V = Q / A
    T_agua = b + 2.0 * m * y
    D_hid = A / T_agua
    Fr = V / math.sqrt(G * D_hid)
    tau_fondo = gamma * y * S0
    BL, rango_q = borde_libre_ranga(Q)
    H = y + BL

    print("")
    print("Paso 5: Chequeo fondo, Froude y BL")
    print("tau_fondo = gamma * y * S0")
    print("tau_fondo =", round(tau_fondo, 3), "N/m2")
    if tau_fondo <= tau_pc * 1.001:
        print("Chequeo: tau_fondo <= tau_p -> CUMPLE")
    else:
        print("Chequeo: tau_fondo > tau_p -> NO CUMPLE")
    print("A =", round(A, 4), "m2, V =", round(V, 4), "m/s")
    print("T =", round(T_agua, 4), "m, Fr =", round(Fr, 4))
    print("Regimen:", regimen_froude(Fr))
    print("BL (Tabla 9-1) =", round(BL, 2), "m")
    print("-> H = y + BL =", round(H, 4), "m")


def menu():
    print("=== Diseno de Canales ===")
    print("1. Vel. Max. Permisible")
    print("2. Secc. Hidr. Optima (Rect/Trap)")
    print("3. Fuerza Tractiva (PDF 2)")

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
