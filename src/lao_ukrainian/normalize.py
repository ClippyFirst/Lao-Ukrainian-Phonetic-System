import unicodedata

def normalize_lao(text: str) -> str:
    return unicodedata.normalize("NFC", text)

def validate_unicode(text: str) -> list[str]:
    problems=[]
    for ch in text:
        cp=ord(ch)
        if cp < 0x20 and ch not in "\n\t":
            problems.append(f"control character U+{cp:04X}")
        if 0x0E80 <= cp <= 0x0EFF:
            continue
        if ch.isspace() or (ch.isascii() and (ch.isalnum() or ch in "-'.")):
            continue
        if cp > 0x7F:
            problems.append(f"unsupported non-Lao character U+{cp:04X} {ch}")
    return problems
