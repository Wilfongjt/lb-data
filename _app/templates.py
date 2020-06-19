'''
from list_fields import FieldList

from functions import Function_Extentions, Function_DeclareUpsert,  Function_InsertSyncJSONValues, \
    Function_InsertColumns, Function_InsertParameters,  Function_InsertValues, Function_RequiredInsertInputs,  \
    Function_SelectColumns, Function_SelectParameterTypes, Function_SetDefaults, Function_TableFields, \
    Function_UpdateParameterTypes, Function_UpdateSyncJSONValues, Function_UpdateColumns, \
    Function_WhereClause, Function_DeleteParameterTypes,\
    Function_InsertParameterTypes, Function_InsertParameterTypes,Function_RequiredUpdateInputs, \
    Function_Reference,Function_UpdateCombinationCode
'''

#from function_weld import
from function_anchor import Function_Anchor
from function_simple_templatize import Function_SimpleTemplatize
from function_update_combination_code import Function_UpdateCombinationCode
from function_table_fields_code import Function_TableFieldCode
from configuration_interface import InterfaceConfiguration
from util import Util
from file import ListFile
from test_func import test_table, test_table_template, test_upsert_template

from pprint import pprint

class Template(ListFile):
    def __init__(self, dictionary, folder_name=None, file_name=None, aux_template_list=None):
        super().__init__(folder_name=folder_name, file_name=file_name)
        #print('init Template')
        if type(dictionary) == str:
            raise Exception('Parameter one should be a dictionary')

        # when dictionary is set to {} then no templatization will occure... use TextFile?
        self.dictionary = dictionary
        #print('template dictionary', file_name, self.dictionary)
        self.aux_template_list = aux_template_list
        #self.process()
        self.run()

    def toString(self):
        return '\n'.join(self)

    def run(self):
        self.process()
        self.postProcess()

    def process(self):

        # do templating as lines are added to template
        if self.getDictionary() == {}: # skip templatization
            # load without inject or inline templating
            for tmpl_line in self.getTemplateList():
                #print('A')
                #print('templates tmpl_line', tmpl_line)
                self.append(tmpl_line)
        else: # do templatization
            for tmpl_line in self.getTemplateList():
                #print('templates tmpl_line', tmpl_line)
                #print('B', tmpl_line)
                # do << first to allow potentially hidden [[ to appear
                if '<<' in tmpl_line:   # INJECT may create new inline
                    tmpl_line = self.inject(tmpl_line)
                    #self.append(ln)

                if '[[' in tmpl_line: # IN-LINE
                    tmpl_line = self.inline(tmpl_line)
                    #self.append(ln)

                #if '<<' not in tmpl_line and '[[' not in tmpl_line: # PASSTHROUGH
                #    tmpl_line = self.passthrough(tmpl_line)

                self.append(tmpl_line)

        return self

    def getDictionary(self):
        return self.dictionary

    def postProcess(self):
        self.validate()
        return self

    def inject(self, line): # <<
        #if 'tbl-fields' not in self.getDictionary():
        #    return line
        print('Template inject {}'.format(line) )
        #print('A Template getTemplateLine', func.getTemplateLine())

        func = Function_Anchor(self.getDictionary(), line)\
            .add(Function_UpdateCombinationCode())\
            .add(Function_TableFieldCode())
        #print('B Template getTemplateLine', func.getTemplateLine())
        code = func.getTemplateLine()
        return code

    def inline(self, line): # [[
        # values = line.replace('[[','<inline-value>').replace(']]','') # remove later
        # return self.processInlineFunctions(line)
        #print('Template inline 1 {}'.format(line))
        func = Function_Anchor(self.getDictionary(), line) \
            .add(Function_SimpleTemplatize())

        if '{{' in line:  # try root search
            #print('Template inline 2')
            for key in self.getDictionary():
                rootkey = '{{' + key + '}}'
                #print('Template inline 3 {}'.format(key))

                if type(self.getDictionary()[key]) != list:
                    #print('Template inline 4 key ', key)
                    line = line.replace(rootkey, self.getDictionary()[key])  # inline value
                # print('key', rootkey , ' line ', line)
                if '{{' not in line:  # found so stop
                    break
        #print('Template inline out {}'.format(func.getTemplateLine()))
        return func.getTemplateLine()

    def passthrough(self, line):
        return line

    def validate(self):
        #print('validate 1' )
        if len(self.getDictionary()) == 0: # no dictionary
            # the template was initiated without a dictionary
            # assume intention is to output the template without templitazation
            #print('validate 1a')
            return self
        _type = None
        #print('validate 2')
        if 'type' in self.getDictionary():
            _type = self.getDictionary()['type']

        for line in self:
            if 'models' in line:
                print('validate {}'.format(line))
            if '[[' in line:
                pprint(self.getDictionary())
                pprint(self)

                raise Exception('Validate failed, undefined tag in dictionary. "{}" type:{}'.format(line, _type))
            if '<<' in line:
                raise Exception('Validate failed, undefined tag in dictionary. "{}" type:{}'.format(line, _type))
        #print('validate out')
        return self

    def setAuxTemplateList(self, aux_tmpl_list):
        self.aux_template_list = aux_tmpl_list
        return self
    '''
    def templatize(self, template_line, temp_dictionary=None):
        print('templateize 1')
        if temp_dictionary == None:
            temp_dictionary = self.getDictionary()

        if '[[' not in template_line and '<<' not in template_line :
            return template_line

        for key_ in temp_dictionary:
            v = temp_dictionary[key_]
            if type(v) != list and type(v) != dict:
                #print('process key', key_, ' v ', v)
                if '[[' in template_line:
                    template_line = template_line.replace('[[{}]]'.format(key_), v)
                elif '<<' in template_line:
                    template_line = template_line.replace('<<{}>>'.format(key_), v)

        return template_line
    '''
    def getFileName(self):
        return self.file_name

    def read(self):
        # template automatically reads without read
        return self

    def getTemplateList(self):
        lines = []
        if self.aux_template_list != None: # testing
            print('using Aux Template')
            lines = self.aux_template_list
        elif self.exists():
            #print('loading template {}  {}'.format(self.getFolderName(), self.getFileName() ))
            path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
            with open(path_filename) as f:
                for line in f:
                    line = line.rstrip()
                    lines.append(line)
            #print('loaded template {} lines from {} {}'.format(len(self),self.getFileName(), self.getFolderName()))
        else: ## small test set
            lines.append('No Template Lines')
            #raise Exception('Template folder({}) filename({}) doesnt exist.'.format(self.getFolderName(), self.getFileName()))

        return lines

def main():
    import os
    from app_settings import AppSettingsTest
    from test_func import test_table, test_table_template, test_upsert_template
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    os.environ['LB-TESTING'] = '1'
    # folders
    appSettings = AppSettingsTest().createFolders()
    dictionary_tbl = test_table()
    #dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    #print('test_table_template()', test_table_template())

    template = Template(dictionary_tbl, aux_template_list=test_table_template())
    template.getTemplateList() == test_table_template()

    print('toString', template.toString())

    assert type(template) == Template

    os.environ['LB-TESTING'] = '1'


if __name__ == "__main__":
    main()