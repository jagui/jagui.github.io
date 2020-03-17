from tabulate import tabulate

total_infectados = 1
horas_de_simulacion = 24
horas_transcurridas = 0
tasa_de_contagio = 5
headers = ["hora", "nuevos", "total"]
simulacion = [(0, 1, 1)]

while (horas_transcurridas := horas_transcurridas + 1) < horas_de_simulacion:
    nuevos_infectados = total_infectados * tasa_de_contagio
    total_infectados += nuevos_infectados
    simulacion.append((horas_transcurridas, nuevos_infectados, total_infectados))

print(tabulate(simulacion, headers))
