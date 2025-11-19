def coord_to_label(x: int, y: int) -> str:
    """Преобразует координаты массива (x, y) в формат 'A1'... 'G7'."""
    column = chr(ord('A') + x)
    row = y + 1
    return f"{column}{row}"
