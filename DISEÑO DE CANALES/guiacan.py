# Guia de procedimientos y tablas de diseno de canales


def pausa():
    input("\n[Enter] para continuar...")


def proc_vel_permisible():
    print("\n=== PROC. VEL. MAX. PERMISIBLE ===")
    print("Paso 1: Elegir para el material:")
    print(" - n (Tabla 4-1), Talud m (Tabla 9-2)")
    print(" - Vel. permisible V (Tabla 9-3)")
    print("Paso 2: Calcular R y A:")
    print(" - R = (V * n / sqrt(S0))^(3/2)")
    print("   (en ft usar 1.486 o 1.49 en denom)")
    print(" - A = Q / V  (Continuidad)")
    pausa()
    print("Paso 3: Perimetro mojado P = A / R")
    print("Paso 4: Hallar tirante y y ancho b:")
    print(" - De P = b + 2*y*sqrt(1+m^2)")
    print("   despejar: b = P - 2*y*sqrt(1+m^2)")
    print(" - Sustituir en A = (b + m*y)*y:")
    print("   Cm * y^2 - P * y + A = 0")
    print("   donde Cm = 2*sqrt(1+m^2) - m")
    print(" - y = [P - sqrt(P^2 - 4*Cm*A)]/(2*Cm)")
    print("Paso 5: Borde libre BL (Tabla 9-1):")
    print(" - Altura total H = y + BL")


def proc_fuerza_tractiva():
    print("\n=== PROC. FUERZA TRACTIVA ===")
    print("Paso 1: Del material obtener:")
    print(" - Talud m (T.9-2), phi (Fig 9-3)")
    print(" - tau_p (Fig 9-4 no coh / 9-5 coh)")
    print(" - Factor sinuosidad: Recto=1.0,")
    print("   Lig=0.90, Mod=0.75, Muy=0.60")
    pausa()
    print("Paso 2: Factor K en los taludes:")
    print(" - theta = atan(1/m)")
    print(" - K = sqrt(1 - sin^2(theta)/sin^2(phi))")
    print(" - tau_p(lados) = K * tau_p")
    print("Paso 3: Despejar tirante y:")
    print(" - 0.76 * 9810 * y * S0 = tau_p(lados)")
    print("Paso 4: Hallar ancho b por Manning:")
    print(" - A * R^(2/3) = Q * n / sqrt(S0)")
    print("Paso 5: Verificar fondo y BL:")
    print(" - tau_fondo = 9810 * y * S0 <= tau_p")
    print(" - H = y + BL (Tabla 9-1)")


def proc_optima_manning():
    print("\n=== SECC. OPTIMA Y MANNING ===")
    print("1) Deduccion Secc. Hidr. Optima:")
    print("   A = (b+z*y)*y => b = A/y - z*y")
    print("   P = A/y + (2*sqrt(1+z^2) - z)*y")
    print("   dP/dy = -A/y^2 + 2*sqrt(1+z^2)-z = 0")
    print("   => b/y = 2*(sqrt(1+z^2) - z)")
    print("   => R = A / P = y / 2  (R/y = 0.5)")
    print("   - Si z=0 (Rect): b/y = 2, R/y = 0.5")
    print("   - Talud optimo (dP/dz = 0):")
    print("     z = 1/sqrt(3) = 0.5774 (ang=60 gr)")
    print("     b/y = 2/sqrt(3) = 1.1547, T/b = 2")
    pausa()
    print("2) Relacion sin n ni S0 (mismo canal):")
    print("   - K = sqrt(S0)/n = Q1 / (A1*R1^(2/3))")
    print("   - Nuevo y2: Q2 = K * A2 * R2^(2/3)")
    print("   - Nuevo Q3: A3 * R3^(2/3) = Q3 / K")
    print("3) Conversiones utiles:")
    print("   - 1 ft = 0.3048 m (1 m = 3.2808 ft)")
    print("   - 1 ft2 = 0.092903 m2")
    print("   - 1 ft3/s = 0.028317 m3/s")


def tabla_manning_n():
    print("\n=== TABLA 4-1: n DE MANNING ===")
    print("-- Metales --")
    print("Acero: 0.012 | Hierro fund: 0.013")
    print("Metal corrugado: 0.025")
    print("-- No metales --")
    print("Lucita : 0.009 | Vidrio   : 0.010")
    print("Cemento: 0.011 | Madera   : 0.012")
    print("Concreto/Arcilla/Ladrillo : 0.013")
    print("Gunita : 0.019 | Mampost. : 0.025")
    print("Cortes en roca            : 0.035")
    print("-- Cauces naturales --")
    print("Limpio y recto            : 0.030")
    print("Fondo grava y cantos      : 0.040")
    print("Cantos y grandes bloques  : 0.050")


def tablas_bl_talud():
    print("\n=== TABLA 9-1: BORDE LIBRE ===")
    print("Q < 0.75 m3/s     -> BL = 0.45 m")
    print("0.75 a 1.50 m3/s  -> BL = 0.60 m")
    print("1.50 a 85.0 m3/s  -> BL = 0.75 m")
    print("Q > 85.0 m3/s     -> BL = 0.90 m")
    print("\n=== TABLA 9-2: TALUDES (z:1) ===")
    print("Roca (Rock)           : ~0:1 (vert)")
    print("Arcilla rigida (Stiff): 0.5:1 a 1:1")
    print("Suelo firme (Firm)    : 1:1")
    print("Arenoso suelto (Loose): 2:1")
    print("Franco arenoso (Loam) : 3:1")


def tablas_vel_limo_figs():
    print("\n=== TABLA 9-3: VEL. PERMISIBLE ===")
    print("Arena fina: 0.6 | Arena gruesa: 1.2")
    print("Tierra - Limo arenoso   : 0.6 m/s")
    print("Tierra - Arcilla limosa : 1.1 m/s")
    print("Tierra - Arcilla        : 1.8 m/s")
    print("Pasto Bermuda (Limo/Arc): 1.8 / 2.4")
    print("Pasto Kentucky(Limo/Arc): 1.5 / 2.1")
    print("Arenisca / Lutita blanda: 2.4 / 1.1")
    print("Roca buena (ignea/metam): 6.1 m/s")
    pausa()
    print("=== TABLA 9-4: LIMO (Gupta 89) ===")
    print("Cantos (64-256mm) : f = 6.12-9.75")
    print("Grava gr (8-64mm) : f = 4.68")
    print("Grava fn (4-8mm)  : f = 2.0")
    print("Arena gr (0.5-2mm): f = 1.44-1.56")
    print("Arena md (.25-.5) : f = 1.31")
    print("Arena fn (.06-.25): f = 1.1-1.3")
    print("Limo coloidal / fn: f = 1.0 / 0.4-0.9")
    pausa()
    print("=== GUIA FIGS 9-3, 9-4 Y 9-5 ===")
    print("Fig 9-3 (phi gr, d=1..100mm):")
    print(" - Muy redond: 21..39 | Mod: 23..40")
    print(" - Mod angul : 29..41 | Muy: 31..42")
    print("Fig 9-4 (tau_p no coh N/m2):")
    print(" - Agua clara (d=0.1..5mm): 1.2..4.0")
    print(" - Poco sedim (d=0.1..5mm): 2.5..4.6")
    print(" - Mucho sed  (d=0.1..5mm): 4.5..6.2")
    print(" - Grueso (d>=5mm): tau_p = 0.75*d(mm)")


def menu():
    while True:
        print("\n=== Guia y Tablas Canales ===")
        print("1. Proc: Vel. Max. Permisible")
        print("2. Proc: Fuerza Tractiva")
        print("3. Proc: Secc. Optima y Manning")
        print("4. Tabla 4-1: n de Manning")
        print("5. Tablas 9-1 y 9-2: BL y Talud")
        print("6. Tablas 9-3, 9-4 y Figs 9-3..5")
        print("0. Salir")
        op = input("Opcion (0-6): ")
        if op == "0":
            break
        elif op == "1":
            proc_vel_permisible()
        elif op == "2":
            proc_fuerza_tractiva()
        elif op == "3":
            proc_optima_manning()
        elif op == "4":
            tabla_manning_n()
        elif op == "5":
            tablas_bl_talud()
        elif op == "6":
            tablas_vel_limo_figs()
        else:
            print("Opcion invalida.")


menu()
