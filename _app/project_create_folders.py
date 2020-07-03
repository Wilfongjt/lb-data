import os
from pathlib import Path
from step import Step
from util import Util
from app_settings import AppSettings

class ProjectCreateFolders(Step):
    def __init__(self):
        super().__init__()
        # folders define in Step
        # folders defined in project_environment
        self.description=['Create folders for project in user\'s folder']

    def getProjectFolder(self, key):
        return self.getData()['project-folders'][key]

    def process(self):
        super().process()
        '''
        expect that path names are expanded and held in "projects-folder"
        :return:
        '''

        if 'projects-folder' not in self.getData():
            raise Exception('Projects-folder is not defined.')

        if 'project-folders' not in self.getData():
            self.getData()['project-folders']={}
        # expand the project folders
        for key in self.appSettings.getProjectFolders():
            val = '{}/{}'.format(self.appSettings.getFolder('working_folder'),
                           self.appSettings.getProjectFolders()[key])
            self.getData()['project-folders'][key]=val

        if len(self.getData()['project-folders']) == 0:
            raise Exception('Project folders are not initialized.')

        # create folders
        for key in self.getData()['project-folders']:
            if not os.path.exists(self.getData()['project-folders'][key]):
                Util().createFolder(self.getData()['project-folders'][key])

        return self


def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from project_environment import ProjectEnvironment
    from app_settings import AppSettingsTest
    from util import Util

    os.environ['LB-TESTING']='1'
    appSettings = AppSettingsTest()
    appSettings.createAppFolders()

    step = ProjectCreateFolders().run()

    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    assert(Util().folder_exists( appSettings.getFolder('projects-folder')))
    assert (Util().folder_exists(appSettings.getFolder('project-folder')))
    assert (Util().folder_exists(appSettings.getFolder('compiled-folder')))
    assert (Util().folder_exists(appSettings.getFolder('con-fig-folder')))
    assert (Util().folder_exists(appSettings.getFolder('script-folder')))
    assert (Util().folder_exists(appSettings.getFolder('log-folder')))
    assert (Util().folder_exists(appSettings.getFolder('merged-folder')))
    assert (Util().folder_exists(appSettings.getFolder('temp-lates-folder')))

    #appSettings.removeFolders()
    os.environ['LB-TESTING']='0'

if __name__ == "__main__":
    main()