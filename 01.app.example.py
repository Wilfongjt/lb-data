import sys
print(sys.path)
import os
from pathlib import Path
import settings

print('os.getenv', os.getenv('LB_WORKING_FOLDER_NAME'))
print('change projects in .env')
def main():
    from app import App

    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize

    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_initialize import ProjectInitialize

    from project_expand import ProjectExpand
    from project_compile import ProjectCompile

    #from project_merge import ProjectMerge
    from project_move_to_sql import ProjectMoveToSQL
    from project_cleanup import ProjectCleanup
    #from project_organize_files import ProjectOrganizeFiles

    os.environ['LB-TESTING'] = '0'
    os.environ['LB-TESTING'] = '1'

    # check env variable
    for v in os.environ:
        if v.startswith('LB'):
            print(v, os.getenv(v))

    app = App()
    #print('env', app.appSettings.getEnvJSON())
    # load environment variables
    # create app folders,
    # copy stub templates,
    # copy stub configuration files
    # copy system files

    # Folders
    # /<working-folder>
    #     - /<code-folder>
    #     --- /<umbrella-folder>
    #     ----- /<branch-folder>
    #     --------- / <app-folder>
    #     ----------- /db-api-table
    #     ------------- /sql
    #     ----------- /web

    # application setup
    install_app = AppEnvironment()\
        .add(AppCreateFolders())\
        .add(AppInitialize())
    print('env',install_app.appSettings.getEnvJSON())
    # project setup
    setup_project = ProjectEnvironment()\
        .add( ProjectCreateFolders() )\
        .add( ProjectInitialize() )\
        .add( ProjectExpand() )\
        .add( ProjectCompile())
        #.add( ProjectMerge())\
        #.add( ProjectMoveToSQL())
        #.add( ProjectCleanup())
        #.add(Projec#tOrganizeFiles())

    # run the steps
    app.append(install_app)

    app.append(setup_project)

    app.run()

    '''
     setup_project = ProjectEnvironment(project_name='example')\
        .add(ProjectCreateFolders())\
        .add(ProjectConfigurationInitialize())\
        .add(ProjectTemplateInitialize())\
        .add(ProjectConfigurationGenerateAPI())\
        .add(ProjectTemplateCompile())\
        .add(ProjectTemplateMerge())\
        .add(ProjectOrganizeFiles())

    app.append(install_app)

    app.append(setup_project)

    app.run()
    
    '''

if __name__ == "__main__":
    main()