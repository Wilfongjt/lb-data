
class ResourceName():
    '''
    stores a folder and file names
    '''
    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name
        if folder_name == None:
            raise Exception('ResourceName folder_name is undefined.')

        if file_name == None:
            raise Exception('ResourceName file_name is undefined.')

    def getFolder(self):
        return self.folder_name

    def getFileName(self):
        return self.file_name

    def getResourceName(self):
        return '{}/{}'.format(self.getFolder(), self.getFileName())

    def exists(self):
        exists = os.path.isfile(self.getResourceName())
        return exists
