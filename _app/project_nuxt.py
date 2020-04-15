from util import Util
from step import Step
import os
# doesnt work
class ProjectNuxt(Step):
    def __init__(self):
        super().__init__()

        self.description = [
            'Generate a nuxtjs application ',
            'This is a stub application that only shows the standard startup page.'
        ]

    def process(self):
        raise Exception('ProjectNuxt doesnt work')
        #temp folder cleanup
        self.getData()

        web_folder =  self.appSettings.getCodeFolder('web')
        # if nuxt already exists then skip

        # change folder to web_folder
        # call os to execute 'npx create-nuxt-app web'

        #os.system('cd {} | npx create-nuxt-app web'.format(web_folder))
        os.chdir(web_folder)
        #os.system('cd {} | env | ls'.format(web_folder))
        os.system('ls'.format(web_folder))
        os.system('npx create-nuxt-app web')
        os.system('ls')

        #os.system("some_command < input_file | another_command > output_file")

        return self

def main():
    from app_settings import AppSettingsTest
    from project_merge import ProjectMerge
    from project_compile import ProjectCompile
    from mockup_test_data import MockupData

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    ProjectNuxt().run()
    # appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()