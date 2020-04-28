'''
from app_settings import AppSettingsTest
from step import Step
from util import Util

class MockupData(Step):
    def __init__(self):
        super().__init__()
        self.appSettings = AppSettingsTest()

    def process(self):
        fromfolder = self.appSettings.getResourceFolder('shared')
        tofolder = self.appSettings.getFolder('shared-folder')
        filelist = Util().getFileList(fromfolder)
        #print('fromfolder',fromfolder, ' tofolder', tofolder)
        self.copy(fromfolder,
                  filelist,
                  tofolder
                  )

        fromfolder = self.appSettings.getResourceFolder('templates')
        tofolder = self.appSettings.getFolder('temp-lates-folder')
        filelist = Util().getFileList(fromfolder)

        self.copy(fromfolder,
                  filelist,
                  tofolder
                  )

        fromfolder = self.appSettings.getResourceFolder('config')
        tofolder = self.appSettings.getFolder('con-fig-folder')
        filelist = Util().getFileList(fromfolder)

        self.copy(fromfolder,
                  filelist,
                  tofolder
                  )

    def copy(self, fromfolder, fromlist, tofolder ):
        # read froms
        # write tos
        for fn in fromlist:
            path_filename = '{}/{}'.format(fromfolder, fn)
            out_path_filename =  '{}/{}'.format(tofolder, fn)
            lines = ''
            #if '.DS_Store' not in fn:
            with open(path_filename) as f:
                lines = f.read()
            with open(out_path_filename,'w') as f:
                f.write(lines)

def testCopy(fromfolderkey, tofolderkey):
    appSettings = AppSettingsTest()

    fromfolder = appSettings.getResourceFolder(fromfolderkey)
    tofolder = appSettings.getFolder(tofolderkey)
    fromfilelist = Util().getFileList(fromfolder)

    for fn in fromfilelist:
        print('file', tofolder,fn)
        assert(Util().file_exists(tofolder, fn))

def main():
    import os
    from util import Util
    from app_settings import AppSettingsTest
    from configuration_file import ConfigurationDict

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    MockupData().run()

    testCopy('shared', 'shared-folder')
    testCopy('templates', 'temp-lates-folder')
    testCopy('config', 'con-fig-folder')

    folder =  appSettings.getResourceFolder('config')
    filelist = Util().getFileList(folder)
    print('filelist', filelist)
    for fn in filelist:

        file=ConfigurationDict(folder, fn).read().write()
        print('dict', file)


    appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()
'''