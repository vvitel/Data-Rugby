class VideoCacheManager:

    def __init__(self):
        self.cache = {}

    def get(self, date, match, frame):
        key = (date, match)
        if key in self.cache:
            cached = self.cache[key]
            if frame < cached["start"] or frame >= cached["end"]:
                return cached
        return None

    def set(self, date, match, start, end, players):
        key = (date, match)
        self.cache[key] = {
            "start": start,
            "end": end,
            "players": players,
        }
        return self.cache[key]

    def clear_key(self, date, match):
        key = (date, match)
        if key in self.cache:
            del self.cache[key]
