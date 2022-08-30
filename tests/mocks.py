class MockChannel:
    def __init__(self):
        self.id = 1000


class MockAuthor:
    def __init__(self):
        self.id = 2000


class MockMessage:
    def __init__(self, content):
        self.content = content
        self.channel = MockChannel()
        self.author = MockAuthor()
