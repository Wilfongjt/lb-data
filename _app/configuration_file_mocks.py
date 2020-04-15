
from configuration_file import ConfigurationDict
from app_settings import AppSettingsTest, AppSettings
import os
from util import Util
'''
class ConfigurationFileMock(FileAsDict):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        # read from code folders

        self.appSettings = AppSettingsTest()

        if foldername == None:
            self.setFolderName(self.appSettings.getFolder('con-fig-folder'))

    def write(self):
        # write to examples
        self.copy(
            AppSettingsTest().getFolder('temp-lates-folder'),
            self.getFileName())
        return self

    def mockup(self):
        print('READ', self.getFolderName())
        self.read()
        self.write()
        return self
'''
'''
class ConfigurationMockups():
    def mockups(self):
        #os.environ['LB-TESTING'] = '1'
        appSettings = AppSettingsTest()
        filelist = Util().getFileList(appSettings.getResourceFolder('config'))
        print('filelist', filelist)
        #folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder())

        for fn in filelist:
            print('A filename ', fn)
            #if '.DS_Store' not in fn:
                #ConfigurationFileMock(appSettings.getResourceFolder('config'), fn) \
                #    .mockup()

'''
'''
class ConfigurationDictFileDatabaseMock(ConfigurationDict):
    
    #loads a single configuration file from the projects/project/config folder
    
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = self.appSettings.getFolder('con-fig-folder')
        self.setFileName('db-api-table.database.pg.json')
        self.setFolderName(self.default_folder)

        self.add(
            {"type": "database",
             "db-prefix": "mock",
             "db-api-table-type": "postgres",
             "db-api-table-type-abbr": "pg",
             "extensions": [
                 "pgcrypto",
                 "pgtap",
                 "pgjwt"
             ]
             }
            )
'''
'''
class ConfigurationDictFileTableMock(ConfigurationDict):
    
    #loads a single configuration file from the projects/project/config folder
    
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = self.appSettings.getFolder('con-fig-folder')

        self.setFileName('mock.db-api-table-table.pg.json')
        self.setFolderName(self.default_folder)

        self.add({
            "type": "db-api-table-table",
            "include": "./db-api-table.database.pg.json",
            "tbl-name": "mock",
            "tbl-prefix": "mck",
            "api-name": "user",
            "fields": [
                {"name": "id", "context": "pk", "type": "INTEGER", "crud": "r"},
                {"name": "firstname", "context": "name", "type": "TEXT", "crud": "cur"},
                {"name": "lastname", "context": "name", "type": "TEXT", "crud": "cur"},
                {"name": "created", "context": "created", "type": "timestamp", "crud": "r"},
                {"name": "updated", "context": "updated", "type": "timestamp", "crud": "r"},
                {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ur"}
            ],
            "api-methods": ["insert", "select", "update"],
            "tbl-role": "guest"
        })
'''

def main():
    import os
    from util import Util
    from app_settings import AppSettingsTest

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    '''
    ####################################################
    # write a junk file to temp folder
    aFile = ConfigurationDictFileDatabaseMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/config'.format(appSettings.getHomeFolder(), )
    file = 'db-api-table.database.pg.json'

    assert(Util().folder_exists(folder))
    assert(Util().file_exists(folder, file))

    ####################################################
    aFile = ConfigurationDictFileTableMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/config'.format(appSettings.getHomeFolder(), )
    file = 'mock.db-api-table-table.pg.json'

    assert (Util().folder_exists(folder))
    assert (Util().file_exists(folder, file))
    '''

    appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'


    # ConfigurationDictFileDatabaseMock().write()
    # ConfigurationDictFileTableMock().write()

if __name__ == "__main__":
    main()