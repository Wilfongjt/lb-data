
Environment Variables
* LB_WORKING_NAME

AppEnvironment()
    * container holds application steps
AppCreateFolders()
    * application step
    * Setup the folders used by the application
    * folders are defined in AppSettings
    * creates folders
        * system-folder, systems-folders
        *
AppInitialize()
    * application step
    * copy context.template.list.json to work-folder/shared-folder

setup_project = ProjectEnvironment(project_name='example')\
    .add(ProjectCreateFolders())\
    .add(ProjectConfigurationInitialize())\
    .add(ProjectTemplateInitialize())\
    .add(ProjectConfigurationGenerateAPI())\
    .add(ProjectTemplateCompile())\
    .add(ProjectTemplateMerge())\
    .add(ProjectOrganizeFiles())

work-folder is LyttleBit/. All project subfolders are found under LyttleBit.
resource-folder is a development folder _res/. All original data is found in resource-folder.
shared-folder is a subfolder of work-folder

Project Initialize
Project Expand