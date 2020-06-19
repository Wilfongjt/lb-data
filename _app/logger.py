from file import ListFile
#from copy_file import CopyFile
from app_settings import AppSettingsTest

class Logger(ListFile):
    def __init__(self, folder_name=None, file_name='logger.log'):
        super().__init__(folder_name, file_name)
        if self.getFolderName() == None:
            # default to source code resource, assume we are going to copy
            self.setFolderName(AppSettingsTest().getFolder('log-folder'))

    def log(self, item):
        with open('{}/{}'.format(self.getFolderName(),
                                    self.getFileName()), 'a') as f:
            f.write('{}\n'.format(item))
            if self.isEcho():
                print(item)

        return self

def main():
    import os
    from util import Util
    os.environ['LB-TESTING'] = '1'
    AppSettingsTest().createFolders()
    print('* Logger')
    #folder_name = CopyFile().getTempFolderName()
    file_name = 'logger.log'
    '''
    log = Logger()\
        .setEcho(False) # write to screen too
    log.log('hi').log('ho').log('hi')
    log.setEcho(False) # write to storage onlh


    expected = file_name
    assert ( Util().file_exists(log.getFolderName(), log.getFileName()))

    print('  - create {}/{}'.format(log.getFolderName(), log.getFileName()))
    assert(expected == log.getFileName())
    print('  - exists {}'.format(Util().file_exists(log.getFolderName(), expected)))
    assert(Util().file_exists(log.getFolderName(), expected))

    # read the junk file
    log2 = Logger().read()
    expected = 3
    print('  - line count actual {} expected {}'.format(len(log2), expected))
    assert(len(log2)==expected)

    # cleanup
    log.delete()
    expected = file_name
    print('  - deleted {}'.format(not Util().file_exists(log.getFolderName(), expected)))
    assert(not Util().file_exists(log.getFolderName(), expected))

    #AppSettingsTest().removeFolders()
    '''
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()