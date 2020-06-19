import sys
print(sys.path)
import os
from pathlib import Path
import settings


print('os.getenv', os.getenv('LB_WORKING_FOLDER_NAME'))
print('change projects in .env')
import os
from util import Util
from app_settings import AppSettings, AppSettingsTest
from text_file import TextFile
from pprint import pprint
from configuration_file import ConfigurationDict
from configuration_interface import InterfaceConfiguration

class MakeList(dict):
    def __init__(self):
        self.appSettings = AppSettings()
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
        #
        self.type_map = {
            'database': {'prefix': '01', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'role': {'prefix': '03', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'validate-function': {'prefix': '04', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'table': {'prefix': '05', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'function': {'prefix': '07', 'ext': 'sql', 'folder-key': 'sql-folder'},

            #'table-api-upsert': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'interface-upsert': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'interface-select': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'interface-test': {'prefix': '99', 'ext': 'sql', 'folder-key': 'sql-folder'},

            #'table-api-insert': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            #'table-api-update': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            #'table-api-select': {'prefix': '09', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'initialize': {'prefix': '11', 'ext': 'sql', 'folder-key': 'sql-folder'},
            'test': {'prefix': '99', 'ext': 'sql', 'folder-key': 'sql-folder'},

            'script-sh': {'prefix': '13', 'ext': 'sh', 'folder-key': 'script-folder'},

            'dockerfile-admin': {'prefix': '15', 'ext': '', 'folder-key': 'admin-folder'},
            'dockerfile-db': {'prefix': '15', 'ext': '', 'folder-key': 'db-folder'},
            'dockerfile-web': {'prefix': '15', 'ext': '', 'folder-key': 'web-folder'},
            'docker-compose': {'prefix': '17', 'ext': 'yml', 'folder-key': 'code-folder'},

            'environment': {'prefix': '19', 'ext': 'env', 'folder-key': 'web-folder'},
        }
        self.process()

    def process(self):
        #print('process')
        folder_list = Util().getFolderList(self.appSettings.getResourceFolder('config'))
        #pprint(folder_list)
        for folder in folder_list:  # get all the sub folders in the resource folder
            print('folder', folder)
            for filename in Util().getFileList(folder, ext='json'):  # open all the template files
                #print('folder', folder)

                self[self.toKey(filename)] = {'class-name':    self.getClassName(filename),
                                              'conf-folder':   folder,
                                              'conf-filename': filename,
                                              'tmpl-folder':   self.toTmplFolder(folder),
                                              'tmpl-filename': self.toTmpl(folder, filename),
                                              'out-filename':  self.toOutput(filename),
                                              'out-folder':    self.getOutFolder(filename)}
        return self

    def getOutFolder(self, filename):
        rc = 'fix me'
        parts = filename.split('.')
        #print('parts', parts)
        rc = self.appSettings.getFolder(self.type_map[parts[1]]['folder-key'])
        return rc

    def getNameOrder(self, filename):
        parts = filename.split('.')
        #print('parts', parts)
        return self.type_map[parts[1]]['prefix']

    def getExt(self, filename):
        parts = filename.split('.')
        return self.type_map[parts[1]]['ext']

    def toOutput(self, file_name):
        rc = ''
        parts = file_name.split('.')
        #print('parts', parts)
        ext = self.getExt(file_name)
        if ext == 'sql':
            rc = '{}.{}.{}.{}.{}'.format(self.getNameOrder(file_name), parts[0],parts[1], parts[2],self.getExt(file_name))
        elif ext == 'sh':
            rc = '{}.{}'.format(parts[0], ext)
        elif ext == 'env':
            rc = '{}'.format(ext)
        elif ext == 'yml':
            rc = '{}.{}'.format(parts[0], ext)
        else:  # ext == '':
            rc = '{}'.format(parts[0])
        return rc

    def toKey(self, file_name ):
        parts = file_name.split('.')
        return '{}.{}.{}'.format(parts[0],parts[1], parts[2])

    def toTmplFolder(self, folder):
        return folder.replace('config','templates')

    def toTmpl(self,folder, file_name):
        rc = ''
        #print('toTmpl', file_name)
        parts = file_name.split('.')
        #print('parts', parts)

        fullname = '{}.{}.{}.{}'.format(parts[0],parts[1], parts[2], 'tmpl')
        partname = '{}.{}.{}'.format(parts[1], parts[2], 'tmpl')

        if Util().file_exists(self.toTmplFolder(folder), fullname):
            rc = fullname
        elif Util().file_exists(self.toTmplFolder(folder), partname):
            rc = partname
        else:
            raise Exception('Missing template name {} and/or {} in {}'.format(fullname, partname, self.toTmplFolder(folder)))
        return rc


    def getClassName(self, file_name):
        rc = []

        parts = [p for p in file_name.split('.')]
        parts = [p.split('-') for p in parts]

        for wl in parts:
            for w in wl:
                rc.append(w.capitalize())
        return 'Template_{}'.format(''.join(rc))

class MakeAPIConfigurations():
    def __init__(self):
        self.appSettings = AppSettings()
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
        self.process()

    def process(self):
        folder_list = Util().getFolderList(self.appSettings.getResourceFolder('config'))
        for folder in folder_list:  # get all the sub folders in the resource folder
            for filename in Util().getFileList(folder, ext='json'):  # open all the template files
                parts = filename.split('.')
                if len(parts) == 4:
                    if parts[1]=='table': # this is table configuration
                        # out_folder_list = '{}/db-api'.format(self.appSettings.getResourceFolder('config'))
                        confFile = ConfigurationDict(folder, filename).read()
                        for interface in confFile['interfaces']:
                            interfaceConfiguration = InterfaceConfiguration(interface).load(confFile)
                            for m in confFile['interfaces'][interface]['methods']:
                                out_folder_list = '{}/db-api'.format(self.appSettings.getResourceFolder('config'))
                                interfaceConfiguration['type']='interface'
                                interfaceConfiguration.copy(out_folder_list,self.toAPI(filename,interface, m))
                                if m == 'upsert':
                                    out_folder_list = '{}/db-initialize'.format(self.appSettings.getResourceFolder('config'))
                                    interfaceConfiguration.copy(out_folder_list, self.toInitialize(filename, interface, m))
        return self

    def toAPI(self, filename, interface, method):
        parts = filename.split('.')
        return '{}.{}.{}.{}'.format('{}-{}'.format(parts[0],interface), 'interface-{}'.format(method), parts[2], 'json')

    def toInitialize(self, filename, interface, method):
        parts = filename.split('.')
        return '{}.{}.{}.{}'.format('{}-{}'.format(parts[0],interface), 'initialize', parts[2], 'json')
        #return '{}.{}.{}.{}'.format('{}-{}'.format(parts[0], interface), 'initialize-{}'.format(method), parts[2], 'json')


def showFolders():
    print('---- FOLDERS ----')
    appSettings = AppSettingsTest()
    print('* working-folder', appSettings.getFolder('working-folder'))
    print('* getProjectFolders')
    pprint(appSettings.getProjectFolders())


def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    #pprint(MakeList())

    appSettings = AppSettingsTest()

    # out_file = TextFile(appSettings.getAppFolder(), '00.templates_gen.py')
    print('cwd', os.getcwd())
    out_file = TextFile(os.getcwd(), '00.templates_gen.py')

    out_file.append('import sys')
    out_file.append('print(sys.path)')
    out_file.append('import os')
    out_file.append('from pathlib import Path')
    out_file.append('import settings')

    out_file.append('print(\'os.getenv\', os.getenv(\'LB_WORKING_FOLDER_NAME\'))')
    out_file.append('print(\'change projects in .env\')')
    out_file.append('from templates import Template')
    out_file.append('from app_settings import AppSettings, AppSettingsTest')

    progeny = MakeAPIConfigurations() # gen api json files

    makeList = MakeList()

    print('---- MakeList ---- ')
    pprint(makeList)

    #pprint([makeList[f]['out-filename'] for f in makeList])

    class_list = []

    for _key in makeList:
        #print('key', _key)
        #class_list.append(self.getClassName(filename))
        tmpl_file = TextFile(makeList[_key]['tmpl-folder'], makeList[_key]['tmpl-filename']).read()

        conf_file = TextFile(makeList[_key]['conf-folder'], makeList[_key]['conf-filename']).read()
        #print('key', _key, makeList[_key]['class-name'])
        class_list.append(makeList[_key]['class-name']) # use later

        out_file.append(' ')

        out_file.append('class {}(Template):'.format(makeList[_key]['class-name']))
        out_file.append(' ')
        out_file.append('    def __init__(self):')
        out_file.append('        super().__init__({})')
        out_file.append(' ')
        out_file.append('    def process(self):')
        out_file.append('        super().process()')
        out_file.append('        print(\'{}\'.format(\'\\n\'.join(self)))')
        out_file.append('        self.copy(self.getOutputFolder(), self.getOutputName())')

        out_file.append('        return self')
        out_file.append(' ')
        #out_file.append('    def getInputTemplate(self): return \'{}\''.format(makeList[_key]['conf-filename']))

        out_file.append('    def getInputTemplate(self): return \'{}\''.format(makeList[_key]['tmpl-filename']))

        #out_file.append('    def getTemplateSourceName(self): return \'{}\''.format(makeList[_key]['tmpl-filename']))
        out_file.append('    def getOutputFolder(self): return \'{}\''.format(makeList[_key]['out-folder']))
        out_file.append('    def getOutputName(self): return \'{}\''.format(makeList[_key]['out-filename']))
        #out_file.append('    def getOutputFileName(self): return \'{}/{}\''.format(makeList[_key]['out-folder'], makeList[_key]['out-filename']))

        out_file.append('    def getTemplateList(self):')
        out_file.append('        return \'\'\'')
        for ln in tmpl_file: # add lines from template
            out_file.append(ln)

        out_file.append('\'\'\'.split(\'\\n\')')
        out_file.append(' ')

        out_file.append('    def getDictionary(self):')
        out_file.append('        return \\')

        for ln in conf_file: # add lines from template
            out_file.append('\t\t\t{}'.format(ln))

        out_file.append('        ')
        out_file.append('##########')
        out_file.append('##########')
        out_file.append('##########')

    out_file.append('def main():')
    # out_file.append('    if self.lbtesting = os.getenv(\'LB-TESTING\') or \'0\'')
    out_file.append('    appSettings = AppSettings()')
    out_file.append('    if \'LB-TESTING\' in os.environ:')
    out_file.append('        appSettings = AppSettingsTest()')
    for class_name in class_list:
        out_file.append('    {}()'.format(class_name))

    out_file.append('if __name__ == "__main__":')
    out_file.append('    main()')

    out_file.write()
    print('output to ' , out_file.getFolderName(), out_file.getFileName())
    #showFolders()

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()