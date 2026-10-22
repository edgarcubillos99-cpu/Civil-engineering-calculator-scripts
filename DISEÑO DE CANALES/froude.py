import math

def froude_solver():
    print("--- Froude Calc ---")
    print("1. Rectangular")
    print("2. Trapezoidal")
    print("3. Triangular")
    print("4. Circular")

    tipo = input("Seccion (1-4): ")
    if tipo not in ('1', '2', '3', '4'):
        print("Opcion invalida")
        return

    try:
        Q = float(input("Caudal Q (m3/s): "))
        y = float(input("Tirante y (m): "))
        if Q <= 0 or y <= 0:
            print("Datos invalidos")
            return
        g = 9.81

        # Manejo de condicionales segun el tipo de seccion
        if tipo == '1':
            b = float(input("Ancho b (m): "))
            if b <= 0:
                print("Datos invalidos")
                return
            A = b * y
            T = b
        elif tipo == '2':
            b = float(input("Ancho b (m): "))
            z = float(input("Talud z: "))
            if b <= 0 or z <= 0:
                print("Datos invalidos")
                return
            A = (b + z * y) * y
            T = b + 2 * z * y
        elif tipo == '3':
            z = float(input("Talud z: "))
            if z <= 0:
                print("Datos invalidos")
                return
            A = z * (y ** 2)
            T = 2 * z * y
        elif tipo == '4':
            d0 = float(input("Diametro d0 (m): "))
            if d0 <= 0:
                print("Datos invalidos")
                return
            r = d0 / 2
            # Control de desbordamiento para tuberias llenas
            if y >= d0:
                print("Flujo a presion!")
                return
            # Uso de radianes para la seccion circular
            theta = 2 * math.acos(1 - y/r)
            A = (r**2 / 2) * (theta - math.sin(theta))
            T = 2 * math.sqrt(r**2 - (r-y)**2)
    except ValueError:
        print("Error: Use valores numericos.")
        return

    # Calculos hidraulicos unificados
    D = A / T
    V = Q / A
    Fr = V / math.sqrt(g * D)

    # Salida por consola truncada a 4 decimales
    print("\n--- Resultados ---")
    print("A =", round(A, 4), "m2")
    print("T =", round(T, 4), "m")
    print("D =", round(D, 4), "m")
    print("V =", round(V, 4), "m/s")
    print("Fr=", round(Fr, 4))

    # Evaluacion del regimen
    if abs(Fr - 1.0) < 1e-4:
        print("-> Critico")
    elif Fr < 1.0:
        print("-> Subcritico")
    else:
        print("-> Supercritico")

# Llamada a la funcion principal al ejecutar el script
froude_solver()
