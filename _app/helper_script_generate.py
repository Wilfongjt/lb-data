# Deprecated
#from template_file import TemplateFile
#from configuration_generate import ConfigurationGenerate
#from script_file import Script File
from helper import Helper
from app_settings import AppSettings

class HelperScriptGenerate(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.scriptFile=None

    def setScriptFile(self,scriptFile):
        self.scriptFile = scriptFile
        return self

    def getScriptFile(self):
        return self.scriptFile

    def generate(self):

        self.process()

        return self

    def process(self):
        # tempatize
        if self.getScriptFile() == None:
            raise Exception('ScriptFile is not set!')

        self.getScriptFile().write()
        return self


def main():
    #from __classes__.setup import Setup
    from copy_file import CopyFile
    from script_file import ScriptFile
    from util import Util
    from step import StepMock

    #step = StepMock()
    # setup


    #tmpl_folder = AppSettings().getFolder('temp-lates-folder')
    #config_folder = AppSettings().getFolder('con-fig-folder')

    script_folder = AppSettings().getFolder('script-folder')
    print('script-folder', script_folder)

    script_file = 'junk.database.pg.sql'

    scriptFile = ScriptFile().setFileName(script_file)\
        .append('A')\
        .append('B')\
        .append('C')

    HelperScriptGenerate()\
        .setScriptFile(scriptFile)\
        .generate()
    assert scriptFile.exists()

    scriptFile.delete()
    assert not scriptFile.exists()

if __name__ == "__main__":
    main()