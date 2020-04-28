#from copy import Process
#from copy_file import CopyFile
from file import FileAsList
from util import Util
from lyttle_parser import LyttleParser
from app_settings import AppSettingsTest

class ScriptFile(FileAsList):
    def __init__(self, script_folder=None, script_file_name=None):
        super().__init__(script_folder, script_file_name)

        if self.getFolderName() == None:
            # default to source code resource, assume we are going to copy
            self.setFolderName(AppSettingsTest().getFolder('temp-folder'))
            #print('self.getFolderName()', self.getFolderName())

    #def getFileName(self):
    #    return '{}.{}'.format(self.getPrefix(super().getFileName()),super().getFileName())
    '''
    def getPrefix(self, file_name):

        prefix = '00'

        if 'database.' in file_name :
            prefix = '01'
        elif 'role-create' in file_name:
            prefix = '02'
        elif 'table-api' in file_name:
            prefix = '04'
        elif 'table.' in file_name:
            prefix = '03'
        elif 'function.' in file_name:
            prefix = '05'
        elif 'grant' in file_name:
            prefix = '06'

        return prefix
    '''
    '''
    def delete(self):
        Util().deleteFile(self.getFolderName(), self.getFileName())
        return self

    def read(self):
        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
        with open(path_filename) as f:
            for line in f:
                # self.lineList.append(line)
                line = line.replace('\n','')
                self.append(line)

        return self
    '''
    def write(self):

        with open('{}/{}'.format(self.getFolderName(),
                                    self.getFileName()), 'w') as f:
            if '-- generated' not in self:
                f.write('-- generated\n')

            for line in self:

                if '[[' in line:

                    print('  -- script file', self)
                    #print('lyttleparser: ', LyttleParser(line).parse())
                    raise Exception('Unresolved tag {} in {}'.format(line, self.getFileName()))

                f.write('{}\n'.format(line))

        return self

def main():
    from pathlib import Path
    from util import Util

    print('* ScriptFile')

    AppSettingsTest().createFolders()
    #folder = '{}/temp'.format(str(Path.home()))
    #folder = AppSettings().getFolder('temp-folder')

    #if not Util().folder_exists(folder):
    #    Util().createFolder(folder)

    file_name = 'junk.sql'
    # file name trick
    expected = file_name

    # write a junk file
    aFile = ScriptFile().setFileName(file_name)\
        .append('A')\
        .append('B')\
        .append('C')\
        .write()

    #
    print('  - create {}/{}'.format(aFile.getFolderName(), aFile.getFileName()))
    assert(expected == aFile.getFileName())

    print('  - exists {}'.format(Util().file_exists(aFile.getFolderName(), expected)))
    assert(Util().file_exists(aFile.getFolderName(), expected))

    # read the junk file
    aFile2 = ScriptFile().setFileName(file_name).read()
    expected = 4
    print('  - line count actual {} expected {}'.format(len(aFile2), expected))
    assert(len(aFile2)==expected)

    # cleanup
    aFile.delete()
    expected = file_name
    print('  - deleted {}'.format(not Util().file_exists(aFile.getFolderName(), expected)))
    assert(not Util().file_exists(aFile.getFolderName(), expected))
    AppSettingsTest().removeFolders()

if __name__ == "__main__":
    main()