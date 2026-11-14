# Shorts Generator 🎬

Generador automático de videos verticales (1080x1920) para Shorts, Reels y TikTok.

Toma pares de frases de `frases.txt`, genera una imagen con Pillow, un audio con `edge-tts` (gratis, sin API key) y compone el MP4 final con `ffmpeg`.

## Requisitos

- Python 3.10+
- `ffmpeg` instalado en el sistema
- Fuente `Montserrat-Bold.ttf` (renombrada a `font.ttf` en la raíz del proyecto)

En Debian/Ubuntu:

```bash
sudo apt install python3 python3-pip python3-venv ffmpeg fonts-montserrat
cp /usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf ./font.ttf
