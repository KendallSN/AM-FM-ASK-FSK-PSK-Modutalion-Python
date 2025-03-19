import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sounddevice as sd

# 1. Cargar y visualizar la señal de audio
def load_audio(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    if len(audio_data.shape) > 1:  # Convertir a mono si es estéreo
        audio_data = audio_data.mean(axis=1)
    audio_data = audio_data / np.max(np.abs(audio_data))  # Normalizar entre -1 y 1
    return sample_rate, audio_data

# 2. Definir la onda portadora
def generate_carrier_wave(sample_rate, duration, carrier_freq):
    time = np.linspace(0, duration, int(sample_rate * duration))
    carrier_wave = np.sin(2 * np.pi * carrier_freq * time)
    return time, carrier_wave

# 3. Implementar la modulación AM
def am_modulation(audio_data, carrier_wave):
    am_signal = (1 + audio_data) * carrier_wave
    return am_signal

# 4. Implementar la modulación FM
def fm_modulation(audio_data, sample_rate, carrier_freq, freq_deviation):
    phase_deviation = np.cumsum(audio_data) / sample_rate
    time = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))
    fm_signal = np.sin(2 * np.pi * carrier_freq * time + 2 * np.pi * freq_deviation * phase_deviation)
    return fm_signal

# 5. Comparación de Resultados
def compare_signals(time, original_audio, am_signal, fm_signal):
    plt.figure(figsize=(12, 8))

    # Señal Original
    plt.subplot(3, 1, 1)
    plt.plot(time, original_audio, color='blue')
    plt.title("Señal Original")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid()

    # Señal Modulada AM
    plt.subplot(3, 1, 2)
    plt.plot(time, am_signal, color='orange')
    plt.title("Señal Modulada AM")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid()

    # Señal Modulada FM
    plt.subplot(3, 1, 3)
    plt.plot(time, fm_signal, color='green')
    plt.title("Señal Modulada FM")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid()

    plt.tight_layout()
    plt.show()

# 6. Reproducir señales
def play_signal(signal, sample_rate):
    print("Reproduciendo señal...")
    sd.play(signal, samplerate=sample_rate)
    sd.wait()  # Esperar a que termine la reproducción
    print("Reproducción terminada.")

# Ejecución del flujo
if __name__ == "__main__":
    # Ruta del archivo .wav
    file_path = "./resources/sound2.wav"
    
    # 1. Cargar la señal de audio
    sample_rate, audio_data = load_audio(file_path)
    duration = len(audio_data) / sample_rate  # Duración de la señal en segundos

    # 2. Generar la onda portadora
    carrier_freq = 10  # Frecuencia de la portadora en Hz
    time, carrier_wave = generate_carrier_wave(sample_rate, duration, carrier_freq)

    # 3. Modulación AM
    am_signal = am_modulation(audio_data, carrier_wave)

    # 4. Modulación FM
    freq_deviation = 5000  # Desviación de frecuencia para FM
    fm_signal = fm_modulation(audio_data, sample_rate, carrier_freq, freq_deviation)

    # 5. Comparar señales
    compare_signals(time, audio_data, am_signal, fm_signal)
    
    # Reproducir señales
    while True:
        print("\nSeleccione una señal para reproducir:")
        print("1. Señal Original")
        print("2. Señal Modulada AM")
        print("3. Señal Modulada FM")
        print("4. Salir")
        choice = input("Ingrese su elección: ")
        
        if choice == "1":
            play_signal(audio_data, sample_rate)
        elif choice == "2":
            play_signal(am_signal, sample_rate)
        elif choice == "3":
            play_signal(fm_signal, sample_rate)
        elif choice == "4":
            print("Saliendo...")
            break
        else:
            print("Selecciones una opcion")