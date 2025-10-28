"""
------------------------------------------------------------
SISTEMA DE CONTROL DE GASTOS PERSONALES
Autores Gerardo Ochoa y Diego Fernandez
Versión: 1.00
------------------------------------------------------------
Descripción:
Este programa permite a una persona registrar y analizar sus gastos
diarios o semanales de manera sencilla. Utiliza estructuras básicas 
de programación (for, while, if, listas, diccionarios) y permite 
guardar o leer los datos desde un archivo Excel (.xlsx).

Funciones principales:
- Registrar nuevos gastos (día, categoría, monto)
- Consultar y eliminar gastos
- Guardar y cargar los registros desde Excel
- Establecer presupuestos por categoría
- Analizar los gastos y generar un reporte en Excel

Dirigido a:
Cualquier usuario que desee llevar un control básico de sus finanzas 
personales sin necesidad de usar software complejo.
------------------------------------------------------------
"""

import pandas as pd

# ------------------- FUNCIONES DE VALIDACIÓN -------------------

def validaDecimal(texto):
    """Pide un número decimal positivo."""
    while True:
        try:
            num = float(input(texto))
            if num >= 0:
                return num
            else:
                print("Debe ser un número positivo.")
        except ValueError:
            print("Eso no es un número válido.")

def validaTexto(texto):
    """Pide una cadena de texto no vacía."""
    valor = input(texto).strip().capitalize()
    if valor == "":
        valor = "Sin especificar"
    return valor


# ------------------- FUNCIONES DEL SISTEMA -------------------

def altaGasto(gastos):
    """Registra un nuevo gasto y lo agrega a la lista."""
    print("\n--- Registrar nuevo gasto ---")
    dia = validaTexto("Día (Lunes, Martes, etc.): ")
    categoria = validaTexto("Categoría (Comida, Transporte, etc.): ")
    monto = validaDecimal("Monto gastado: ")

    gasto = {"Día": dia, "Categoría": categoria, "Monto": monto}
    gastos.append(gasto)

    print("✅ Gasto agregado correctamente.")
    return gastos


def mostrarGastos(gastos):
    """Muestra todos los gastos registrados."""
    if not gastos:
        print("No hay gastos registrados.")
        return
    print("\n--- Lista de gastos registrados ---")
    for i, g in enumerate(gastos, start=1):
        print(f"{i}. {g['Día']} - {g['Categoría']} - ${g['Monto']}")
    print()


def eliminarGasto(gastos):
    """Elimina un gasto por número de registro."""
    mostrarGastos(gastos)
    if not gastos:
        return gastos
    try:
        pos = int(input("Número de gasto a eliminar: "))
        if 1 <= pos <= len(gastos):
            eliminado = gastos.pop(pos - 1)
            print(f"🗑️ Gasto eliminado: {eliminado}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Debes ingresar un número.")
    return gastos


def guardarEnExcel(gastos, presupuestos):
    """Guarda los gastos y presupuestos en archivos Excel."""
    if not gastos:
        print("No hay datos para guardar.")
        return
    pd.DataFrame(gastos).to_excel("gastos.xlsx", index=False)
    pd.DataFrame(list(presupuestos.items()), columns=["Categoría", "Presupuesto"]).to_excel("presupuestos.xlsx", index=False)
    print("💾 Archivos 'gastos.xlsx' y 'presupuestos.xlsx' guardados correctamente.")


def leerDesdeExcel():
    """Carga los gastos y presupuestos desde Excel (si existen)."""
    gastos, presupuestos = [], {}
    try:
        gastos_df = pd.read_excel("gastos.xlsx")
        gastos = gastos_df.to_dict("records")
        print("📂 Datos de gastos cargados desde 'gastos.xlsx'")
    except FileNotFoundError:
        print("No existe el archivo 'gastos.xlsx'. Se creará uno nuevo al guardar.")

    try:
        presup_df = pd.read_excel("presupuestos.xlsx")
        for _, row in presup_df.iterrows():
            presupuestos[row["Categoría"]] = row["Presupuesto"]
        print("📂 Presupuestos cargados desde 'presupuestos.xlsx'")
    except FileNotFoundError:
        print("No existe el archivo 'presupuestos.xlsx'. Se creará uno nuevo al guardar.")

    return gastos, presupuestos


def establecerPresupuesto(presupuestos):
    """Permite establecer o modificar un presupuesto por categoría."""
    print("\n--- Establecer o modificar presupuestos ---")
    categoria = validaTexto("Categoría: ")
    monto = validaDecimal(f"Presupuesto semanal para {categoria}: $")
    presupuestos[categoria] = monto
    print(f"💰 Presupuesto para {categoria} establecido en ${monto}")
    return presupuestos


def analizarGastos(gastos, presupuestos):
    """Analiza los gastos y genera un reporte comparando con el presupuesto."""
    if not gastos:
        print("No hay gastos para analizar.")
        return

    # Sumar gastos por categoría
    resumen = {}
    for g in gastos:
        cat = g["Categoría"]
        resumen[cat] = resumen.get(cat, 0) + g["Monto"]

    print("\n--- Análisis de gastos ---")
    resultado = []
    for cat, total in resumen.items():
        presupuesto = presupuestos.get(cat, 0)
        if presupuesto == 0:
            estado = "⚠️ Sin presupuesto definido"
        else:
            estado = "✅ Dentro del presupuesto" if total <= presupuesto else "❌ Se pasó"
        print(f"{cat}: ${total} (Presupuesto: ${presupuesto}) → {estado}")
        resultado.append({"Categoría": cat, "Total Gasto": total, "Presupuesto": presupuesto, "Estado": estado})

    pd.DataFrame(resultado).to_excel("reporte_gastos.xlsx", index=False)
    print("\n📊 Reporte guardado como 'reporte_gastos.xlsx'")


# ------------------- MENÚ PRINCIPAL -------------------

def menu():
    """Muestra las opciones disponibles del sistema."""
    print("\n--- Sistema de Control de Gastos ---")
    print("1. Registrar nuevo gasto")
    print("2. Ver gastos registrados")
    print("3. Eliminar gasto")
    print("4. Guardar datos en Excel")
    print("5. Cargar datos desde Excel")
    print("6. Establecer/modificar presupuestos")
    print("7. Analizar gastos y generar reporte")
    print("8. Salir")


# ------------------- PROGRAMA PRINCIPAL -------------------

gastos = []
presupuestos = {}

while True:
    menu()
    try:
        opcion = int(input("Elige una opción (1-8): "))
    except ValueError:
        print("Debes ingresar un número entre 1 y 8.")
        continue

    if opcion == 1:
        gastos = altaGasto(gastos)
    elif opcion == 2:
        mostrarGastos(gastos)
    elif opcion == 3:
        gastos = eliminarGasto(gastos)
    elif opcion == 4:
        guardarEnExcel(gastos, presupuestos)
    elif opcion == 5:
        gastos, presupuestos = leerDesdeExcel()
    elif opcion == 6:
        presupuestos = establecerPresupuesto(presupuestos)
    elif opcion == 7:
        analizarGastos(gastos, presupuestos)
    elif opcion == 8:
        print("👋 Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("Opción inválida. Intenta de nuevo.")
