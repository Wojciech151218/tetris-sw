class Timer:
    def __init__(self, limit: int = 10):
        self.timer = 0
        self.limit = limit


    def increment(self):
        self.timer += 1
        if self.timer >= self.limit:
            self.timer = 0
            return True
        return False

    def set_limit(self, limit):
        self.limit = limit

    def reset(self):
        self.timer = 0