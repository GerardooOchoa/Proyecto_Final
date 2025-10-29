
# Sistema de Control de Gastos

Autores: Gerardo Ochoa y Diego Fernandez 
Programado en Codespaces

Este programa permite registrar, consultar, analizar y exportar los gastos personales de un usuario.
Fue creado con Python como proyecto para practicar estructuras de control (for, while, if), manejo de diccionarios, listas y lectura/escritura de archivos Excel (.xlsx).

Además, se añadieron mejoras con librerías externas:

tabulate: para mostrar tablas con formato en consola

matplotlib: para graficar gastos vs presupuestos

requests (API Frankfurter): para convertir totales a USD

reportlab: para generar reportes en PDF

👤 ¿Quién puede usarlo?

Cualquier persona o estudiante que desee llevar un control simple de sus gastos y presupuestos semanales o diarios.

🚀 Funcionalidades principales

- Registrar gastos y presupuestos

- Consultar gastos en lista o tabla

- Eliminar registros

- Guardar y cargar datos desde Excel (gastos.xlsx y presupuestos.xlsx)

- Analizar el gasto total por categoría y comparar con presupuestos

- Graficar gastos vs presupuesto

- Convertir el total de gastos a USD usando la API Frankfurter (o tasa fija si falla)

- Generar reporte en PDF (reporte_gastos.pdf)

- Generar reporte en Excel (reporte_gastos.xlsx)

📁 Archivos generados por el programa

1. gastos.xlsx

- Contiene todos los gastos registrados: día, categoría y monto

- Se actualiza al guardar datos desde el menú


2. presupuestos.xlsx

- Contiene los presupuestos por categoría

- Se actualiza al establecer o modificar presupuestos y luego guardar


3. reporte_gastos.xlsx

- Contiene el análisis comparando gastos vs presupuestos

- Se genera al elegir "Analizar gastos y generar reporte"


4. reporte_gastos.pdf

- Contiene un reporte de gastos en PDF, con día, categoría, monto, presupuesto y estado

- Se genera al elegir "Generar reporte en PDF"


5. grafica_gastos.png

- Gráfica de barras comparando gastos vs presupuesto por categoría

- Se genera al elegir "Graficar gastos vs presupuesto"

- Permite visualizar fácilmente en qué categorías se excedió o se mantuvo dentro del presupuesto