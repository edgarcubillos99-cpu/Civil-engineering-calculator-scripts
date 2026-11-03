<h1 align="center">🧮 Scripts Casio FX-CG100 — Ingeniería civil</h1>

<p align="center">
  Programas en Python para la calculadora <b>Casio FX-CG100</b>:<br>
  hidráulica, canales, estructuras y demás asignaturas de la carrera.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/MicroPython-Casio%20FX--CG100-blue?logo=python&logoColor=white">
  <img alt="Scripts" src="https://img.shields.io/badge/scripts-7-success">
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

Cada script explica primero qué problema resuelve, pide los datos por consola y muestra el **procedimiento paso a paso** junto con los resultados en pantalla.

El objetivo es tener en la calculadora las mismas herramientas y tablas que se usan en clase y en exámenes, sin depender de hojas de cálculo.

| | |
|---|---|
| 🎯 **Uso** | Cálculos y procedimientos paso a paso directamente en la FX-CG100 |
| 🐍 **Lenguaje** | MicroPython (intérprete Python de Casio) |
| 💾 **Memoria** | Los `.py` van a la *Storage Memory* (~4,5 MB) |
| 🧩 **Dependencias** | Ninguna: cada script es independiente |

---

## 🚀 Cómo pasar un script a la calculadora

**1. Conectar** la FX-CG100 al PC por USB. En la pantalla de la calculadora elige el modo **USB Flash Drive** (memoria de almacenamiento); aparecerá como una unidad extraíble de unos 4,5 MB.

**2. Copiar** el archivo `.py` **a la raíz** de esa unidad. La app Python solo lista los archivos de la raíz: si lo dejas dentro de una carpeta, no lo verás.

En Linux, con la calculadora montada en `/media/$USER/disk`:

```bash
cp "DISEÑO DE CANALES/manning.py" "DISEÑO DE CANALES/discanal.py" "DISEÑO DE CANALES/guiacan.py" /media/$USER/disk/
rm -rf /media/$USER/disk/.Trash-1000   # el gestor de archivos deja basura al borrar
sync && gio mount -u /media/$USER/disk # expulsar de forma segura
```

**3. Desconectar** el USB y salir del modo memoria en la calculadora.

**4. Ejecutar:** abre el menú **Python**, sitúate sobre el archivo y pulsa `Run` (`F1` / `EXE`) directamente desde la lista, o ábrelo con `tools` → `file` → `open` y luego `tools` → `Run`.

**5. Introducir** los datos cuando se pidan y leer el procedimiento y resultados en pantalla.

---

## 📐 Requisitos y notas de uso

> [!IMPORTANT]
> Estas cinco reglas son la causa habitual de que un script "no se ejecute" o lance error al abrirlo.

| | Regla | Detalle |
|---|---|---|
| 🔤 | **Solo ASCII** | Nada de tildes ni `ñ`, tampoco en los comentarios. MicroPython de Casio falla al abrir archivos con caracteres acentuados. Escribe `Calculos`, `seccion`, `regimen` |
| ✂️ | **Nombre corto** | Máximo 8 caracteres antes del `.py`, sin espacios ni acentos (`manning.py`, `discanal.py`, `guiacan.py`) |
| 📏 | **Máximo 300 líneas** | El editor de Python de la Casio FX-CG100 admite como máximo **300 líneas** por archivo `.py` (y 255 caracteres por línea). Si un script supera 300 líneas, lanza el error **`Invalid Data Size`** (`invaliddatasize`) |
| 📂 | **En la raíz** | De la memoria de almacenamiento, nunca en subcarpetas |
| 💾 | **Archivo guardado** | Comprueba que no pesa 0 bytes (`ls -l`); un buffer sin guardar en el editor copia un archivo vacío |

> [!TIP]
> Otras notas:
> - Usa punto decimal (`1.6`, no `1,6`).
> - Unidades del SI: m, m³/s, m/s (salvo `discanal.py`, que también acepta unidades inglesas ft, ft³/s y ft/s y las convierte automáticamente).
> - Los scripts son independientes: puedes llevar solo los que necesites.
> - La app **Memory** solo muestra 200 archivos por carpeta: ese es el tope práctico de scripts en la raíz.

---

## 📁 Organización del repositorio

Los archivos se agrupan por tema, no por número de práctica. Así se pueden añadir scripts sin reestructurar el repositorio:

```text
scripts-para-la-u/
├── README.md                   → esta documentación
├── DISEÑO DE CANALES/          → flujo en canales abiertos y diseño
│   ├── froude.py               → número de Froude y régimen del flujo
│   ├── E_especifica.py         → curva de energía específica (E-y)
│   ├── E_espf.py               → versión de nombre corto (8 chars) de E_especifica
│   ├── manning.py              → flujo uniforme por Manning paso a paso (b, yn, Q y relación Q-y)
│   ├── discanal.py             → diseño de canales y bordes libres paso a paso (Velocidad Permisible, Sección Óptima y Fuerza Tractiva)
│   ├── guiacan.py              → guía de procedimientos y tablas de diseño (Chow, USACE, Ranga Raju, Gupta, USBR)
│       ├── fig9_3.csv          → ángulo de reposo vs diámetro de partícula (USBR)
│       ├── fig9_4.csv          → esfuerzo cortante admisible tau_p vs diámetro en no cohesivos (USBR)
│       ├── fig9_5.csv          → esfuerzo cortante admisible tau_p vs relación de vacíos en cohesivos (USBR)
│       ├── tab4_1.csv          → coeficientes de rugosidad n de Manning (Chow)
│       ├── tab9_1.csv          → borde libre según caudal Q (Ranga Raju)
│       ├── tab9_2.csv          → taludes laterales sugeridos (Fortier & Scobey)
│       └── tab9_3.csv          → velocidades máximas permisibles (USACE)
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
| 🌊 Diseño de canales | [`manning.py`](DISEÑO%20DE%20CANALES/manning.py) | Flujo uniforme con la ecuación de Manning paso a paso: dimensionamiento de base `b`, relación `Q–y` sin conocer `n` ni `S0`, tirante normal `yn` y cálculo directo de `Q` y `V` |
| 🌊 Diseño de canales | [`discanal.py`](DISEÑO%20DE%20CANALES/discanal.py) | Diseño de canales paso a paso con borde libre: Velocidad Máxima Permisible en SI o ft, Sección Hidráulicamente Óptima y Fuerza Tractiva |
| 🌊 Diseño de canales | [`guiacan.py`](DISEÑO%20DE%20CANALES/guiacan.py) | Guía interactiva de procedimientos paso a paso y tablas de consulta: `n` de Manning (Tabla 4-1), bordes libres (Tabla 9-1), taludes (Tabla 9-2), velocidades máximas (Tabla 9-3), limo y esfuerzo cortante (Tabla 9-4 y Figs. 9-3 a 9-5) |
| 🏛️ Diseño de estructuras | [`barras.py`](DISEÑO%20DE%20ESTRUCTURAS/barras.py) | Consulta de barras ASTM y configuración económica de refuerzo a flexión: cubre el `As` mínimo con el menor peso |
| 🏛️ Diseño de estructuras | [`asdviga.py`](DISEÑO%20DE%20ESTRUCTURAS/asdviga.py) | Viga rectangular por ASD: `As` (Viète), sección económica, revisión, capacidad `Mr` y `w` de viga simple |

---

## 📌 Descripción de scripts

### 🌊 `froude.py` — Régimen de flujo (Froude)

Determina si el flujo en un canal es **subcrítico** (`Fr < 1`), **crítico** (`Fr = 1`) o **supercrítico** (`Fr > 1`).

> [!WARNING]
> Los canales son típicos, o sea simétricos. No usar si el objetivo es un canal trapezoidal o triangular con dos pendientes (`z`) diferentes.

**📥 Datos según la sección**

| Sección | Datos que pide |
|---------|----------------|
| ▭ Rectangular | Caudal `Q`, tirante `y`, ancho de solera `b` |
| ⏢ Trapezoidal | `Q`, `y`, `b`, talud `z` (horizontal:vertical) |
| 🔻 Triangular | `Q`, `y`, talud `z` |
| ⭕ Circular | `Q`, `y`, diámetro `d0` |

**📤 Salida:** área `A`, ancho superficial `T`, profundidad hidráulica `D = A/T`, velocidad `V = Q/A` y número de Froude `Fr = V / √(gD)` con `g = 9.81 m/s²`.

**🚧 Aviso:** si en sección circular el tirante iguala o supera el diámetro, avisa de flujo a presión y termina.

<br>

### 🌊 `E_especifica.py` (y `E_espf.py`) — Curva de energía específica

Genera una **tabla de puntos** de la curva energía específica–tirante (`E`–`y`) para un caudal fijo. Sirve para dibujar a mano o localizar el mínimo de `E` (tirante crítico) mirando los valores.

> [!WARNING]
> Los canales son típicos, o sea simétricos. No usar si el objetivo es un canal trapezoidal o triangular con dos pendientes (`z`) diferentes.

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
> `E_espf.py` contiene el mismo programa pero con nombre de 6 caracteres para copiarlo directamente a la calculadora sin renombrar.

<br>

### 🌊 `manning.py` — Flujo uniforme y ecuación de Manning (Paso a paso)

Resuelve problemas de **flujo uniforme** explicando primero qué busca el ejercicio, pidiendo los datos y detallando en pantalla cada paso del desarrollo algebraico y numérico.

**📥 Opciones del menú y datos que pide**

| Opción | Qué resuelve | Datos que pide |
|--------|--------------|----------------|
| **1. Hallar base `b`** | Calcula el ancho de solera `b` necesario en un canal rectangular (`m = 0`) o trapezoidal (`m > 0`) | `Q` (m³/s), `n`, pendiente `S0`, tirante `yn` (m), talud `m` (`0` = rectangular) |
| **2. Sin `n` ni `S0` (Relación Q–y)** | Cuando `n` y `S0` no se conocen pero son constantes en el mismo canal, despeja la constante `K = √S0 / n = Q1 / (A1 R1^(2/3))` para hallar: **a)** el caudal `Q2` a un nuevo tirante `y2`, y **b)** el tirante `y3` para un nuevo caudal `Q3` (p. ej. la mitad del caudal) | `b` (m), `m` (`0` = rect.), caudal base `Q1` (m³/s), tirante base `y1` (m), nuevo tirante `y2` (m), nuevo caudal `Q3` (`0` usa automáticamente `Q1 / 2`) |
| **3. Hallar tirante `yn`** | Calcula la profundidad normal `yn` conociendo la base `b` | `Q` (m³/s), `n`, `S0`, `b` (m), `m` (`0` = rect.) |
| **4. Calcular `Q` y `V` directo** | Calcula área `A`, perímetro `P`, radio hidráulico `R`, velocidad `V` y caudal `Q` | `b` (m), `yn` (m), `m`, `n`, `S0` |

**📤 Desarrollo paso a paso que muestra en pantalla**

- **Opción 1 (Hallar base `b`):**
  1. Plantea las ecuaciones de `A(b)`, `P(b)` y `R(b) = A/P` sustituyendo `yn`.
  2. Despeja el factor de sección requerido por Manning: `A · R^(2/3) = (Q · n) / √S0`.
  3. Plantea `A^(5/3) / P^(2/3) = Factor` y resuelve numéricamente para `b` (ej. para `Q=9, n=0.013, S0=0.0005, yn=1.60, m=0` entrega `b = 3.6402 m`).
  4. Comprueba `A`, `P`, `R`, `V` y `Q`.
- **Opción 2 (Relación Q–y sin `n` ni `S0`):**
  1. Calcula `A1`, `P1`, `R1`, `Z1 = A1 · R1^(2/3)` y la constante `K = √S0 / n = Q1 / Z1`.
  2. **Inciso a):** Con `y2`, calcula `A2`, `P2`, `R2`, `Z2` y obtiene `Q2 = K · Z2` (ej. para `y2 = 0.75 m` entrega `Q2 = 2.7294 m³/s`).
  3. **Inciso b):** Con `Q3`, halla `Z3 = Q3 / K`, plantea la ecuación en función de `y3` y resuelve `y3` (ej. para `Q3 = 5 m³/s` entrega `y3 = 1.0431 m`).

<br>

### 🌊 `discanal.py` — Diseño de canales en flujo uniforme (Paso a paso)

Diseña la sección transversal completa de un canal (`b`, `y`, borde libre `BL` según la Tabla 9-1 de Ranga Raju, altura total `H = y + BL` y espejo de agua `T`) explicando cada paso del procedimiento.

**📥 Opciones del menú y datos que pide**

| Opción | Método de diseño | Datos que pide |
|--------|------------------|----------------|
| **1. Vel. Max. Permisible** | **Método de la velocidad máxima permisible (Guía PDF 1):** diseña un canal erosionable sin superar `Vmax`, verifica Froude y Manning | Sistema de unidades (`1` = SI en m, `2` = Inglés en ft), `Q`, `Vmax`, `n`, `S0`, talud `z` |
| **2. Secc. Hidr. Optima** | **Método de la sección hidráulicamente óptima (máxima eficiencia):** minimiza el perímetro mojado cumpliendo `R = y / 2`, verifica Froude y Manning | `Q` (m³/s), `n`, `S0`, talud `z` (`0` = rectangular óptimo, `-1` = trapezoidal con talud óptimo `z = 1/√3`, `> 0` = talud fijo) |
| **3. Fuerza Tractiva (PDF 2)** | **Método del esfuerzo cortante permisible (Guía PDF 2):** diseña por fuerza tractiva en los taludes (`0.76 γ y S0 = K τp`) y verifica el fondo (`γ y S0 ≤ τp`), Froude y Manning | `Q` (m³/s), `n`, `S0`, `m`, esfuerzo admisible `tau_p` (N/m²), ángulo de reposo `phi` (grados; `0` si es cohesivo) y factor de sinuosidad (`0` = 1.0 canal recto) |

**📤 Desarrollo paso a paso que muestra en pantalla**

- **Opción 1 (Velocidad Máxima Permisible):**
  1. Si se eligen unidades inglesas (`ft³/s` y `ft/s`), convierte primero `Q` y `V` al SI (`1 ft = 0.3048 m`) y muestra los resultados en cada paso **tanto en metros (m) como en pies (ft)** (incluyendo una nota con `ku = 1.49` directo en pies).
  2. Calcula `R = (V · n / √S0)^(3/2)` de Manning y `A = Q / V` de continuidad.
  3. Calcula el perímetro mojado `P = A / R`.
  4. Despeja `b = P - 2y√(1+m²)`, lo sustituye en `A = (b + my)y` para formar la cuadrática `Cm · y² - P · y + A = 0` (con `Cm = 2√(1+m²) - m`), muestra el discriminante, ambas raíces `(y1, b1)` y `(y2, b2)` y selecciona la raíz físicamente válida (`b > 0`). Por ejemplo, para `Q=74 ft³/s, V=2.80 ft/s, n=0.021, S0=0.0009, z=2.0` entrega `y = 0.6712 m (2.202 ft)` y `b = 2.3157 m (7.597 ft)`.
  5. Asigna el borde libre `BL` de la Tabla 9-1 (`BL = 0.75 m`) y calcula `H = y + BL = 1.4212 m (4.663 ft)`.
- **Opción 2 (Sección Hidráulicamente Óptima):**
  1. Obtiene las relaciones óptimas en función de `y`: `b = 2y(√(1+m²) - m) = cb · y`, `A = (2√(1+m²) - m)y² = cA · y²`, `P = 2 cA · y` y `R = y / 2 = 0.5 y`.
  2. Sustituye `A` y `R` en Manning: `(cA · y²)(0.5 y)^(2/3) = (Q · n) / √S0`.
  3. Despeja `y`, `b`, `A`, `P`, `R` y `V`. Por ejemplo, para `Q=7 m³/s, n=0.015, S0=0.0006, z=1.25` entrega `y = 1.5974 m` y `b = 1.1207 m`.
  4. Suma el borde libre de la Tabla 9-1 (`BL = 0.75 m`) obteniendo `H = 2.3474 m`.
- **Opción 3 (Guía PDF 2 — Fuerza Tractiva):**
  1. Ajusta `tau_p` por sinuosidad.
  2. Calcula el ángulo del talud `θ = atan(1/m)` y el factor de reducción `K = √(1 - sin²θ / sin²φ)` para obtener `tau_p(lados) = K · tau_p`.
  3. Iguala `0.76 · γ · y · S0 = tau_p(lados)` (con `γ = 9810 N/m³`) y despeja `y`.
  4. Con `y` fijo, despeja `b` de la ecuación de Manning.
  5. Verifica que en el fondo `tau_fondo = γ · y · S0 ≤ tau_p` y añade `BL` de la Tabla 9-1.

<br>

### 🌊 `guiacan.py` — Guía de procedimientos y tablas de diseño

Script interactivo de consulta rápida para llevar las **guías de procedimiento, fórmulas y tablas de los PDFs**

**📋 Opciones de consulta**

| Opción | Contenido |
|--------|-----------|
| `1. Proc: Vel. Max. Permisible` | Los 5 pasos del procedimiento del PDF 1 y el despeje de la ecuación cuadrática `Cm · y² - P · y + A = 0` |
| `2. Proc: Fuerza Tractiva` | Los 5 pasos del procedimiento del PDF 2, factores de sinuosidad, ecuación de `K`, cortante en lados (`0.76 γ y S0`) y fondo (`γ y S0`) |
| `3. Proc: Secc. Optima y Manning` | Fórmulas de sección hidráulicamente óptima (`R = y/2`), relación a `n` y `S0` constantes (`K = √S0 / n`) y factores de conversión `ft ↔ m` |
| `4. Tabla 4-1: n de Manning` | Coeficientes `n` de Manning para metales, no metales y cauces naturales (Chow, 1959) |
| `5. Tablas 9-1 y 9-2: BL y Talud` | Borde libre recomendado según el caudal `Q` (Ranga Raju, 1983) y taludes laterales `m:1` según el material (Fortier & Scobey, 1926) |
| `6. Tablas 9-3, 9-4 y Figs 9-3..5` | Velocidades máximas permisibles (USACE, 1970), tamaño de partícula y factor de limo (Gupta, 1989) y guía de lectura de las Figuras 9-3 (`φ`), 9-4 (`τp` no cohesivo) y 9-5 (`τp` cohesivo) |

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

**📤 Salida**

- Opción 1: diámetro de referencia, `d` (mm), `As` (mm²), perímetro `P` (mm) y masa `m` (kg/m).
- Opción 2: la combinación óptima y hasta dos alternativas, con `As` colocada, excedente `exc = As − As_req` y masa total `m` (kg/m).

<br>

### 🏛️ `asdviga.py` — Viga rectangular por ASD

Diseño, revisión y **capacidad** de viga rectangular a flexión por el **Método de los Esfuerzos Admisibles** (ASD): sección fisurada, comportamiento elástico lineal. Usa la **solución analítica de Viète** para la cuantía (no el algoritmo iterativo, que en la Casio sería lento).

> [!WARNING]
> Solo sección rectangular simplemente armada (acero a tracción). No calcula cortante, deflexión, adherencia ni acero a compresión. La carga uniforme `w` asume viga **simplemente apoyada** (`M = w L² / 8`).

**📥 Datos según la opción**

Materiales en todas: `f'c` (MPa), factor `kfc` (pon `0` para usar `0.45`, o sea `fc = 0.45 f'c`), `fs` (MPa) y `n = Es/Ec` (si pones `0`, pide `Es` y `Ec`).

| Opción | Datos que pide |
|--------|----------------|
| 1. Diseñar `As` | `M` (o `w` y `L`), ancho `b` (m), peralte efectivo `d` (m) |
| 2. Diseñar `d` (económica) | `M` (o `w` y `L`), `b` y recubrimiento al centroide `r` (m; `0` omite `h`); usa `ρ_b` |
| 3. Revisar sección | `M` (o `w` y `L`), `b`, `d` y `As` (mm²) |
| 4. Capacidad `Mr` | `b`, `d`, `As` (mm²) y `L` (m; `0` omite `w_max`) |

**📤 Salida**

- Opción 1: `k`, `j`, `ρ`, `ρ_b`, tipo (subreforzado / balanceado) y `As` (mm²).
- Opción 2: `d`, `h = d + r` si diste recubrimiento al centroide (`d'`), `R = ½ fc k_b j_b` y `As`.
- Opción 3: `Ms`, `Mc`, `M_all = min(Ms, Mc)`, esfuerzos reales `fs,r` y `fc,r` bajo `M`, y si **cumple**.
- Opción 4: `k`, `j`, `kd`, tipo (subreforzado / balanceado / sobrereforzado), `fc` si el acero llega a `fs`, `Ms`, `Mc`, `Mr` y `w_max` si hay `L`.

---

## 💡 Cómo añadir un script nuevo

1. 📁 Colócalo en la carpeta del tema (crea la carpeta si no existe) con un nombre de **máximo 8 caracteres** antes de `.py`, **menos de 300 líneas** y **100% ASCII**.
2. 📚 Añade una fila en la tabla de [Catálogo de scripts](#-catálogo-de-scripts) y actualiza el contador del badge superior.
3. 🌊 Escribe su apartado en [Descripción de scripts](#-descripción-de-scripts) indicando qué problema resuelve, qué datos pide y qué pasos muestra.
4. 📐 Repasa los [requisitos](#-requisitos-y-notas-de-uso) antes de pasarlo a la calculadora.
