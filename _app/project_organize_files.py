from step import Step
from util import Util
from configuration_file import ConfigurationDict
from template_file import TemplateFile
#from script_file import ScriptFile
#from helper_temporary_file import HelperTemporaryFile
#from helper_template_merge import HelperTemplateMerge
from helper_copy_file import HelperCopyFile

# last step
# Input  : temp-folder/*.compiled
# Input  : template-folder/*.tmpl
# Outputs: script-folder/*.sql

class ProjectOrganizeFiles(Step):
    def __init__(self):
        super().__init__()
        #self.fileHelper=fileHelper # helper class for writing to storage
    '''
        def __init__(self, fileHelper=None):
        super().__init__()
        self.fileHelper=fileHelper # helper class for writing to storage

    '''

    def getDescription(self):
        return 'Compile and insert simple tags. Write SQL file when helper is available.'

    def process(self):
        print('  -- process')
        self.getData()

        # Input
        #script_folder = self.getCopyFile().getProjectFolder(child_folder='script')
        temp_folder =  self.getFolder('temp-folder')
        # Outputs
        #docker_folder = self.getCopyFile().getProjectFolder(child_folder='docker')
        #database_folder = self.getCopyFile().getProjectFolder(child_folder='db-api-table-script')
        docker_folder = self.getFolder('docker-folder')
        script_folder = self.getFolder('script-folder')

        print('script_folder', temp_folder)
        print('docker_folder', docker_folder)
        print('database_folder', script_folder)

        # get pg.sql list

        file_name_list  = Util().getFileList(temp_folder, ext='.pg.sql') # compiled files
        print('    - inputs',len(file_name_list) )

        # convert all conf files to temp/files
        for file_name in file_name_list:
            if 'docker' in file_name:
                print('docker {}'.format(file_name))
                fromFile = TemplateFile(temp_folder,file_name)
                toFile = TemplateFile(docker_folder, 'docker-compose.yml')
                HelperCopyFile(fromFile, toFile, step=self).run()
            else:
                print('sql {}'.format(file_name))
                fromFile = TemplateFile(temp_folder, file_name)
                toFile = TemplateFile(script_folder, file_name)
                HelperCopyFile(fromFile, toFile).run()
        return self

def main():
    '''
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from project_environment import ProjectEnvironment
    from project_create_folders import  ProjectCreateFolders
    from project_configuration_initialize import ProjectConfigurationInitialize
    from project_template_initialize import ProjectTemplateInitialize
    from project_configuration_generate_api import ProjectConfigurationGenerateAPI
    from project_template_compile import ProjectTemplateCompile
    from helper_temporary_file import HelperTemporaryFile
    from util import Util
    '''
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    step = ProjectOrganizeFiles().run()
    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    # appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()