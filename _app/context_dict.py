import json
import os.path
#from copy_file import CopyFile
from file import FileAsDict
from app_settings import AppSettings, AppSettingsTest

class ContextDict(FileAsDict):
    def __init__(self, foldername=None, filename='context.template.list.json'):
        super().__init__(foldername, filename)

        self.tagid='templates'
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        self.appSettings = AppSettings()
        self.setFolderName(self.appSettings.getFolder('shared-folder'))
        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
            # default to source code resource, assume we are going to copy
            self.setFolderName(self.appSettings.getResourceFolder('shared'))

    def read(self):

        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())

        if not os.path.exists(path_filename):
            raise NameError('Missing file: {}'.format( path_filename))

        with open(path_filename) as json_file:
            contextDict= json.load(json_file)

        for key in contextDict:
            self[key] = contextDict[key]

        return self

    #def getDictionary(self):
    #    return self.templatesDict

    def getTemplate(self, key):
        val = None
        if key in self:
            val = self[key]
        return val

def main():
    os.environ['LB-TESTING'] = '1'
    #from app_settings import AppSettingsTest()
    print('* Test ContextDict')
    res_folder = AppSettingsTest().getResourceFolder('shared')
    #shared_folder = AppSettings().getFolder('shared-folder')
    temp_folder = AppSettingsTest().getFolder('temp-folder')

    #AppSettings().createAppFolders(temp_folder)
    #AppSettings().createFolders(temp_folder)
    AppSettingsTest().createFolders()


    #contextDict =  ContextDict(res_folder).read()
    contextDict = ContextDict().read()

    assert len(contextDict) > 0

    assert contextDict.getTemplate('active') == "[[tbl-prefix]]_active BOOLEAN NOT NULL DEFAULT true"

    AppSettingsTest().removeFolders()
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()