import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sounddevice as sd

# Cargar y normalizar la señal de audio
def cargar_audio(ruta_archivo):
    frecuencia_muestreo, datos_audio = wavfile.read(ruta_archivo)
    if len(datos_audio.shape) > 1:
        datos_audio = datos_audio.mean(axis=1)
    datos_audio = datos_audio / np.max(np.abs(datos_audio))
    return frecuencia_muestreo, datos_audio

# Generar onda portadora
def generar_portadora(frecuencia_muestreo, duracion, frecuencia_portadora):
    tiempo = np.linspace(0, duracion, int(frecuencia_muestreo * duracion))
    onda_portadora = np.sin(2 * np.pi * frecuencia_portadora * tiempo)
    return tiempo, onda_portadora

# Modulación AM
def modulacion_am(datos_audio, onda_portadora):
    senal_am = (1 + datos_audio) * onda_portadora
    return senal_am

# Modulación FM
def modulacion_fm(datos_audio, frecuencia_muestreo, frecuencia_portadora, desviacion_frecuencia):
    tiempo = np.linspace(0, len(datos_audio) / frecuencia_muestreo, len(datos_audio))
    fase = 2 * np.pi * desviacion_frecuencia * np.cumsum(datos_audio) / frecuencia_muestreo
    senal_fm = np.sin(2 * np.pi * frecuencia_portadora * tiempo + fase)
    return senal_fm

# Visualizar señales
def visualizar_senales(tiempo, audio_original, onda_portadora, senal_am, senal_fm, frecuencia_portadora):
    
    plt.figure(figsize=(14, 10))
    plt.suptitle("Vista Completa de Modulaciones AM y FM", fontsize=16)

    # Señal original
    plt.subplot(4, 1, 1)
    plt.plot(tiempo, audio_original, color='blue')
    plt.title("Señal Original")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Señal Portadora
    plt.subplot(4, 1, 2)
    plt.plot(tiempo, onda_portadora, color='purple')
    plt.title(f"Señal Portadora ({frecuencia_portadora} Hz)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Señal AM
    plt.subplot(4, 1, 3)
    plt.plot(tiempo, senal_am, color='orange')
    plt.title("Señal Modulada AM")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Señal FM
    plt.subplot(4, 1, 4)
    plt.plot(tiempo, senal_fm, color='green')
    plt.title("Señal Modulada FM")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Reproducir señales
def reproducir_senal(senal, frecuencia_muestreo):
    print("Reproduciendo señal...")
    sd.play(senal, samplerate=frecuencia_muestreo)
    sd.wait()
    print("Reproducción terminada.")

if __name__ == "__main__":
    
    ruta_archivo = "./resources/sound2.wav"
    
    # Cargar la señal de audio
    frecuencia_muestreo, datos_audio = cargar_audio(ruta_archivo)
    duracion = len(datos_audio) / frecuencia_muestreo
    
    # Generar la onda portadora
    frecuencia_portadora = 30  # Hz reducida para que los ciclos sean más visibles
    tiempo, onda_portadora = generar_portadora(frecuencia_muestreo, duracion, frecuencia_portadora)
    
    # Modulación AM 
    senal_am = modulacion_am(datos_audio, onda_portadora)
    
    # Modulación FM
    desviacion_frecuencia = 4000  # Hz aumentada para ver mejor los cambios de frecuencia
    senal_fm = modulacion_fm(datos_audio, frecuencia_muestreo, frecuencia_portadora, desviacion_frecuencia)
    
    visualizar_senales(tiempo, datos_audio, onda_portadora, senal_am, senal_fm, frecuencia_portadora)
    
    # Menú
    while True:
        print("\nSeleccione una señal para reproducir:")
        print("1. Señal Original")
        print("2. Señal Modulada AM")
        print("3. Señal Modulada FM")
        print("4. Salir")
        opcion = input("Ingrese su elección: ")
        
        if opcion == "1":
            reproducir_senal(datos_audio, frecuencia_muestreo)
        elif opcion == "2":
            reproducir_senal(senal_am, frecuencia_muestreo)
        elif opcion == "3":
            reproducir_senal(senal_fm, frecuencia_muestreo)
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Seleccione una opción válida")