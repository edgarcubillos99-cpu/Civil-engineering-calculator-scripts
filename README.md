<h1 align="center">🧮 Scripts Casio FX-CG100 — Ingeniería civil</h1>

<p align="center">
  Programas en Python para la calculadora <b>Casio FX-CG100</b>:<br>
  hidráulica, canales, estructuras y demás asignaturas de la carrera.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/MicroPython-Casio%20FX--CG100-blue?logo=python&logoColor=white">
  <img alt="Scripts" src="https://img.shields.io/badge/scripts-3-success">
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
├── DISEÑO DE ESTRUCTURAS/      → acero de refuerzo en vigas
│   └── barras.py               → consulta ASTM y config. económica
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

---

## 💡 Cómo añadir un script nuevo

1. 📁 Colócalo en la carpeta del tema (crea la carpeta si no existe).
2. 📚 Añade una fila en la tabla de [Catálogo de scripts](#-catálogo-de-scripts).
3. 🌊 Si el uso no es obvio, escribe un apartado en [Descripción de scripts](#-descripción-de-scripts).
4. 📐 Repasa los [requisitos](#-requisitos-y-notas-de-uso) antes de pasarlo a la calculadora.
