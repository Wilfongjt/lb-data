
from step import Step
from util import Util
from app_settings import AppSettings
from configuration_file import ConfigurationDict
from template_file import TemplateFile


class ProjectInitialize(Step):
    def __init__(self):
        super().__init__()

        self.description = [
            'Copy configuration files from resources config folders ',
            'Copy template files from resource to project template folder'
        ]


    def process(self):
        super().process()
        #print('process')
        self.getData() # bring data forward
        # copy files from code source
        res_tmpl_folder = self.appSettings.getResourceFolder('templates')
        res_config_folder = self.appSettings.getResourceFolder('config')

        if 'testing' in res_tmpl_folder:
            raise Exception('A not pulling from code'.format(res_tmpl_folder))

        if 'testing' in res_config_folder:
            raise Exception('B not pulling from code {}'.format(res_config_folder))

        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')

        #############################################################
        self._copyConfigurationFromCode()
        self._copyTemplatesFromCode()

        return self

    def _copyConfigurationFromCode(self):
        res_config_folder = self.appSettings.getResourceFolder('config')
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')


        # move from resource to project
        folder_list = Util().getFolderList(res_config_folder)

        for folder in folder_list:
            if '_DEP' not in folder:
                print('folder', folder)
                file_list = Util().getFileList(folder, '.json')
                # copy config from resource
                for fn in file_list:
                    confFile = ConfigurationDict(folder, fn) \
                        .read() \
                        .copy(prj_config_folder, fn)

        return self

    def _copyTemplatesFromCode(self):

        res_tmpl_folder = self.appSettings.getResourceFolder('templates')
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')

        # move from resource to project
        folder_list = Util().getFolderList(res_tmpl_folder)

        for folder in folder_list:
            if '_DEP' not in folder:
                file_list = Util().getFileList(folder, '.tmpl')
                for fn in file_list:
                    TemplateFile(folder, fn) \
                        .read() \
                        .copy(prj_tmpl_folder, fn)


def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from project_environment import ProjectEnvironment
    from project_create_folders import  ProjectCreateFolders
    from util import Util
    import os
    from app_settings import AppSettingsTest
    #from configuration_file_mocks import ConfigurationDictFileDatabaseMock, ConfigurationDictFileTableMock
    from template_file_mocks import TemplateMockups, TemplateFileCreateDatabaseMock, TemplateFileCreateTableMock,TemplateFileTableApiUpdateMock,TemplateFileTableApiSelectMock,TemplateFileTableApiInsertMock
    from mockup_test_data import   MockupData
    from project_compile import ProjectCompile
    from project_merge import ProjectMerge

    os.environ['LB-TESTING'] = '1'
    ######################################################################
    # create folders
    appSettings = AppSettingsTest().createFolders()

    # setup mock files
    #MockupData().run()

    ######################################################################
    # create files to work on
    # no need to copy files

    ######################################################################
    step = ProjectInitialize().run()

    #ProjectCompile()\
    #    .add(ProjectMerge())\
    #    .add(step)\
    #    .run()


    #AppInitialize()\
    #    .add(step)\
    #    .run()

    #print('* {}'.format(step.getClassName()))
    #print('  - {}'.format(step.getDescription()))

    ######################################################################
    #filelist = Util().getFileList( step.getFolder('con-fig-folder'))
    filelist = Util().getFileList( appSettings.getFolder('con-fig-folder'))

    assert( len(filelist)>0) # has files

    ######################################################################
    filelist = Util().getFileList( appSettings.getFolder('temp-lates-folder'))
    #print('templates copied {}'.format(len(filelist)))
    assert( len(filelist)>=20) # has files

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()