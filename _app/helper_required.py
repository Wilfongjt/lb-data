"""
from helper import Helper
from app_settings import AppSettings
#from helper_test_object_json import HelperTestObjectJSON
import json
from list_forms import FormList
from list_fields import FieldList

class HelperRequired(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        self.dictionary = None
        self.lines = []

        self.expand = {"C": "required insert", "U": "required update", "R": "required read", "c": "optional insert",
                       "u": "optional update", "r": "optional read", "d": "delete", "I": "Imutable"}

    def set_dictionary(self, table_dictionary):
        self.dictionary = table_dictionary
        return self
    '''
    def getTypes(self):
        return [f for f in self.dictionary['forms']]
    '''
    def format(self):

        self.process()
        return self.lines

    def getForms(self, _type, crud_list):
        #crud_value ='C'
        # C is for required insert
        # U is for required update
        # I is required for update but is not updatable itself
        required = []
        #imputed = []
        #if crud_value in ['u','U']:
        #    imputed = [f for f in self.dictionary['forms'][_type]
        #                if 'json' in f
        #                and 'I' in f['json']]
        '''
        required = [f for f in FormList(self.dictionary, _type, [])
                    if 'json' in f
                    and crud_value in f['json']]
        '''
        required = FormList(self.dictionary, _type, crud_list)

        return required

    def getColumns(self, crud_list):
        #crud_value = 'C'
        required = []
        #required = [f
        #            for f in self.dictionary['fields']
        #            if 'crud' in f
        #            and crud_value in f['crud']]

        return FieldList(self.dictionary, crud_list)


def main():
    from test_func import test_table
    import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    #print("###################### Required")
    form_name = 'app'
    helper = HelperRequired().set_dictionary(test_table())
    # cols
    form_name='app'
    #print('xxx',type(helper.getColumns(['C'])) )
    assert type(helper.getColumns(['C'])) == FieldList

    #assert [f['name'] for f in FormList(test_table(), form_name, ['C'])]

    #print('xxx', [f['name'] for f in helper.getForms(form_name, ['C'])] )
    assert  [f['name'] for f in helper.getForms(form_name, ['C'])] == ['type', 'app-name', 'version', 'username','password']

    #print('xxx',[f['name'] for f in helper.getColumns('C')] )
    #assert [f['name'] for f in helper.getColumns('C')] == ['type', 'form', 'password']

    #
    #assert type(helper.getForms('app','C')) == list

    #print('yyy', [f['name'] for f in helper.getForms('app','C')] )
    assert [f['name'] for f in helper.getForms('app','C')] == ['type', 'app-name', "version", 'username','password']

    '''
    #
    assert type(helper.getForms('user','C')) == list
    assert [f['name'] for f in helper.getForms('user','C')] == ['type', 'app_id', 'username', 'password']
    #
    assert type(helper.getColumns('U')) == list
    assert [f['name'] for f in helper.getColumns('U')] == []
    #
    assert type(helper.getForms('app', 'U')) == list
    assert [f['name'] for f in helper.getForms('app','U')] == []
    #
    assert type(helper.getForms('user', 'U')) == list
    assert [f['name'] for f in helper.getForms('user','U')] == []
    '''
    #print("######################")

    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()
"""