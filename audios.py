from pytube import YouTube
from pydub import AudioSegment
import os
import math

def descargar_audio_youtube(url, carpeta_salida='audios', nombre_base='audio'):
    # Crear carpeta de salida si no existe
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Descargar audio
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    archivo_mp4 = audio_stream.download(output_path=carpeta_salida, filename=nombre_base + '.mp4')
    
    # Convertir a WAV
    archivo_wav = os.path.join(carpeta_salida, nombre_base + '.wav')
    audio = AudioSegment.from_file(archivo_mp4)
    audio.export(archivo_wav, format="wav")
    
    print(f"Audio descargado y convertido: {archivo_wav}")
    return archivo_wav

def segmentar_audio(archivo_wav, duracion_segmento=2*60*1000):  # 2 minutos en milisegundos
    audio = AudioSegment.from_wav(archivo_wav)
    duracion_total = len(audio)
    num_segmentos = math.ceil(duracion_total / duracion_segmento)
    
    nombre_base = os.path.splitext(archivo_wav)[0]
    
    for i in range(num_segmentos):
        inicio = i * duracion_segmento
        fin = min((i + 1) * duracion_segmento, duracion_total)
        segmento = audio[inicio:fin]
        nombre_segmento = f"{nombre_base}_part{i+1}.wav"
        segmento.export(nombre_segmento, format="wav")
        print(f"Segmento guardado: {nombre_segmento}")

# --- USO ---
url_video = "https://www.youtube.com/watch?v=VIDEO_ID"  # Reemplaza con tu URL
archivo = descargar_audio_youtube(url_video)
segmentar_audio(archivo)
