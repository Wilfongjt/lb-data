#from copy import Process
#from copy_file import CopyFile
from file import ListFile
#from weld import ListFile

from util import Util
from lyttle_parser import LyttleParser
from app_settings import AppSettingsTest

class ScriptFile(ListFile):
    def __init__(self, folder_name=None, file_name=None):
        super().__init__(folder_name, file_name)

        if self.getFolderName() == None:
            # default to source code resource, assume we are going to copy
            self.setFolderName(AppSettingsTest().getFolder('temp-folder'))
            print('self.getFolderName()', self.getFolderName())

    #def getFileName(self):
    #    return '{}.{}'.format(self.getPrefix(super().getFileName()),super().getFileName())

    def write(self):
        print('folder', self.getFolderName(), ' file ', self.getFileName())
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
    import os

    os.environ['LB-TESTING'] = '1'

    print('* ScriptFile')

    AppSettingsTest().createFolders()
    #folder = '{}/temp'.format(str(Path.home()))
    folder = AppSettingsTest().getFolder('temp-folder')

    #if not Util().folder_exists(folder):
    #    Util().createFolder(folder)

    file_name = 'junk.sql'
    # file name trick
    expected = file_name

    # write a junk file
    print('folder: ', folder)
    print('file: ', file_name)

    aFile = ScriptFile(folder_name=folder, file_name=file_name)\
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
    aFile2 = ScriptFile(folder_name=folder, file_name=file_name).read()
    expected = 4
    print('  - line count actual {} expected {}'.format(len(aFile2), expected))
    assert(len(aFile2)==expected)

    # cleanup
    aFile.delete()
    expected = file_name
    print('  - deleted {}'.format(not Util().file_exists(aFile.getFolderName(), expected)))
    assert(not Util().file_exists(aFile.getFolderName(), expected))
    #AppSettingsTest().removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()