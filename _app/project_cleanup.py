from util import Util
from step import Step

class ProjectCleanup(Step):
    def __init__(self):
        super().__init__()


    def description(self):
        return 'Cleanup temp files. '

    def cleanOut(self, folder):
        print('cleanout ', folder )
        #expanded_folder = self.appSettings.getFolder('expanded-folder')
        filelist = Util().getFileList(folder)
        #print('files', filelist)
        for fn in filelist:
            #print('file', fn)
            Util().deleteFile(folder, fn)

        return self

    def process(self):

        #ext_list = ['.compiled', '.tmpl','.json']

        #####
        self.cleanOut(self.appSettings.getFolder('expanded-folder'))

        return self

def main():
    from app_settings import AppSettingsTest

    #from app_environment import AppEnvironment
    #from app_create_folders import AppCreateFolders
    #from app_initialize import AppInitialize
    #from project_environment import ProjectEnvironment
    import os

    from util import Util
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest()

    step = ProjectCleanup().run()

    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    filelist = Util().getFileList(appSettings.getFolder('expanded-folder'))
    print('filelist', filelist)
    assert( len(filelist)==0) # has files
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()