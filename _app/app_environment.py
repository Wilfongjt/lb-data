import os
from pathlib import Path

from step import Step
'''
stub for environment Step.process handles setup
'''
class AppEnvironment(Step):
    def __init__(self):
        super().__init__()

    def process(self):
        super().process()
        #print('process', self.getClassName())
        return self

def main():
    from app_settings import AppSettingsTest

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest()

    step = AppEnvironment().run() #.setWorkingFolder('temp')

    # check environment
    step.log('getData {}'.format(step.getData()))
    assert ('LB_WORKING_FOLDER_NAME' in step.getData())
    assert ('LB_SECRET_PASSWORD' in step.getData())
    assert ('LB_POSTGRES_PASSWORD' in step.getData())
    assert ('LB_JWT_PASSWORD' in step.getData())

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()