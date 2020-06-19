
from step import Step
from util import Util
from app_settings import AppSettings
#from configuration_file import ConfigurationDict
#from template_file import TemplateFile
from templates import Template
from template_upsert_test import Template_InterfaceTest

#from helper_test_api_template import HelperTestAPITemplate
from forms import FormKeyList
from pprint import pprint
from list_methods import MethodList
from configuration_interface import InterfaceConfiguration
from configuration_file import ConfigurationDict
from text_file import TextFile
from app_settings import AppSettings, AppSettingsTest

import os

class File_Preview(list):
    '''
    Show all .json file and
    Map all .json files to outputs
    '''
    def __init__(self):
        self.appSettings = AppSettings()
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        if self.lbtesting == '1':
            # print('Using AppSettingsTest')
            self.appSettings = AppSettingsTest()

        self.process()

    def process(self):

        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        file_list = Util().getFileList(prj_expand_folder, '.json')
        print('file_list',file_list)
        #
        for conf_name in file_list:
            parts = conf_name.split('.')
            stuff = {'type': parts[1],
                     'config': conf_name,
                     'template-expected': self.appSettings.to_tmpl_expected(conf_name),
                     'template-actual': self.appSettings.to_tmpl(conf_name),
                     'folder': prj_expand_folder}
            self.append(stuff)
        return self


class ProjectExpand(Step):
    def __init__(self):
        super().__init__()

        self.description = [
            'Create missing configuration files ',
            'Create missing template files',
            'Overwrites any existing templates'
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
        #self._createTestConfigurationFiles()
        self._moveConfigurationFiles()
        self._createTemplateFiles()
        #self._moveTemplateFiles()

        return self

    def _createAPIConfigurationFiles(self):
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')
        # get list of table configs
        file_list = Util().getFileList(prj_config_folder, '.table.pg.json')
        # everything starts with config file
        for conf_name in file_list:
            #print('conf', conf_name)
            confFile = ConfigurationDict(prj_config_folder, conf_name).read()

            #print('confFile')
            #pprint(confFile)
            # handle multiple Interfaces
            for interface in FormKeyList(confFile):
                interfaceFile = InterfaceConfiguration(interface, prj_config_folder, conf_name).read()
                for method in MethodList(confFile, interface):
                    #print('method', method)
                    #print('output ', '{}  {}'.format( self.appSettings.to_api(conf_name, method), prj_expand_folder ))
                    interfaceFile['type'] = 'interface-{}'.format(method)
                    interfaceFile.copy( prj_expand_folder, self.appSettings.to_interface(conf_name, interface, method))
        #add code to create test json
        return self

    def dep_createTestConfigurationFiles(self):
        '''
        didnt work for multiple interfaces
        :return:
        '''
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')
        # get list of table configs
        file_list = Util().getFileList(prj_config_folder, '.table.pg.json')
        # everything starts with config file
        #print('tables', file_list)
        for conf_name in file_list:
            #print('conf', conf_name)
            confFile = ConfigurationDict(prj_config_folder, conf_name).read()
            #print('conf 2',confFile)
            if 'tbl-tests' in confFile:
                #print('test 1')
                for test in confFile['tbl-tests']:
                    #print('test 2')
                    confFile['type'] = 'table-{}-test'.format(test)
                    confFile.copy(prj_expand_folder, self.appSettings.to_test(conf_name,test))
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
        return self

    def _createTemplateFiles(self):
        #
        prj_config_folder = self.appSettings.getFolder('con-fig-folder')
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        # look in the expand folder to pick up the generated config files
        file_list = Util().getFileList(prj_expand_folder, '.json')

        files=[]
        #
        '''
        for conf_name in file_list:
            parts = conf_name.split('.')
            stuff = {'type':parts[1],
                     'config': conf_name,
                     'template-expected': self.appSettings.to_tmpl_expected(conf_name),
                     'template-actual': self.appSettings.to_tmpl(conf_name)}
            print('stuff', stuff)

            files.append(stuff)
        '''

        for stuff in File_Preview(): # formerly Stuff
            #print('stuff', stuff)
            tmplFile = None
            # custom template available when ==
            # no custom and no default available when
            if stuff['template-expected'] == stuff['template-actual']: # means custom file is available
                print('A Custom Template', stuff)
                #tmplFile = TemplateFile(prj_tmpl_folder, stuff['template']).read()
                tmplFile = Template({}, prj_tmpl_folder, stuff['template-expected'])

            elif stuff['template-actual'] == 'table-api-test.pg.tmpl':
                # look for tests attribute
                print('B API Test Template', stuff)
                #print(' * Function_UpsertTest goes here')
                tmplFile = Template_InterfaceTest({}) # with no dictionary to avoid templatization

            else:
                print('C Default Template', stuff)

                tmplFile = TextFile(prj_tmpl_folder, stuff['template-actual']).read()

            if len(tmplFile) == 0 :
                #print('folder', prj_tmpl_folder)
                raise Exception('Empty template {}'.format(stuff['template-actual']))

            # copy files to expand folder
            #print('Z copy', prj_expand_folder, stuff['template-expected'])
            Util().deleteFile(prj_expand_folder, stuff['template-expected'])
            tmplFile.copy(prj_expand_folder, stuff['template-expected'])

        return self




    def _moveTemplateFiles(self):
        prj_tmpl_folder = self.appSettings.getFolder('temp-lates-folder')
        prj_expand_folder = self.appSettings.getFolder('expanded-folder')

        file_list = Util().getFileList(prj_tmpl_folder, '.tmpl')
        # everything starts with config file
        for tmpl_name in file_list:
            parts = tmpl_name.split('.')
            if len(parts) == 4:
                #print('move tmpl', tmpl_name)
                tmplFile = TextFile(prj_tmpl_folder, tmpl_name)\
                    .copy(prj_expand_folder, tmpl_name)

        return self



def main():
    #from app_environment import AppEnvironment
    #from app_create_folders import AppCreateFolders
    #from app_initialize import AppInitialize
    #from project_environment import ProjectEnvironment
    #from project_create_folders import  ProjectCreateFolders
    from project_initialize import ProjectInitialize
    #from util import Util
    import os
    from app_settings import AppSettingsTest
    #from configuration_file_mocks import ConfigurationDictFileDatabaseMock, ConfigurationDictFileTableMock
    #from template_file_mocks import TemplateMockups, TemplateFileCreateDatabaseMock, TemplateFileCreateTableMock,TemplateFileTableApiUpdateMock,TemplateFileTableApiSelectMock,TemplateFileTableApiInsertMock
    #from mockup_test_data import   MockupData
    #from project_compile import ProjectCompile
    #from project_merge import ProjectMerge

    os.environ['LB-TESTING'] = '1'

    # pprint(File_Preview())

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