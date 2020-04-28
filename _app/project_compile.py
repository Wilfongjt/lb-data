import os
from util import Util
from step import Step
from configuration_file import ConfigurationDict
from template_file import TemplateFile
from context_dict import ContextDict
from resource_name import ResourceName
#from helper_insert_format import HelperInsertFormat
from helper_required_insert_attributes_format import HelperRequiredInsertAttributesFormat
from helper_declare_upsert_format import HelperDeclareUpsertFormat
from helper_where_clause_format import HelperWhereClauseFormat
from helper_set_clause_format import HelperSetClauseFormat
from helper_set_defaults_format import HelperSetDefaultsFormat
from helper_sync_json_values_format import HelperSyncJSONValuesFormat
from helper_insert_columns_format import HelperInsertColumnsFormat
from helper_insert_values_format import HelperInsertValuesFormat
from helper_required_input_attributes_format import HelperRequiredInputAttributesFormat
from helper_update_combos_format import HelperUpdateCombosFormat
#from template_compiled_file import ResourceName, TemplateCompiledFile
#from helper_template_compile import HelperTemplateCompile
from app_settings import AppSettings
#from helper_configuration_generate_api import HelperConfigurationGenerateAPI
'''
config: expect that for every config file there is a matching template file 
template: replace [[fields]], [[update-columns]], [[update-parameters]], ...
example
input:  config/*.db-api-table-table.pg.json
output: compiled/*.db-api-table-table.pg.tmpl.compiled
'''



class ProjectCompile(Step):

    def __init__(self):
        super().__init__()
        #self.cmplFile = None
        self.description = [
            'Compile template files and write to project template-folder.',
            'Inserts columns, parameters, values, extensions, fields',
            'Overwrites the existing template'
        ]
        self.configFile = None
        self.context=None

    def getContext(self):
        if self.context == None:
            self.context = ContextDict().read()
        return self.context

    def getConfigFile(self):
        return self.configFile

    def setConfigFile(self, confFile):
        self.configFile = confFile
        return self
    '''
    def setCompiledFile(self, cmplFile):
        self.cmplFile
        return self

    def getCompileFile(self):
        return self.cmplFile
    '''
    def process(self):
        super().process()
        '''
        if config file has a matching template file just expand it, write it to compiled-folder
        if config file has a default template, rename it, expand it, write copy to compiled-folder
        :return:
        '''
        #print('process 1')
        self.getData()
        # get folders
        #conf_folder = self.appSettings.getFolder('con-fig-folder')
        #tmpl_folder = self.appSettings.getFolder('temp-lates-folder')

        conf_folder = self.appSettings.getFolder('expanded-folder')
        tmpl_folder = self.appSettings.getFolder('expanded-folder')
        expd_folder = self.appSettings.getFolder('expanded-folder')

        # list of config files
        file_name_list = Util().getFileList(conf_folder, ext='.json')
        #file_name_list = Util().getFileList(conf_folder, ext='.tmpl')
        # Project Template Compile

        for file_name in file_name_list:
            #print('process 3')

            # file
            #print('file_name',file_name, file_name.replace('.json','.tmpl'))
            # expand template file
            #expdResourceName = ResourceName(expd_folder, file_name)
            expdResourceName = ResourceName(expd_folder, file_name)
            #confResourceName = ResourceName(conf_folder, file_name)
            #tmplResourceName = ResourceName(tmpl_folder,
            #                                self.appSettings.to_tmpl(file_name))
            #cmplResourceName = ResourceName(expd_folder,
            #                                self.appSettings.to_cmpl(file_name))

            #print('conf | ', confResourceName.getResourceName())
            #print('tmpl | ', tmplResourceName.getResourceName())
            #print('cmpl | ', cmplResourceName.getResourceName())

            # config holds some of the source data for expand
            #self.setConfigFile(ConfigurationDict(confResourceName.getFolder(),
            #                                   confResourceName.getFileName()).read())
            self.setConfigFile(ConfigurationDict(expdResourceName.getFolder(),
                                                 expdResourceName.getFileName()).read())
            #print('configFile', self.getConfigFile())
            #cmplFile = self.expand(tmplResourceName)
            cmplFile = self.expand(expdResourceName)
            '''
             cmplFile = self.expand(tmplResourceName,
                                   confResourceName,
                                   cmplResourceName)
            '''

            if cmplFile == None:
                raise Exception('Compiled file cannot be None')

            cmplFile.write()

        return self

    def expand(self, expd_res):
        #compiled_file = None
        ##############
        # get template
        ###
        #expd_res.getFolder()
        #print('tmpl', expd_res.getFolder(), expd_res.getFileName())
        tmplFile = TemplateFile( expd_res.getFolder(), expd_res.getFileName())\
            .read()

        #####
        # expand
        ####
        cmplFile = TemplateFile(expd_res.getFolder(), expd_res.getFileName())
        tmplFile = [fn for fn in tmplFile if len(fn.rstrip()) > 0]
        for ln in tmplFile:

            lines = self._expand(ln)
            cmplFile.append_lines(lines)

        return cmplFile
    '''
    def expand(self, tmpl_res, conf_res, cmpl_res):
        #compiled_file = None
        ##############
        # get template
        ###
        tmpl_res.getFolder()
        tmplFile = TemplateFile( tmpl_res.getFolder(), tmpl_res.getFileName())\
            .read()

        #####
        # expand
        ####
        cmplFile = TemplateFile(cmpl_res.getFolder(), cmpl_res.getFileName())
        tmplFile = [fn for fn in tmplFile if len(fn.rstrip()) > 0]
        for ln in tmplFile:
            #print('', )
            lines = self._expand(ln)
            cmplFile.append_lines(lines)

        return cmplFile
    '''

    def _expand(self, line):

        lines = []
        if  '[[update_combos_format]]' in line:
            lines = HelperUpdateCombosFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[required_input_attributes]]' in line:
            lines = HelperRequiredInputAttributesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[insert-values]]' in line:
            lines = HelperInsertValuesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[insert-columns]]' in line:
            lines = HelperInsertColumnsFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[sync-json-values]]' in line:
            lines = HelperSyncJSONValuesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[set-defaults]]' in line:
            lines = HelperSetDefaultsFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[declare-upsert]]' in line:
            lines = HelperDeclareUpsertFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[where-clause]]' in line:
            lines = HelperWhereClauseFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[set-clause]]' in line:
            lines = HelperSetClauseFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[required-insert-attributes]]' in line:
            lines = HelperRequiredInsertAttributesFormat().set_dictionary(self.getConfigFile()).format()
        #elif '[[insert-statement]]' in line:
        #    lines =  HelperInsertFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[insert-parameter-types]]' in line:
            lines = self._expandParameterTypes('C')
        elif '[[select-parameter-types]]' in line:
            lines = self._expandParameterTypes('R')
        elif '[[update-parameter-types]]' in line:
            lines = self._expandParameterTypes('U')
        elif '[[delete-parameter-types]]' in line:
            lines = self._expandParameterTypes('D')
        elif '[[select-columns]]' in line: # db-api-table-table.pg.tmpl
            #print('    - select-columns found')
            lines = self._expandSelectColumns()
        elif '[[update-parameters]]' in line: # db-api-table-table.pg.tmpl
            #print('    - update-parameters found')
            lines = self._expandUpdateParameters()
        elif '[[update-columns]]' in line: # db-api-table-table.pg.tmpl
            #print('    - update-settings found')
            #lines = self._expandUpdateColumns()
            lines = self._expandUpdateSettings()
        #elif '[[insert-values]]' in line: # db-api-table-table.pg.tmpl
        #    #print('    - insert-values found')
        #    lines = self._expandInsertValues()
        #elif '[[insert-columns]]' in line:
        #    #print('    - insert-columns found') # db-api-table-table.pg.tmpl
        #    lines = self._expandInsertColumns()
        elif '[[insert-parameters]]' in line: # db-api-table-table.pg.tmpl
            #print('    - insert-parameters found')
            lines = self._expandInsertParameters()
        elif '[[extensions]]' in line:
            lines = self._expandExtensions()
        elif '[[fields]]' in line: # db-api-table-table.pg.tmpl
            #print('    - fields found')
            lines = self._expandFields()
        else:
            #super().append(line)
            lines.append(line)
        return lines


    def _expandUpdateParameters(self):
        lines = []
        # raise Exception('_expandInsertParameters not defined')
        # inject_tag used to find place to inject parameters
        # [[parameters]] has been found in a template line
        # assume [[parameters]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields

        for t in self.getConfigFile()[tag]:  # scan fields
            # print('tag: ', tag, ' t: ', t)
            if 'crud' in t:
                if 'U' in t['crud'].upper():  # skip the primary key on insert
                    if len(lines) > 0:
                        lines[len(lines)-1] = '{}, '.format(lines[len(lines)-1])
                    lines.append('  _{} {}'.format(t['name'], t['type']))
        return lines


    def _expandUpdateSettings(self):
        lines = []
        # raise Exception('_expandUpdateSettings not defined')
        # inject_tag used to find place to inject parameters
        # [[parameters]] has been found in a template line
        # assume [[parameters]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields
        parameters = ''
        sz = len(self.getConfigFile()[tag])

        for t in self.getConfigFile()[tag]:  # scan fields
            # print('tag: ', tag, ' t: ', t)
            if 'crud' in t:
                if 'U' in t['crud'].upper():  # skip the primary key on insert
                    if len(lines) > 0:
                        lines[len(lines)-1] = '{}, '.format(lines[len(lines)-1])
                        #parameters = '{}, \n'.format(parameters)
                    #parameters += '          [[tbl-prefix]]_{}={}'.format(t['name'], t['name'])
                    lines.append('        [[tbl-prefix]]_{}=_{}'.format(t['name'], t['name']))
        #lines.append('        ,usr_updated=CURRENT_DATE')
        #lines.append(parameters)

        return lines
    '''
    def _expandUpdateColumns(self):
        lines = []
        # raise Exception('_expandUpdateColumns not defined')
        # inject_tag used to find place to inject parameters
        # [[parameters]] has been found in a template line
        # assume [[parameters]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields
        parameters = ''
        #sz = len(self.getConfigFile()[tag])

        for t in self.getConfigFile()[tag]:  # scan fields
            # print('tag: ', tag, ' t: ', t)
            if 'crud' in t:
                if 'U' in t['crud'].upper():  # skip the primary key on insert
                    if len(parameters) > 0:
                        parameters = '{}, \n'.format(parameters)
                    parameters += '[[tbl-prefix]]_{}=_{}'.format(t['name'], t['name'])

        lines.append(parameters)

        return lines
    '''
    '''
    def _expandInsertValues(self):
        lines = []
        # raise Exception('_expandInsertValues not defined')
        # inject_tag used to find place to inject parameters
        # [[parameters]] has been found in a template line
        # assume [[parameters]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields
        parameters = ''
        #sz = len(self.getConfigFile()[tag])
        # print('config', self.getConfigurationDict().getDictionary())
        # print('sz', sz)
        for t in self.getConfigFile()[tag]:  # scan fields
            # print('tag: ', tag, ' t: ', t)
            if 'crud' in t:
                if 'C' in t['crud'].upper():  # skip the primary key on insert
                    if len(lines) > 0:
                        parameters = '{}, '.format(parameters)
                        lines[len(lines)-1] = lines[len(lines)-1] + ','
                    lines.append('_{}'.format(t['name']))
                    #parameters += '_{}'.format(t['name'])
            if 'defaultValue' in t: #what is it
                #print('default', t)
                if 'default' in t: # should it be added
                    if 'C' in t['default'].upper():# is it an Insert
                        lines[len(lines)-1] = t['defaultValue'] # replace previous value

            #lines.append('({});'.format(parameters))
        return lines
    '''
    '''
    def _expandInsertColumns(self):
        lines = []
        #raise Exception('_expandInsertColumns not defined')
        # inject_tag used to find place to inject parameters
        #[[parameters]] has been found in a template line
        #assume [[parameters]] is embedded into the template line
        #replace it with list of parameters derived from config."fields"
        #put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields
        parameters = ''
        #sz = len(self.getConfigFile()[tag])
        # print('config', self.getConfigurationDict().getDictionary())
        # print('sz', sz)
        for t in self.getConfigFile()[tag]:  # scan fields
            #print('tag: ', tag, ' t: ', t)
            if 'crud' in t:
                if 'C' in t['crud'].upper():  # skip the primary key on insert

                    if len(lines) > 0:
                        lines[len(lines)-1] = lines[len(lines)-1] + ','

                    lines.append('[[tbl-prefix]]_{}'.format(t['name']))
         
        #lines.append('({})'.format(parameters))
        return lines
    '''
    def _expandParameterTypes(self, targetType):
        lines = []
        # inject_tag used to find place to inject parameters
        # [[parameter-types]] has been found in a template line
        # assume [[parameter-types]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields

        #print('fields', self.getConfigFile()[tag])

        lines.append('    TEXT') # token is TEXT,
        #if targetType == 'U':
        #    lines.append('    INT') # id

        for t in self.getConfigFile()[tag]:  # scan fields
            if 'crud' in t: # ensure crud is defined
                if targetType in t['crud'].upper():  # skip the primary key on insert
                    if targetType == 'C':
                        if len(lines) > 0:
                            lines[len(lines)-1] += ','
                        lines.append('    {}'.format(t['type'].upper()))
                    elif targetType == 'R':
                        if 'R' in t['crud'].upper() and t['context']=='pk':
                            if len(lines) > 0:
                                lines[len(lines)-1] += ','
                            lines.append('    INT')
                    elif targetType == 'U':
                        if t['context']=='pk':
                            if len(lines) > 0:
                                lines[len(lines)-1] += ','
                            lines.append('    INT')
                        elif 'U' in t['crud'].upper():
                            if len(lines) > 0:
                                lines[len(lines)-1] += ','
                            lines.append('    {}'.format(t['type'].upper()))
                    elif targetType == 'D':
                        if 'R' in t['crud'].upper() and t['context'] == 'pk':
                            if len(lines) > 0:
                                lines[len(lines) - 1] += ','
                            lines.append('    INT')
        return lines

    def _expandInsertParameters(self):
        lines = []
        #raise Exception('_expandInsertParameters not defined')
        # inject_tag used to find place to inject parameters
        # [[parameters]] has been found in a template line
        # assume [[parameters]] is embedded into the template line
        # replace it with list of parameters derived from config."fields"
        # put new line back into the template list

        i = 1
        tag = 'fields'  # parameters are derived from fields

        #print('fields', self.getConfigFile()[tag])
        for t in self.getConfigFile()[tag]:  # scan fields
            if 'crud' in t:
                if 'C' in t['crud'].upper():  # skip the primary key on insert

                    if len(lines) > 0:
                        lines[len(lines)-1] += ','

                    lines.append('  _{} {}'.format(t['name'], t['type']))

        return lines

    def _expandSelectColumns(self):
        # prepare line that define field involved in a select statement
        # inject_tag used to find place to inject parameters
        #[[parameters]] has been found in a template line
        #assume [[parameters]] is embedded into the template line
        #replace it with list of parameters derived from config."fields"
        #put new line back into the template list
        lines = []
        tag = 'fields'  # parameters are derived from fields
        selects = ''
        #raise Exception('_expandSelectColumns not defined')
        for t in self.getConfigFile()[tag]:  # scan fields

            if 'crud' in t:
                if 'R' in t['crud'].upper():  # skip the primary key on insert
                    if len(selects) > 0:
                        selects = '{} || \'",\' || '.format(selects)

                    selects += '\'"{}":"\''.format(t['name'])

                    selects += ' || '
                    selects += '[[tbl-prefix]]_{}'.format(t['name'])

        selects += ' || \'"\''
        lines.append(selects)
        return lines

    def _expandExtensions(self):
        # no delemiters
        # assume [[extentions]] is on single line
        lines = []
        tag = 'extensions'
        for e in self.configFile[tag]:  # get template from list
            # ln = '{}\n'.format(self.getDictionary().getTemplateFile(e))
            ln = '{}\n'.format(self.getContext()[e])  # get context.template.list key
            #self.targetTemplateFile.append(ln) # add line to
            lines.append(ln)
        return lines

    def _expandFields(self):
        #at this point, we are loading the template
        #[[fields]] has been found in template line
        #assume [[fields]] is alone on its own line
        #skip template line, replace with sql column defintions derived from config."fields" list
        #add each column definition back to the template list as a template
        lines = []
        i = 1
        tag = 'fields'

        sz = len(self.getConfigFile()[tag])

        # add fields to list
        for f in self.getConfigFile()[tag]: # field by field

            if 'crud' in f and len(f['crud'])>0:
                #print('field', f)
                ln = self.getContext()[f['context']] # get context.template.list key
                if ln == None:
                    raise NameError('Unknown Context', f['context'])

                ln = self._templatize(f, ln) # go get template
                if i < sz: # check for last field
                    ln = '{},'.format(ln)
                ln = '  {}\n'.format(ln)
                #self.targetTemplateFile.append(ln) # add line to
                lines.append(ln)
            i += 1

        return lines

    def _templatize(self, key_value_dict, tmpl_str):
        # case 1: key_value_dict is {"name": "id", "context":"id"} primary key
        # case 2: key_value_dict is {"name": "role", "context":"fk"} foreign key
        for key_ in key_value_dict:
            v = key_value_dict['name']
            tmpl_str = tmpl_str.replace('[[{}]]'.format(key_), v)
        return tmpl_str



def main():
    from app_settings import AppSettingsTest
    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_initialize import ProjectInitialize
    from project_expand import ProjectExpand
    #from configuration_file_mocks import ConfigurationDictFileDatabaseMock,ConfigurationDictFileTableMock
    #from template_file_mocks import TemplateFileCreateTableMock, TemplateFileCreateDatabaseMock
    import os
    from mockup_test_data import   MockupData

    os.environ['LB-TESTING'] = '1'
    # folders
    appSettings = AppSettingsTest().createFolders()
    # conf_folder = appSettings.getFolder('con-fig-folder')
    conf_folder = appSettings.getFolder('expanded-folder')

    cmpl_folder =  appSettings.getFolder('expanded-folder')
    # mockups
    #MockupData().run()

    # expand templates
    step = ProjectCompile()
    ProjectEnvironment()\
        .add(ProjectCreateFolders())\
        .add(ProjectInitialize())\
        .add( ProjectExpand())\
        .add(step)\
        .run()

    #print('* {}'.format(step.getClassName()))
    #print('  -x {}'.format(step.getDescription()))

    # tests
    filelist = Util().getFileList(conf_folder, ext='pg.tmpl-compiled')

    filelist = [appSettings.to_cmpl(fn) for fn in filelist]

    for fn in filelist:
        print('    - compiled', fn)
        assert(Util().file_exists(cmpl_folder,fn))
        tFile = TemplateFile(cmpl_folder,fn)
        for ln in tFile:
            assert( '[[' not in ln)

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()

