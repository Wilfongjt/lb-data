from pathlib import Path
from step import Step
from util import Util
from configuration_file import ConfigurationDict
#from template_file import TemplateFile
from templates import Template
#from script_file import ScriptFile
#from helper_temporary_file import HelperTemporaryFile
#from helper_template_merge import HelperTemplateMerge
from app_settings import AppSettings
from resource_name import ResourceName
import os

# last step
# Input  : temp-folder/*.compiled
# Input  : template-folder/*.tmpl
# Outputs: merge-folder/*.sql
'''

'''
class dep_ProjectMerge(Step):
    def __init__(self):
        super().__init__()
        self.description = [
            'Compile and insert simple tags. Write SQL file when helper is available.',
            'Replace all template tags [[<name>]] with <name> values found in config file',
            'Working folder is /expanded'
            'Overwrites template file'
        ]

    def process(self):
        super().process()
        self.getData()
        # inputs
        #conf_folder = self.appSettings.getFolder('con-fig-folder')
        #compiled_folder = self.appSettings.getFolder('compiled-folder')
        conf_folder = self.appSettings.getFolder('expanded-folder')
        compiled_folder = self.appSettings.getFolder('expanded-folder')
        # GATHER FILE NAMEs
        # output
        # merge_folder = self.appSettings.getFolder('merged-folder')
        merge_folder = self.appSettings.getFolder('expanded-folder')

        # get list of files to process
        file_name_list  = Util().getFileList(conf_folder, ext='.json') # compiled files

        # use config file name as source for other files
        for conf_file_name in file_name_list:

            # OUTPUT file name
            merge_file_name = self.appSettings.to_merged(conf_file_name)

            # INPUTS set input files
            cmpl_file_name = self.appSettings.to_cmpl(conf_file_name) # compiled_file_name

            # make up the file names
            confResourceName = ResourceName(conf_folder,     conf_file_name)
            cmplResourceName = ResourceName(compiled_folder, cmpl_file_name)
            mrgResourceName  = ResourceName(merge_folder,    merge_file_name)
            #print('conf | ', confResourceName.getResourceName())
            #print('cmpl | ', cmplResourceName.getResourceName())
            #print('mrg  | ', mrgResourceName.getResourceName())

            mergedFile = self.merge(cmplResourceName,
                                    confResourceName,
                                    mrgResourceName)

            if mergedFile == None:
                raise Exception('Merged file cannot be None')
            if len(mergedFile) == 0:
                raise Exception('Merged file is empty')

            mergedFile.write()

        return self

    def merge(self, cmpl_res, conf_res, mrg_res):

        # input
        #print('merge',cmpl_res.getFolder(), cmpl_res.getFileName())
        #cmplFile = TemplateFile(cmpl_res.getFolder(), cmpl_res.getFileName() ).read()
        confFile = ConfigurationDict(conf_res.getFolder(), conf_res.getFileName()).read()
        cmplFile = Template(confFile, cmpl_res.getFolder(), cmpl_res.getFileName() )

        # output file
        #mrgFile = TemplateFile(mrg_res.getFolder(), mrg_res.getFileName())
        mrgFile = Template(mrg_res.getFolder(), mrg_res.getFileName())

        #print('confFile', confFile)
        #print('env',os.environ)
        # merge template and configuration
        for line in cmplFile:
            # for each line check for tags and inject replacement value(s)
            for item in confFile:

                # simple substitution
                if type(confFile[item]) is str:
                    line = line.replace('[[{}]]'.format(item), confFile[item])

            # check for incomplete tags
            #print('merge' ,cmplFile.getFileName() )

            if '[[' in line:
                #print('dups', line)
                raise Exception('Unresolved tag {} {} {}'.format(line,
                                                                 cmplFile.getFileName(),
                                                                 cmplFile.getFolderName()))
            # clean up line
            line = line.replace('\n','')
            line = line.rstrip()

            mrgFile.append(line.rstrip())
        # return the file for writing
        return mrgFile
'''
class ProjectTemplateMergeMock(ProjectTemplateMerge):
    def __init__(self):
        super().__init__()
'''

def main():
    import os
    from util import Util
    from test_func import test_table
    from app_settings import AppSettingsTest

    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_initialize import ProjectInitialize
    from project_expand import ProjectExpand
    from project_compile import ProjectCompile

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    # setup mock files
    #MockupData().run()

    # run step
    step = ProjectMerge()

    ProjectEnvironment()\
        .add(ProjectCreateFolders())\
        .add(ProjectInitialize())\
        .add( ProjectExpand())\
        .add(ProjectCompile())\
        .add(step)\
        .run()

    #print('* {}'.format(step.getClassName()))
    #print('  - {}'.format(step.getDescription()))

    filelist = Util().getFileList(appSettings.getFolder('expanded-folder'))

    print('expanded-folder', appSettings.getFolder('expanded-folder'))
    print('filelist', filelist)

    assert( len(filelist) > 0)
    for fn in filelist:
        assert(Util().file_exists(appSettings.getFolder('expanded-folder'),fn))
        print('folder',appSettings.getFolder('merged-folder'),'file',fn)
        tFile = TemplateFile(appSettings.getFolder('expanded-folder'),fn)\
            .read()

        assert(len(tFile)>0)
        for ln in tFile:
            print('ln', ln, fn)
            assert( '[[' not in ln)
        print('    - merged {}'.format(fn))

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()