# utils.py
# Small helpers (not used heavily in minimal demo)
def chunk_text(s, limit=4000):
    # Telegram message limit ~4096; naive chunker
    parts = []
    while s:
        parts.append(s[:limit])
        s = s[limit:]
    return parts
