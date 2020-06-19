
import json
import os.path
from pathlib import Path
from util import Util
#from __classes__.application import Application
from file import FileAsDict
from app_settings import AppSettings, AppSettingsTest
#from crud import CRUD
from text_file import TextFile


class ConfigurationDict(FileAsDict):
    '''
    loads a single configuration file from the projects/project/config folder
    '''
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.LB = True # ad env taht start with LB
        self.appSettings = AppSettings()

        self.lbtesting = os.getenv('LB-TESTING') or '0'
        self.appSettings = AppSettings()

        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
            # default to source code resource, assume we are going to copy
            if foldername == None:
                self.setFolderName(self.appSettings.getFolder('con-fig-folder'))
        #self.fixEnv()

    def setLB(self, tf):
        self.LB = tf
        return self

    def dep_fixEnv(self):
        #self['LB_DB_PREFIX'] = self.appSettings.lbdb_prefix or 'NA'
        self['LB_DB_PREFIX'] = self.appSettings.lbdb_prefix or 'NA'
        self['db-api-table-type'] = self.appSettings.lbdb_type or 'NA'
        self['db-api-table-type-abbr'] = self.appSettings.lbdb_type_abbr or 'NA'
        self['app-name'] = self.appSettings.lb_project['name']
        # collect env vars
        '''
        for v in os.environ:
            if v.startswith('LB_'):
                #print('STEP',v,os.getenv(v))
                self[v] = os.getenv(v)
        '''
    def getTemplateFileName(self, tmpl_folder, find_ext='.json', repl_ext='.compiled'):
        '''
        get correct template file to match config file
        :param tmpl_folder:
        :return:
        '''
        tmpl_file_name = self.getFileName().replace(find_ext, repl_ext)
        #tmpl_file_name = self.getFileName().replace('.tmpl', '.compiled')

        if not Util().file_exists(tmpl_folder, tmpl_file_name):
            tmpl_file_name = Util().getFileExtension(tmpl_file_name)

        return tmpl_file_name

    #def add(self, key , value):
    #    self[key]= value
    #    return self

    def add(self, dictionary):
        '''
        added for testing
        '''
        for key in dictionary:
            #self[key]=self.expand(key, dictionary[key])
            self[key] = dictionary[key]
            #print('add key', key)
        return self

    def read(self):
        #super().read()
        #self.__include() # read variales from a file if configured
        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
        #print('path_filename', path_filename)
        with open(path_filename) as json_file:
            #print('cfile', path_filename)
            configuration_dict = json.load(json_file)
        # copy to the dic
        #for key in configuration_dict:
        #    self[key] = configuration_dict[key]
        self.add(configuration_dict)

        #self.fixEnv()

        return self

    def _include(self, includePathAndFileName):

        #includePathAndFileName = '{}/{}'.format(self.appSettings.getFolder('con-fig-folder'), includePathAndFileName.replace('./', ''))
        includePathAndFileName = '{}/{}'.format(self.getFolderName(), includePathAndFileName.replace('./', ''))

        if not os.path.exists(includePathAndFileName):
            raise NameError('Include defined but file is not found', includePathAndFileName)
            #print('Include defined but file is not found', includePathAndFileName)

        includejson = {}
        with open(includePathAndFileName) as json_file:
            includejson = json.load(json_file)

        for item in includejson:
            if item != 'type':
                self[item] = includejson[item]
        # environment
        '''
        for v in os.environ:
            if self.LB and v.startswith('LB'):
                self[v] = os.environ[v]
        '''
    def delete(self):
        Util().deleteFile(self.getFolderName(), self.getFileName())
        return self

    def copy(self, folder, filename, noLB=False):
        '''
        overloads super().copy
        remove any keys containing 'LB_'
        :param folder:
        :param filename:
        :return:
        '''
        #print('C copy {} {} {}'.format(self.getClassName(), folder, filename))

        path_filename = '{}/{}'.format(folder, filename)

        with open(path_filename, 'w') as json_file:
            # remove keys starting with LB
            data = {}
            for key in self:
                if key.startswith('LB_'):
                    # dont overwrite source folder

                    if self.getFolderName() != folder:
                        data[key] = self[key]
                else:
                    data[key]=self[key]

            configuration_dict = json.dump(data, json_file)

        return self

    #def getDictionary(self):
    #    return self.configuration_dict

def test_config():
    appSettings = AppSettingsTest()
    folder = appSettings.getResourceFolder('config')
    ofolder = appSettings.getFolder('temp-folder')
    print('  - config-folder', folder)

    print('  - temp-folder', ofolder)

    #filelist = Util().getFileList(folder, ext='db-api-table-table.pg.json')
    filelist = Util().getFileList(folder)

    for fn in filelist:
        tableConfigFile = ConfigurationDict(folder, fn).read()
        print('  - config file', tableConfigFile.getFileName(), tableConfigFile)

        # print('tableConfigFile', tableConfigFile)
        assert(len(tableConfigFile)>0 )
        assert('type' in tableConfigFile)
        assert(tableConfigFile['type'] in ['table',
                                           'database',
                                           'role',
                                           'function',
                                           'table-api-insert',
                                           'table-api-update',
                                           'table-api-select',
                                           'table-api-delete',
                                           'docker-compose',
                                           'dockerfile',
                                           'test',
                                           'script'])
        tableConfigFile.copy(ofolder, fn)


def main():
    from pathlib import Path
    from util import Util
    from test_func import test_table
    from pprint import pprint

    os.environ['LB-TESTING']='1'

    appSettings = AppSettingsTest()\
        .createFolders()
    # make some data
    #MockupData().run()

    print('* ConfigurationDict')
    test_config()
    confFile = ConfigurationDict().add(test_table())
    pprint(confFile)
    # ConfigurationAPI
    #print('* ConfigurationApi')
    #test_api('insert')
    #test_api('select')
    #test_api('update')

    # clean up

    #appSettings.removeFolders()
    os.environ['LB-TESTING']='0'

if __name__ == "__main__":
    main()