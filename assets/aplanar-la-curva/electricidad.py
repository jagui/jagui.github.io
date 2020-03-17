import matplotlib.pyplot as plt

potencia_bombilla_vatios = 25
euros_por_kilovatio = 0.13
horas = list()
consumos = list()
hora = 0


def coste(vatios, horas):
    kilovatios = vatios / 1000
    coste = euros_por_kilovatio * kilovatios * horas
    return coste


while (hora := hora + 1) < 24:
    horas.append(hora)
    consumos.append(coste(potencia_bombilla_vatios, hora))


plt.plot(horas, consumos, "bo-")
plt.xlabel("horas encendida")
plt.ylabel("coste en €")
plt.title("coste por horas de una bombilla")
plt.grid(True)
plt.show()
