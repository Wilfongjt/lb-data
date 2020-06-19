from step import Step
from configuration_file import ConfigurationDict
from util import Util
from text_file import TextFile
'''
copy the context.template.list.json to working folder
'''
class AppInitialize(Step):

    def __init__(self):
        super().__init__()
        #'LB_ENV', self.env_default)
        #self.set('LB_WORKING_FOLDER_NAME', self.working_folder_name_default)
        #self.set('LB_PROJECT_NAME', 'example')
        self.description=[
            'Copies files from res/shared to {}'.format(self.get('LB_WORKING_FOLDER_NAME'))
        ]

    def process(self):
        super().process()
        #file_name = 'context.template.list.json'
        res_shared_folder = self.appSettings.getResourceFolder('shared')
        shared_folder = self.appSettings.getFolder('shared-folder')
        filelist = Util().getFileList(res_shared_folder)

        for fn in filelist:
            TextFile(res_shared_folder, fn)\
                .read()\
                .copy(shared_folder, fn)
        return self

def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from util import Util
    from app_settings import AppSettingsTest
    import os

    print('* AppInitialize')
    os.environ['LB-TESTING'] = '1'

    appSettings = AppSettingsTest()
    appSettings.createAppFolders()

    step = AppInitialize().run()
    #    shared_folder = '{}/..LyttleBit/testing/shared'.format(appSettings.getHomeFolder()) #'{}/shared'.format(step.getFolder('working-folder'))

    shared_folder = '{}/..LyttleBit/testing/shared'.format(appSettings.getHomeFolder()) #'{}/shared'.format(step.getFolder('working-folder'))
    exp_file = 'context.template.list.json'
    #print('  - copy {}'.format(exp_file))

    # did file copy?
    assert(Util().file_exists(shared_folder, exp_file))

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
