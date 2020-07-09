import os
from pathlib import Path

from link import Link
#from copy_file import CopyFile
from app_settings import AppSettings
from dotenv import load_dotenv
import pprint as pprint
import warnings
from app_settings import AppSettings, AppSettingsTest

class Step(Link):

    def __init__(self):
        super().__init__()

        # use for testing,  set os.environ['LB-TESTING'] = '1' to turn or '0' to turn off

        self.appSettings = AppSettings()
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        if self.lbtesting == '1':
            #print('Using AppSettingsTest')
            self.appSettings = AppSettingsTest()

        self.data = None
        self.copyFile = None
        self.default_folder = None  # '{}/temp'.format(str(Path.home()))
        self.child_folder_dict = AppSettings().getProjectFolders()
        # self.lbproject_name = os.getenv('LB_PROJECT_name') or 'example'
        #self.lbproject_name =
        self.working_folder_name_default = 'example'
        self.env_default = 'dev'
        self.description = ['NEED TO ADD DESCRIPTION']

        self.fixEnv()

    def fixEnv(self):
        # collect env variables
        self.set('LB_ENV', self.env_default)
        self.set('LB_WORKING_FOLDER_NAME', self.working_folder_name_default)
        self.set('LB_PROJECT_name', 'example')

        #if os.getenv('LB_DB_MODEL_password') == None:
        #    raise Exception('Please set environment variable LB_DB_MODEL_password')

        if os.getenv('LB_POSTGRES_MODEL_password') == None:
            raise Exception('Please set environment variable LB_POSTGRES_MODEL_password')

        if os.getenv('LB_JWT_MODEL_password') == None:
            raise Exception('Please set environment variable LB_JWT_MODEL_password')

        # find resource-folder
        # add resource-folder path to data
        if 'resource-folder' not in self.getData():
            self.getData()['resource-folder'] = self.appSettings.getResourceFolder()

        # collect environment variable starting with LB
        for v in os.environ:
            if v.startswith('LB'):
                self.getData()[v]=os.getenv(v)
                #print('STEP',v,os.getenv(v))
        # find projects-folder

        self.getData()['working_folder'] = self.appSettings.getFolder('working_folder')
        self.getData()['shared-folder'] = self.appSettings.getFolder('shared-folder')
        self.getData()['projects-folder'] = self.appSettings.getFolder('projects-folder')

        return self

    def setDescription(self, desc):
        if type(self.description) is list:
            self.description.append(desc)
        else:
            self.description = desc

        return self

    def getDescription(self):
        return self.description

    def show(self):
        print('* ', self.getClassName())
        for desc in self.description:

            print('  - ', desc)

    def set(self, key, default_value):
        if os.getenv(key) != None:
            self.env = os.getenv(key)
        else:
            self.getData()[key] = default_value

    def get(self, key=None):
        if key == None:
            return self.getData()
        return self.getData()[key]

    def setWorkingFolder(self, working_folder_name, env_name='dev'):
        # use to overide working folder
        #self.set('LB_WORKING_FOLDER_NAME', working_folder_name)
        self.set('LB_WORKING_FOLDER_NAME', '{}_{}'.format(working_folder_name, env_name))

        return self

    def getWorkingFolder(self):
        return self.get('LB_WORKING_FOLDER_NAME')
        #return AppSettings().working_folder_name
        #return self.get('LB_WORKING_FOLDER_NAME')

    def run(self):
        #self.log('run')
        self.process()

        if self.next != None:
            self.next.run()
        return self

    def process(self):
        # load env file variables
        # set env variable defaults
        # find resource-folder and add to data
        # collect environment variables that start with LB
        # find projects-folder
        # Set working folder to default
        # collect the environment variables
        load_dotenv()
        self.fixEnv()
        self.show()





    '''
    def dep_getFolder(self, key):

        if key in self.getData(): # search in the root of data
            return self.getData()[key]

        if 'project-folders' in self.getData():
            if key in self.getData()['project-folders']:
                return self.getData()['project-folders'][key]

        #return self.default_folder # used for testing
        return  '{}/{}'.format(str(Path.home()), self.get('LB_WORKING_FOLDER_NAME'))
    '''
    def getData(self):
        # self.data is available to all the links
        if self.data == None:

            if self.prev == None: # create stub
                #self.log('---- a ')
                self.data = {}  # hasn't been set so set it, the caller may want to use it

            else: # move data object forward
                #self.log('---- b')
                self.data = self.prev.getData()

        return self.data

'''
class StepMock(Step):
    def __init__(self):
        super().__init__()
'''
def main():
    import os

    os.environ['LB-TESTING'] = '1'
    #a = Step().setWorkingFolder('temp')
    a = Step()
    a.log('process getData {}'.format(a.getData()))

    print('a.getWorkingFolder()',a.getWorkingFolder())
    #assert(a.getWorkingFolder()=='temp')
    assert(a.prev == None)
    assert(a.next == None)
    assert(a.id == None)
    assert(a.no == 0)
    # print('a.getdata', len(a.getData()))

    assert(len(a.getData()) > 0)

    a.getData()['a']='A'

    b = Step()#.setWorkingFolder('temp')
    a.log('process getData {}'.format(b.getData()))

    a.add(b)

    assert(a.prev == None)
    assert(a.next != None)
    assert(a.id == None)
    assert(a.no == 0)
    print('getdata', a.getData())
    assert ('a' in a.getData())
    assert (b.prev != None)
    assert (b.next == None)
    assert (b.id == None)
    assert (b.no == 1) # increment b's no
    #print('getdata', b.getData())
    #assert (b.getData() == {"a": "A"}) # brings a's data forward
    b.getData()['b'] = 'B'
    #print(b.getData())
    #assert ('a' in b.getData())
    #assert (b.getData() == {"a": "A", "b": "B"})
    assert ( 'b' in b.getData())
    b.run()
    #print('a.getCopyFile().working_folder_name', a.getCopyFile().working_folder_name)
    #assert(a.getCopyFile() != None)
    #assert(a.getCopyFile().working_folder_name == 'pg-dev')
    #assert(a.getCopyFile().project_name == 'example')
    a.log('process getData {}'.format(b.getData()))
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()