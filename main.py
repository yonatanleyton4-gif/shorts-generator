"""Orquestador principal de shorts-generator."""
import sys
from pathlib import Path

from combinator import load_phrases, make_pairs
from renderer import render
from voice import generate_voice
from video import make_video

OUTPUT_DIR = Path("output")


def generate_batch(n: int, seed: int | None = None) -> list[str]:
    """Genera N videos y devuelve la lista de rutas MP4 creadas."""
    frases = load_phrases()
    if len(frases) < 2:
        raise ValueError("Necesitas al menos 2 frases en frases.txt")

    pares = make_pairs(frases, n=n, seed=seed)
    if not pares:
        print("No se generaron pares. Revisa frases.txt.")
        return []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generados = []

    for i, par in enumerate(pares, start=1):
        num = f"{i:03d}"
        png = OUTPUT_DIR / f"img_{num}.png"
        mp3 = OUTPUT_DIR / f"voice_{num}.mp3"
        mp4 = OUTPUT_DIR / f"video_{num}.mp4"

        print(f"\n[{num}/{len(pares)}] Generando...")
        print(f"  A: {par[0]}")
        print(f"  B: {par[1]}")

        render(par, str(png))
        print(f"  ✅ Imagen: {png}")

        texto = f"{par[0]} {par[1]}"
        generate_voice(texto, str(mp3))
        print(f"  ✅ Audio:  {mp3}")

        make_video(str(png), str(mp3), str(mp4))
        print(f"  ✅ Video:  {mp4}")

        generados.append(str(mp4))

    return generados


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(f"Generando {n} short(s)...\n")
    videos = generate_batch(n)
    print(f"\n🎉 Listo. {len(videos)} video(s) generados:")
    for v in videos:
        print(f"  - {v}")
