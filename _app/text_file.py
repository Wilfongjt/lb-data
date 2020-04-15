from file import FileAsList

class TextFile(FileAsList):
    def __init__(self, folder, filename):
        super().__init__(folder, filename)
