
import os
from pathlib import Path
from step import Step
from util import Util
from app_settings import AppSettings, AppSettingsTest

class AppCreateFolders(Step):
    def __init__(self):
        super().__init__()
        self.description=[
            'Create folders for application under user\'s folder.'
        ]

    def process(self):
        super().process()
        #print('process', self.getClassName())

        #print('process ')
        self.getData()  # call to bring data forward
        #self.log('data {}'.format(self.get()))
        #self.appSettings.createFolders()
        print('working_folder', self.appSettings.getFolder('working_folder'))
        self.appSettings.createAppFolders(self.appSettings.getFolder('working_folder'))

        #

        for folder_key in self.appSettings.getAppFolders():

            folder = self.appSettings.getFolder(folder_key)

            if folder not in self.getData():
                self.getData()[folder_key] = folder


        return self
    '''
    def setChildFolderDict(self, child_folder_dict):
        self.child_folder_dict = child_folder_dict
        return self

    def getChildFolderList(self):
        return self.child_folder_dict
    
    def create(self):
        # read folders list
        #for folder_key in self.getChildFolderList():

        appSettings = AppSettings()

        for folder_key in appSettings.getAppFolders():
            #working_folder = '{}/{}'.format(self.getFolder(), self.getChildFolderList()[folder_key])
            #working_folder = '{}/{}'.format(appSettings.getFolder(), appSettings.getAppFolders()[folder_key])
            print('folder_key',folder_key)

            working_folder = appSettings.getFolder('working_folder')

            print('system folder', working_folder)
            if working_folder not in self.getData()['working_folder']:
                self.getData()['working_folder'].append(working_folder)
            # make easier to reference
            self.getData()[folder_key] = working_folder

        # create folders
        print('working_folder', appSettings.getAppFolders())
        for folder_name in self.getData()['working_folder']:
            print('  folder_name',folder_name)
            if not os.path.exists(folder_name):
                Util().createFolder(folder_name)

        # folders by key
        #for folder_key in self.getChildFolderList():
        #    self.log('key {}'.format(folder_key))
        #    self.getData()[folder_key]=self.getChildFolderList()[folder_key]
        return self

    def process(self):
        super().process()
        # self.log('--')
        self.getData()['working_folder'] = []  # call to bring data forward
        self.log('data {}'.format(self.get()))
        #self.getData()['working_folder'].append(self.getFolder())
        self.get('working_folder').append(AppSettings().getAppFolders())

        #self.getData()['working_folder'].append(self.getFolder())
        #.append('{}/.{}'.format(str(Path.home()), self.getData()['working_folder-name']))  # working folder

        self.create()
        #self.log('---- data: {}'.format(self.getData()))

        return self
    '''


def main():
    #from app_environment import AppEnvironment
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest()

    step = AppCreateFolders().run() #.setWorkingFolder('temp')
    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    # folders stashed in data
    assert( 'working_folder' in step.getData())
    assert ('shared-folder' in step.getData())
    assert ('projects-folder' in step.getData())
    # folders exist
    assert (Util().folder_exists(step.get('working_folder')))
    assert (Util().folder_exists(step.get('shared-folder')))
    assert (Util().folder_exists(step.get('projects-folder')))

    #print('data', step.getData())
    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()