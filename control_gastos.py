"""
------------------------------------------------------------
SISTEMA DE CONTROL DE GASTOS PERSONALES
Autores: Gerardo Ochoa y Diego Fernandez
------------------------------------------------------------
"""

import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openpyxl


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

def mostrarGastos_tabulate(gastos):
    """Muestra los gastos con formato de tabla usando tabulate."""
    if not gastos:
        print("No hay gastos registrados.")
        return
    print("\n📋 GASTOS (tabla):")
    print(tabulate(gastos, headers="keys", tablefmt="fancy_grid", floatfmt=".2f"))

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

# ------------------- FUNCIONES NUEVAS (librerías) -------------------

def convertir_totales_a_usd(gastos):
    """Convierte el total de gastos a USD usando la API Frankfurter o una tasa fija si falla."""
    if not gastos:
        print("No hay gastos para convertir.")
        return

    total_mx = sum(g["Monto"] for g in gastos)
    print(f"Total en MXN: ${total_mx:.2f}")

    url = "https://api.frankfurter.app/latest?from=MXN&to=USD"
    tasa_fija = 0.055  # Tasa aproximada MXN→USD si no hay conexión

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        tasa = data.get("rates", {}).get("USD", None)
        if tasa:
            total_usd = total_mx * tasa
            print(f"Tasa MXN→USD (API): {tasa:.6f}")
            print(f"Total aproximado en USD: ${total_usd:.2f}")
        else:
            print("⚠️ No se pudo obtener la tasa de cambio desde la API. Se usará tasa fija.")
            total_usd = total_mx * tasa_fija
            print(f"Total aproximado en USD (fijo): ${total_usd:.2f}")
    except Exception as e:
        print("No se pudo conectar a la API de conversión. Se usará tasa fija.")
        print("Error:", e)
        total_usd = total_mx * tasa_fija
        print(f"Total aproximado en USD (fijo): ${total_usd:.2f}")


def generar_reporte_pdf(gastos, presupuestos):
    """Genera un reporte de gastos en PDF."""
    if not gastos:
        print("No hay gastos para generar PDF.")
        return

    c = canvas.Canvas("reporte_gastos.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "REPORTE DE GASTOS PERSONALES")
    c.setFont("Helvetica", 12)

    y = 720
    for g in gastos:
        categoria = g['Categoría']
        dia = g['Día']
        monto = g['Monto']
        presupuesto = presupuestos.get(categoria, 0)
        estado = "Dentro del presupuesto" if monto <= presupuesto else "Se pasó" if presupuesto > 0 else "Sin presupuesto"
        linea = f"{dia} | {categoria} | ${monto:.2f} | Presupuesto: ${presupuesto} | {estado}"
        c.drawString(50, y, linea)
        y -= 20
        if y < 50:  # Nueva página si se llena
            c.showPage()
            y = 750

    c.save()
    print("📄 Reporte PDF generado: 'reporte_gastos.pdf'")


def graficar_gastos(gastos, presupuestos):
    """Genera una gráfica de barras de gastos vs presupuesto por categoría."""
    if not gastos:
        print("No hay gastos para graficar.")
        return

    # Sumar gastos por categoría
    resumen = {}
    for g in gastos:
        cat = g["Categoría"]
        resumen[cat] = resumen.get(cat, 0) + g["Monto"]

    categorias = list(resumen.keys())
    gastos_totales = [resumen[cat] for cat in categorias]
    presupuestos_totales = [presupuestos.get(cat, 0) for cat in categorias]

    x = range(len(categorias))
    plt.figure(figsize=(8,5))
    plt.bar(x, gastos_totales, width=0.4, label="Gastos", color='skyblue')
    plt.bar([i+0.4 for i in x], presupuestos_totales, width=0.4, label="Presupuesto", color='lightgreen')
    plt.xticks([i+0.2 for i in x], categorias, rotation=45)
    plt.ylabel("Monto ($)")
    plt.title("Gastos vs Presupuesto por Categoría")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafica_gastos.png")  # Guarda la gráfica
    plt.show()
    print("📊 Gráfica generada y guardada como 'grafica_gastos.png'.")




# ------------------- MENÚ PRINCIPAL -------------------

def menu():
    """Muestra las opciones disponibles del sistema."""
    print("\n--- Sistema de Control de Gastos ---")
    print("1. Registrar nuevo gasto")
    print("2. Ver gastos registrados (lista)")
    print("3. Ver gastos registrados (tabla)")
    print("4. Eliminar gasto")
    print("5. Guardar datos en Excel")
    print("6. Cargar datos desde Excel")
    print("7. Establecer/modificar presupuestos")
    print("8. Analizar gastos y generar reporte")
    print("9. Graficar gastos vs presupuesto")
    print("10. Convertir total a USD (API)")
    print("11. Generar reporte en PDF")
    print("12. Salir")

# ------------------- PROGRAMA PRINCIPAL -------------------

gastos = []
presupuestos = {}

while True:
    menu()
    try:
        opcion = int(input("Elige una opción (1-12): "))
    except ValueError:
        print("Debes ingresar un número entre 1 y 12.")
        continue

    if opcion == 1:
        gastos = altaGasto(gastos)
    elif opcion == 2:
        mostrarGastos(gastos)
    elif opcion == 3:
        mostrarGastos_tabulate(gastos)
    elif opcion == 4:
        gastos = eliminarGasto(gastos)
    elif opcion == 5:
        guardarEnExcel(gastos, presupuestos)
    elif opcion == 6:
        gastos, presupuestos = leerDesdeExcel()
    elif opcion == 7:
        presupuestos = establecerPresupuesto(presupuestos)
    elif opcion == 8:
        analizarGastos(gastos, presupuestos)
    elif opcion == 9:
        graficar_gastos(gastos, presupuestos)
    elif opcion == 10:
        convertir_totales_a_usd(gastos)
    elif opcion == 11:
        generar_reporte_pdf(gastos, presupuestos)

    elif opcion == 12:
        guardarEnExcel(gastos, presupuestos)
        print("👋 Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("Opción inválida. Intenta de nuevo.")

