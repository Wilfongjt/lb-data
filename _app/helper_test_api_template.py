
from helper import Helper
from app_settings import AppSettings
import itertools
#from helper_where_clause_format import HelperWhereClauseFormat
#from context_dict_test_data import ContextDictTestData
#from helper_test_object_json import HelperTestObjectJSON
import json
from context_dict import ContextDict, ContextKey
from list_fields import FieldList
from list_forms import FormList
from forms import InsertForm, UpdateForm, FormKeyList
from pprint import pprint
# Todo
#   add form based tests

class HelperTestAPITemplate(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        #self.dictionary = None
        self.field_dictionary = None
        #self.contextDictTestData = None
        self.lines=[]
    '''
    def getContextDictTestData(self):
        if self.contextDictTestData == None:
            self.contextDictTestData = ContextDictTestData().read()
        # print('getContextDictTestData', self.contextDictTestData)

        return self.contextDictTestData
    '''
    '''
    def set_dictionary(self, table_dictionary ):
        if 'interfaces' not in table_dictionary:
            raise Exception('table dictionary missing interfaces')
        self.dictionary = table_dictionary
        return self
    '''
    def get_field_dictionary(self):
        if self.field_dictionary == None:
            self.field_dictionary = {f['name']: f for f in self.dictionary['fields']}

        return self.field_dictionary

    def template(self):
        self.process()
        return self.lines


    def process(self):
        print("* Test API")
        rc = []
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        print("  - Table: {}".format(self.dictionary['tbl-name']))
        self.lines.append('\c {}_db'.format(self.get('LB_DB_PREFIX')))

        self.lines.append('select \'##### {} TESTS\';'.format(self.get('tbl-name')))
        self.lines.append('BEGIN;')
        self.lines.append('  SELECT plan(5);')

        self.lines.append('  select \'###### {}\';'.format(self.get('tbl-name')))

        self.lines.append('  select \'############################################## Upsert \';')
        # the first combo is the good insert


        #combo_list = self.expectedColumnCombinations(self.getFields(), type='c')
        #print('dictionary',self.dictionary)
        #pprint(self.dictionary)
        for formKey in FormKeyList(self.dictionary):
            self.setInsertTest(formKey,  {"result":"1"})

        #self.setInsertTest(self.getFields(), combo_list[0], {"result":"2"})

        # Bad insert combinations
        #for combo in combo_list[1::] :
        #    print('combbo', combo)

        self.lines.append('  select \'#############################################\';')
        self.lines.append('  SELECT * FROM finish();')
        self.lines.append('  select \'##### {} TESTS Done\';'.format(self.get('tbl-name')))
        self.lines.append('ROLLBACK;')

        return self
    #def get_expected_row(self):

    def get_values(self, combo):
        rc = []

        for v in combo:

            if 'test' not in  self.get_field_dictionary()[v]:
                rc.append('TBD')
            elif type(self.get_field_dictionary()[v]['test']['good']) is dict:
                rc.append(json.dumps(self.get_field_dictionary()[v]['test']['good'] ))
            elif type(self.get_field_dictionary()[v]['test']['good']) is list:
                rc.append(json.dumps(self.get_field_dictionary()[v]['test']['good']))
            else:
                rc.append(self.get_field_dictionary()[v]['test']['good'] )

        #rc =[self.get_field_dictionary()[v]['test']['good'] for v in combo]
        return rc

    def expectedColumnCombinations(self, fields, type='c'):

        names = [f['name'] for f in fields
                 if ('crud' in f and type in f['crud']) or ('json' in f and type in f['json'])]
        all_combinations = []
        for r in range(len(names) + 1):
            combinations_object = itertools.combinations(names, r)
            combinations_list = list(combinations_object)
            all_combinations += combinations_list

        r = [f for f in reversed(all_combinations)]
        r = r[:len(r)-1]

        return r

    def insertJSON(self, attrib_list):
        print('attrib_list',attrib_list)
        #items = [f['name'] for f in self.dictionary['fields'] if 'json' in f and 'c' in f['json']]
        #print('insertRecord', items)
        print('combo', attrib_list['combo'])
        attribs = ['"{}":"{}"'.format(a, self.getGood(a)) for a in attrib_list['combo']]
        self.lines.append('      \'{{{}}}\'::JSONB'.format(', '.join(attribs)))
        expected = '"result":"{}"'.format('ccc')

        return expected

    def getForms(self):
        rc = []
        rc = [f for f in self.dictionary['forms']]
        return rc

    def getForms(self, type):
        rc = {}
        # get type from self.dictionary['forms']
        # print('forms',self.dictionary['forms'][type])
        print('rc', [f for f in self.dictionary['forms'][type]])
        rc = {f['name']:"{}".format(f['json']) for f in self.dictionary['forms'][type]}
        return rc

    def insertGoodTests(self):
        for combo in self.expectedInsertColumnCombinations('c'):
            self.lines.append('  select \'############################################## INSERTS {}\';'.format('-'.join(combo)))

            self.lines.append('  SELECT is (')
            self.lines.append('    {}_schema.{}('.format(self.get('LB_DB_PREFIX'), self.get('api-name')))
            self.lines.append('      sign(\'{"username":"testuser@register.com","role":"registrant"}\'::json, current_setting(\'app.jwt_secret\')),')

            attribs = ['"{}":"{}"'.format(a, self.getGood(a)) for a in combo['combo']]

            self.lines.append('      \'{{{}}}\'::JSONB'.format(', '.join(attribs)))
            self.lines.append('    )::JSONB,')
            self.lines.append('    \'{{"result":{}}}\'::JSONB,'.format(combo['expect']))
            self.lines.append('    \'{} testuser@request.com UPSERT\'::TEXT'.format(self.get('tbl-name')))
            self.lines.append('  );')

        return self


    def getForm(self, type_key):
        #return self.dictionary['forms'][type_key]
        return FormList(self.dictionary, type_key)

    def dep_getFields(self):

        #return self.dictionary['fields']
        return FieldList(self.dictionary)


    def get(self, key):

        return self.dictionary[key]

    def getTemper(self, field, temper):
        if 'default' in field:
            return field['default']
        #return self.getContextDictTestData().getTemper(field['context'], temper)
        return self.getContext().get(ContextKey('data-context', field))[temper]
    '''
    def getTestInsertObject(self, fields, temper='good'):

        rc = {f['name']:self.getTemper(f,temper) for f in fields if ('crud' in f and 'c' in f['crud']) or ('json' in f and 'c' in f['json'])}
        
        return rc
    '''


    '''
    def getTestUpdateObject(self, fields, temper='good'):

        rc = {f['name']:self.getTemper(f,temper) for f in fields
              if ('crud' in f
                and 'u' in f['crud'])
                or ('json' in f and 'u' in f['json'])}
        return rc
    '''

    def setInsertTest(self, formkey, expected):

        # first in list is good
        self.lines.append('  select \'######################################## INSERT {}\';')

        self.lines.append('  SELECT is (')
        #self.lines.append('    {}_schema.{}('.format(self.get('LB_DB_PREFIX'), self.get('api-name')))
        self.lines.append('    {}_schema.{}('.format(self.get('LB_DB_PREFIX'), self.dictionary['interfaces'][formkey]['name']))

        self.lines.append('      sign(\'{"username":"testuser@register.com","role":"registrant"}\'::json, current_setting(\'app.jwt_secret\')),')

        self.lines.append('      \'{}\'::JSONB'.format( json.dumps( self.getContext().goodify(InsertForm(self.dictionary, formkey)) )))

        self.lines.append('    )::JSONB,')

        self.lines.append('    \'{}\'::JSONB,'.format(json.dumps(expected)))

        self.lines.append('    \'{} testuser@request.com UPSERT\'::TEXT'.format(self.get('tbl-name')))

        self.lines.append('  );')

        return self



def main():
    import test_func
    import pprint
    import os

    os.environ['LB-TESTING'] = '1'


    #if 1== 1: exit(0)
    helper = HelperTestAPITemplate().set_dictionary(test_func.test_table())
    #lines = helper.template()
    #print('\n'.join(lines))
    #print('fields', helper.getRequiredFields())

    #assert type(helper.getFields())==FieldList
    #assert type(helper.getFields()[0])==dict
    #print('xxx', [f['name'] for f in helper.getFields()])
    #assert [f['name'] for f in helper.getFields()] == ['id', 'type', 'form', 'password', 'active', 'created', 'updated']

    print('lsit', helper.getForm('app'))
    print('type',type(helper.getForm('app') ))
    assert type(helper.getForm('app') ) == FormList
    assert type(helper.getForm('app')[0]) == dict
    #print('app', helper.getForm('app'))
    #print('app[0]', helper.getForm('app')[0])

    print('app',  [f['name'] for f in helper.getForm('app')] )
    assert [f['name'] for f in helper.getForm('app')] == ['id', 'type', 'app-name', 'version', 'username', 'password','token']

    #print('insert object', {'app-name': 'my-app', 'version': '1.0.0', 'app-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'})

    print('getTpye', helper.getForm('app'))

    #if 1==1 : exit(0)

    '''
    assert helper.getTestUpdateObject(helper.getForm('app')) == {'id': 'e53229aa-d09c-4cec-b566-ea553ae8078d', 'app-name': 'my-app', 'version': '1.0.0', 'app-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'}

    assert type(helper.getForm('user')) == list
    assert type(helper.getForm('user')[0]) == dict
    assert type(helper.getTestUpdateObject(helper.getForm('user'))) == dict

    assert helper.getTestUpdateObject(helper.getForm('user')) == {'id': 'e53229aa-d09c-4cec-b566-ea553ae8078d', 'username': 'John Smith', 'password': 't1T!tttt'}

    print('combo list',    helper.expectedColumnCombinations(helper.getFields(), type='c'))
    assert helper.expectedColumnCombinations(helper.getFields(), type='c') == [('type', 'attributes'), ('attributes',), ('type',)]
    '''

    lines = helper.template()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))

    #print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
