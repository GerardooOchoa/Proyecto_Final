# Sistema de Control de Gastos

Este programa permite registrar, consultar y analizar los gastos personales de un usuario.  
Fue creado con Python como proyecto para practicar estructuras de control (`for`, `while`, `if`), manejo de diccionarios, listas y lectura/escritura de archivos Excel (`.xlsx`).

## 👤 ¿Quién puede usarlo?
Cualquier persona o estudiante que desee llevar un control simple de sus gastos y presupuestos mensuales.

## 🚀 Funcionalidades principales
- Registrar gastos y presupuestos
- Consultar y eliminar registros
- Guardar y cargar datos desde Excel
- Analizar el gasto total por categoría
- Generar un reporte en Excel con resultados

## ▶️ Cómo ejecutar
1. Instala Python 3.8 o superior  
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt



                     ┌─────────────────────────┐
                     │  Iniciar Programa      │
                     └───────────┬───────────┘
                                 │
                                 ▼
                   ┌───────────────────────────┐
                   │   Mostrar Menú Principal   │
                   │ 1. Registrar gasto        │
                   │ 2. Ver gastos             │
                   │ 3. Eliminar gasto         │
                   │ 4. Guardar en Excel       │
                   │ 5. Cargar desde Excel     │
                   │ 6. Establecer presupuestos│
                   │ 7. Analizar gastos        │
                   │ 8. Salir                  │
                   └───────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Usuario elige una opción    │
                └───────────┬─────────────────┘
                            │
     ┌──────────────────────┼────────────────────────┐
     ▼                      ▼                        ▼
Registrar gasto         Ver gastos           Establecer presupuestos
     │                      │                        │
     ▼                      ▼                        ▼
Pedir día, categoría,     Mostrar lista       Pedir categoría y
monto → Guardar en lista  de gastos           monto presupuesto
     │                      │                        │
     └───────────────┬──────┴─────────────┐
                     ▼                      ▼
           Guardar datos en Excel      Analizar gastos
           (gastos.xlsx,             Comparar gastos vs
            presupuestos.xlsx)        presupuestos
                     │                      │
                     ▼                      ▼
                   Fin de acción ───────────┘
                               │
                               ▼
                     Volver a mostrar menú
                               │
                               ▼
                     Opción “8” → Salir

1. gastos.xlsx

Archivo automático generado por el programa.

Guarda todos los gastos registrados por el usuario: día, categoría y monto.

Se actualiza cada vez que eliges Guardar datos en Excel en el menú.


2. presupuestos.xlsx

Archivo automático generado por el programa.

Guarda los presupuestos establecidos por categoría.

Se actualiza cuando estableces o modificas un presupuesto y luego guardas.


3. reporte_gastos.xlsx

Archivo automático generado por el programa.

Contiene el análisis comparando gastos vs presupuestos.

Se genera cada vez que eliges Analizar gastos y generar reporte en el menú.

Se sobrescribe si generas un nuevo reporte con datos actualizados.