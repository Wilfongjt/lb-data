import os
from util import Util
from step import Step
from configuration_file import ConfigurationDict
from configuration_interface import InterfaceConfiguration
#from template_file import TemplateFile
from templates import Template
from context_dict import ContextDict, ContextKey
from resource_name import ResourceName
"""
#from helper_insert_format import HelperInsertFormat
from helper_required_insert_attributes_format import HelperRequiredInsertAttributesFormat
#from helper_declare_upsert_format import HelperDeclareUpsertFormat
from helper_where_clause_format import HelperWhereClauseFormat
from helper_set_clause_format import HelperSetClauseFormat
from helper_set_defaults_format import HelperSetDefaultsFormat
from helper_sync_json_values_format import HelperInsertSyncJSONValuesFormat, HelperUpdateSyncJSONValuesFormat
#from helper_insert_columns_format import HelperInsertColumnsFormat
#from helper_insert_values_format import HelperInsertValuesFormat
#from helper_required_input_attributes_format import HelperRequiredInputAttributesFormat
from helper_update_combos_format import HelperUpdateCombosFormat
#from helper_fields_format import HelperFieldsFormat
from helper_required_insert_format import HelperRequiredInsertFormat
from helper_required_update_format import HelperRequiredUpdateFormat
"""
"""
from functions import Function_Extentions, Function_DeclareUpsert,  Function_InsertSyncJSONValues, \
    Function_InsertColumns, Function_InsertParameters,  Function_InsertValues, Function_RequiredInsertInputs,  \
    Function_SelectColumns, Function_SelectParameterTypes, Function_SetDefaults, Function_TableFields, \
    Function_UpdateParameterTypes, Function_UpdateSyncJSONValues, Function_UpdateColumns, \
    Function_WhereClause, Function_DeleteParameterTypes,\
    Function_InsertParameterTypes, Function_InsertParameterTypes,Function_RequiredUpdateInputs, \
    Function_Reference,Function_UpdateCombinationCode
"""
from list_fields import FieldList
from test_func import test_table
#from templatize import Templatize
from pprint import pprint
#from helper_expand_update_parameters_format import HelperExpandUpdateParametersFormat
#from template_compiled_file import ResourceName, TemplateCompiledFile
#from helper_template_compile import HelperTemplateCompile
from app_settings import AppSettings
#from helper_configuration_generate_api import HelperConfigurationGenerateAPI
"""
config: expect that for every config file there is a matching template file 
expect extra json files for the api forms
template: replace [[tbl-fields]], [[update-columns]], [[update-parameters]], ...
example
input:  config/*.db-api-table-table.pg.json
output: compiled/*.db-api-table-table.pg.tmpl.compiled
"""

class ProjectCompile(Step):

    def __init__(self):
        super().__init__()
        #self.cmplFile = None
        self.description = [

            'Compile template files',
            'Write to project template-folder.',
            'Inserts columns, parameters, values, extensions, fields into template',
            'Overwrites the existing template'
        ]
        self.dictionary = None
        self.context=None

    def getContext(self):
        if self.context == None:
            self.context = ContextDict().read()
        return self.context

    def getConfigFile(self):
        return self.dictionary

    def setConfigFile(self, confFile):
        self.dictionary = confFile
        return self

    def process(self):
        super().process()
        """
        if config file has a matching template file just expand it, write it to compiled-folder
        if config file has a default template, rename it, expand it, write copy to compiled-folder
        :return:
        """
        self.getData()
        # get folders

        conf_folder = self.appSettings.getFolder('expanded-folder')
        tmpl_folder = self.appSettings.getFolder('expanded-folder')
        expd_folder = self.appSettings.getFolder('expanded-folder')
        merge_folder = self.appSettings.getFolder('merged-folder')
        # list of config files
        file_name_list = Util().getFileList(conf_folder, ext='.json')

        # Project Template Compile

        for file_name in file_name_list:
            #print('filename', file_name)
            confFile = ConfigurationDict(conf_folder, file_name).read()

            if 'api-name' in confFile:
                #print('* api_name', confFile['api-name'])
                #print('* naem', self.appSettings.to_cmpl(file_name))
                #have register-user.interface-upsert.pg
                #print('* conffile', confFile)
                #print('* tmpl_folder', tmpl_folder, 'to_cmpl', self.appSettings.to_cmpl(file_name))
                tmplFile = Template(confFile, tmpl_folder, self.appSettings.to_cmpl(file_name))
                merge_file_name = self.appSettings.to_merged(file_name)
                print('merged', merge_file_name)

                #print('template ', tmplFile.toString())
                #print('template ',  tmplFile)
                tmplFile.copy(merge_folder, merge_file_name)
                #pprint(tmplFile)
            else:
                tmplFile = Template(confFile, tmpl_folder, self.appSettings.to_cmpl(file_name))
                merge_file_name = self.appSettings.to_merged(file_name)
                print('merged', merge_file_name)

                # print('template ', tmplFile.toString())
                # print('template ',  tmplFile)
                tmplFile.copy(merge_folder, merge_file_name)
            #print('to_tmpl',self.appSettings.to_tmpl(file_name, source_key='merged-folder'))
            #tmplFile = Template(confFile, tmpl_folder,self.appSettings.to_api(file_name,))
            #print('Results')
            #pprint(tmplFile)
            """
            #print('template name', self.appSettings.to_tmpl(file_name))
            #print('templ', tmplFile.toString())
            #print('confFile', confFile)
            #if confFile['type'] == 'interface-upsert':
                print('* table interface')
                print('confFile', confFile)

                # loop interfaces

                #confFile = InterfaceConfiguration(conf_folder, file_name)
                #print('conf filename', file_name, 'confFile', confFile)
                #print('tmpl filename', self.appSettings.to_tmpl(file_name, source_key='expanded-folder'))
                #print('handle table aux template files')
                tmpl = Template(confFile,)
            #else:
                print('')
                #print('straight template {}'.format(file_name))
                # tmplFile = Template(confFile, tmpl_folder,
                #                    self.appSettings.to_tmpl(file_name, source_key='expanded-folder'))
            """
            """
            expdResourceName = ResourceName(expd_folder, file_name)

            self.setConfigFile(ConfigurationDict(expdResourceName.getFolder(),
                                                 expdResourceName.getFileName()).read())

            cmplFile = self.expand(expdResourceName)

            if cmplFile == None:
                raise Exception('Compiled file cannot be None')

            cmplFile.write()
            """
        return self


    '''
    def expand(self, expd_res):
        ##############
        # get template
        ###

        tmplFile = TemplateFile( expd_res.getFolder(), expd_res.getFileName())\
            .read()

        #####
        # expand
        ####
        cmplFile = TemplateFile(expd_res.getFolder(), expd_res.getFileName())
        #print('template', cmplFile.getFileName())

        tmplFile = [fn for fn in tmplFile if len(fn.rstrip()) > 0]
        """
        for ln in tmplFile:
            lines = self._expand(ln)
            #print('linesout', lines)

            cmplFile.append_lines(lines)
        """

        for tmpl_line in tmplFile:
            if '[[' in tmpl_line:

                """
                apply template functions to a single line of the template
                """
                Function_DeclareUpsert(self.dictionary, tmpl_line, cmplFile)

                Function_DeleteParameterTypes(self.dictionary, tmpl_line, cmplFile)

                Function_Extentions(self.dictionary, tmpl_line, cmplFile)

                Function_InsertSyncJSONValues(self.dictionary, tmpl_line, cmplFile)
                Function_InsertColumns(self.dictionary, tmpl_line, cmplFile)
                Function_InsertParameters(self.dictionary, tmpl_line, cmplFile)
                Function_InsertParameterTypes(self.dictionary, tmpl_line, cmplFile)
                Function_InsertValues(self.dictionary, tmpl_line, cmplFile)

                Function_Reference(self.dictionary, tmpl_line, cmplFile)

                Function_RequiredInsertInputs(self.dictionary, tmpl_line, cmplFile)

                Function_RequiredUpdateInputs(self.dictionary, tmpl_line, cmplFile)

                Function_SelectColumns(self.dictionary, tmpl_line, cmplFile)
                Function_SelectParameterTypes(self.dictionary, tmpl_line, cmplFile)
                Function_SetDefaults(self.dictionary, tmpl_line, cmplFile)

                Function_TableFields(self.dictionary, tmpl_line, cmplFile)

                # Function_UpdateCombosFormat(self.dictionary, tmpl_line, cmplFile)
                Function_UpdateCombinationCode(self.dictionary, tmpl_line, cmplFile)
                Function_UpdateParameterTypes(self.dictionary, tmpl_line, cmplFile)
                Function_UpdateSyncJSONValues(self.dictionary, tmpl_line, cmplFile)
                Function_UpdateColumns(self.dictionary, tmpl_line, cmplFile)
                # Function_UpdateCombinationCode(self.dictionary, tmpl_line, cmplFile)

                Function_WhereClause(self.dictionary, tmpl_line, cmplFile)


            else:
                # print('append none template template {}'.format(tmpl_line))
                cmplFile.append(tmpl_line)

        return cmplFile
    """
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
    """

    def dep_expand(self, line):
        lines = []
        if  '[[update_combos_format]]' in line:
            """
                 -- all possible update combinations of updatable fields
                [[update_combos_format]]
                Function_UpdateCombosFormat
            """
            lines = HelperUpdateCombosFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[required_update_inputs]]' in line:
            """
                -- check required attributes by type
                [[required_update_inputs]]
                Function_RequiredUpdateInputs
            """
            lines = HelperRequiredUpdateFormat().set_dictionary(self.getConfigFile()).format()

        elif '[[required_insert_inputs]]' in line:
            """
                -- check required attributes by type
                [[required_insert_inputs]]
                Function_RequiredInsertInputs
            """
            lines = HelperRequiredInsertFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[insert-values]]' in line:
            """
                INSERT
                  INTO [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
                  (
                    [[insert-columns]]
                  ) VALUES (
                    [[insert-values]]
                  );
               Function_InsertColumns   
            """
            #lines = HelperInsertValuesFormat().set_dictionary(self.getConfigFile()).format()
            lines = ['_{}'.format(f['name'])
                            for f in FieldList(self.getConfigFile(), ['c', 'C', 'F'])]

            lines = ['                {}'.format(', '.join(lines))]

        elif '[[insert-columns]]' in line:
            """
                INSERT
                  INTO [LB_PROJECT_prefix]]_schema.[[tbl-name]]
                  (
                    [[insert-columns]]
                  ) VALUES (
                    [[insert-values]]
                  );
                  Function_InsertColumns
            """
            prefix = self.getConfigFile()['tbl-prefix']
            #lines = HelperInsertColumnsFormat().set_dictionary(self.getConfigFile()).format()
            lines = ['{}_{}'.format(prefix, f['name'])
                          for f in FieldList(self.getConfigFile(),['C','c','F'])]

            lines = ['                {}'.format(', '.join(lines))]
            print('colunn lines', lines)



        elif '[[insert-sync-json-values]]' in line:
            """
                -- sync json values to table values
                [[insert-sync-json-values]]
                Function_InsertSyncJSONValues
            """
            lines = HelperInsertSyncJSONValuesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[update-sync-json-values]]' in line:
            """
                -- sync-json-values to table values
                [[update-sync-json-values]]
                Function_UpdateSyncJSONValues
            """
            lines = HelperUpdateSyncJSONValuesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[set-defaults]]' in line:
            """
                 -- set defaults just in case
                [[set-defaults]]
                Function_SetDefaults
            """
            lines = HelperSetDefaultsFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[declare-upsert]]' in line:
            """
            CREATE OR REPLACE FUNCTION
                [[LB_PROJECT_prefix]]_schema.[[api-name]](_token TEXT, _json JSONB) RETURNS JSONB
                AS $$
                    Declare rc jsonb;
                    Declare _cur_row JSONB;
                
                    Declare _anonymous JSONB;
                    Declare _registrant JSONB;
                    Declare _app_id TEXT;
                
                    [[declare-upsert]]
            Function_DeclareUpsert        
            """
            lines = HelperDeclareUpsertFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[where-clause]]' in line:
            """
                select [[tbl-prefix]]_row as _usr
                      into _cur_row
                      from [[LB_PROJECT_prefix]]_schema.[[api-table]]
                      where
                        [[where-clause]]
                Function_WhereClause        
            """
            lines = HelperWhereClauseFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[set-clause]]' in line:
            """
                isnt used
            """
            lines = HelperSetClauseFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[required-insert-attributes]]' in line:
            """
                isnt used
            """
            lines = HelperRequiredInsertAttributesFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[insert-parameter-types]]' in line:
            """
                GRANT EXECUTE ON FUNCTION
                  [[LB_PROJECT_prefix]]_schema.[[api-name]](
                  [[insert-parameter-types]]
                  ) TO anonymous;
                  Function_InsertParameterTypes
            """
            lines = self._expandParameterTypes('C')
        elif '[[select-parameter-types]]' in line:
            """
            Function_SelectParameterTypes
            """
            lines = self._expandParameterTypes('R')
        elif '[[update-parameter-types]]' in line:
            """
            Function_UpdateParameterTypes
            """
            lines = self._expandParameterTypes('U')
        elif '[[delete-parameter-types]]' in line:
            """
            N/A
            Function_DeleteParameterTypes
            """
            lines = self._expandParameterTypes('D')
        elif '[[select-columns]]' in line: # db-api-table-table.pg.tmpl
            """
             select
                '{' || [[select-columns]] || '}'
                into rc from
                [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
                where [[tbl-prefix]]_id=id;
                
                Function_SelectColumns
            """
            lines = self._expandSelectColumns()
        #elif '[[update-parameters]]' in line: # db-api-table-table.pg.tmpl
        #    print('    - [[update-parameters]] Deprecated')
        #    #lines = self._expandUpdateParameters()
        #    #lines = HelperExpandUpdateParametersFormat().set_dictionary(self.getConfigFile()).format()
        elif '[[update-columns]]' in line: # db-api-table-table.pg.tmpl
            """
            Update <table-name>
                set
                    [[update-columns]]
                where
                    [[where-clause]]   
                     
            Function_UpdateColumns        
            """
            lines = ['[[tbl-prefix]]_{}=_{}'.format(f['name'], f['name'])
                        for f in FieldList(self.dictionary, ['u', 'U'])
                            if 'pk-uuid' not in f['context']
                                and 'pk' not in f['context']]
        #elif '[[insert-values]]' in line: # db-api-table-table.pg.tmpl
        #    #print('    - insert-values found')
        #    lines = self._expandInsertValues()
        #elif '[[insert-columns]]' in line:
        #    #print('    - insert-columns found') # db-api-table-table.pg.tmpl
        #    lines = self._expandInsertColumns()
        elif '[[insert-parameters]]' in line: # db-api-table-table.pg.tmpl
            """
                   CREATE OR REPLACE FUNCTION
                       <func-name>(
                         _token TEXT,
                         [[insert-parameters]]
                       ) RETURNS TEXT
                       
                   Function_InsertParameters    
            """
            lines = self._expandInsertParameters()

        elif '[[db-extensions]]' in line:
            """
                    [[db-extensions]]
                    
                    Function_Extentions
            """
            #print('A configfile', self.getConfigFile())
            #print('A line ', line)
            #print('A filename', self.getConfigFile().getFileName())
            lines = self._expandExtensions()

        elif '[[tbl-fields]]' in line: # db-api-table-table.pg.tmpl
            """
            [[tbl-fields]]
            Function_TableFields
            """
            #lines = self._expandFields()
            lines = Function_TableFields(self.dictionary, line,)
        else:
            """
            no tags
            Passthrough line
            """
            #super().append(line)
            lines.append(line)
        return lines

    def _expandFields(self):
        # get template and then templatize it
        """
        [[tbl-fields]]
        create table if not exists
            reg_schema.register (
                [[tbl-fields]]
            );
        """
        return [Templatize()
                   .set_dictionary(f).templatize(self.getContext().get(ContextKey('context',f['context'])))
                    for f in FieldList(self.getConfigFile())
                    ]

    def _expandParameterTypes(self, targetType):
        lines = []
        # inject_tag used to find place to inject parameters
        # [[parameter-types]] has been found in a template line
        # assume [[parameter-types]] is embedded into the template line
        # replace it with list of parameters derived from config."tbl-fields"
        # put new line back into the template list

        i = 1
        tag = 'tbl-fields'  # parameters are derived from fields

        #print('tbl-fields', self.getConfigFile()[tag])

        lines.append('    TEXT') # token is TEXT,
        #if targetType == 'U':
        #    lines.append('    INT') # id
        #for FieldList()
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
                    elif targetType == 'D': # crud['R',]
                        if 'R' in t['crud'].upper() and t['context'] == 'pk':
                            if len(lines) > 0:
                                lines[len(lines) - 1] += ','
                            lines.append('    INT')
        return lines

    def _expandInsertParameters(self, table=None):
        """
        [[insert-parameters]]
        CREATE OR REPLACE FUNCTION
            <func-name>(
              _token TEXT,
              [[insert-parameters]]
            ) RETURNS TEXT
        """
        lines = []
        dictionary = None
        if table != None:
            dictionary = test_table()
        else:
            dictionary = self.getConfigFile()

        lines = [' _{} {}'.format(f['name'], f['type']) for f in FieldList(dictionary, ['c','C','F'])];
        # return single line in list
        return [', '.join(lines)]

    def _expandSelectColumns(self):
        """
         select
            '{' || [[select-columns]] || '}'
            into rc from
            [[LB_PROJECT_prefix]_schema.[[tbl-name]]
            where [[tbl-prefix]]_id=id;
        """
        return  ['\'{{\' || {} ||\'}}\''.format(' || '.join( ['format(\'"{}":"%s"\',{}_{})'.format(f['name'],self.getConfigFile()['tbl-prefix'],f['name'])
                  for f in FieldList(self.getConfigFile(), ['r', 'R'])]))]

    def _expandExtensions(self):
        # no delemiters
        # assume [[extensions]] is on single line
        """
            create extension IF NOT EXISTS pgcrypto;
            ...
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """
        rc = []
        # return ['{}\n'.format( ContextKey('context',f)) for f in self.configFile['db-extensions']]

        #return ['{}\n'.format( self.getContext().get(ContextKey('context',f)))
        #                       for f in self.configFile['db-extensions']]
        #print('xxx',self.getConfigFile())
        #for k in self.getConfigFile():
        #    print('key', k, 'value', self.getConfigFile()[k])
        #print('AAAA')
        #pprint(self.getConfigFile())
        #print('db-extensions', self.getConfigFile()['db-extensions'])
        if 'db-extensions' in self.getConfigFile():
            rc = ['CREATE EXTENSION IF NOT EXISTS "{}";'.format(n) for n in self.getConfigFile()['db-extensions'] ]

        #print('zzzzz', rc)
        return rc

    def _expandFields(self):
        #at this point, we are loading the template
        #[[tbl-fields]] has been found in template line
        #assume [[tbl-fields]] is alone on its own line
        #skip template line, replace with sql column defintions derived from config."tbl-fields" list
        #add each column definition back to the template list as a template
        lines = []
        i = 1
        tag = 'tbl-fields'

        sz = len(self.getConfigFile()[tag])

        # add fields to list
        #self._templatize(f, self.getContext().get(ContextKey('context',f)))
        lines = ['{}'.format(self._templatize(f, self.getContext().get(ContextKey('context',f))))
            for f in FieldList(self.getConfigFile())]
        lines =[',\n'.join(lines)]
        """
        for f in self.getConfigFile()[tag]: # field by field

            if 'crud' in f and len(f['crud'])>0:
                #print('field', f)
                ln=self.getContext().get(ContextKey('context',f))
                #ln = self.getContext()[f['context']] # get context.template.list key
                if ln == None:
                    raise NameError('Unknown Context', f['context'])

                ln = self._templatize(f, ln) # go get template
                if i < sz: # check for last field
                    ln = '{},'.format(ln)
                ln = '  {}\n'.format(ln)
                #self.targetTemplateFile.append(ln) # add line to
                lines.append(ln)
            i += 1
        """
        return lines

    def _templatize(self, key_value_dict, tmpl_str):
        # case 1: key_value_dict is {"name": "id", "context":"id"} primary key
        # case 2: key_value_dict is {"name": "role", "context":"fk"} foreign key
        for key_ in key_value_dict:
            v = key_value_dict['name']
            tmpl_str = tmpl_str.replace('[[{}]]'.format(key_), v)
        return tmpl_str

'''

def main():
    from app_settings import AppSettingsTest
    from project_environment import ProjectEnvironment
    from project_create_folders import ProjectCreateFolders
    from project_initialize import ProjectInitialize
    from project_expand import ProjectExpand
    #from configuration_file_mocks import ConfigurationDictFileDatabaseMock,ConfigurationDictFileTableMock
    #from template_file_mocks import TemplateFileCreateTableMock, TemplateFileCreateDatabaseMock
    import os
    from test_func import test_table
    #from mockup_test_data import   MockupData

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

    #print('_expandExtensions',step._expandExtensions())

    #assert step.setConfigFile(test_table())._expandInsertParameters() == [' _type TEXT,  _form JSONB,  _password TEXT']

    #print('lin ', step._expand('[[required_insert_inputs]]'))

    #assert step._expand('[[required_insert_inputs]]') == ['                reg_type, reg_form, reg_password']
    #assert step._expand('[[insert-columns]]') == ['                reg_type, reg_form, reg_password']
    #assert step._expand('[[insert-values]]') == ['                _type, _form, _password']


    # tests
    filelist = Util().getFileList(conf_folder, ext='pg.tmpl-compiled')

    filelist = [appSettings.to_cmpl(fn) for fn in filelist]

    for fn in filelist:
        print('    - compiled', fn)
        assert(Util().file_exists(cmpl_folder,fn))
        #tFile = TemplateFile(cmpl_folder,fn)

        #for ln in tFile:
        #    assert( '[[' not in ln)

    #appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()

