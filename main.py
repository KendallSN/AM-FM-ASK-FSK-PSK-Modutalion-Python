import numpy as np
import matplotlib.pyplot as plt

# Generar la señal de datos binarios
def generar_datos_binarios(mensaje):
    binario = ''.join(format(ord(c), '08b') for c in mensaje)
    return np.array([int(b) for b in binario])

# ASK
def modulacion_ask(binario, frecuencia, tiempo_bit):
    t = np.linspace(0, len(binario) * tiempo_bit, int(len(binario) * tiempo_bit * 1000))
    portadora = np.sin(2 * np.pi * frecuencia * t)
    señal_ask = np.repeat(binario, int(tiempo_bit * 1000)) * portadora
    return t, señal_ask

# FSK
def modulacion_fsk(binario, f0, f1, tiempo_bit):
    t = np.linspace(0, len(binario) * tiempo_bit, int(len(binario) * tiempo_bit * 1000))
    señal_fsk = np.zeros_like(t)
    for i, bit in enumerate(binario):
        f = f1 if bit == 1 else f0
        señal_fsk[i * int(tiempo_bit * 1000):(i + 1) * int(tiempo_bit * 1000)] = np.sin(2 * np.pi * f * t[i * int(tiempo_bit * 1000):(i + 1) * int(tiempo_bit * 1000)])
    return t, señal_fsk

# PSK
def modulacion_psk(binario, frecuencia, tiempo_bit):
    t = np.linspace(0, len(binario) * tiempo_bit, int(len(binario) * tiempo_bit * 1000))
    portadora = np.sin(2 * np.pi * frecuencia * t)
    señal_psk = np.copy(portadora)
    for i, bit in enumerate(binario):
        if bit == 0:
            señal_psk[i * int(tiempo_bit * 1000):(i + 1) * int(tiempo_bit * 1000)] *= -1
    return t, señal_psk

# Imprimir los gráficos de las señales
def imprimir_graficos(binario, tiempo_bit, t, señal_ask, señal_fsk, señal_psk):
    plt.figure(figsize=(12, 10))

    # Señal Binaria
    plt.subplot(4, 1, 1)
    t_bin = np.linspace(0, len(binario) * tiempo_bit, len(binario) + 1)
    binario_extendido = np.repeat(binario, 2)
    t_bin_extendido = np.repeat(t_bin, 2)[1:-1]
    plt.step(t_bin_extendido, binario_extendido, where='post')
    plt.title("Señal Binaria")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()

    # Señal Modulada ASK
    plt.subplot(4, 1, 2)
    plt.plot(t, señal_ask)
    plt.title("Señal Modulada ASK")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()

    # Señal Modulada FSK
    plt.subplot(4, 1, 3)
    plt.plot(t, señal_fsk)
    plt.title("Señal Modulada FSK")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()

    # Señal Modulada PSK
    plt.subplot(4, 1, 4)
    plt.plot(t, señal_psk)
    plt.title("Señal Modulada PSK")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()

    plt.tight_layout()
    plt.show()

mensaje = "Hola Mundo!"
tiempo_bit = 0.01
frecuencia = 5000  # 5 kHz frecuencia estandar
f0 = 2000  # 2 kHz frecuencia baja para FSK
f1 = 5000  # 5 kHz frecuencia alta para FSK

# Generar datos binarios
binario = generar_datos_binarios(mensaje)

# Modulación ASK
t, señal_ask = modulacion_ask(binario, frecuencia, tiempo_bit)

# Modulación FSK
t, señal_fsk = modulacion_fsk(binario, f0, f1, tiempo_bit)

# Modulación PSK
t, señal_psk = modulacion_psk(binario, frecuencia, tiempo_bit)

# Imprimir graficos
imprimir_graficos(binario, tiempo_bit, t, señal_ask, señal_fsk, señal_psk)