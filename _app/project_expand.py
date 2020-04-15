
from step import Step
from util import Util
from app_settings import AppSettings
from configuration_file import ConfigurationDict
from template_file import TemplateFile


class ProjectExpand(Step):
    def __init__(self):
        super().__init__()

        self.description = [
            'Create missing configuration files ',
            'Create missing template files',
            'Overwrites the existing template'
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

        # create api files

        self._createAPIConfigurationFiles() # alway create config before template
        self._moveConfigurationFiles()
        self._createTemplateFiles()
        self._moveTemplateFiles()

        return self

    def _moveConfigurationFiles(self):
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        file_list = Util().getFileList(prj_config_folder, '.json')
        # everything starts with config file
        for conf_name in file_list:
            #print('conf', conf_name)
            confFile = ConfigurationDict(prj_config_folder, conf_name)\
                .read()\
                .copy(prj_expand_folder, conf_name)

    def _moveTemplateFiles(self):
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        file_list = Util().getFileList(prj_tmpl_folder, '.tmpl')
        # everything starts with config file
        for tmpl_name in file_list:
            parts = tmpl_name.split('.')
            if len(parts) == 4:
                #print('tmpl', tmpl_name)
                tmplFile = TemplateFile(prj_tmpl_folder, tmpl_name)\
                    .read()\
                    .copy(prj_expand_folder, tmpl_name)


    def _createAPIConfigurationFiles(self):
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')
        # get list of table configs
        file_list = Util().getFileList(prj_config_folder, '.table.pg.json')
        # everything starts with config file
        for conf_name in file_list:
            #print('conf', conf_name)
            confFile = ConfigurationDict(prj_config_folder, conf_name).read()
            for method in confFile['api-methods']:
                #print('method', method)
                #print('output ', '{}  {}'.format( self.appSettings.to_api(conf_name, method), prj_expand_folder ))
                confFile['type'] = 'table-api-{}'.format(method)
                confFile.copy( prj_expand_folder, self.appSettings.to_api(conf_name, method))

    def _createTemplateFiles(self):
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        # look in the expand folder to pick up the generated config files
        file_list = Util().getFileList(prj_expand_folder, '.json')

        files=[]

        for conf_name in file_list:
            parts = conf_name.split('.')
            stuff = {'type':parts[1],
                     'config': conf_name,
                     'template': self.appSettings.to_tmpl_expected(conf_name),
                     'template-actual': self.appSettings.to_tmpl(conf_name)}

            files.append(stuff)
            print('stuff',stuff)
        print('files', len(files))
        for stuff in files:
            #print('stuff', stuff)
            tmplFile = None
            if stuff['template'] == stuff['template-actual']:
                tmplFile = TemplateFile(prj_tmpl_folder, stuff['template']).read()
            else:
                #print('prj_tmpl_folder', prj_tmpl_folder)
                #print('stuff[template-actual]',stuff['template-actual'])
                tmplFile = TemplateFile(prj_tmpl_folder, stuff['template-actual']).read()

            if len(tmplFile) == 0 :
                raise Exception('Empty template {}'.format(stuff['template-actual']))

            tmplFile.copy(prj_expand_folder, stuff['template'])

        return self


def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from project_environment import ProjectEnvironment
    from project_create_folders import  ProjectCreateFolders
    from project_initialize import ProjectInitialize
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
    step = ProjectExpand()
    ProjectInitialize()\
        .add(step)\
        .run()
    ###############
    #filelist = Util().getFileList(appSettings.getFolder('expanded-folder'), ext='role-create.pg.tmpl._DEP')
    #print('filelist', filelist)
    #assert(len(filelist) > 0)


    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()