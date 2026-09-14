# Tabla ASTM: (num, d_ref, d_mm, As_mm2, peri_mm, masa_kg_m)
TABLA = [
    (2, "1/4", 6.4, 32, 20.0, 0.2500),
    (3, "3/8", 9.5, 71, 30.0, 0.5600),
    (4, "1/2", 12.7, 129, 40.0, 0.9944),
    (5, "5/8", 15.9, 199, 50.0, 1.5520),
    (6, "3/4", 19.1, 284, 60.0, 2.2350),
    (7, "7/8", 22.2, 387, 70.0, 3.0420),
    (8, "1", 25.4, 510, 80.0, 3.9730),
    (9, "1-1/8", 28.7, 645, 90.0, 5.0600),
    (10, "1-1/4", 32.3, 819, 101.3, 6.4040),
    (11, "1-3/8", 35.8, 1006, 112.5, 7.9070),
    (14, "1-3/4", 43.0, 1452, 135.1, 11.3800),
    (18, "2-1/4", 57.3, 2581, 180.1, 20.2400),
]

# Flexion de vigas: se excluye #2 (estribos / temperatura)
IDX_VIGA = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)


def buscar_barra(num):
    i = 0
    while i < len(TABLA):
        if TABLA[i][0] == num:
            return TABLA[i]
        i = i + 1
    return None


def datos_barra(num):
    b = buscar_barra(num)
    if b is None:
        print("Barra #", num, " no esta en la tabla.", sep="")
        return None
    print("--- Barra #", b[0], " ---", sep="")
    print("d ref =", b[1], "pulg")
    print("d =", b[2], "mm")
    print("As =", b[3], "mm2")
    print("P =", b[4], "mm")
    print("m =", b[5], "kg/m")
    return b


def txt_cfg(k1, num1, k2, num2):
    if k2 == 0:
        return str(k1) + "#" + str(num1)
    return str(k1) + "#" + str(num1) + " + " + str(k2) + "#" + str(num2)


def config_optima(As_req, n):
    # Lista de (masa, nsizes, spread, As, texto)
    cands = []
    nv = len(IDX_VIGA)

    i = 0
    while i < nv:
        b = TABLA[IDX_VIGA[i]]
        As = n * b[3]
        if As >= As_req:
            masa = n * b[5]
            cands.append((masa, 1, 0, As, txt_cfg(n, b[0], 0, 0)))
        i = i + 1

    i = 0
    while i < nv:
        b1 = TABLA[IDX_VIGA[i]]
        j = i + 1
        while j < nv:
            b2 = TABLA[IDX_VIGA[j]]
            spread = b2[2] - b1[2]
            k = 1
            while k < n:
                As = k * b1[3] + (n - k) * b2[3]
                if As >= As_req:
                    masa = k * b1[5] + (n - k) * b2[5]
                    cands.append((masa, 2, spread, As, txt_cfg(k, b1[0], n - k, b2[0])))
                k = k + 1
            j = j + 1
        i = i + 1

    if len(cands) == 0:
        print("No hay config. con", n, "barras")
        print("que cubra", As_req, "mm2.")
        print("Pruebe mas barras.")
        return None

    cands.sort()
    return cands


def mostrar_config(As_req, n, cands):
    print("As req =", As_req, "mm2")
    print("n =", n, "barras")
    print("")

    tope = 3
    if len(cands) < tope:
        tope = len(cands)

    i = 0
    while i < tope:
        c = cands[i]
        if i == 0:
            print("--- Optima ---")
        else:
            print("--- Alt.", i + 1, " ---", sep="")
        print(c[4])
        print("As =", c[3], "mm2")
        print("exc =", c[3] - As_req, "mm2")
        print("m =", round(c[0], 4), "kg/m")
        if i < tope - 1:
            print("")
        i = i + 1


def menu():
    print("=== Acero de refuerzo ===")
    print("1. Consultar barra")
    print("2. Config. optima")

    op = input("Opcion (1-2): ")

    try:
        if op == "1":
            num = int(input("Numero de barra: "))
            print("")
            datos_barra(num)
        elif op == "2":
            As_req = float(input("As requerida (mm2): "))
            n = int(input("Numero de barras: "))
            if As_req <= 0 or n < 1:
                print("Datos invalidos.")
                return
            print("")
            cands = config_optima(As_req, n)
            if cands is not None:
                mostrar_config(As_req, n, cands)
        else:
            print("Opcion invalida.")
    except ValueError:
        print("Error: Use valores numericos.")


menu()
