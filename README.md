# Gym Tracker (CLI)

Sistema de registro de entrenamiento por consola, escrito en Python. Permite guardar, consultar, buscar y eliminar ejercicios de gimnasio, persistiendo los datos en un archivo CSV local.

> 📖 Este documento es una **referencia técnica**: describe qué hace cada función del sistema, no un tutorial paso a paso. Está pensado para quien quiera entender rápido el alcance y la arquitectura del proyecto.

---

## Descripción General

- **Lenguaje:** Python 3 (usa `match`/`case`, por lo que requiere **Python 3.10 o superior**).
- **Dependencias externas:** ninguna. Usa únicamente librerías estándar: `csv`, `os`, `time`.
- **Persistencia:** un archivo `ejercicios.csv` en el mismo directorio del script, más un archivo auxiliar `next_id.txt` que lleva el control del próximo ID a asignar.
- **Interfaz:** menú de consola interactivo con salida coloreada (ANSI escape codes).

---

## Requisitos e Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd gym-tracker

# Ejecutar (no requiere instalar dependencias)
python main.py
```

**Requisito mínimo:** Python 3.10+ (por el uso de `match`/`case` en `menu()`, `buscar_ejercicios()` y `eliminar_ejercicios()`).

---

## Estructura de Datos

### `ejercicios.csv`

Cada fila representa un ejercicio registrado en una fecha determinada.

| Columna     | Tipo   | Descripción                                  |
|-------------|--------|-----------------------------------------------|
| `id`        | int    | Identificador único y secuencial del registro |
| `fecha`     | str    | Fecha de registro (`YYYY-MM-DD`, autogenerada)|
| `ejercicio` | str    | Nombre del ejercicio                          |
| `sets`      | int    | Cantidad de series (≥ 1)                      |
| `reps`      | int    | Repeticiones por serie (≥ 1)                  |
| `peso`      | float  | Peso utilizado, en kg (≥ 0)                   |
| `nota`      | str    | Comentario libre, opcional                    |

### `next_id.txt`

Archivo auxiliar de una sola línea que guarda el próximo ID disponible. Evita tener que recalcular el máximo ID existente cada vez que se agregan ejercicios. Si no existe, el sistema lo reconstruye leyendo el máximo `id` presente en `ejercicios.csv`.

---

## Referencia del Menú Principal

| Opción | Función                  | Estado           |
|--------|---------------------------|-------------------|
| 1      | Guardar ejercicios        | ✅ Implementado   |
| 2      | Ver ejercicios             | ✅ Implementado   |
| 3      | Buscar ejercicios          | ✅ Implementado   |
| 4      | Eliminar ejercicios        | ✅ Implementado (con una limitación, ver abajo) |
| 5      | Modificar ejercicios       | 🚧 Pendiente      |
| 6      | Análisis de ejercicios     | 🚧 Pendiente      |
| 0      | Salir                      | ✅ Implementado   |

---

## 1. Guardar Ejercicios

Registra uno o más ejercicios nuevos en `ejercicios.csv`.

**Flujo:**
1. Pide la cantidad de ejercicios a guardar (entero > 0).
2. Por cada ejercicio, solicita: nombre, sets, reps, peso y nota. La fecha se asigna automáticamente (`time.strftime("%Y-%m-%d")`).
3. Si `ejercicios.csv` no existe, lo crea con encabezado. Si existe, agrega las filas (modo *append*).
4. Actualiza `next_id.txt` con el siguiente ID disponible.
5. Al finalizar, calcula e imprime el **volumen de entrenamiento** de la tanda recién ingresada:

```
volumen = Σ (sets × reps × peso)   — solo de los ejercicios ingresados en esta sesión
```

**Validaciones:**
- Cantidad, sets y reps deben ser enteros válidos (se reintenta ante `ValueError`).
- Sets y reps deben ser ≥ 1; peso debe ser ≥ 0.

---

## 2. Ver Ejercicios

Muestra el historial completo de `ejercicios.csv` en formato de tabla (sin columna de ID).

- Si el archivo no existe, informa "Archivo no encontrado".
- Si el archivo existe pero está vacío, informa "No hay ejercicios registrados".

---

## 3. Buscar Ejercicios

Submenú con dos métodos de búsqueda:

| Opción | Método | Comportamiento |
|--------|--------|----------------|
| 1 | Por ID | Solo acepta dígitos (`str.isdigit()`). Busca coincidencia exacta de ID. |
| 2 | Por Nombre | Coincidencia **exacta** (no parcial), sin distinguir mayúsculas/minúsculas. |

En ambos casos, si no hay coincidencias se informa al usuario; si las hay, se muestran en tabla con columna de ID incluida.

---

## 4. Eliminar Ejercicios

Submenú con dos métodos de eliminación:

### Por ID
1. Solicita el ID a eliminar.
2. Muestra el registro encontrado.
3. Pide confirmación (`s`/`n`).
4. Si se confirma, reescribe `ejercicios.csv` sin esa fila.

### Por Nombre
1. Solicita el nombre del ejercicio.
2. Muestra todos los registros que coinciden (case-insensitive).
3. Pide al usuario elegir un ID de entre los resultados mostrados.

---

## Tabla Resumen de Validaciones

| Campo / Acción                  | Regla de validación                    |
|----------------------------------|------------------------------------------|
| Cantidad a guardar               | Entero, > 0                              |
| Sets                              | Entero, ≥ 1                              |
| Reps                              | Entero, ≥ 1                              |
| Peso                              | Decimal (float), ≥ 0                     |
| ID de búsqueda/eliminación        | Solo dígitos                             |
| Confirmación de eliminación       | `s` o `n`                                |
| Opción de menú principal         | `0`–`6`                                   |
| Opción de submenú (buscar/eliminar) | `0`, `1` o `2`                        |

---

## Roadmap

- [ ] **Modificar ejercicios** — actualmente sin implementar (placeholder).
- [ ] **Análisis de ejercicios** — actualmente sin implementar (placeholder). Pensado para métricas como progresión de volumen o peso máximo por ejercicio.
- [ ] Completar el flujo de **eliminar por nombre** (conectar con `eliminar_id()`).