"""Lee frases y genera combinaciones únicas de pares."""
from itertools import combinations
from pathlib import Path


def load_phrases(path: str = "frases.txt") -> list[str]:
    """Lee frases.txt, una frase por línea. Ignora líneas vacías."""
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"No existe {path}")
    phrases = [line.strip() for line in file.read_text(encoding="utf-8").splitlines()]
    return [p for p in phrases if p]


def make_pairs(phrases: list[str], n: int, seed: int | None = None) -> list[tuple[str, str]]:
    """Devuelve hasta n pares únicos (sin orden interno, sin repetir el mismo par).

    combinations garantiza que (a,b) == (b,a): no aparecen duplicados invertidos.
    """
    if n <= 0:
        return []
    all_pairs = list(combinations(phrases, 2))
    if seed is not None:
        import random
        random.Random(seed).shuffle(all_pairs)
    return all_pairs[:n]


if __name__ == "__main__":
    frases = load_phrases()
    print(f"Frases cargadas: {len(frases)}")
    pares = make_pairs(frases, n=5, seed=42)
    print(f"Pares generados: {len(pares)}")
    for i, (a, b) in enumerate(pares, 1):
        print(f"  {i}. {a}  +  {b}")
