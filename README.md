<h1 align="center">🧮 Scripts Casio FX-CG100 — Ingeniería civil</h1>

<p align="center">
  Programas en Python para la calculadora <b>Casio FX-CG100</b>:<br>
  hidráulica, canales, estructuras y demás asignaturas de la carrera.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/MicroPython-Casio%20FX--CG100-blue?logo=python&logoColor=white">
  <img alt="Scripts" src="https://img.shields.io/badge/scripts-4-success">
  <img alt="Temas" src="https://img.shields.io/badge/temas-canales%20%7C%20hidr%C3%A1ulica%20%7C%20estructuras-lightgrey">
</p>

---

## 📋 Índice

- 🔎 [Descripción general](#-descripción-general)
- 🚀 [Cómo pasar un script a la calculadora](#-cómo-pasar-un-script-a-la-calculadora)
- 📐 [Requisitos y notas de uso](#-requisitos-y-notas-de-uso)
- 📁 [Organización del repositorio](#-organización-del-repositorio)
- 📚 [Catálogo de scripts](#-catálogo-de-scripts)
- 📌 [Descripción de scripts](#-descripción-de-scripts)
- 💡 [Cómo añadir un script nuevo](#-cómo-añadir-un-script-nuevo)

---

## 🔎 Descripción general

Cada script pide los datos por consola, calcula y muestra el resultado en pantalla.

El objetivo es tener en la calculadora las mismas herramientas que se usan en clase y en exámenes, sin depender de hojas de cálculo.

| | |
|---|---|
| 🎯 **Uso** | Cálculos de carrera directamente en la FX-CG100 |
| 🐍 **Lenguaje** | MicroPython (intérprete Python de Casio) |
| 💾 **Memoria** | Los `.py` van a la *Storage Memory* (~4,5 MB) |
| 🧩 **Dependencias** | Ninguna: cada script es independiente |

---

## 🚀 Cómo pasar un script a la calculadora

**1. Conectar** la FX-CG100 al PC por USB. En la pantalla de la calculadora elige el modo **USB Flash Drive** (memoria de almacenamiento); aparecerá como una unidad extraíble de unos 4,5 MB.

**2. Copiar** el archivo `.py` **a la raíz** de esa unidad. La app Python solo lista los archivos de la raíz: si lo dejas dentro de una carpeta, no lo verás.

En Linux, con la calculadora montada en `/media/$USER/disk`:

```bash
cp "DISEÑO DE CANALES/froude.py" /media/$USER/disk/
rm -rf /media/$USER/disk/.Trash-1000   # el gestor de archivos deja basura al borrar
sync && gio mount -u /media/$USER/disk # expulsar de forma segura
```

**3. Desconectar** el USB y salir del modo memoria en la calculadora.

**4. Ejecutar:** abre el menú **Python**, sitúate sobre el archivo y pulsa `tools` → `file` → `open` para abrirlo, luego `tools` → `Run`.

**5. Introducir** los datos cuando se pidan y leer los resultados en pantalla.

---

## 📐 Requisitos y notas de uso

> [!IMPORTANT]
> Estas cuatro reglas son la causa habitual de que un script "no se ejecute".

| | Regla | Detalle |
|---|---|---|
| 🔤 | **Solo ASCII** | Nada de tildes ni `ñ`, tampoco en los comentarios. MicroPython de Casio falla al abrir archivos con caracteres acentuados. Escribe `Calculos`, `seccion`, `regimen` |
| ✂️ | **Nombre corto** | Máximo 8 caracteres antes del `.py`, sin espacios ni acentos (`froude.py`, no `froude_casio_v2.py`) |
| 📂 | **En la raíz** | De la memoria de almacenamiento, nunca en subcarpetas |
| 💾 | **Archivo guardado** | Comprueba que no pesa 0 bytes (`ls -l`); un buffer sin guardar en el editor copia un archivo vacío |

> [!TIP]
> Otras notas:
> - Usa punto decimal (`1.6`, no `1,6`).
> - Unidades del SI: m, m³/s, m/s (se recomienda para que todos los scripts concuerden).
> - Los scripts son independientes: puedes llevar solo los que necesites.
> - La app **Memory** solo muestra 200 archivos por carpeta: ese es el tope práctico de scripts en la raíz.

---

## 📁 Organización del repositorio

Los archivos se agrupan por tema, no por número de práctica. Así se pueden añadir scripts sin reestructurar el repositorio:

```text
scripts-para-la-u/
├── README.md                   → esta documentación
├── DISEÑO DE CANALES/          → flujo en canales abiertos
│   ├── froude.py               → número de Froude y régimen del flujo
│   └── E_especifica.py         → curva de energía específica (E-y)
├── DISEÑO DE ESTRUCTURAS/      → acero de refuerzo y vigas (ASD)
│   ├── barras.py               → consulta ASTM y config. económica
│   └── asdviga.py              → diseño/revisión de viga por ASD
└── HIDRÁULICA/                 → (próximos)
```

Nombres de archivo en `snake_case`, en minúsculas, con extensión `.py`.

---

## 📚 Catálogo de scripts

| 🗂 Tema | 📄 Script | ⚙️ Qué calcula |
|---------|-----------|----------------|
| 🌊 Diseño de canales | [`froude.py`](DISEÑO%20DE%20CANALES/froude.py) | Número de Froude y régimen del flujo (subcrítico / crítico / supercrítico) para sección rectangular, trapezoidal, triangular o circular |
| 🌊 Diseño de canales | [`E_especifica.py`](DISEÑO%20DE%20CANALES/E_especifica.py) | Tabla de energía específica `E` frente al tirante `y` (curva E–y) para sección rectangular, trapezoidal, triangular o circular |
| 🏛️ Diseño de estructuras | [`barras.py`](DISEÑO%20DE%20ESTRUCTURAS/barras.py) | Consulta de barras ASTM y configuración económica de refuerzo a flexión: cubre el `As` mínimo con el menor peso |
| 🏛️ Diseño de estructuras | [`asdviga.py`](DISEÑO%20DE%20ESTRUCTURAS/asdviga.py) | Viga rectangular por ASD: `As` (Viète), sección económica, revisión, capacidad `Mr` y `w` de viga simple |

---

## 📌 Descripción de scripts

### 🌊 `froude.py` — Régimen de flujo (Froude)

Determina si el flujo en un canal es **subcrítico** (`Fr < 1`), **crítico** (`Fr = 1`) o **supercrítico** (`Fr > 1`).

> [!WARNING]
> Los canales son tipicos, osea simetricos. No usar si por ejemplo el objetivo es un trapezoidal o triangular con dos pendientes (`z`) diferentes.

**📥 Datos según la sección**

| Sección | Datos que pide |
|---------|----------------|
| ▭ Rectangular | Caudal `Q`, tirante `y`, ancho de solera `b` |
| ⏢ Trapezoidal | `Q`, `y`, `b`, talud `z` (horizontal:vertical) |
| 🔻 Triangular | `Q`, `y`, talud `z` |
| ⭕ Circular | `Q`, `y`, diámetro `d0` |

**📤 Salida:** área `A`, ancho superficial `T`, profundidad hidráulica `D = A/T`, velocidad `V = Q/A` y número de Froude `Fr = V / √(gD)` con `g = 9.81 m/s²`.

**🚧 Aviso:** si en sección circular el tirante supera el diámetro, avisa de flujo a presión y termina.

<br>

### 🌊 `E_especifica.py` — Curva de energía específica

Genera una **tabla de puntos** de la curva energía específica–tirante (`E`–`y`) para un caudal fijo. Sirve para dibujar a mano o localizar el mínimo de `E` (tirante crítico) mirando los valores.

> [!WARNING]
> Los canales son tipicos, osea simetricos. No usar si por ejemplo el objetivo es un trapezoidal o triangular con dos pendientes (`z`) diferentes.

**📥 Datos según la sección**

| Sección | Datos que pide |
|---------|----------------|
| ▭ Rectangular | Caudal `Q`, ancho de solera `b` |
| ⏢ Trapezoidal | `Q`, `b`, talud `z` (horizontal:vertical) |
| 🔻 Triangular | `Q`, talud `z` |
| ⭕ Circular | `Q`, diámetro `d0` |

Después pide el **rango de la gráfica**: tirante inicial `y`, tirante final y tamaño del paso. Recorre ese intervalo y, para cada `y`, calcula el área `A` y la energía específica.

**📤 Salida:** columnas `y (m)` y `E (m)`, con `E = y + Q² / (2 g A²)` y `g = 9.81 m/s²`.

**🚧 Aviso:** si en sección circular el tirante llega al diámetro, imprime `Tubo Lleno` en esa fila y sigue con el siguiente paso.

> [!NOTE]
> En la calculadora el nombre supera 8 caracteres: al copiarlo a la raíz, renómbralo a algo corto (`energia.py`, `Espec.py`).

<br>

### 🏛️ `barras.py` — Acero de refuerzo (vigas)

Consulta la tabla ASTM de barras (diámetro en octavos de pulgada) o busca la **configuración más económica** para un `As` de diseño y un número de barras: la que cubre el área mínima y pesa menos (el acero se cotiza por kg/m).

> [!WARNING]
> No verifica separación, recubrimiento, capas ni longitud de desarrollo. Mezcla como máximo dos diámetros. En la configuración no usa `#2` (estribos / temperatura).

**📥 Datos según la opción**

| Opción | Datos que pide |
|--------|----------------|
| 1. Consultar barra | Número de barra (`2`–`11`, `14`, `18`) |
| 2. Config. optima | Área requerida `As` (mm²) y número de barras `n` |

La opción 2 recorre combinaciones de **un solo diámetro** (`n` barras iguales) y de **dos diámetros** (`k` de un tamaño y `n − k` del otro). Descarta las que no llegan a `As` y ordena el resto así: menor masa; si empatan, un solo diámetro; luego diámetros más cercanos; luego menos excedente.

**📤 Salida**

- Opción 1: diámetro de referencia, `d` (mm), `As` (mm²), perímetro `P` (mm) y masa `m` (kg/m).
- Opción 2: la combinación óptima y hasta dos alternativas, con `As` colocada, excedente `exc = As − As_req` y masa total `m` (kg/m).

**🚧 Aviso:** si con `n` barras no se alcanza `As_req` (ni con `#18`), indica que hay que probar más barras.

<br>

### 🏛️ `asdviga.py` — Viga rectangular por ASD

Diseño, revisión y **capacidad** de viga rectangular a flexión por el **Método de los Esfuerzos Admisibles** (ASD): sección fisurada, comportamiento elástico lineal. Usa la **solución analítica de Viète** para la cuantía (no el algoritmo iterativo, que en la Casio sería lento).

> [!WARNING]
> Solo sección rectangular simplemente armada (acero a tracción). No calcula cortante, deflexión, adherencia ni acero a compresión. La carga uniforme `w` asume viga **simplemente apoyada** (`M = w L² / 8`).

**📥 Datos según la opción**

Materiales en todas: `f'c` (MPa), factor `kfc` (pon `0` para usar `0.45`, o sea `fc = 0.45 f'c`), `fs` (MPa) y `n = Es/Ec` (si pones `0`, pide `Es` y `Ec`). El `fs` es el esfuerzo **admisible** del acero (en clase a veces lo anotan como `fy`).

En las opciones 1–3 puedes dar el momento `M` (kN·m) o poner `0` y el script lo calcula con `w` (kN/m) y `L` (m).

| Opción | Datos que pide |
|--------|----------------|
| 1. Diseñar `As` | `M` (o `w` y `L`), ancho `b` (m), peralte efectivo `d` (m) |
| 2. Diseñar `d` (económica) | `M` (o `w` y `L`), `b` y recubrimiento `r` (m); usa `ρ_b` |
| 3. Revisar sección | `M` (o `w` y `L`), `b`, `d` y `As` (mm²) |
| 4. Capacidad `Mr` | `b`, `d`, `As` (mm²) y `L` (m; `0` omite `w_max`) |

La opción 1 comprueba primero `M_max = ½ fc k_b j_b b d²` con `k_b = n fc / (n fc + fs)` y `ρ_b = fc k_b / (2 fs)`. Si `M` cabe, resuelve el cúbico `k³ − 3k² − Ck + C = 0` con `C = 6nM / (fs b d²)` y entrega `k`, `j`, `ρ` y `As`.

La opción 4 usa el `k` de la cuantía **real** `ρ = As/(b d)` (no el `k_b`) para `Ms = As fs j d` y `Mc = ½ fc k j b d²`. El resistente es `Mr = min(Ms, Mc)`. Si diste `L`, `w_max = 8 Mr / L²`.

**📤 Salida**

- Opción 1: `k`, `j`, `ρ`, `ρ_b`, tipo (subreforzado / balanceado / sobrereforzado) y `As` (mm²).
- Opción 2: `d`, `h = d + r` si diste recubrimiento, `R = ½ fc k_b j_b` y `As`.
- Opción 3: `Ms`, `Mc`, `M_all = min(Ms, Mc)`, esfuerzos reales `fs,r` y `fc,r` bajo `M`, y si **cumple**.
- Opción 4: `k`, `j`, `kd`, tipo, `fc` si el acero llega a `fs`, `Ms`, `Mc`, `Mr` y `w_max` si hay `L`.

**🚧 Aviso:** si `M > M_max`, la opción 1 indica que no cabe como simplemente armada: hay que aumentar `b` o `d`. El momento se imprime en **kN·m** (no kN/m; eso es la carga `w`).

---

## 💡 Cómo añadir un script nuevo

1. 📁 Colócalo en la carpeta del tema (crea la carpeta si no existe).
2. 📚 Añade una fila en la tabla de [Catálogo de scripts](#-catálogo-de-scripts).
3. 🌊 Si el uso no es obvio, escribe un apartado en [Descripción de scripts](#-descripción-de-scripts).
4. 📐 Repasa los [requisitos](#-requisitos-y-notas-de-uso) antes de pasarlo a la calculadora.
