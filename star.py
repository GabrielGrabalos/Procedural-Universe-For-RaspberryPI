class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = (x << 16) | y

    def _xorshift32(self):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >> 17) & 0xFFFFFFFF
        self.state ^= (self.state << 5) & 0xFFFFFFFF
        return self.state & 0xFFFFFFFF