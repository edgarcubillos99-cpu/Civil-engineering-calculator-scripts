import math

# ASD: viga rectangular, flexion, acero a traccion.
# Unidades internas: N, m, Pa. Pantalla: kN.m, kN/m, MPa, mm2.
# fc adm = kfc * f'c  (kfc=0.45 por ACI / apuntes de clase).


def k_de_rho(rho, n):
    np_ = n * rho
    return math.sqrt(2.0 * np_ + np_ * np_) - np_


def bloque_balanceado(fc, fs, n):
    kb = (n * fc) / (n * fc + fs)
    jb = 1.0 - kb / 3.0
    rhob = (fc * kb) / (2.0 * fs)
    R = 0.5 * fc * kb * jb
    return kb, jb, rhob, R


def clasificar(rho, rhob):
    if rhob <= 0:
        return "N/D"
    dif = (rho - rhob) / rhob
    if dif < -0.01:
        return "Subreforzado"
    if dif > 0.01:
        return "Sobrereforzado"
    return "Balanceado"


def viete_k(C):
    # Raiz admisible 0<k<1 del cubico k^3 - 3k^2 - C k + C = 0
    if C <= 0:
        return 0.0
    base = 3.0 / (3.0 + C)
    arg = base * math.sqrt(base)
    if arg > 1.0:
        arg = 1.0
    if arg < -1.0:
        arg = -1.0
    theta = math.acos(arg) / 3.0
    k = 1.0 + 2.0 * math.sqrt((3.0 + C) / 3.0) * math.cos(theta + 4.0 * math.pi / 3.0)
    return k


def as_desde_M(M, fc, fs, n, b, d):
    kb, jb, rhob, R = bloque_balanceado(fc, fs, n)
    Mmax = R * b * d * d
    C = (6.0 * n * M) / (fs * b * d * d)
    k = viete_k(C)
    if k <= 0.0 or k >= 1.0:
        return None
    j = 1.0 - k / 3.0
    rho = (k * k) / (2.0 * n * (1.0 - k))
    As = rho * b * d
    return k, j, rho, As, kb, jb, rhob, Mmax


def revisar(As, M, fc, fs, n, b, d):
    rho = As / (b * d)
    k = k_de_rho(rho, n)
    j = 1.0 - k / 3.0
    Ms = As * fs * j * d
    Mc = 0.5 * fc * k * j * b * d * d
    fs_r = M / (As * j * d)
    fc_r = (2.0 * M) / (k * j * b * d * d)
    kb, jb, rhob, R = bloque_balanceado(fc, fs, n)
    Mmax = R * b * d * d
    return rho, k, j, Ms, Mc, fs_r, fc_r, rhob, kb, Mmax


def capacidad(As, fc, fs, n, b, d):
    rho = As / (b * d)
    k = k_de_rho(rho, n)
    j = 1.0 - k / 3.0
    Ms = As * fs * j * d
    Mc = 0.5 * fc * k * j * b * d * d
    fc_fs = (fs / n) * (k / (1.0 - k))
    kb, jb, rhob, R = bloque_balanceado(fc, fs, n)
    return rho, k, j, Ms, Mc, fc_fs, rhob, kb


def mm2(As_m2):
    return As_m2 * 1000000.0


def knm(M_Nm):
    return M_Nm / 1000.0


def mpa(p):
    return p / 1000000.0


def pedir_materiales():
    fcp = float(input("f'c (MPa): "))
    kfc = float(input("kfc (0=0.45): "))
    if kfc <= 0:
        kfc = 0.45
    fc = kfc * fcp
    print("fc =", round(fc, 3), "MPa")
    fs = float(input("fs (MPa): "))
    n = float(input("n=Es/Ec (0 calc): "))
    if n <= 0:
        Es = float(input("Es (MPa): "))
        Ec = float(input("Ec (MPa): "))
        if Ec <= 0:
            print("Ec invalido.")
            return None
        n = Es / Ec
        print("n =", round(n, 4))
    if fcp <= 0 or fs <= 0 or n <= 0:
        print("Datos invalidos.")
        return None
    return fc * 1000000.0, fs * 1000000.0, n


def pedir_M():
    # Viga simple, carga uniforme: M = w L^2 / 8
    M = float(input("M (kN.m, 0=wL2/8): "))
    if M > 0:
        return M * 1000.0
    w = float(input("w (kN/m): "))
    L = float(input("L (m): "))
    if w <= 0 or L <= 0:
        print("Datos invalidos.")
        return None
    M = w * L * L / 8.0
    print("M =", round(M, 3), "kN.m")
    return M * 1000.0


def mostrar_tipo(rho, rhob):
    print("rho =", round(rho, 6))
    print("rhob =", round(rhob, 6))
    print("tipo:", clasificar(rho, rhob))


def op_disenar_As():
    mat = pedir_materiales()
    if mat is None:
        return
    fc, fs, n = mat
    M = pedir_M()
    if M is None:
        return
    b = float(input("b (m): "))
    d = float(input("d (m): "))
    if b <= 0 or d <= 0:
        print("Datos invalidos.")
        return

    res = as_desde_M(M, fc, fs, n, b, d)
    if res is None:
        print("No hay raiz k admisible.")
        return
    k, j, rho, As, kb, jb, rhob, Mmax = res

    print("")
    print("--- Diseno As ---")
    print("kb =", round(kb, 4), "  jb =", round(jb, 4))
    print("Mmax =", round(knm(Mmax), 3), "kN.m")
    if M > Mmax * 1.001:
        print("M > Mmax: no cabe")
        print("como simple armada.")
        print("Aumente b o d.")
        return

    print("k =", round(k, 4), "  j =", round(j, 4))
    mostrar_tipo(rho, rhob)
    print("As =", round(mm2(As), 2), "mm2")


def op_disenar_d():
    mat = pedir_materiales()
    if mat is None:
        return
    fc, fs, n = mat
    M = pedir_M()
    if M is None:
        return
    b = float(input("b (m): "))
    r = float(input("recubr. r (m): "))
    if b <= 0:
        print("Datos invalidos.")
        return

    kb, jb, rhob, R = bloque_balanceado(fc, fs, n)
    d = math.sqrt(M / (R * b))
    As = rhob * b * d

    print("")
    print("--- Seccion economica ---")
    print("kb =", round(kb, 4), "  jb =", round(jb, 4))
    print("R =", round(mpa(R), 4), "MPa")
    print("d =", round(d, 4), "m")
    if r > 0:
        print("h =", round(d + r, 4), "m")
    mostrar_tipo(rhob, rhob)
    print("As =", round(mm2(As), 2), "mm2")


def op_revisar():
    mat = pedir_materiales()
    if mat is None:
        return
    fc, fs, n = mat
    M = pedir_M()
    if M is None:
        return
    b = float(input("b (m): "))
    d = float(input("d (m): "))
    As = float(input("As (mm2): ")) / 1000000.0
    if b <= 0 or d <= 0 or As <= 0:
        print("Datos invalidos.")
        return

    rho, k, j, Ms, Mc, fs_r, fc_r, rhob, kb, Mmax = revisar(As, M, fc, fs, n, b, d)
    Mall = Ms
    if Mc < Mall:
        Mall = Mc

    print("")
    print("--- Revision ---")
    print("k =", round(k, 4), "  j =", round(j, 4))
    mostrar_tipo(rho, rhob)
    print("Ms =", round(knm(Ms), 3), "kN.m")
    print("Mc =", round(knm(Mc), 3), "kN.m")
    print("Mall =", round(knm(Mall), 3), "kN.m")
    print("fs,r =", round(mpa(fs_r), 2), "MPa")
    print("fc,r =", round(mpa(fc_r), 2), "MPa")
    if Mall + 0.5 >= M and fs_r <= fs * 1.001 and fc_r <= fc * 1.001:
        print("-> Cumple")
    else:
        print("-> No cumple")


def op_capacidad():
    mat = pedir_materiales()
    if mat is None:
        return
    fc, fs, n = mat
    b = float(input("b (m): "))
    d = float(input("d (m): "))
    As = float(input("As (mm2): ")) / 1000000.0
    L = float(input("L (m, 0=omitir): "))
    if b <= 0 or d <= 0 or As <= 0:
        print("Datos invalidos.")
        return

    rho, k, j, Ms, Mc, fc_fs, rhob, kb = capacidad(As, fc, fs, n, b, d)
    Mr = Ms
    if Mc < Mr:
        Mr = Mc

    print("")
    print("--- Capacidad ---")
    print("k =", round(k, 4), "  j =", round(j, 4))
    print("kd =", round(k * d, 4), "m")
    mostrar_tipo(rho, rhob)
    print("fc@fs =", round(mpa(fc_fs), 2), "MPa")
    print("Ms =", round(knm(Ms), 3), "kN.m")
    print("Mc =", round(knm(Mc), 3), "kN.m")
    print("Mr =", round(knm(Mr), 3), "kN.m")
    if L > 0:
        wmax = (8.0 * knm(Mr)) / (L * L)
        print("wmax =", round(wmax, 3), "kN/m")
        print("(viga simple wL2/8)")


def menu():
    print("=== ASD viga rect. ===")
    print("1. Disenar As")
    print("2. Disenar d (econ.)")
    print("3. Revisar seccion")
    print("4. Capacidad Mr")

    op = input("Opcion (1-4): ")
    try:
        if op == "1":
            op_disenar_As()
        elif op == "2":
            op_disenar_d()
        elif op == "3":
            op_revisar()
        elif op == "4":
            op_capacidad()
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")
    except ZeroDivisionError:
        print("Error en el calculo.")


menu()
