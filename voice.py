"""Genera audio MP3 a partir de texto usando edge-tts (gratis, sin API key)."""
import asyncio
from pathlib import Path

import edge_tts

# Voz por defecto: colombiana femenina. Cambia si prefieres otra.
DEFAULT_VOICE = "es-CO-SalomeNeural"
DEFAULT_RATE = "+0%"   # velocidad normal. Ej: "+10%" más rápido, "-10%" más lento


async def _generate(text: str, voice: str, rate: str, out_path: str) -> str:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(out_path)
    return out_path


def generate_voice(text: str, out_path: str, voice: str = DEFAULT_VOICE, rate: str = DEFAULT_RATE) -> str:
    """Genera un MP3 con el texto dado. Devuelve la ruta de salida.

    Uso:
        generate_voice("Hola mundo", "output/voice.mp3")
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_generate(text, voice, rate, out_path))
    return out_path


if __name__ == "__main__":
    from combinator import load_phrases, make_pairs

    ps = load_phrases()
    pair = make_pairs(ps, n=1, seed=42)[0]
    # Unimos las dos frases con un punto para que haya pausa natural
    texto = f"{pair[0]} {pair[1]}"
    out = generate_voice(texto, "output/test.mp3")
    print(f"Guardado en: {out}")
    print(f"Texto: {texto}")
    
