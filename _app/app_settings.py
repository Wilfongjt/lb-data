import os
from pathlib import Path
from util import Util
from dotenv import load_dotenv
import shutil
import json
from pprint import pprint
import re


class AppSettings(dict):
    '''
    production folders under ~/<work-folder-name>
    '''

    def __init__(self):
        # ~/<work-folder-name>/projects/<project-name>/

        load_dotenv()

        temp_env = {}
        for key in os.environ:
            if key.startswith('LB_'):
                #print('LB key: ', key, ' val: ', os.environ[key])
                if '{' in os.environ[key] or '[' in os.environ[key]:
                    #print('dict')
                    self[key] = json.loads(os.environ[key])
                    # break up json environment variables
                    for k in self[key]:
                        temp_env['{}_{}'.format(key, k)]= self[key][k]
                else:
                    #print('str')
                    self[key] = os.environ[key]

        for key in temp_env: # put into memory
            os.environ[key]=temp_env[key]
            #print('key',key,os.environ[key])

        self.setEnviron()

        lbworking_name = self['LB_ENV']['working_folder']  # '..LyttleBit'

        umbrella_folder_name = '00-{}'.format(self['LB_PROJECT']['name'])
        branch = self['LB_PROJECT']['branch']
        project_name = self['LB_PROJECT']['name']

        stage = ''
        if 'stage' in self['LB_PROJECT'] and self['LB_PROJECT']['stage'] != 'prod':
            # skips stage when stage is prod
            stage = '{}/'.format(self['LB_PROJECT']['stage'])

        self['working_folder'] = '{}'.format(lbworking_name)
        self['umbrella-folder'] = 'code/{}'.format(umbrella_folder_name)
        self['code-folder']    = 'code/{}/{}/{}'.format(umbrella_folder_name, branch, project_name)
        self['script-folder']  = 'code/{}/{}'.format( umbrella_folder_name, branch)
        self['db-folder']      = 'code/{}/{}/{}/db'.format( umbrella_folder_name, branch, project_name)
        self['sql-folder']     = 'code/{}/{}/{}/db/sql'.format( umbrella_folder_name, branch, project_name)
        self['web-folder']     = 'code/{}/{}/{}/web'.format( umbrella_folder_name, branch, project_name)
        self['admin-folder']   = 'code/{}/{}/{}/admin'.format( umbrella_folder_name, branch, project_name)

        self['con-fig-folder'] = 'projects/{}/common/config'.format( project_name)
        self['temp-lates-folder'] = 'projects/{}/common/templates'.format( project_name)
        self['config-folder']  = 'projects/{}/custom/config'.format( project_name)
        self['templates-folder'] = 'projects/{}/custom/templates'.format( project_name)
        self['compiled-folder'] = 'projects/{}/expanded'.format( project_name)
        self['expanded-folder'] = 'projects/{}/expanded'.format( project_name)
        self['merged-folder']  = 'projects/{}/expanded'.format( project_name)
        self['custom-folder']  = 'projects/{}/custom'.format( project_name)
        self['common-folder']  = 'projects/{}/common'.format( project_name)

        self['log-folder']     = 'projects/{}/logs'.format( project_name)
        self['shared-folder']  = 'shared'
        self['projects-folder'] = 'projects'
        self['temp-folder']    = 'temp'

        #### for conveniece push some vars into memory


    def setEnviron(self):
        # does nothing in this class see AppSettingsTest
        return self

    def load(self, key, default):
        rc = os.getenv(key) or json.dumps(default)

        rc = json.loads(rc)
        return rc

    def getEnvJSON(self):
        rc = {}
        for key in os.environ:
            # print('item', key)
            if key.startswith('LB_'):
                rc[key] = os.environ[key]
        return rc

    def getModels(self):
        rc = []
        for key in self:
            if key.endswith('_MODEL'):
                print(key, ' is ', self[key])
                rc.append(self[key])
        return rc

    def getHomeFolder(self):
        return str(Path.home())

    def getWorkingFolder(self):
        rc = '{}/{}'.format(self.getHomeFolder(),self['working_folder'])
        return rc

    def getUmbrellaFolder(self):
        return '00-{}'.format(self['LB_PROJECT']['name'])

    def getStageFolder(self):
        rc = '{}/{}/{}'.format(self.getHomeFolder(),self['working_folder'], self['LB_PROJECT']['stage'])
        return rc

    def getAppFolder(self):
        '''
               returns path to resource folder in the source code
               suffix can be a folder name or a file name
               '''
        rc = os.getcwd()
        print('cwd', rc)

        if rc.endswith('_app'):
            return rc
        else:
            rc = '{}/_app'.format(rc)

        # if rc.endswith('_app'):
        #    rc = rc.replace('_app', '_res')

        # if suffix != None:
        #    rc = '{}/{}'.format(rc, suffix)
        #print('getAppFolder', rc)
        return rc

    def getResourceFolder(self, suffix=None):
        '''
        returns path to resource folder in the source code
        suffix can be a folder name or a file name
        '''
        rc = os.getcwd()
        # print('getResourceFolder',rc)

        if not (rc.endswith('_app' or rc.endswith('_res'))):
            rc = '{}/_res'.format(rc)

        if rc.endswith('_app'):
            rc = rc.replace('_app', '_res')

        if suffix != None:
            rc = '{}/{}'.format(rc, suffix)

        return rc

    def getAppFolders(self):
        rc = {}
        for key in self:
            if 'projects/' not in self[key]:
                rc[key] = self[key]
            if 'code/' not in self[key]:
                rc[key] = self[key]
        return rc

    def getProjectFolders(self):
        rc = {}
        for key in self:
            if 'projects/' in self[key]:
                rc[key] = self[key]
            if 'code/' in self[key]:
                rc[key] = self[key]
        return rc

    def removeFolders(self, project_folder):
        '''
        deletes a project, folder by folder
        will not delete folder with files
        '''
        if 1 == 1:
            print('removeFolders is diabled')
            return self

        # iterate through all the childern folders of the project
        for key in self.getProjectFolders():
            del_list = []
            # break up the path into a list, strip out blanks/empty items
            parts = [k for k in self.getProjectFolders()[key].split('/') if len(k) > 0]
            parts = parts[::-1]  # reverse list order
            # prepare the deep folder for deletion
            folder_path = '{}/{}'.format(project_folder, self.getProjectFolders()[key])
            folder_path = folder_path.replace('//', '/')  # this is a artifact that must be corrected
            for p in parts:  # step backwards through path
                if len(project_folder) < len(folder_path):
                    print('delete', folder_path)
                    Util().deleteFolder(folder_path)
                # set the parent folded
                folder_path = folder_path.replace('/{}'.format(p), '').replace('//', '/')

        return self

    '''
    def depfolders_exist(self, project_folder):
        rc = True
        for key in self.getProjectFolders():

            if not Util().folder_exists(AppSettings().getFolder(key, project_folder)):

                rc = False
        return rc
    '''

    def createFolders(self):
        for key in self:
            if key.endswith('folder'):
                self.createFolder(self.getFolder(key))

        return self

    def createFolder(self, folder_name):
        if not Util().folder_exists(folder_name):
            # print('folder_name',folder_name)
            Util().createFolder(folder_name)
        return self

    def getFolder(self, key):
        key = key.strip()
        if key == 'working_folder':
            return self.getWorkingFolder()
            #rc = '{}/{}'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))

        elif key == 'test-folder':
            #rc = '{}/{}/test'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))
            return '{}/test'.format(self.getStageFolder())

        elif key == 'temp-folder':
            rc = '{}/temp'.format(self.getStageFolder())
           # rc = '{}/{}/temp'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))

        elif key == 'system-folder':  # should be working_folder
            raise Exception('replace system-folder with work-folder')

        elif key == 'resource-folder':  # deprecated
            raise Exception('resource-folder')

        elif key == 'shared-folder':
            rc = self.getResourceFolder('shared')

        elif key == 'projects-folder':
            # ~/<work-folder-name>/projects
            rc = '{}/projects'.format(self.getStageFolder())
            #rc = '{}/{}/projects'.format(self.getHomeFolder(), self['working_folder'])

        elif key == 'project-folder':
            #rc = '{}/{}/projects/{}'.format(self.getHomeFolder(), self['working_folder'], self['LB_PROJECT']['name'])
            rc = '{}/projects/{}'.format(self.getStageFolder(), self['LB_PROJECT']['name'])

        elif key == 'env-file':
            rc = '{}/projects/{}/.env'.format(self.getWorkingFolder(), self['LB_PROJECT']['name'])

            #rc = '{}/{}/projects/{}/.env'.format(self.getHomeFolder(), self['working_folder'],
            #                                     self['LB_PROJECT']['name'])

        else:
            # project folders
            rc = '{}/{}'.format(self.getStageFolder(),
                                   self.getProjectFolders()[key]
                                   ).replace('//', '/')
            '''
            rc = '{}/{}/{}'.format(self.getHomeFolder(),
                                   self['working_folder'],
                                   self.getProjectFolders()[key]
                                   ).replace('//', '/')
            
            
            '''

        return rc
    '''
       def getFolder(self, key):
        key = key.strip()
        if key == 'working_folder':
            return self.getWorkingFolder()
            #rc = '{}/{}'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))

        elif key == 'test-folder':
            #rc = '{}/{}/test'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))
            return '{}/test'.format(self.getWorkingFolder())

        elif key == 'temp-folder':
            rc = '{}/temp'.format(self.getWorkingFolder())
           # rc = '{}/{}/temp'.format(self.getHomeFolder(), self['working_folder'].replace('//', '/'))

        elif key == 'system-folder':  # should be working_folder
            raise Exception('replace system-folder with work-folder')

        elif key == 'resource-folder':  # deprecated
            raise Exception('resource-folder')

        elif key == 'shared-folder':
            rc = self.getResourceFolder('shared')

        elif key == 'projects-folder':
            # ~/<work-folder-name>/projects
            rc = '{}/projects'.format(self.getWorkingFolder())
            #rc = '{}/{}/projects'.format(self.getHomeFolder(), self['working_folder'])

        elif key == 'project-folder':
            #rc = '{}/{}/projects/{}'.format(self.getHomeFolder(), self['working_folder'], self['LB_PROJECT']['name'])
            rc = '{}/projects/{}'.format(self.getWorkingFolder(), self['LB_PROJECT']['name'])

        elif key == 'env-file':
            rc = '{}/projects/{}/.env'.format(self.getWorkingFolder(), self['LB_PROJECT']['name'])

            #rc = '{}/{}/projects/{}/.env'.format(self.getHomeFolder(), self['working_folder'],
            #                                     self['LB_PROJECT']['name'])

        else:

            rc = '{}/{}/{}'.format(self.getHomeFolder(),
                                   self['working_folder'],
                                   self.getProjectFolders()[key]
                                   ).replace('//', '/')

        return rc
    '''
    def to_interface(self, filename, interface, api_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_interface expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format('{}-{}'.format(parts[0], interface), 'interface-{}'.format(api_method), parts[2],
                                    'json')

    def to_api(self, filename, api_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_api expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format(parts[0], 'table-api-{}'.format(api_method), parts[2], 'json')

    def to_test(self, filename, test_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_test expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format(parts[0], 'table-{}-test'.format(test_method), parts[2], 'json')

    def to_tmpl(self, filename, source_key='temp-lates-folder'):
        parts = filename.split('.')
        # print('app_settings', parts)
        if len(parts) != 4:
            raise Exception('to_tmpl expects a 4 part file name not {}'.format(filename))
        # return self.file_name_to(filename, 'tmpl')
        # print('to_tmpl', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl'))
        f = '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')
        # print('source key', source_key,self.getFolder(source_key))
        if Util().file_exists(self.getFolder(source_key), f):
            return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')
        return '{}.{}.{}'.format(parts[1], parts[2], 'tmpl')

    '''
        def to_tmpl(self, filename):
        return self.file_name_to(filename, 'tmpl')
    '''

    def to_tmpl_expected(self, filename):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('Expected 4 parts in the filename {}'.format(filename))
        return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')

    def to_cmpl(self, filename):
        # return self.file_name_to(filename, 'tmpl-compiled')
        # return self.file_name_to(filename, 'tmpl')
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_cmpl expects a 4 part file name not {}'.format(filename))
        # return self.file_name_to(filename, 'tmpl')
        # print('to_cmpl', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl'))
        return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')

    def to_merged(self, filename):
        # print('to_merged', filename, self.file_name_to(filename, 'tmpl-compiled-merged'))
        # return self.file_name_to(filename, 'tmpl-compiled-merged')
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_merged expects a 4 part file name not {}'.format(filename))
        # return self.file_name_to(filename, 'tmpl')
        # print('to_merged', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2],'tmpl'))
        return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')

    def file_name_to(self, filename, to_type):
        rc = ''
        types = ['db-api-table-table', 'role-create', 'function', 'table-api-insert', 'table-api-update',
                 'table-api-select']
        ends = ['json', 'tmpl', 'tmpl-compiled', 'tmpl-compiled-merged', 'tmpl-compiled-merged-sql']
        group = ['pg', 'sh']
        '''
        <name>.<type>.<action>.<database>.
        table-api-create.pg
        db-api-table-table.pg
        role-create.pg
        function.pg

        | from                                   | to
        | users.db-api-table-table.pg.json._DEP                    | db-api-table-table.pg.tmpl
        | users.table.pg.json._DEP                    | users.table-api-update.json, 
        |                                        | users.table-api-select.json,
        |                                        | users.table-api-insert.json
        | db-api-table-table.pg.tmpl                          | N/A
        | users.db-api-table-table.pg.json._DEP                    | users.db-api-table-table.pg.tmpl
        | users.db-api-table-table.pg.tmpl                    | users.db-api-table-table.pg.tmpl.compiled
        | users.db-api-table-table.pg.tmpl                    | users.db-api-table-table.pg.tmpl.compiled.merged
        | users.db-api-table-table.pg.tmpl.compiled.merged    | users.db-api-table-table.pg.tmpl.compiled.merged.sql
        | name.table-api-update.pg.json          | 
        | anonymous.role-create.pg.json          | 
        | get_id.function.pg.json                | 

        '''
        # <name>.<type>.<database>.<end>
        parts = filename.split('.')
        # print('parts', parts)
        # classify filename
        name = None
        type = None
        database = None
        end = None

        if len(parts) == 3:  # type.database.end ... templates with no name (defaults)
            name = None
            type = parts[0]
            database = parts[1]
            end = parts[-1]
            # print('split', parts)
            raise Exception('Not a convertable file name ({})'.format(filename))
        elif len(parts) == 4:  # name.type.database.end
            name = parts[0]
            type = parts[1]
            database = parts[2]
            end = parts[-1]
        else:
            raise Exception('Unrecognized file parts! {}'.format(parts))

        if database not in group:
            raise Exception('{} is not an expected database type.'.format(to_type))

        # if to_type not in ends:
        #    raise Exception('{} is not an expected to-type.'.format(to_type))

        if database == 'pg' and end == 'json':
            if to_type == 'tmpl':
                rc = '{}.{}.{}.{}'.format(name, type, database, to_type)
            elif to_type == 'json':
                rc = '{}.{}.{}.{}'.format(name, type, database, to_type)
            elif to_type == 'tmpl-compiled':
                rc = '{}.{}.{}.{}'.format(name, type, database, to_type)
            elif to_type == 'tmpl-compiled-merged':
                rc = '{}.{}.{}.{}'.format(name, type, database, to_type)
            elif to_type == 'interface-select':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            elif to_type == 'interface-upsert':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            elif to_type == 'table-api-select':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            elif to_type == 'table-api-update':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            elif to_type == 'table-api-insert':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            elif to_type == 'table-api-delete':
                rc = '{}.{}.{}.{}'.format(name, to_type, database, end)
            else:
                raise Exception('Not an available conversion')
        else:
            rc = filename

        # print('A rc', rc)
        # print('to_type', to_type)
        # template only, switch to default when template doesnt exist
        if to_type == 'tmpl':
            # print('type',type )
            if type == 'function':  # function has to have a custom template
                # if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                    raise Exception('{} not found!'.format(rc))
            else:
                # if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                # print('B here ', rc, self.getFolder('expanded-folder'))
                if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                    rc = '{}.{}.{}'.format(type, database, to_type)

            # print('rc', rc)

        return rc

class AppSettingsTest(AppSettings):
    '''
    production folders under ~/<work-folder-name>
    '''
    def __init__(self):
        super().__init__()
        # ~/<work-folder-name>/projects/<project-name>/

    def setEnviron(self):
        print('setEnviron')
        # does nothing in this class see AppSettingsTest
        self['LB_PROJECT']['name']= 'register'
        self['LB_PROJECT']['prefix'] ='reg'
        self['LB_PROJECT']['stage']= 'testing'
        self['LB_PROJECT']['owner']= 'sillyrabit'
        self['LB_PROJECT']['branch'] = '#00.testing.branch'

        #
        os.environ['LB_PROJECT_name'] = self['LB_PROJECT']['name']
        os.environ['LB_PROJECT_prefix'] = self['LB_PROJECT']['prefix']
        os.environ['LB_PROJECT_stage'] = self['LB_PROJECT']['stage']
        os.environ['LB_PROJECT_owner'] = self['LB_PROJECT']['owner']
        os.environ['LB_PROJECT_branch'] = self['LB_PROJECT']['branch']

def main():
    from util import Util
    # from mockup_test_data import   MockupData

    print('* Test AppSettings')
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()
    #appSettings = AppSettingsTest().createFolders()
    # pprint(appSettings)

    print('- Folders')
    for key in appSettings:
        if key.endswith('-folder'):
            print(key, ' is ', appSettings.getFolder(key))
            assert appSettings.getFolder(key).startswith('/Users/')
            assert os.path.isdir('{}'.format(appSettings.getFolder(key)))

    print('- Models')
    for key in appSettings:
        if key.endswith('_MODEL'):
            print(key, ' is ', appSettings[key])
            assert type(appSettings[key]) == dict
            assert 'username' in appSettings[key]
            assert 'role' in appSettings[key]
            assert 'password' in appSettings[key]

    print('- Users')
    for key in appSettings:
        if key.endswith('_USER'):
            print(key, ' is ', appSettings[key])
            assert type(appSettings[key]) == dict
            assert 'app_id' in appSettings[key]
            assert re.match('[a-zA-Z-_]+@[0-9\.]+', appSettings[key]['app_id'])
            assert 'type' in appSettings[key]
            assert 'username' in appSettings[key]
            assert 'password' in appSettings[key]
    # print('models', appSettings.getModels())
    print('- Project')
    for key in appSettings:
        if key.endswith('_PROJECT'):
            print(key, ' is ', appSettings[key])
            assert type(appSettings[key]) == dict
            assert 'name' in appSettings[key]
            assert 'stage' in appSettings[key]
            assert 'prefix' in appSettings[key]
            assert 'owner' in appSettings[key]
            assert 'branch' in appSettings[key]
    print('- Environment')
    for key in appSettings:
        if key.endswith('_ENV'):
            print(key, ' is ', appSettings[key])
            assert type(appSettings[key]) == dict
            assert 'working_folder' in appSettings[key]
            assert 'data_folder' in appSettings[key]

    print('getStageFolder', appSettings.getStageFolder())

    #pprint(appSettings)

    os.environ['LB-TESTING'] = '0'



if __name__ == "__main__":
    main()
