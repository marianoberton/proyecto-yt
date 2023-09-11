import subprocess
import time
import os
import threading

# Rutas a los scripts
SCRIPT_DESCARGAR = os.path.join(os.getcwd(), "src", "descargar.py")
SCRIPT_TRANSCRIBIR = os.path.join(os.getcwd(), "src", "transcribir.py")

# Directorio donde se guardarán los segmentos
DIR_SEGMENTOS = os.path.join(os.getcwd(), "data", "segmentos")

def leer_salida(proceso, etiqueta):
    for linea in proceso.stdout:
        print(f"[{etiqueta}] {linea.strip()}")

def main():
    # Iniciar el proceso de descarga de segmentos
    proceso_descargar = subprocess.Popen(["python", SCRIPT_DESCARGAR], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Esperar un poco para asegurarse de que haya al menos un segmento descargado antes de comenzar a transcribir
    time.sleep(70)  # Espera 70 segundos

    # Iniciar el proceso de transcripción
    proceso_transcribir = subprocess.Popen(["python", SCRIPT_TRANSCRIBIR], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Crear hilos para leer la salida de ambos procesos
    hilo_descargar = threading.Thread(target=leer_salida, args=(proceso_descargar, "DESCARGAR"))
    hilo_transcribir = threading.Thread(target=leer_salida, args=(proceso_transcribir, "TRANSCRIBIR"))

    # Iniciar hilos
    hilo_descargar.start()
    hilo_transcribir.start()

    # Esperar a que ambos hilos terminen
    hilo_descargar.join()
    hilo_transcribir.join()

    print("Ambos procesos han finalizado.")

if __name__ == "__main__":
    main()
