"""Renderiza un par de frases como imagen vertical 1080x1920."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (15, 15, 18)          # casi negro
FG = (245, 245, 245)        # blanco roto
ACCENT = (255, 200, 60)     # amarillo para el separador

FONT_PATH = "font.ttf"
PADDING = 100               # margen interno
MAX_FONT_SIZE = 90
MIN_FONT_SIZE = 55


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Parte el texto en líneas que caben en max_w."""
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = f"{current} {w}".strip()
        if draw.textlength(test, font=font) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _fit_text(draw, phrase_a: str, phrase_b: str) -> tuple[ImageFont.FreeTypeFont, list[str], list[str]]:
    """Baja el tamaño de fuente hasta que ambas frases quepan con márgenes."""
    max_w = W - 2 * PADDING
    for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -2):
        font = ImageFont.truetype(FONT_PATH, size)
        lines_a = _wrap(draw, phrase_a, font, max_w)
        lines_b = _wrap(draw, phrase_b, font, max_w)
        line_h = size + 12
        total_h = (len(lines_a) + len(lines_b)) * line_h + size * 2  # separador + aire
        if total_h <= H - 2 * PADDING:
            return font, lines_a, lines_b
    # fallback: el más chico posible
    font = ImageFont.truetype(FONT_PATH, MIN_FONT_SIZE)
    return font, _wrap(draw, phrase_a, font, max_w), _wrap(draw, phrase_b, font, max_w)


def render(pair: tuple[str, str], out_path: str) -> str:
    """Renderiza el par y guarda la imagen. Devuelve la ruta de salida."""
    phrase_a, phrase_b = pair
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    font, lines_a, lines_b = _fit_text(draw, phrase_a, phrase_b)
    line_h = font.size + 12
    sep_h = font.size            # espacio del separador
    block_h = len(lines_a) * line_h + sep_h + len(lines_b) * line_h
    y = (H - block_h) // 2

    def draw_lines(lines, y_start):
        for line in lines:
            w = draw.textlength(line, font=font)
            x = (W - w) // 2
            draw.text((x, y_start), line, font=font, fill=FG)
            y_start += line_h
        return y_start

    y = draw_lines(lines_a, y)

    # separador: línea corta centrada
    sep_w = 120
    sep_y = y + sep_h // 2
    draw.rectangle(
        [(W - sep_w) // 2, sep_y, (W + sep_w) // 2, sep_y + 6],
        fill=ACCENT,
    )
    y += sep_h

    draw_lines(lines_b, y)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    from combinator import load_phrases, make_pairs

    ps = load_phrases()
    pair = make_pairs(ps, n=1, seed=42)[0]
    out = render(pair, "output/test.png")
    print(f"Guardado en: {out}")
    print(f"Frase A: {pair[0]}")
    print(f"Frase B: {pair[1]}")
