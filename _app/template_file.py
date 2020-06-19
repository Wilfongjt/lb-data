"""
#from __classes__.configuration import Configuration
#from configuration import Configuration
#from __classes__.application import Application
#from application import Application
from file import ListFile
from pathlib import Path
from util import Util

# pass template to app.Templatize(Template)
#from context_dict import ContextDict
from os.path import isfile, join
import os
from app_settings import AppSettingsTest


class TemplateFile(ListFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.lbtesting = os.getenv('LB-TESTING') or '0'
        if self.getFolderName() == None or self.lbtesting == '1':
            self.lbtesting = AppSettingsTest()
            #print('set folder')
            # default to source code resource, assume we are going to copy
            #self.setFolderName(AppSettingsTest().getFolder('temp-lates-folder'))

        # change config file name to template file name

        if filename != None and filename.endswith('.json'): # assume this a config file...chang name
            parts = filename.split('.')
            if len(parts) == 4:
                self.file_name = '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')
            '''    
            cnv_filename = filename.replace('.json','.tmpl')
            if Util().file_exists(foldername, cnv_filename):
                self.file_name = filename.replace('.json','.tmpl')
            else:
                tmpl_file_name = Util().getFileExtension(cnv_filename)
                self.file_name = tmpl_file_name
            '''

    def setFileName(self, filename):

        if filename.endswith('.json'):  # assume this a config file...chang name
            #print('B self.getFileName()', filename.replace('.json','.tmpl'))
            filename = filename.replace('.json', '.tmpl')
            if Util.file_exists(self.getFolderName(), filename ):
                filename = Util().getFileExtension(filename)
        super().setFileName(filename)
        return self

    def getFileExtension(self, filename):
        lst = filename.split('.')[1:]
        ext = '.'.join(lst)
        return ext

    def add(self, text_list):

        for line in text_list:
            self.append(line)
        return self

    def read(self):

        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())

        # check if filename exists
        #if not os.path.isfile(path_filename):
        #    path_filename = '{}/{}'.format(self.getFolderName(), self.getFileExtension(self.getFileName()))
        #print('path_filename',path_filename )
        if not Util().file_exists(self.getFolderName(), self.getFileName()):
            filelist = Util().getFileList(self.getFolderName())
            #print('self.getFolderName()', self.getFolderName())
            #print('filename', self.getFileName())
            raise FileNotFoundError('Template not found: {}'.format(path_filename))

        if not os.path.isfile(path_filename):
            raise FileNotFoundError('Template not found: {}'.format(path_filename))

        if len(self) > 0:
            raise FileNotFoundError('list already loaded')

        with open(path_filename) as f:
            for line in f:
                #self.lineList.append(line)
                #if 'VALUES' in line:
                #    print('rline', line)
                self.append(line)
                # need to read field templates from template_list
                # need tbl-fields from configuration_file ... add func to configureation to pull those... conf.getTemplateFile('tbl-fields')
        return self
    '''
    def delete(self):
        Util().deleteFile(self.getFolderName(), self.getFileName())
        return self
    '''




def crud_file_test(aFile, expected_file_name, expected_folder_name, expected_size ):
    # folder and filename
    #aFile = TemplateFile(folder, tmpl_name).append('A').append('B').append('C').write()
    print('  - CRUD File Test')
    print('    aFile', aFile)
    aFile.write()

    actual = aFile.getFileName()

    print('    -- create expected {}/{}'.format(expected_folder_name, expected_file_name))
    print('    -- create actual   {}/{}'.format(aFile.getFolderName(), aFile.getFileName()))

    # values
    print('expected', expected_file_name)
    print('actual', actual)
    assert(expected_file_name == actual )

    actual = aFile.getFolderName()
    assert(expected_folder_name == actual)

    print('    -- exists expected {}'.format(Util().file_exists(expected_folder_name, expected_file_name)))
    print('    -- exists actual   {}'.format(Util().file_exists(aFile.getFolderName(), aFile.getFileName())))
    # exists
    assert(Util().file_exists(expected_folder_name, expected_file_name))

    # read the ABC file

    aFile = TemplateFile(aFile.getFolderName(), aFile.getFileName()).read()

    print('    -- line count actual {} expected {}'.format(len(aFile), expected_size))
    assert(len(aFile)==expected_size)

    #aFile.delete()
    #assert(not Util().file_exists(expected_folder_name, expected_file_name))

def main():
    from pathlib import Path
    from util import Util
    #from template_file_create_database_mock import TemplateFileCreateDatabaseMock
    #from template_file_mocks import TemplateFileCreateTableMock, TemplateFileCreateDatabaseMock
    #from template_file_create_table_mock import TemplateFileCreateTableMock
    #from mockup_test_data import MockupData

    os.environ['LB-TESTING'] = '1'

    appSettings = AppSettingsTest().createFolders()
    # copy some files
    #MockupData().run()

    print('* TemplateFile')
    print('  - no tests available')
    '''
    # folder and full filename
    # Template should take full name e.g., ABC.db-api-table-table.pg.tmpl
    print('tmpl-folder', appSettings.getFolder('temp-lates-folder'))
    print('temp-folder', appSettings.getFolder('temp-folder'))

    lbenv = os.getenv('LB_ENV') or 'dev'
    lbproject_name = os.environ['LB_PROJECT_NAME'] or 'example'
    expected_file_name = 'credentials.db-api-table-table.pg.tmpl._DEP'
    expected_folder_name = '{}/..LyttleBit/testing/projects/{}-{}/templates'.format(appSettings.getHomeFolder(),lbproject_name, lbenv )
    #expected_folder_name = '{}/..LyttleBit/testing/temp'.format(appSettings.getHomeFolder() )
    
    expected_size = 3
    aFile = TemplateFile(expected_folder_name, expected_file_name).append('A').append('B').append('C')

    crud_file_test(aFile, expected_file_name, expected_folder_name, expected_size)

    # folder and full config file name
    # full name doesnt exist
    # when full template name not found switch to genralize template
    
    # folder and full config file name
    # full name exists
    # when full template file exists use it
    alt_file_name = 'credentials.db-api-table-table.pg.json._DEP'
    expected_file_name = 'credentials.db-api-table-table.pg.tmpl._DEP'
    #expected_folder_name = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder())
    expected_folder_name = '{}/..LyttleBit/testing/projects/{}-{}/templates'.format(appSettings.getHomeFolder(),lbproject_name, lbenv )
    #expected_folder_name = '{}/..LyttleBit/testing/temp'.format(appSettings.getHomeFolder() )

    expected_size = 3

    #TemplateFileCreateTableMock(filename=expected_file_name).write() # set up a file

    aFile = TemplateFile(expected_folder_name, alt_file_name).append('A').append('B').append('C')
    crud_file_test(aFile, expected_file_name, expected_folder_name, expected_size)
    '''
    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
"""