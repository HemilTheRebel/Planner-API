class Task:
    def __init__(self, title, description, complete_before, is_completed=False, id=None):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.complete_before = complete_before
        self.id = id

    def is_valid(self):
        return len(self.title) > 0
