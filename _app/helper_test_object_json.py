'''
from helper import Helper
from app_settings import AppSettings
import json
#from context_dict_test_data import ContextDictTestData
from context_dict import ContextDict, ContextKey
from pprint import pprint
'''
'''
formats any list of fields or attributes into a json object
do any field filtering before you add field list to this formatter 
'''


'''
class dep_HelperTestObjectJSON(Helper):
    def __init__(self, fields, step=None, temper='good', crud_value='c'):
        super().__init__(step)

        self.dictionary = None
        self.lines=[]
        self.context = None
        self.temper = temper
        self.fields = fields
        self.json_obj=None
        self.crud_value = crud_value

    def getContext(self):
        if self.context == None:
            self.context = ContextDict().read()

        return self.context

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):

        self.process()

        return self.lines

    def json(self):
        # return the dict representing json obj
        self.process()
        return self.json_obj

    def getTemper(self, field, temper):
        if 'default' in field:
            #print('default', field)
            return field['default']
        #print('temper context', self.getContextDictTestData().getTemper(field['context'], temper))
        #print('xfield', field)
        #print('xfield context', field['context'])

        #return self.getContextDictTestData().getTemper(field['context'], temper)
        #return self.getContextDict().getTemper(field['context'], temper)
        #pprint(self.getContext())
        #pprint(self.getContext()['data-context'])
        return self.getContext().get(ContextKey('data-context', field))[temper]

    def process(self):
        #print('fields', self.fields)
        self.json_obj = {f['name']: self.getTemper(f, self.temper) for f in self.fields}

        #self.lines.append('            -- sync json values to table values')
        if len(self.json_obj)==0:
            self.lines.append('            /* No assignments defined. Add  \'c\' to crud to fields. */')
        else:
            self.lines.append('            {}'.format(json.dumps(self.json_obj)))
        return self

def testFields():
    import test_func
    import os

    os.environ['LB-TESTING'] = '1'
    helper = dep_HelperTestObjectJSON(test_func.test_table()['tbl-fields'])
    assert (type(helper.json()) == dict)  # is a dict
    assert helper.json() == {'id': 'e53229aa-d09c-4cec-b566-ea553ae8078d', 'type': 'app', 'password': 't1T!tttt', 'form': {}, 'created': '2020-04-30 22:34:25.919433', 'updated': '2020-04-30 22:34:25.919433', 'active': 'true'}
    #print('json', helper.json())
    os.environ['LB-TESTING'] = '0'

def testFormApp():
    import test_func
    import os
    os.environ['LB-TESTING'] = '1'
    _form = 'app'
    #print('test_table', test_func.test_table())
    helper = dep_HelperTestObjectJSON(test_func.test_table()['forms'][_form])
    assert (type(helper.json()) == dict)  # is a dict
    print('helper.json()',helper.json())
    assert helper.json() == {'id': 'e53229aa-d09c-4cec-b566-ea553ae8078d', 'type': 'app', 'app-name': 'my-app', 'version': '1.0.0', 'username': 'abc@xyx.com', 'password': 't1T!tttt', 'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'}

    #print('json', helper.json())
    os.environ['LB-TESTING'] = '0'

def main():

    import pprint
    import os
    os.environ['LB-TESTING'] = '1'

    testFields()
    testFormApp()

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
'''