
from template_file import TemplateFile
from app_settings import AppSettings
from configuration_file import ConfigurationDict
from context_dict import ContextDict
from app_settings import AppSettingsTest
import os


class Appender():
    def __init__(self):
        self.context = None

    def append(self, line, targetFile):
        raise Exception('Extend Appender to handle your append')
        return self

    def getContext(self):
        if self.context == None:
            self.context = ContextDict().read()
        return self.context
    '''
    def templatize(self, key_value_dict, tmpl_str):
        print('templateize 2')
        # case 1: key_value_dict is {"name": "id", "context":"id"} primary key
        # case 2: key_value_dict is {"name": "role", "context":"fk"} foreign key
        for key_ in key_value_dict:
            v = key_value_dict['name']
            tmpl_str = tmpl_str.replace('[[{}]]'.format(key_), v)
        return tmpl_str
    '''
class AppendFields(Appender):
    '''
    append stuf during read
    '''
    def __init__(self, targetTemplateFile, configFile):
        super().__init__()
        #print('AppendFields')
        self.targetTemplateFile = targetTemplateFile
        self.configFile = configFile


    def append(self, line):

        #at this point, we are loading the template
        #[[tbl-fields]] has been found in template line
        #assume [[tbl-fields]] is alone on its own line
        #skip template line, replace with sql column defintions derived from config."tbl-fields" list
        #add each column definition back to the template list as a template

        i = 1
        tag = 'tbl-fields'
        sz = len(self.configFile[tag])

        # add fields to list
        for f in self.configFile[tag]: # field by field
            ln = self.getContext()[f['context']] # get context.template.list key
            if ln == None:
                raise NameError('Unknown Context', f['context'])

            ln = self.templatize(f, ln) # go get template
            if i < sz: # check for last field
                ln = '{},'.format(ln)
            ln = '  {}\n'.format(ln)
            self.targetTemplateFile.append(ln) # add line to

            i += 1

        return self

class AppendExtensions(Appender):
    '''
    append stuf during read
    '''
    def __init__(self, targetTemplateFile, configFile):
        super().__init__()
        #print('AppendExtensions')
        self.targetTemplateFile = targetTemplateFile
        self.configFile = configFile


    def append(self, line):
        # no delemiters
        # assume [[extensions]] is on single line
        tag = 'db-extensions'
        for e in self.configFile[tag]:  # get template from list
            # ln = '{}\n'.format(self.getDictionary().getTemplateFile(e))
            ln = '{}\n'.format(self.getContext()[e])  # get context.template.list key
            self.targetTemplateFile.append(ln) # add line to

        return self


class dep_TemplateCompiledFile(TemplateFile):
    def __init__(self, templateResourceName, configResourceName):
        super().__init__(templateResourceName.getFolder(), templateResourceName.getFileName())

        self.configResourceName = configResourceName
        self.confFile = None
        '''
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        self.appSettings = AppSettings()
        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
        '''
        '''
        if self.getFolderName() == None:
            # default to source code resource, assume we are going to copy
            self.setFolderName(AppSettings().getFolder('temp-folder'))
        '''

    def getConfig(self):
        if self.confFile == None:
            self.confFile = ConfigurationDict(self.configResourceName.getFolder(),
                                              self.configResourceName.getFileName()).read()
        return self.confFile

    def append(self, line):

        if '[[select-columns]]' in line: # db-api-table-table.pg.tmpl
            print('    - select-columns found')
            # self.loadSelectColumns('select-columns', line)  # inject parameters into line
        elif '[[update-parameters]]' in line: # db-api-table-table.pg.tmpl
            print('    - update-parameters found')
            # self.loadUpdateParameters('update-parameters', line)  # inject parameters into line

        elif '[[update-columns]]' in line: # db-api-table-table.pg.tmpl
            print('    - update-settings found')
            # self.loadUpdateSettings('update-columns', line)  # inject parameters into line

        elif '[[insert-values]]' in line: # db-api-table-table.pg.tmpl
            print('    - insert-values found')
            # self.loadInsertValues('insert-values', line)  # inject parameters into line
        elif '[[insert-columns]]' in line:
            print('    - insert-columns found') # db-api-table-table.pg.tmpl
            # self.loadInsertColumns('insert-columns', line)  # inject parameters into line
        elif '[[insert-parameters]]' in line: # db-api-table-table.pg.tmpl
            print('    - insert-parameters found')
            # self.loadInsertParameters('insert-parameters', line)  # inject parameters into line
        elif '[[db-extensions]]' in line:
            #print('    - db-extensions found')
            AppendExtensions(self, self.getConfig()).append(line)
            # self.loadExtensions('db-extensions')  # replace line with db-extensions
        elif '[[tbl-fields]]' in line: # db-api-table-table.pg.tmpl
            #print('    - fields found')
            AppendFields(self, self.getConfig()).append(line)
            # the current line is replaced
            # self.loadFields('tbl-fields')  # replace line with fields
        else:
            super().append(line)

        return self


def main():
    from pathlib import Path
    from util import Util
    from configuration_file_mocks import ConfigurationDictFileDatabaseMock,ConfigurationDictFileTableMock
    from template_file_mocks import TemplateFileCreateTableMock, TemplateFileCreateDatabaseMock

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()

    print('* Appender')
    print('Appender().getContext()',Appender().getContext())
    assert (len(Appender().getContext()) > 0)

    ###########
    # make some working files
    #####
    databaseConfig = ConfigurationDictFileDatabaseMock().write()
    tableConfig = ConfigurationDictFileTableMock().write()
    databaseTmpl = TemplateFileCreateDatabaseMock().write()
    tableTmpl = TemplateFileCreateTableMock().write()

    assert( Util().folder_exists(tableTmpl.getFolderName()))

    #############################
    print('\n############\n')
    print('* TemplateCompiledFile with AppendFields')


    tmplResourceName = ResourceName(appSettings.getFolder('temp-lates-folder'), 'db-api-table-table.pg.tmpl')
    confResourceName = ResourceName(appSettings.getFolder('con-fig-folder'), 'mock.db-api-table-table.pg.json')
    print('  - tmplResourceName', tmplResourceName.getResourceName())
    print('  - confResourceName', confResourceName.getResourceName())

    tmplCompiledFile = TemplateCompiledFile(tmplResourceName, confResourceName).read()

    print('  - tmplCompiledFile',tmplCompiledFile)
    assert(len(tmplCompiledFile)>0) # loaded temp file
    assert(len(tmplCompiledFile.getConfig()) > 0) # loaded config file
    assert('[[tbl-fields]]' not in tmplCompiledFile)
    assert('  [[tbl-prefix]]_id SERIAL PRIMARY KEY,\n' in tmplCompiledFile)

    #############################
    print('\n############\n')
    print('* TemplateCompiledFile with AppendExtensions')
    tmplResourceName = ResourceName(appSettings.getFolder('temp-lates-folder'), 'database.pg.tmpl')
    confResourceName = ResourceName(appSettings.getFolder('con-fig-folder'), 'db-api-table.database.pg.json')
    print('  - tmplResourceName', tmplResourceName.getResourceName())
    print('  - confResourceName', confResourceName.getResourceName())

    tmplCompiledFile = TemplateCompiledFile(tmplResourceName, confResourceName).read()

    print('  - tmplCompiledFile', tmplCompiledFile)
    assert (len(tmplCompiledFile) > 0)  # loaded temp file
    assert (len(tmplCompiledFile.getConfig()) > 0)  # loaded config file
    assert ('[[db-extensions]]' not in tmplCompiledFile)
    assert('create extension IF NOT EXISTS pgcrypto;\n' in tmplCompiledFile)

    #############################
    '''
    print('\n############\n')
    print('* TemplateCompiledFile with AppendParameters')
    tmplResourceName = ResourceName(appSettings.getFolder('temp-lates-folder'), 'db-api-table-dep.table-api-insert.pg.tmpl.dep')
    confResourceName = ResourceName(appSettings.getFolder('con-fig-folder'), 'mock.db-api-table-table.pg.json')
    print('  - tmplResourceName', tmplResourceName.getResourceName())
    print('  - confResourceName', confResourceName.getResourceName())
    '''

    #AppSettingsTest().removeFolders()
    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()