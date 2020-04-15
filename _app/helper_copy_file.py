
#from template_file import TemplateFile
#from configuration_generate import ConfigurationGenerate
#from script_file import ScriptFile
from helper import Helper

class HelperCopyFile(Helper):
    def __init__(self, fromFile, toFile, step=None):
        super().__init__(step)
        self.setTemplateFile(fromFile)
        self.setTemporaryFile(toFile)

    def process(self):
        #print('process')
        # tempatize
        if self.getTemplateFile().isEmpty():
            #print('read ', self.getTemplateFile().getFileName())
            self.getTemplateFile().read()

        self.getTemporaryFile().copy(self.getTemplateFile()).write()

        return self


def main():
    from pathlib import Path
    from template_file import TemplateFile

    to_folder = '{}/temp'.format(str(Path.home()))
    to_file_name = 'to-file.sql'
    fromFile = TemplateFile('whatever','some-file-name')\
        .append('A')\
        .append('B')\
        .append('C')
    toFile = TemplateFile(to_folder, to_file_name)

    HelperCopyFile(fromFile, toFile).run()



if __name__ == "__main__":
    main()