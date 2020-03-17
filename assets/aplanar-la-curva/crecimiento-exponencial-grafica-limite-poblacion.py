import matplotlib.pyplot as plt
import numpy as np

total_infectados = 1
dias_de_simulacion = 7
horas_de_simulacion = 24 * dias_de_simulacion
horas_transcurridas = 0
tasa_de_contagio = 0.2
poblacion = 40000000
simulacion = {"horas": [0], "nuevos": [1], "total": [total_infectados]}

while (horas_transcurridas := horas_transcurridas + 1) < horas_de_simulacion:
    nuevos_infectados = total_infectados * tasa_de_contagio
    total_infectados = min(poblacion, total_infectados + nuevos_infectados)
    simulacion["horas"].append(horas_transcurridas)
    simulacion["nuevos"].append(nuevos_infectados)
    simulacion["total"].append(total_infectados)

plt.plot("horas", "total", "r-", label="total", data=simulacion)
plt.xlabel("horas desde el brote")
plt.ylabel("personas")
# Mostramos el eje horizontal con marcas desde cero hasta horas_de_simulacion en intervalos de 24 horas
plt.xticks(np.arange(0, horas_de_simulacion, step=24))
plt.axis([0, horas_de_simulacion, 0, poblacion * 1.1])
plt.title("expansión de una epidemia limitada por población")
plt.grid(True)
plt.show()
