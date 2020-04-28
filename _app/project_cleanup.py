from util import Util
from step import Step

class ProjectCleanup(Step):
    def __init__(self):
        super().__init__()


    def description(self):
        return 'Cleanup temp files. '

    def process(self):
        #temp folder cleanup
        self.getData()
        #print('data', self.getData())
        temp_folder = self.getFolder('temp-folder')
        ext_list = ['.compiled', '.tmpl','.json']
        #print('Cleanup ', temp_folder)

        ############
        # templates
        # copy <code-folder>/__resource__/template/<file-name>.tmpl TO <working-folder>/example/template/<file-name>.tmpl
        #ext = 'config.tmpl'
        for ext in ext_list:
            file_list = Util().getFileList(temp_folder, ext=ext)

            for fn in file_list:
                Util().deleteFile(temp_folder, fn)

        return self

def main():
    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize
    from project_environment import ProjectEnvironment

    from util import Util

    step = ProjectCleanup().setWorkingFolder('temp').run()

    print('* {}'.format(step.getClassName()))
    print('  - {}'.format(step.getDescription()))

    '''
    app = AppEnvironment()\
        .add(AppCreateFolders())\
        .add(AppInitialize())\
        .add(ProjectEnvironment())\
        .add(step)\
        .run()
    '''

    filelist = Util().getFileList(step.getFolder('temp-folder'),ext='.compiled')
    print('filelist', filelist)
    assert( len(filelist)==0) # has files
if __name__ == "__main__":
    main()