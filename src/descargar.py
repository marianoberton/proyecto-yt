import os
import time
import subprocess

URL = "https://youtu.be/QGpHLgRnrx4"
SEGMENT_DURATION = 300  # Duración de cada segmento en segundos (5 minutos)
OUTPUT_DIRECTORY = "segmentos"
DELAY = 30  # Retraso en segundos para comenzar el siguiente segmento

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

def capture_segment(segment_number):
    output_file = os.path.join(OUTPUT_DIRECTORY, f"transmision_{segment_number}.ts")
    cmd = [
        "streamlink",
        "--hls-live-restart",
        "--hls-duration", str(SEGMENT_DURATION),
        "-o", output_file,
        URL, "best"
    ]
    subprocess.run(cmd)

def main():
    segment_number = 0
    while True:
        print(f"Descargando segmento {segment_number}...")
        capture_segment(segment_number)
        segment_number += 1
        time.sleep(SEGMENT_DURATION - DELAY)  # Espera 5 minutos menos el retraso de 30 segundos

if __name__ == "__main__":
    main()
