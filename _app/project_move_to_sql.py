from util import Util
from step import Step

import os, sys, stat
'''
file name
.type
.destination
.template identity (tmpl)
'''
class ProjectMoveToSQL(Step):
    def __init__(self):
        super().__init__()

        self.description = ['Rename any file ending in .merged to .sql ',
                            'Control execution of sql by adding numeric prefix',
                            'Overwrites template file with sql file'
                            ]
        self.type_map = {
            'database': {'prefix': '01', 'ext': 'sql'},
            'role': {'prefix': '03', 'ext': 'sql'},
            'validate-function': {'prefix': '04', 'ext': 'sql'},
            'table': {'prefix': '05', 'ext': 'sql'},
            'function': {'prefix': '07', 'ext': 'sql'},
            'table-api-upsert': {'prefix': '09', 'ext': 'sql'},
            'table-api-insert': {'prefix': '09', 'ext': 'sql'},
            'table-api-update': {'prefix': '09', 'ext': 'sql'},
            'table-api-select': {'prefix': '09', 'ext': 'sql'},
            'initialize': {'prefix': '11', 'ext': 'sql'},
            'script-sh': {'prefix': '13', 'ext': 'sh'},
            'dockerfile': {'prefix': '15', 'ext': ''},
            'docker-compose': {'prefix': '17', 'ext': 'yml'},
            'environment': {'prefix': '19', 'ext': 'env'},
            'test': {'prefix': '99', 'ext': 'sql'},
        }

    def getNameOrder(self, filename):
        parts = filename.split('.')
        #print('parts', parts)
        return self.type_map[parts[1]]['prefix']

    def getExt(self, filename):
        parts = filename.split('.')
        return self.type_map[parts[1]]['ext']

    def process(self):
        super().process()
        #temp folder cleanup
        self.getData()
        #self.log('getData {}'.format(self.getData()))

        mrgd_folder = self.appSettings.getFolder('merged-folder')
        prj_folder = self.appSettings.getFolder('project-folder')
        code_folder = self.appSettings.getFolder('code-folder')

        admin_folder = self.appSettings.getFolder('admin-folder')
        web_folder =  self.appSettings.getFolder('web-folder')
        db_folder = self.appSettings.getFolder('db-folder')
        sql_folder = self.appSettings.getFolder('sql-folder')

        script_folder = self.appSettings.getFolder('script-folder')

        self.log('  - {}    {}'.format('env-file', self.appSettings.getFolder('env-file')))
        self.log('  - {} {}'.format('code-folder', code_folder))
        self.log('  - {}  {}'.format('prj_folder', prj_folder))
        self.log('  - {}   {}'.format('db_folder', db_folder))
        self.log('  - {}  {}'.format('sql-folder', sql_folder))
        self.log('  - {}  {}'.format('script-folder', script_folder))
        # make folder in code project
        if not Util().folder_exists(sql_folder):
            #print('sql_folder',sql_folder)
            Util().createFolder(sql_folder)
        # make folder in code project
        if not Util().folder_exists(web_folder):
            #print('sql_folder',web_folder)
            Util().createFolder(web_folder)

        # file_list = Util().getFileList(mrgd_folder, ext='tmpl-compiled-merged')
        file_list = Util().getFileList(mrgd_folder, ext='tmpl')

        #print('file_list', len(file_list),file_list)

        for fn in file_list:
            #Util().deleteFile(temp_folder, fn)
            #print('ProjectMoveToSQL fn', fn)
            fromname = '{}/{}'.format(mrgd_folder, fn)
            toname = '{}/sql/{}.{}'.format(mrgd_folder,
                                       self.getNameOrder(fn),
                                       fn.replace('pg.tmpl',
                                                  self.getExt(fn)))
            parts = fn.split('.')

            if 'dockerfile' in fn:
                if '-db' in fn:
                    fromname = '{}/{}'.format(mrgd_folder, fn)
                    toname = '{}/{}'.format(db_folder,
                                            fn.replace('.dockerfile.dk.tmpl',''))
                if '-web' in fn:
                    fromname = '{}/{}'.format(mrgd_folder, fn)
                    toname = '{}/{}'.format(web_folder, fn.replace('.dockerfile.dk.tmpl', ''))
                if '-admin' in fn:
                    fromname = '{}/{}'.format(mrgd_folder, fn)
                    toname = '{}/{}'.format(admin_folder, fn.replace('.dockerfile.dk.tmpl', ''))

            elif 'docker-compose' in fn:
                fromname = '{}/{}'.format(mrgd_folder, fn)
                toname = '{}/{}.{}'.format(code_folder,
                                           fn.replace('.docker-compose.dc.tmpl', ''),
                                           self.getExt(fn))
            elif 'environment' == parts[1]:
                fromname = '{}/{}'.format(mrgd_folder, fn)
                toname = '{}/{}.{}'.format(code_folder,
                                           fn.replace('.environment.env.tmpl', ''),
                                           self.getExt(fn))
            elif 'script-sh' == parts[1] :
                    fromname = '{}/{}'.format(mrgd_folder, fn)
                    toname = '{}/{}.{}'.format(script_folder,
                                               fn.replace('.script-sh.sh.tmpl', ''),
                                               self.getExt(fn))


            #elif 'initialize' == parts[1] :
            #        fromname = '{}/{}'.format(mrgd_folder, fn)
            #        toname = '{}/{}.{}'.format(sql_folder,
            #                                   fn.replace('.initialize.pg.tmpl', ''),
            #                                   self.getExt(fn))

            else:
                #print('move default fn', fn)
                fromname ='{}/{}'.format(mrgd_folder, fn)
                toname =  '{}/{}.{}'.format(sql_folder,
                                            self.getNameOrder(fn),
                                            fn.replace('pg.tmpl',
                                                       self.getExt(fn) ))
            #print('fromname', fromname)
            #print('toname',toname)

            os.rename(fromname, toname)
            if 'script' in fn:
                #print('set permissions {}'.format(toname))
                #                          -rw-r--r--  1
                os.system('ls -l {}'.format(toname))
                os.chmod(toname, 0o755) # -rwxr-xr-x
                os.system('ls -l {}'.format(toname))

        return self

    #def delete(self, folder, filename):

def main():
    from app_settings import AppSettingsTest
    #from project_expand import ProjectExpand
    #from project_expand import ProjectExpand

    #from mockup_test_data import MockupData
    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_initialize import ProjectInitialize
    from project_expand import ProjectExpand
    from project_compile import ProjectCompile
    from project_merge import ProjectMerge

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()
    # setup mock files
    #MockupData().run()
    # prior steps
    #ProjectExpand()\
    #    .add(ProjectMerge())\
    #    .run()
    # this step
    step = ProjectMoveToSQL()

    ProjectEnvironment()\
        .add(ProjectCreateFolders())\
        .add(ProjectInitialize())\
        .add( ProjectExpand())\
        .add(ProjectCompile())\
        .add(ProjectMerge())\
        .add(step)\
        .run()

    #print('* {}'.format(step.getClassName()))
    #print('  - {}'.format(step.getDescription()))

    mrgd_folder = appSettings.getFolder('merged-folder')
    file_list = Util().getFileList(mrgd_folder, ext='.sql')

    #print('merge folder', mrgd_folder)
    #print('file list', file_list)
    for fn in file_list:
        #print('    - rename ', fn)
        assert(Util().file_exists(mrgd_folder, fn))

    # appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()