
from step import Step
from util import Util
from app_settings import AppSettings
from configuration_file import ConfigurationDict
from template_file import TemplateFile


class ProcessVerifyOutput(Step):
    def __init__(self):
        super().__init__()

        self.description = [
            'Calculate expected output files',
            'Count actual output files'
        ]


    def process(self):
        super().process()
        #print('process')
        self.getData() # bring data forward

        print('* Configuration')
        print('  - source config count', self.source_count(self.appSettings.getFolder('con-fig-folder'),'.json'))
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'),'.json'))
        print('  - actual', self.actual_count(self.appSettings.getFolder('expanded-folder'), '.json'))

        print('* Templates')
        print('  - source tmpl count', self.source_count(self.appSettings.getFolder('temp-lates-folder'),'.tmpl'))
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'),'.json'))
        print('  - actual', self.countTemplates())

        print('* SQL') # one sql per expanded tmpl
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'),'.pg.json'))
        print('  - actual', self.actual_count(self.appSettings.getFolder('sql-folder'), '.sql'))

        print('* sh')  # one sql per expanded tmpl
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'),'.sh.json'))
        print('  - actual', self.actual_count(self.appSettings.getFolder('script-folder'), '.sh'))

        print('* docker-compose dc')  # one sql per expanded tmpl
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'), '.dc.json'))
        print('  - actual', self.actual_count(self.appSettings.getFolder('code-folder'), '.yml'))

        print('* dockerfile dk')  # one sql per expanded tmpl
        print('  - expected', self.expected_count(self.appSettings.getFolder('con-fig-folder'), '.dk.json'))
        print('  - actual', self.actual_dockerfile_count(self.appSettings.getFolder('con-fig-folder')))

        return self
    ##########
    #def countConfig(self):
    #    return self.source_count(self.appSettings.getFolder('con-fig-folder'),'.json')

    def countTemplates(self):
        #rc = self.source_count(self.appSettings.getFolder('temp-lates-folder'),'.tmpl')
        rc = self.actual_count(self.appSettings.getFolder('sql-folder'), '.sql')
        rc += self.actual_count(self.appSettings.getFolder('script-folder'), '.sh')
        rc += self.actual_count(self.appSettings.getFolder('code-folder'), '.yml')
        rc += self.actual_count(self.appSettings.getFolder('db-folder'), 'dockerfile-db')
        rc += self.actual_count(self.appSettings.getFolder('web-folder'), 'dockerfile-web')

        return rc

    def source_count(self, folder, extension):
        filelist = Util().getFileList(folder, ext=extension)
        return len(filelist)

    ###########

    def expected_count(self, folder, extension):
        # count json and tmpl files
        cnt = 0

        filelist = Util().getFileList(folder, ext=extension)
        for fn in filelist:
            parts = fn.split('.')
            cnt += 1
            if parts[1] == 'table' and parts[3] == 'json':
                confFile = ConfigurationDict(folder, fn).read()
                if 'api-methods' in confFile:
                    for meth in confFile['api-methods']:
                        cnt += 1

        return cnt


    ##########

    def actual_count(self, folder, extension):

        filelist = Util().getFileList(folder, ext=extension)

        return len(filelist)

    def actual_dockerfile_count(self, folder):
        rc = 0
        folderlist = Util().getFolderList(self.appSettings.getFolder('code-folder'))

        for folder in folderlist:
            #print('folder', folder)
            filelist = Util().getFileList(folder)
            for fn in filelist:
                if 'docker' in fn:
                    #print('file', fn)
                    rc += 1

        return rc

def main():
    import os



    os.environ['LB-TESTING'] = '1'

    ProcessVerifyOutput().run()

if __name__ == "__main__":
    main()