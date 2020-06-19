import os
from pathlib import Path
from util import Util
from dotenv import load_dotenv
import shutil
import json
class AppSettings():
    '''
    production folders under ~/<work-folder-name>
    '''
    def __init__(self):
        #~/<work-folder-name>/projects/<project-name>/

        load_dotenv()
        #### LOCAL
        os.environ['LB_ENV']= self.lbenv = os.getenv('LB_ENV') or 'dev'
        os.environ['LB_WORKING_NAME']= self.lbworking_name = os.getenv('LB_WORKING_NAME') or '..LyttleBit'

        ######### PASSWORDS
        os.environ['LB_JWT_PASSWORD']=self.lbjwt_password =  os.getenv('LB_JWT_PASSWORD') or 'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG'
        os.environ['LB_DB_PASS']=self.lbdb_password =  os.getenv('LB_DB_PASS') or self.lbjwt_password
        os.environ['LB_POSTGRES_PASSWORD'] = self.lbpostgres_password = os.getenv('LB_POSTGRES_PASSWORD') or self.lbjwt_password
        os.environ['LB_SECRET_PASSWORD'] = self.lbsecret_password = os.getenv('LB_SECRET_PASSWORD') or self.lbjwt_password
        os.environ['LB_WEB_PASSWORD'] = self.lbweb_password = os.getenv('LB_WEB_PASSWORD') or self.lbjwt_password
        #os.environ['LB_WEB_GUEST_PASSWORD'] = self.lbweb_anonymous_password = os.getenv('LB_WEB_GUEST_PASSWORD') or self.lbjwt_password
        os.environ['LB_ADMIN_PASSWORD'] = self.lbadmin_password = os.getenv('LB_ADMIN_PASSWORD') or self.lbjwt_password
        os.environ['LB_ADMIN_GUEST_PASSWORD'] = self.lbadmin_anonymous_password = os.getenv('LB_ADMIN_GUEST_PASSWORD') or self.lbjwt_password
        os.environ['LB_ADMIN_REGISTRAR_PASSWORD'] = self.lbadmin_registrar_password = os.getenv('LB_ADMIN_REGISTRAR_PASSWORD') or self.lbjwt_password

        ######### PROJECT
        # os.environ['LB_PROJECT'] = os.getenv('LB_PROJECT') or '{"name":"register", "prefix":"reg"}'

        self.lb_project = self.load('LB_PROJECT', {"name":"register", "prefix":"reg", "owner":"Wilfongjt"})
        #print('lb_project',self.lb_project)
        os.environ['LB_PROJECT_NAME']=os.getenv('LB_PROJECT_NAME') or self.lb_project['name']
        os.environ['LB_PROJECT_PREFIX']=os.getenv('LB_PROJECT_PREFIX') or self.lb_project['prefix']

        ########## GIT
        self.lb_git = self.load('LB_GIT', {"branch":"#01.initialize.{}".format(self.lb_project['name']), "owner":"Wilfongjt"})
        #print('lb_git',self.lb_git)
        os.environ['LB_GIT_PROJECT']=os.getenv('LB_GIT_PROJECT') or self.lb_project['name']
        #self.lbgit_project = os.getenv('LB_GIT_PROJECT') or self.lb_project['name']
        # os.environ['LB_BRANCH']=self.lbbranch = os.getenv('LB_BRANCH') or '#01.initialize.{}'.format(self.lbproject_name)
        os.environ['LB_BRANCH']=os.getenv('LB_BRANCH') or '#01.initialize.{}'.format(self.lb_project)
        #os.environ['LB_GIT_OWNERNAME']=self.lbgit_owner= os.getenv('LB_GIT_OWNERNAME') or 'Wilfongjt'
        os.environ['LB_GIT_OWNERNAME']=os.getenv('LB_GIT_OWNERNAME') or 'Wilfongjt'

        ######### APPLICATION
        os.environ['LB_APP_NAME'] = os.getenv('LB_APP_NAME') or self.lb_project['name']
        os.environ['LB_APP_PREFIX'] = os.getenv('LB_APP_PREFIX') or self.lb_project['prefix']
        #os.environ['LB_APP_NAME']=self.lbapp_name = os.getenv('LB_APP_NAME') or self.lb_project['name']
        #os.environ['LB_APP_PREFIX']=self.lbapp_prefix = os.getenv('LB_APP_PREFIX') or self.lb_project['prefix']
        #
        os.environ['LB_REGISTER_JWT'] = os.getenv('LB_REGISTER_JWT') or '{"name":"jwt@register.com","password":"?1?!????","role":"jwt"}'
        os.environ['LB_REGISTER_ANONYMOUS'] = os.getenv('LB_REGISTER_ANONYMOUS') or '{"name":"anonymous@register.com","password":"?1?!????","role":"anonymous"}'
        os.environ['LB_REGISTER_EDITOR'] = os.getenv('LB_REGISTER_EDITOR') or '{"name":"editor@register.com","password":"?1?!????","role":"editor"}'
        os.environ['LB_REGISTER_REGISTRAR'] = os.getenv('LB_REGISTER_REGISTRAR') or '{"name":"registrar@register.com","password":"?1?!????","role":"registrar"}'

        self.lbregister_jwt = json.loads(os.environ['LB_REGISTER_JWT'])
        self.lbregister_anonymous = json.loads(os.environ['LB_REGISTER_GUEST'])
        self.lbregister_editor = json.loads(os.environ['LB_REGISTER_EDITOR'])
        self.lbregister_registrar = json.loads(os.environ['LB_REGISTER_REGISTRAR'])

        os.environ['LB_WEB_GUEST_PASSWORD']=self.lbapp_anonymous_password = os.getenv('LB_WEB_GUEST_PASSWORD') or '?1?!????'
        os.environ['LB_ADMIN_REGISTRAR_NAME']=self.lbapp_registrar_name= os.getenv('LB_ADMIN_REGISTRAR_NAME') or self.lb_git['owner']
        os.environ['LB_ADMIN_REGISTRAR_PASSWORD'] = self.lbapp_registrar_password = os.getenv('LB_ADMIN_REGISTRAR_PASSWORD') or '?1?!????'

        os.environ['LB_WEB_GUEST_ROLE'] = self.lbweb_anonymous_role = os.getenv('LB_WEB_ANONYMOUS_ROLE') or 'anonymous'

        ######### DATABASE
        os.environ['LB_DATA_FOLDER_NAME']=self.lbdata_folder_name = os.getenv('LB_DATA_FOLDER_NAME') or '.data'
        os.environ['LB_DB_TYPE']=self.lbdb_type = os.getenv('LB_DB_TYPE') or 'postgres'
        os.environ['LB_DB_TYPE_ABBR']=self.lbdb_type_abbr = os.getenv('LB_DB_TYPE_ABBR') or 'pg'

        os.environ['LB_DB_PREFIX']=self.lbdb_prefix = os.getenv('LB_DB_PREFIX') or self.lb_project['prefix']

        self.lbdata_folder = os.getenv('LB_DATA_FOLDER') or '{}/.data/{}_db'.format(self.getHomeFolder(), self.lb_project['prefix'])

        ######### Code
        self.lbcode_folder = os.getenv('LB_CODE_FOLDER') or '{}/{}/code'.format(self.getHomeFolder(), self.lbworking_name)
        self.working_folder_name = '{}'.format(self.lbworking_name)
        self.project_folder_name = '{}-{}'.format(self.lb_project['name'], self.lbenv)

        self.umbrella_folder_name = '01-{}'.format(self.lb_git['name'])
        if not Util().folder_exists(self.lbcode_folder):
            Util().createFolder(self.lbcode_folder)

        if self.lbenv != 'prod':
            # switch to a disposable folder
            self.working_folder_name = '{}'.format(self.lbworking_name)
            self.project_child_folders = {
                'code-folder': 'code/{}/{}/{}'.format(self.umbrella_folder_name, self.lb_git['branch'], self.lb_git['name']),
                'script-folder': 'code/{}/{}'.format(self.umbrella_folder_name, self.lb_git['branch']),
                'db-folder': 'code/{}/{}/{}/db'.format(self.umbrella_folder_name, self.lb_git['branch'], self.lb_git['name']),
                'sql-folder': 'code/{}/{}/{}/db/sql'.format(self.umbrella_folder_name, self.lb_git['branch'], self.lb_git['name']),
                'web-folder': 'code/{}/{}/{}/web'.format(self.umbrella_folder_name, self.lb_git['branch'], self.lb_git['name']),
                'admin-folder': 'code/{}/{}/{}/admin'.format(self.umbrella_folder_name, self.lb_git['branch'], self.lb_git['name']),

                'con-fig-folder': 'projects/{}/common/config'.format( self.project_folder_name),
                'temp-lates-folder': 'projects/{}/common/templates'.format(self.project_folder_name),
                'config-folder': 'projects/{}/custom/config'.format(self.project_folder_name),
                'templates-folder': 'projects/{}/custom/templates'.format(self.project_folder_name),
                'compiled-folder': 'projects/{}/expanded'.format(self.project_folder_name),
                'expanded-folder': 'projects/{}/expanded'.format(self.project_folder_name),
                'merged-folder': 'projects/{}/expanded'.format(self.project_folder_name),
                'custom-folder': 'projects/{}/custom'.format(self.project_folder_name),
                'common-folder': 'projects/{}/common'.format(self.project_folder_name),

                'log-folder': 'projects/{}/logs'.format(self.project_folder_name),
                'shared-folder': 'shared',
                'projects-folder': 'projects',
                'temp-folder': 'temp'
               }

            #print('Environ', self.getEnvJSON())

    def load(self, key, default):
        rc =  os.getenv(key) or json.dumps(default)

        rc = json.loads(rc)
        return rc

    def getEnvJSON(self):
        rc = {}
        for key in os.environ:
            #print('item', key)
            if key.startswith('LB_'):
                rc[key]= os.environ[key]
        return rc

    def getHomeFolder(self):
        return str(Path.home())

    def getAppFolder(self):
        '''
               returns path to resource folder in the source code
               suffix can be a folder name or a file name
               '''
        rc = os.getcwd()
        print('cwd',rc)

        if rc.endswith('_app'):
            return rc
        else:
            rc = '{}/_app'.format(rc)

        #if rc.endswith('_app'):
        #    rc = rc.replace('_app', '_res')

        #if suffix != None:
        #    rc = '{}/{}'.format(rc, suffix)
        print('getAppFolder', rc)
        return rc

    def getResourceFolder(self, suffix=None):
        '''
        returns path to resource folder in the source code
        suffix can be a folder name or a file name
        '''
        rc = os.getcwd()
        #print('getResourceFolder',rc)

        if not (rc.endswith('_app' or rc.endswith('_res'))):
            rc = '{}/_res'.format(rc)

        if rc.endswith('_app'):
            rc = rc.replace('_app','_res')

        if suffix != None:
            rc ='{}/{}'.format(rc, suffix)

        return rc

    def getAppFolders(self):
        rc = {}
        for key in self.project_child_folders:
            if 'projects/' not in self.project_child_folders[key]:
                rc[key] = self.project_child_folders[key]
            if 'code/' not in self.project_child_folders[key]:
                rc[key] = self.project_child_folders[key]
        return rc

    def getProjectFolders(self):
        rc = {}
        for key in self.project_child_folders:
            if 'projects/' in self.project_child_folders[key]:
                rc[key] = self.project_child_folders[key]
            if 'code/' in self.project_child_folders[key]:
                rc[key] = self.project_child_folders[key]
        return rc

    def removeFolders(self, project_folder):
        '''
        deletes a project, folder by folder
        will not delete folder with files
        '''
        if 1==1:
            print('removeFolders is diabled')
            return self

        #iterate through all the childern folders of the project
        for key in self.getProjectFolders():
            del_list = []
            # break up the path into a list, strip out blanks/empty items
            parts = [k for k in self.getProjectFolders()[key].split('/') if len(k)>0]
            parts = parts[::-1] # reverse list order
            # prepare the deep folder for deletion
            folder_path = '{}/{}'.format(project_folder,  self.getProjectFolders()[key] )
            folder_path = folder_path.replace('//','/') # this is a artifact that must be corrected
            for p in parts: # step backwards through path
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

        working_folder = self.getFolder('working-folder')
        # create app folders
        self.createAppFolders(working_folder)
        # create project folders
        self.createProjectFolders(working_folder)

        return self

    def createAppFolders(self, folder_name=None):
        if folder_name == None:
            folder_name =  self.getFolder('working-folder')

        #self.getCodeFolder() # creates if doesnt exist

        for key in self.getAppFolders():
            self.createFolder('{}/{}'.format(folder_name, self.getAppFolders()[key]))

        return self

    def createProjectFolders(self, folder_name=None):
        if folder_name == None:
            #folder_name = self.getFolder('projects-folder')
            folder_name = self.getFolder('working-folder')

        for key in self.getProjectFolders():
            self.createFolder('{}/{}'.format(folder_name, self.getProjectFolders()[key]))

        return self

    def createFolder(self, folder_name):
        if not Util().folder_exists(folder_name):
            #print('folder_name',folder_name)
            Util().createFolder(folder_name)
        return self

    def getFolder(self, key):
        key = key.strip()
        if key == 'working-folder':
            rc = '{}/{}'.format(self.getHomeFolder(), self.working_folder_name).replace('//','/')

        elif key == 'test-folder':
            rc = '{}/{}/test'.format(self.getHomeFolder(), self.working_folder_name).replace('//', '/')

        elif key == 'temp-folder':
            rc = '{}/{}/temp'.format(self.getHomeFolder(), self.working_folder_name).replace('//', '/')

        elif key == 'system-folder': #should be working-folder
            raise Exception('replace system-folder with work-folder')

        elif key == 'resource-folder': # deprecated
            raise Exception('resource-folder')

        elif key == 'shared-folder':
            rc = self.getResourceFolder('shared')
            #rc = '{}/{}/shared'.format(self.getHomeFolder(), self.working_folder_name).replace('//', '/')

        elif key == 'projects-folder':
            # ~/<work-folder-name>/projects
            rc = '{}/{}/projects'.format(self.getHomeFolder(),self.working_folder_name )

        elif key == 'project-folder':

            rc = '{}/{}/projects/{}'.format(self.getHomeFolder(), self.working_folder_name, self.project_folder_name)

        elif key == 'env-file':

            rc = '{}/{}/projects/{}/.env'.format(self.getHomeFolder(), self.working_folder_name, self.project_folder_name)

        #elif key == 'script-folder':
        #    #rc = 'code/01-{}'.format(self.lbproject_name)
        #    rc = '{}/{}/01-{}'.format(self.getHomeFolder(), self.working_folder_name, self.lbproject_name)

        else:

            rc = '{}/{}/{}'.format(self.getHomeFolder(),
                                            self.working_folder_name,
                                            self.getProjectFolders()[key]
                                            ).replace('//', '/')

        return rc

    def to_interface(self, filename, interface, api_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_interface expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format( '{}-{}'.format(parts[0],interface), 'interface-{}'.format( api_method), parts[2], 'json')

    def to_api(self, filename, api_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_api expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format( parts[0], 'table-api-{}'.format(api_method), parts[2], 'json')
    '''
        def to_api(self, filename, api_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_api expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format( parts[0], 'table-api-{}'.format(api_method), parts[2], 'json')

    '''
    def to_test(self, filename, test_method):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_test expects a 4 part file name not {}'.format(filename))

        return '{}.{}.{}.{}'.format(parts[0], 'table-{}-test'.format(test_method), parts[2], 'json')

    def to_tmpl(self, filename, source_key='temp-lates-folder'):
        parts = filename.split('.')
        #print('app_settings', parts)
        if len(parts) != 4:
            raise Exception('to_tmpl expects a 4 part file name not {}'.format(filename))
        # return self.file_name_to(filename, 'tmpl')
        #print('to_tmpl', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl'))
        f = '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')
        # print('source key', source_key,self.getFolder(source_key))
        if Util().file_exists(self.getFolder(source_key), f):
            return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')
        return '{}.{}.{}'.format( parts[1], parts[2], 'tmpl')

    '''
        def to_tmpl(self, filename):
        return self.file_name_to(filename, 'tmpl')
    '''
    def to_tmpl_expected(self, filename):
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('Expected 4 parts in the filename {}'.format(filename))
        return '{}.{}.{}.{}'.format(parts[0],parts[1],parts[2],'tmpl')

    def to_cmpl(self, filename):
        #return self.file_name_to(filename, 'tmpl-compiled')
        #return self.file_name_to(filename, 'tmpl')
        parts = filename.split('.')
        if len(parts) != 4:
            raise Exception('to_cmpl expects a 4 part file name not {}'.format(filename))
        # return self.file_name_to(filename, 'tmpl')
        #print('to_cmpl', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl'))
        return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], 'tmpl')

    def to_merged(self, filename):
        #print('to_merged', filename, self.file_name_to(filename, 'tmpl-compiled-merged'))
        #return self.file_name_to(filename, 'tmpl-compiled-merged')
        parts = filename.split('.')
        if len(parts) !=  4:
            raise Exception('to_merged expects a 4 part file name not {}'.format(filename))
        #return self.file_name_to(filename, 'tmpl')
        #print('to_merged', '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2],'tmpl'))
        return '{}.{}.{}.{}'.format(parts[0], parts[1], parts[2],'tmpl')

    def file_name_to(self, filename, to_type):
        rc = ''
        types = ['db-api-table-table', 'role-create', 'function', 'table-api-insert', 'table-api-update', 'table-api-select']
        ends = ['json', 'tmpl', 'tmpl-compiled', 'tmpl-compiled-merged', 'tmpl-compiled-merged-sql']
        group = ['pg','sh']
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
        #print('parts', parts)
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
            #print('split', parts)
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

        #if to_type not in ends:
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

        #print('A rc', rc)
        #print('to_type', to_type)
        # template only, switch to default when template doesnt exist
        if to_type == 'tmpl':
            #print('type',type )
            if type == 'function':  # function has to have a custom template
                #if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                    raise Exception('{} not found!'.format(rc))
            else:
                #if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                #print('B here ', rc, self.getFolder('expanded-folder'))
                if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                    rc = '{}.{}.{}'.format(type, database, to_type)

            #print('rc', rc)
        '''
        if to_type == 'tmpl':
            print('type',type )
            if type == 'function':  # function has to have a custom template
                #if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                if not Util().file_exists(self.getFolder('expanded-folder'), rc):
                    raise Exception('{} not found!'.format(rc))
            else:
                #if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                print('B here ', rc, self.getFolder('expanded-folder'))
                if not Util().file_exists(self.getFolder('temp-lates-folder'), rc):
                    rc = '{}.{}.{}'.format(type, database, to_type)
        elif to_type == 'tmpl-compiled':
            rc = '{}.{}.{}.{}'.format(name, type, database, 'tmpl-compiled')
        elif to_type == 'tmpl-compiled-merged':
            rc = '{}.{}.{}.{}'.format(name, type, database, 'tmpl-compiled-merged')
        # print('B rc', rc)
        '''

        '''    
        if type == 'db-api-table-table' and database == 'pg' and end == 'json':

            if to_type == 'role-create':
                rc = '{}.{}.{}.{}'.format(name, 'role-create', database, end)

            elif to_type == 'function':
                print('undefined A')

            elif to_type == 'table-api-insert':
                print('undefined B')

            elif to_type == 'table-api-update':
                print('undefined C')

            elif to_type == 'table-api-select':
                print('undefined D')

            elif to_type == 'table':
                print('undefined E')
        '''
        return rc


class AppSettingsTest(AppSettings):
    '''
    use for testing
    reroutes the dev
    '''
    '''
    dev folders under ~/<work-folder-name>/testing 
    '''
    def __init__(self):
        super().__init__()
        #print('Using AppSettingsTest')
        self.lbcode_folder = os.getenv('LB_CODE_FOLDER') or '{}/{}/testing/code'.format(self.getHomeFolder(), self.lbworking_name)

        #self.lbcode_folder = os.getenv('LB_CODE_FOLDER') or '{}/{}/testing/code/01-{}/{}'.format(self.getHomeFolder(), self.lbworking_name, self.lbproject_name, self.lbproject_name)
        #self.lbumbrella_folder = os.getenv('LB_UMBRELLA_FOLDER') or '{}/{}/testing/code/01-{}'.format(self.getHomeFolder(), self.lbworking_name, self.lbproject_name)
    '''
    def getCodeFolder(self, suffix=None):
        
        #returns path to resource folder in the source code
        #suffix can be a folder name or a file name

        rc = self.lbcode_folder

        if suffix != None:
            rc = '{}/{}'.format(rc, suffix)

        if not Util().folder_exists(rc):
            Util().createFolder(rc)

        return rc
    '''
    def getFolder(self, key):
        key = key.strip()
        if key == 'working-folder':
            rc = '{}/{}/testing'.format(self.getHomeFolder(), self.working_folder_name).replace('//','/')

        elif key == 'testing-folder':
            rc = '{}/{}/testing'.format(self.getHomeFolder(), self.working_folder_name).replace('//','/')

        elif key == 'temp-folder':
            rc = '{}/{}/testing/temp'.format(self.getHomeFolder(), self.working_folder_name).replace('//', '/')

        elif key == 'system-folder': #should be working-folder
            raise Exception('replace system-folder with work-folder')

        elif key == 'resource-folder': # deprecated
            raise Exception('resource-folder')

        elif key == 'shared-folder':
            rc = self.getResourceFolder('shared')
            #rc = '{}/{}/testing/shared'.format(self.getHomeFolder(), self.working_folder_name).replace('//', '/')

        elif key == 'projects-folder':
            # ~/<work-folder-name>/projects
            rc = '{}/{}/testing/projects'.format(self.getHomeFolder(),self.working_folder_name )

        elif key == 'project-folder':

            rc = '{}/{}/testing/projects/{}'.format( self.getHomeFolder(), self.working_folder_name, self.project_folder_name)

        elif key == 'env-file':

            rc = '{}/{}/testing/projects/{}/.env'.format(self.getHomeFolder(), self.working_folder_name, self.project_folder_name)

        #elif key == 'script-folder':
        #    # rc = 'code/01-{}'.format(self.lbproject_name)
        #    rc = '{}/{}/testing/code/01-{}'.format(self.getHomeFolder(), self.working_folder_name, self.lbproject_name)
        #    rc = '{}'.format(self.lbumbrella_folder)

        else:
            rc = '{}/{}/testing/{}'.format(str(Path.home()),
                                            self.working_folder_name,
                                            self.getProjectFolders()[key]
                                            ).replace('//', '/')

        return rc
    '''
    def removeFolders(self):
        
        #remove all files and folders in the testing folder
        

        dir_path = self.getFolder('testing-folder')
        if not Util().folder_exists(dir_path):
            return self
        folderlist = Util().getFolderList(dir_path)
        folderlist = [fld for fld in folderlist if not 'code' in fld ]
        try:
            # remove some folders
            for p in folderlist:
                shutil.rmtree(p)


        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        return self
    '''


def main():
    from util import Util
    #from mockup_test_data import   MockupData

    print('* Test AppSettings')
    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()
    home_folder = appSettings.getHomeFolder()

    #MockupData().run()

    #os.environ['LB_ENV']='dev'
    #os.environ['LB_WORKING_NAME']='..LyttleBit'
    #os.environ['LB_PROJECT_NAME']='example'

    lbenv = os.getenv('LB_ENV') or 'dev'
    lbworking_name = os.getenv('LB_WORKING_NAME') or '..LyttleBit'
    #lbproject_name = os.getenv('LB_PROJECT_NAME') or 'example'
    lb_project = {"name":"register", "prefix":"reg", "owner":"Wilfongjt"}

    working_folder_name = '{}'.format(lbworking_name)
    project_folder_name = '{}-{}'.format(lb_project['name'], lbenv)

    print('  - env                 |', lbenv , appSettings.lbenv)
    print('  - working_name        |', lbworking_name, appSettings.lbworking_name)
    print('  - work-folder-name    |', working_folder_name, appSettings.working_folder_name)
    print('  - project_name        |', lb_project['name'], appSettings.lb_project['name'])
    print('  - project_folder_name |', project_folder_name, appSettings.project_folder_name)
    print('  - resource-folder     |', appSettings.getResourceFolder())
    print('  - projectFolders      |', appSettings.getProjectFolders())

    print('metho', appSettings.to_interface('register.table.pg.json','app', 'upsert'))
    assert( appSettings.to_interface('register.table.pg.json','app', 'upsert') == 'register-app.interface-upsert.pg.json')

    assert( appSettings.lbenv in ['dev','test'])
    assert( appSettings.lbworking_name == lbworking_name)
    assert( appSettings.working_folder_name == '{}'.format( lbworking_name))
    assert( appSettings.lb_project['name'] == lb_project['name'])
    assert( appSettings.project_folder_name == project_folder_name)

    if lbenv != 'prod':
        lbworking_name = '{}_{}'.format(lbworking_name , lbenv)
    else:
        exit(0)

    #### Project Folder List
    #print('getProjectFolders', appSettings.getProjectFolders())
    for key in appSettings.getProjectFolders():
        print('  - project folder |', key, appSettings.getProjectFolders()[key])
    assert(appSettings.getProjectFolders() != None )
    assert(len(appSettings.getProjectFolders()) > 0 )
    assert (len(appSettings.getProjectFolders()) < len(appSettings.project_child_folders))

    #prj_folder = ''. #appSettings.getFolder('project-folder') # autopoetic
    prj_folder = '{}/{}/testing/projects/{}'.format(str(Path.home()), working_folder_name, project_folder_name)

    print('  - createFolders')
    appSettings.createFolders()
    print('  - prj_folder', prj_folder, appSettings.getFolder('project-folder'))
    assert(prj_folder == appSettings.getFolder('project-folder'))
    assert(Util().folder_exists(prj_folder))

    #print('temp-folder |', '{}/temp'.format(str(Path.home())).replace('//', '/'), appSettings.getFolder('temp-folder'))

    #print('  - temp-folder', '{}/{}/testing/projects/{}/temp'.format(str(Path.home()), working_folder_name, project_folder_name ).replace('//','/'),appSettings.getFolder('temp-folder'))
    print('  - temp-folder', '{}/{}/testing/temp'.format(str(Path.home()), working_folder_name, project_folder_name ).replace('//','/'),appSettings.getFolder('temp-folder'))

    #print('               ', '{}/{}/projects/{}/temp'.format(str(Path.home()), working_folder_name, project_folder_name ).replace('//','/'))
    assert(appSettings.getFolder('temp-folder') == '{}/{}/testing/temp'.format(str(Path.home()), working_folder_name, project_folder_name ).replace('//','/'))
    print('  - shared-folder', appSettings.getResourceFolder('shared'))
    #print('  - shared-folder',  '{}/{}/shared'.format(str(Path.home()),working_folder_name).replace('//', '/'),appSettings.getFolder('shared-folder'))
    #print('                 ', '{}/{}/shared'.format(str(Path.home()),working_folder_name).replace('//', '/'))
    #assert (appSettings.getFolder('shared-folder') == '{}/{}/testing/shared'.format(str(Path.home()),working_folder_name).replace('//', '/'))
    #assert (appSettings.getFolder('shared-folder') == '{}/{}/shared'.format(str(Path.home()),working_folder_name).replace('//', '/'))

    print('  - projects-folder',  '{}/{}/testing/projects'.format(str(Path.home()),working_folder_name).replace('//', '/'),appSettings.getFolder('projects-folder'))
    assert (appSettings.getFolder('projects-folder') == '{}/{}/testing/projects'.format(str(Path.home()),working_folder_name).replace('//', '/'))

    prj_folder = '{}/{}/testing/projects/{}'.format(str(Path.home()), working_folder_name, project_folder_name).replace('//', '/')
    print('  - project-folder', prj_folder ,appSettings.getFolder('project-folder'))

    assert (appSettings.getFolder('project-folder') == prj_folder)

    print('* create ', prj_folder, appSettings.getFolder('project-folder'))

    for key in appSettings.getProjectFolders():
        print('  -- create key {} value {}'.format(key, appSettings.getFolder(key)))
        assert(Util().folder_exists(appSettings.getFolder(key)))

    #appSettings.removeFolders()
    #print('  - removeFolders', prj_folder)
    #appSettings.removeFolders(prj_folder)
    #assert(not appSettings.folders_exist(prj_folder))

    print('project folders', appSettings.getProjectFolders())

    #assert( appSettings.to_tmpl('db-api-table-table.pg.json') == 'db-api-table-table.pg.tmpl')
    #assert( appSettings.file_name_to('users.db-api-table-table.pg.json._DEP', 'tmpl') == 'users.db-api-table-table.pg.tmpl')
    #assert( appSettings.to_tmpl('users.db-api-table-table.pg.json._DEP') == 'db-api-table-table.pg.tmpl') gets generated
    #assert( appSettings.to_tmpl('users.db-api-table-table.pg.tmpl') == 'db-api-table-table.pg.tmpl') gets generated
    #assert( appSettings.to_tmpl('users.db-api-table-table-api-select.pg.json') == 'db-api-table-dep.table-api-select.pg.tmpl.dep')
    #assert( appSettings.to_tmpl('users.db-api-table-table-api-update.pg.json') == 'db-api-table-dep.table-api-update.pg.tmpl.dep')
    #assert( appSettings.to_tmpl('users.db-api-table-table-api-insert.pg.json') == 'db-api-table-dep.table-api-insert.pg.tmpl.dep')
    #print('to_tmpl',appSettings.to_tmpl('credentials.table.pg.json._DEP'))
    #assert (appSettings.to_tmpl('credentials.db-api-table-table.pg.json._DEP') == 'db-api-table-table.pg.tmpl')
    #assert (appSettings.to_tmpl('credentials.db-api-table-table.pg.tmpl._DEP') == 'db-api-table-table.pg.tmpl')
    #assert (appSettings.to_tmpl('credentials.db-api-table-table-api-select.pg.json') == 'db-api-table-dep.table-api-select.pg.tmpl.dep')
    #assert (appSettings.to_tmpl('credentials.db-api-table-table-api-update.pg.json') == 'db-api-table-dep.table-api-update.pg.tmpl.dep')
    #assert (appSettings.to_tmpl('credentials.db-api-table-table-api-insert.pg.json') == 'db-api-table-dep.table-api-insert.pg.tmpl.dep')

    #filelist = Util().getFileName(appSettings.getFolder('con-fig-folder'))
    #for fn in filelist:
    #    assert()


    # Compiled Templates
    '''
    assert(appSettings.to_cmpl('users.db-api-table-table.pg.json._DEP') == 'users.db-api-table-table.pg.tmpl')
    assert(appSettings.to_cmpl('users.db-api-table-table.pg.tmpl') == 'users.db-api-table-table.pg.tmpl')
    assert (appSettings.to_cmpl('users.db-api-table-table-api-select.pg.json') == 'users.db-api-table-dep.table-api-select.pg.tmpl.dep')
    assert (appSettings.to_cmpl('users.db-api-table-table-api-update.pg.json') == 'users.db-api-table-dep.table-api-update.pg.tmpl.dep')
    assert (appSettings.to_cmpl('users.db-api-table-table-api-insert.pg.json') == 'users.db-api-table-dep.table-api-insert.pg.tmpl.dep')

    assert (appSettings.to_cmpl('credentials.db-api-table-table.pg.json._DEP') == 'credentials.db-api-table-table.pg.tmpl._DEP')
    assert (appSettings.to_cmpl('credentials.db-api-table-table.pg.tmpl._DEP') == 'credentials.db-api-table-table.pg.tmpl._DEP')
    assert (appSettings.to_cmpl('credentials.db-api-table-table-api-select.pg.json') == 'credentials.db-api-table-dep.table-api-select.pg.tmpl.dep._DEP')
    assert (appSettings.to_cmpl('credentials.db-api-table-table-api-update.pg.json') == 'credentials.db-api-table-dep.table-api-update.pg.tmpl.dep._DEP')
    assert (appSettings.to_cmpl('credentials.db-api-table-table-api-insert.pg.json') == 'credentials.db-api-table-dep.table-api-insert.pg.tmpl.dep._DEP')

    assert (appSettings.to_merged('credentials.db-api-table-table.pg.json._DEP') == 'credentials.db-api-table-table.pg.tmpl._DEP')
    assert (appSettings.to_merged('credentials.db-api-table-table.pg.tmpl._DEP') == 'credentials.db-api-table-table.pg.tmpl._DEP')
    assert (appSettings.to_merged(
        'credentials.db-api-table-table-api-select.pg.json') == 'credentials.db-api-table-dep.table-api-select.pg.tmpl.dep._DEP')
    assert (appSettings.to_merged(
        'credentials.db-api-table-table-api-update.pg.json') == 'credentials.db-api-table-dep.table-api-update.pg.tmpl.dep._DEP')
    assert (appSettings.to_merged(
        'credentials.db-api-table-table-api-insert.pg.json') == 'credentials.db-api-table-dep.table-api-insert.pg.tmpl.dep._DEP')
    '''
    # function
    #assert (appSettings.to_tmpl('get_id.function.pg.json') == 'get_id.function.pg.tmpl')
    #assert (appSettings.to_tmpl('get_bad.function.pg.json') == 'get_bad.function.pg.tmpl')

    #print('code-folder',appSettings.getFolder('code-folder'))
    print('code-folder', appSettings.getFolder('code-folder'))
    #assert (appSettings.getFolder('dev-folder')=='')
    '''
    assert( appSettings.to_tmpl('users.db-api-table-table.pg.tmpl.compiled') == 'users.db-api-table-table.pg.tmpl')

    assert( appSettings.to_tmpl('users.db-api-table-table.pg.tmpl.compiled.merged') == 'users.db-api-table-table.pg.tmpl')
    assert( appSettings.to_tmpl('name.db-api-table-table-api-update.pg.json') == 'name.db-api-table-dep.table-api-update.pg.tmpl.dep')
    assert( appSettings.to_tmpl('anonymous.role-create.pg.json') == 'anonymous.role-create.pg.tmpl._DEP')
    assert( appSettings.to_tmpl('get_id.function.pg.json') == 'get_id.function.pg.tmpl')
    '''

    print('getAppFolder', appSettings.getAppFolder())
    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()

    #3,300,000,000,000
    # 10,000