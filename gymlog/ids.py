class IdGenerator:
    def __init__(self, prefix):
        self._prefix = prefix
        self._counter = 0

    def next_id(self):
        self._counter += 1
        return f"{self._prefix}-{self._counter:03d}"
