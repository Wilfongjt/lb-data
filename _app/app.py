#import sys
#from dotenv import load_dotenv
#import settings
#import os
#from pathlib import Path
#sys.path.insert(0, '{}/__classes__'.format(os.getcwd()))
#load_dotenv()


'''
Goal: make it easier understand what the program does by just reading the main() function
The trick here is stashing data in a dictionary and pulling that dictionary forward class to class
'''


class App(list):
    def append(self, step):
        no = len(self)+1
        step.setNo(no)
        super().append(step)
        return self

    def run(self):
        # run each seperately
        for step in self:
            step.run()
        return self

def main():
    #from helper_script_generate import HelperScript Generate

    from app_environment import AppEnvironment
    from app_create_folders import AppCreateFolders
    from app_initialize import AppInitialize

    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_configuration_initialize import ProjectConfigurationInitialize
    from project_template_initialize import ProjectTemplateInitialize
    from project_configuration_generate_api import ProjectConfigurationGenerateAPI
    from project_template_compile import ProjectTemplateCompile
    from project_template_merge import ProjectTemplateMerge
    #print('start')
    app = App()

    install_app = AppEnvironment()\
        .add(AppCreateFolders())\
        .add(AppInitialize()) # copy system app files

    setup_example_project = ProjectEnvironment(project_name='example') \
        .add(ProjectCreateFolders()) \
        .add(ProjectConfigurationInitialize())\
        .add(ProjectTemplateInitialize())\
        .add(ProjectConfigurationGenerateAPI())\
        .add(ProjectTemplateCompile())\
        .add(ProjectTemplateMerge())

    app.append(install_app)
    app.append(setup_example_project)

    app.run()

    #print('end')

if __name__ == "__main__":
    main()