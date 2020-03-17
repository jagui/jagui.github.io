import matplotlib.pyplot as plt

total_infectados = 1
horas_de_simulacion = 24
horas_transcurridas = 0
tasa_de_contagio = 2
# Diccionario que contiene 3 listas
simulacion = {"horas": [0], "nuevos": [1], "total": [total_infectados]}

while (horas_transcurridas := horas_transcurridas + 1) < horas_de_simulacion:
    nuevos_infectados = total_infectados * tasa_de_contagio
    total_infectados += nuevos_infectados
    simulacion["horas"].append(horas_transcurridas)
    simulacion["nuevos"].append(nuevos_infectados)
    simulacion["total"].append(total_infectados)

# Los parámetros "horas" y "total" especifican qué listas dentro de "simulacion" vamos a pintar
plt.plot("horas", "total", "bo-", data=simulacion)
plt.xlabel("horas desde el brote")
plt.ylabel("personas")
plt.title("expansión incontrolada de una epidemia")
plt.grid(True)

plt.show()
