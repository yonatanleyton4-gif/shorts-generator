"""Compone una imagen fija y un audio en un video MP4 vertical 1080x1920."""
import subprocess
from pathlib import Path


def make_video(image_path: str, audio_path: str, out_path: str) -> str:
    """Crea un MP4 a partir de una imagen y un audio usando ffmpeg.

    - El video dura lo que dura el audio.
    - Fuerza 30 fps, formato yuv420p (compatible con todos los reproductores).
    """
    img = Path(image_path)
    aud = Path(audio_path)
    if not img.exists():
        raise FileNotFoundError(f"No existe la imagen: {image_path}")
    if not aud.exists():
        raise FileNotFoundError(f"No existe el audio: {audio_path}")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",                       # sobrescribir si existe
        "-loop", "1",               # imagen en bucle
        "-i", str(img),
        "-i", str(aud),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",                # corta al terminar el audio
        "-r", "30",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        str(out_path),
    ]

    # -loglevel error para que no llene la pantalla de logs
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg falló:\n{result.stderr}")
    return out_path


if __name__ == "__main__":
    out = make_video("output/test.png", "output/test.mp3", "output/test.mp4")
    print(f"Guardado en: {out}")
