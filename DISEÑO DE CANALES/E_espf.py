import math

def energia_especifica():
    print("=== Curva Energia Especifica ===")
    print("1. Rectangular")
    print("2. Trapezoidal")
    print("3. Triangular")
    print("4. Circular")
    
    tipo = input("Tipo de canal (1-4): ")
    
    try:
        Q = float(input("Caudal Q (m3/s): "))
        g = 9.81
        
        # Pedir datos geometricos segun la seccion
        if tipo == '1':
            b = float(input("Ancho base b (m): "))
        elif tipo == '2':
            b = float(input("Ancho base b (m): "))
            z = float(input("Talud z (m) [H:V]: "))
        elif tipo == '3':
            z = float(input("Talud z (m) [H:V]: "))
        elif tipo == '4':
            d0 = float(input("Diametro d0 (m): "))
        else:
            print("Opcion invalida.")
            return
            
        # Rango para generar la tabla de la curva
        print("\n-- Rango de la grafica --")
        y_inicial = float(input("Tirante y inicial (m): "))
        y_final = float(input("Tirante y final (m): "))
        paso = float(input("Tamano del paso (m): "))
        
        print("\n--- Tabla de Energia ---")
        print(" y (m)   |   E (m)  ")
        print("------------------------")
        
        y_actual = y_inicial
        
        # Generar los puntos evaluando la ecuacion
        while y_actual <= y_final + (paso/10): # Margen para el flotante
            if y_actual <= 0:
                y_actual += paso
                continue
                
            # Calculo del Area segun seccion
            if tipo == '1':
                A = b * y_actual
            elif tipo == '2':
                A = (b + z * y_actual) * y_actual
            elif tipo == '3':
                A = z * (y_actual ** 2)
            elif tipo == '4':
                r = d0 / 2
                if y_actual >= d0:
                    print(str(round(y_actual, 3)) + "    |  Tubo Lleno")
                    y_actual += paso
                    continue
                theta = 2 * math.acos(1 - y_actual/r)
                A = (r**2 / 2) * (theta - math.sin(theta))
            
            # Calculo de la Energia Especifica E = y + (Q^2)/(2gA^2)
            if A > 0:
                E = y_actual + (Q**2) / (2 * g * (A**2))
                # Formateo amigable para la pantalla de la Casio
                print(str(round(y_actual, 3)) + "    |    " + str(round(E, 4)))
            
            y_actual += paso
            
    except ValueError:
        print("Error: Use valores numericos.")

energia_especifica()