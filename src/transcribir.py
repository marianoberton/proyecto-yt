import os
import time
import subprocess

RUTA_SEGMENTOS = os.path.join(os.getcwd(), "data", "segmentos")

def convertir_a_mp3(archivo_ts, archivo_mp3):
    cmd = [
        "ffmpeg",
        "-i", archivo_ts,
        "-q:a", "0",  # Calidad máxima
        "-map", "a",
        archivo_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def transcribir_whisper(archivo_mp3):
    cmd = [
        "whisper",
        archivo_mp3
    ]
    try:
        resultado = subprocess.check_output(cmd).decode('utf-8').strip()
    except UnicodeDecodeError:
        resultado = subprocess.check_output(cmd).decode('latin1').strip()
    return resultado

def procesar_transcribir(segmento_num):
    nombre_segmento = f"{RUTA_SEGMENTOS}transmision_{segmento_num}.ts"
    nombre_mp3 = f"{RUTA_SEGMENTOS}transmision_{segmento_num}.mp3"
    if os.path.exists(nombre_segmento):
        # Convierte el segmento a MP3
        convertir_a_mp3(nombre_segmento, nombre_mp3)
        
        # Usa Whisper para transcribir el MP3
        transcripcion = transcribir_whisper(nombre_mp3)
        with open(f"{RUTA_SEGMENTOS}transcripcion_{segmento_num}.txt", "w", encoding="utf-8") as f:
            f.write(transcripcion)
        print(f"Transcripción del segmento {segmento_num} guardada.")

def main():
    segmento_num = 0
    while True:
        if f"transmision_{segmento_num}.ts" in os.listdir(RUTA_SEGMENTOS):
            procesar_transcribir(segmento_num)
            segmento_num += 1
        time.sleep(10)  # Espera 10 segundos antes de verificar nuevamente

if __name__ == "__main__":
    main()
