import json
import os.path
#from copy_file import CopyFile
from file import FileAsDict
from app_settings import AppSettings, AppSettingsTest
from pprint import pprint

'''
ContextKey formats a key in the form of a dictionary
{'name':'<context-name>','key':'<str>'}
{'name':'<context-name>','key':'<context>-<type>'}
'''
class ContextKey(dict):
    '''
    Goal: find template in one of the context sub-lists (eg "context", "search-context", "data-context")
    Method: search sub-list by string-value
    Method: search sub-list by Fields where <context>-<type>
    this search is not descrite and may return multiple option
    throw exception('Mutiple context values found for <context>-<value>)
    '''
    def __init__(self,context, field):
        #self.append( {"name": context, "key": '{}-{}'.format(field['context'],field['type'])})
        #print('contextkey', context, field)
        #print('contextkey', context, field)

        if type(field) == dict:
            #if field[''].startswith('LB_'):
            #    context = 'lyttlebit'
            #print('type dict')
            self['name'] = context
            self['key'] = '{}-{}'.format(field['context'],field['type'])
        elif type(field)==str:
            if field.startswith('LB_'): # LB_ is only with string
                context = 'lyttlebit'
            #print('type str')
            self['name'] = context
            self['key'] = field


class ContextDict(FileAsDict):
#class ContextDict():

    def __init__(self, foldername=None, filename='context.template.list.json'):
        super().__init__(foldername, filename)

        self.tagid='templates'
        self.lbtesting = os.getenv('LB-TESTING') or '0'
        self.appSettings = AppSettings()
        #print('lbtesting', self.lbtesting)
        if self.lbtesting == '1':
            self.appSettings = AppSettingsTest()
            # default to source code resource, assume we are going to copy
            #self.setFolderName(self.appSettings.getResourceFolder('shared'))
            self.setFolderName((self.appSettings.getFolder('shared-folder')))

        self.setFolderName(self.appSettings.getFolder('shared-folder'))

        self.read()
        #print('ContextDict',self.getFolderName())

    def loadEnv(self):
        # get LB_ env vars
        if 'lyttlebit' not in self:
            self['lyttlebit'] = {}

        for v in os.environ:
            if v.startswith('LB_'):
                self['lyttlebit'][v]= os.getenv(v)

        return self

    def read(self):

        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())

        if not os.path.exists(path_filename):
            raise NameError('Missing file: {}'.format( path_filename))

        with open(path_filename) as json_file:
            contextDict= json.load(json_file)

        for key in contextDict:
            if not key.startswith('LB_'):
                self[key] = contextDict[key]
        self.loadEnv()
        return self

    #def getDictionary(self):
    #    return self.templatesDict
    '''
    def getTemplateList(self, key):
        val = None
        if key in self:
            val = self[key]
        return val
    '''
    def get(self, contextKey):
        #print('ContextKey A', contextKey)
        # switch context when LB_

        val = None

        if contextKey['name'] in self:
            #print('ContextKey B', contextKey)
            if contextKey['key'] in self[contextKey['name']]:
                #print('ContextKey C', contextKey)
                val = self[contextKey['name']][contextKey['key']]

        if val == None:
            #print('context', self)
            raise NameError('Unknown ContextKey', json.dumps(contextKey) )
        return val

    def goodify(self, form):
        # return a dict with fake values
        for k in form:
            if form[k] == 'NA':
                form[k]=self.get(ContextKey('data-context', '{}-good'.format(k) ))

        return form

    def badify(self, form):
        # return a dict with fake values
        for k in form:
            form[k]=self.get(ContextKey('data-context', '{}-bad'.format(k) ))

        return form

def main():
    os.environ['LB-TESTING'] = '1'
    #from app_settings import AppSettingsTest()
    print('* Test ContextDict')
    res_folder = AppSettingsTest().getResourceFolder('shared')
    #shared_folder = AppSettings().getFolder('shared-folder')
    temp_folder = AppSettingsTest().getFolder('temp-folder')

    AppSettingsTest().createFolders()

    print('conteskKey1', ContextKey('search-context', 'uuid') )

    assert ContextKey('search-context', 'uuid') == {'name': 'search-context', 'key': 'uuid'}
    assert ContextKey('search-context', 'LB_PROJECT_prefix') == {'name': 'lyttlebit', 'key': 'LB_PROJECT_prefix'}

    contextKey=ContextKey('search-context', {
        "name": "id",
        "context": "pk",
        "type": "UUID",
        "crud": "RI"
    })
    lb_contextKey = ContextKey('lyttlebit', 'LB_PROJECT_prefix')
    pk_UUID_contextKey = {"name": "search-context", "key": "pk-UUID"}

    print('conteskKey2', contextKey)
    assert contextKey == {'name': 'search-context', 'key': 'pk-UUID'}
    assert lb_contextKey == {'name': 'lyttlebit', 'key': 'LB_PROJECT_prefix'}

    #contextDict = ContextDict().read()
    contextDict = ContextDict()

    #pprint(contextDict)
    assert len(contextDict) > 0

    assert contextDict.get(contextKey) ==  "[[tbl-prefix]]_[[name]]= cast(_json::jsonb ->> '[[name]]' as UUID)"
    assert contextDict.get(lb_contextKey) ==  "reg"
    assert contextDict.get(pk_UUID_contextKey) == "[[tbl-prefix]]_[[name]]= cast(_json::jsonb ->> '[[name]]' as UUID)"

    form = {'email':'', 'type':''}
    print('form', contextDict.goodify(form))
    print('form', contextDict.badify(form))

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()