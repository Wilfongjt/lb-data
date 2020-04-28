
'''
from configuration_file import ConfigurationDictFileDatabaseMock, ConfigurationDictFileTableMock
from template_file import TemplateFile, TemplateFileCreateTableMock, TemplateFileCreateDatabaseMock,TemplateFileTableAPIInsertMock
from util import Util
from pathlib import Path
from copy_file import CopyFile


def main():
    # temp_folder = '{}/'.format(str(Path.home()), )
    source_folder = CopyFile().getResourceFolder(child_folder='templates')
    class_folder = CopyFile().getClassFolder()
    dev_folder = CopyFile().getDevFolder()

    print('temp_folder', source_folder)
    print('class_folder', class_folder)
    print('dev_folder',dev_folder)

    print('setup mockups')
    # store testing copies in temp/ folder

    file_list = Util().getFileList(source_folder, '.tmpl')
    file_list.sort()
    class_list = []
    #print('file_list', file_list)

    mockups_file_name = 'mockups.py'
    Util().deleteFile(class_folder, mockups_file_name)
    mockupsFile = TemplateFile(class_folder, mockups_file_name)
    mockupsFile.append('from pathlib import Path')
    mockupsFile.append('from template_file import TemplateFile')

    for filename in file_list:
        tempFile = TemplateFile(source_folder, filename).read()

        mockupsFile.append('# file: {}'.format( filename))
        mockupsFile.append('class TemplateFile{}Mock(TemplateFile):'.format(Util().toClassName(filename)))
        cl = ' TemplateFile{}Mock'.format(Util().toClassName(filename))
        #print('type', type(cl), cl)
        class_list.append(cl)

        mockupsFile.append('    def __init__(self, foldername=None, filename=None):')
        mockupsFile.append('        super().__init__(foldername, filename)')
        mockupsFile.append('        self.default_folder = \'{}/temp\'.format(str(Path.home()))')

        mockupsFile.append('        if foldername == None:')
        mockupsFile.append('            self.setFolderName(self.default_folder)')
        mockupsFile.append('        if filename == None:')
        mockupsFile.append('            self.setFileName(\'{}\')'.format(filename))

        mockupsFile.append('        self.add([')
        #Util().harden(tempFile)
        for ln in tempFile:
            ln = ln.replace('\n', '')
            mockupsFile.append('            \'{}\','.format(ln.replace("'", "\\'")))
        mockupsFile.append('        ])')
        #mockupsFile.write()

    #for class_name in class_list:

    #mockFile = TemplateFile(dev_folder, '__mockups.py')
    #mockupsFile.append('from mockups import {}'.format(','.join(class_list)))
    mockupsFile.append(' ')
    mockupsFile.append('def main():')
    for class_name in class_list:
        mockupsFile.append('    {}().write()'.format(class_name))

    mockupsFile.append(' ')
    mockupsFile.append('if __name__ == "__main__":')
    mockupsFile.append('    main()')

    mockupsFile.write()

    ######## __mockups.py

if __name__ == "__main__":
    main()

'''