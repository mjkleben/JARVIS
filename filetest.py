class Language:
    def __init__(self):
        self.language = 'en-US'

    def __str__(self):
        return self.language

    def change(self, lang):
        assert isinstance(lang, str)
        self.language = lang

language = Language()