import sys
from dotenv import load_dotenv
import os
from pathlib import Path
from step import Step
from app_environment import AppEnvironment
'''
class ProjectEnvironment(AppEnvironment):
    def __init__(self, project_name='example'):
        super().__init__()
        self.project_name = project_name
        # project folders eg example/docker, example/temp
'''
class ProjectEnvironment(AppEnvironment):
    def __init__(self):
        super().__init__()
        self.description=['Placeholder for other project steps',
                          'Stash project-name, project-folder-name, and project-folder values.']
        #self.project_name = self.appSettings.getFolder('')
        # project folders eg example/docker, example/temp

    def process(self):
        super().process()

        self.set('project-name', self.get('LB_PROJECT_NAME'))
        self.set('project-folder-name', '{}-{}'.format(self.get('project-name'), self.get('LB_ENV') ) )
        self.set('project-folder', self.appSettings.getFolder('project-folder'))
        #print('data', self.getData())

        #appSettings.createProje ctFolders()

        '''
        self.getData()['project-folders'] = {}  # call to bring data forward
        prj_folder = '{}/.{}/projects/{}'.format(str(Path.home()),
                                                 self.getData()['LB_WORKING_FOLDER_NAME'],
                                                 self.project_name)

        self.getData()['project-name'] = self.project_name
        self.getData()['project-folders']['project-folder'] = prj_folder # create project file
        # put togethe full path with kev-val on end
        for key in self.child_folder_dict:
            self.getData()['project-folders'][key]='{}/{}'.format(prj_folder, self.child_folder_dict[key])
        '''
        return self
'''
    def process(self):
        super().process()
        self.getData()['project-folders'] = {}  # call to bring data forward
        prj_folder = '{}/.{}/projects/{}'.format(str(Path.home()),
                                                 self.getData()['LB_WORKING_FOLDER_NAME'],
                                                 self.project_name)

        self.getData()['project-name'] = self.project_name
        self.getData()['project-folders']['project-folder'] = prj_folder # create project file
        # put togethe full path with kev-val on end
        for key in self.child_folder_dict:
            self.getData()['project-folders'][key]='{}/{}'.format(prj_folder, self.child_folder_dict[key])

        return self
'''


def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from app_settings import AppSettingsTest
    from util import Util

    print('* ProjectEnvironment')
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest()

    #step = ProjectEnvironment('example').setWorkingFolder('temp').run()
    step = ProjectEnvironment().run()
    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    print('  - set project data')
    #assert(step.getData()['LB_WORKING_FOLDER_NAME']=='temp')
    assert(step.getData()['project-name']== os.environ['LB_PROJECT_NAME'] or 'example')
    assert(step.get('project-folder').endswith(step.get('project-folder-name')))
    assert ('project-name' in step.getData())
    assert ('project-folder-name' in step.getData())
    assert ('project-folder' in step.getData())
    #step.log(step.getData(), echo=True)
    appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()