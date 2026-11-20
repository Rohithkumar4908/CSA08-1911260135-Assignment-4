"""festreg.reader: read department files, never stopping on a bad line."""


def read_department(path):
    """Yield (lineno, raw_line) for each non-empty line; missing file -> []."""
    try:
        with open(path, encoding="utf-8") as f:
            return [(n, line.rstrip("\n")) for n, line in enumerate(f, 1) if line.strip()]
    except FileNotFoundError:
        return None  # caller logs the missing file
