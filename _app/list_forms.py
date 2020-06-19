from pathlib import Path
from context_dict import ContextDict
'''
common lists of fields
getFields is all fields in table
control list with constraints ['c','C',...]
'''

class FormList(list):
    '''
    list of form items
    '''
    def __init__(self, tbl_dictionary, form_name, constraint_list=[] ):
        self.tbl_dictionary = tbl_dictionary
        self.constraint_list = constraint_list
        self.form_name = form_name
        if 'interfaces' in self.tbl_dictionary:
            if self.constraint_list == []:
                for f in self.tbl_dictionary['interfaces'][self.form_name]['form']:
                    self.append(f)
            else:
                for k in  [f for f in self.tbl_dictionary['interfaces'][self.form_name]['form']
                           if 'json' in f and any(ele in f['json'] for ele in self.constraint_list)]:
                    self.append(k)

        elif 'api-name' in self.tbl_dictionary:
            if self.constraint_list == []:
                for f in self.tbl_dictionary['api-form']:
                    self.append(f)
            else:
                for k in [f for f in self.tbl_dictionary['api-form']
                          if 'json' in f and any(ele in f['json'] for ele in self.constraint_list)]:
                    self.append(k)
'''

class FormList(list):
    def __init__(self, tbl_dictionary, form_name, constraint_list=[] ):
        self.tbl_dictionary = tbl_dictionary
        self.constraint_list = constraint_list
        self.form_name = form_name

        if self.constraint_list == []:
            for f in self.tbl_dictionary['forms'][self.form_name]:
                self.append(f)
        else:
            for k in  [f for f in self.tbl_dictionary['forms'][self.form_name]
                       if 'json' in f and any(ele in f['json'] for ele in self.constraint_list)]:
                self.append(k)
            #for k in  [f for f in self.tbl_dictionary['forms'][self.form_name]  ]:
            #    self.append(k)

'''
def main():
    import pprint
    import os
    from test_func import test_table

    os.environ['LB-TESTING'] = '1'
    form_name='app'
    form = FormList( test_table(), form_name)

    assert type(form) == FormList

    assert len(FormList(test_table(), form_name)) > 0

    assert [f['name'] for f in FormList(test_table(),form_name)] == ['id', 'type', 'app-name', 'version', 'username', 'password', 'token']

    assert [f['name'] for f in FormList(test_table(),form_name,['c'])] == []

    #print('FormList(test_table(),form_name,[C])]', [f['name'] for f in FormList(test_table(),form_name,['c','C'])] )

    assert [f['name'] for f in FormList(test_table(),form_name,['C','c'])] == ['type', 'app-name', 'version', 'username', 'password']
    '''
    assert [f['name'] for f in FormList(test_table(),form_name,['I'])] == ['id', 'type']
    assert [f['name'] for f in FormList(test_table(),form_name,['U'])] == ['form']
    assert [f['name'] for f in FormList(test_table(),form_name,['u'])] == ['password','active']
    assert [f['name'] for f in FormList(test_table(),form_name,['u','U'])] == ['form','password','active']
    assert [f['name'] for f in FormList(test_table(),form_name,['u','U','I'])] == ['id','type','form','password','active']
    assert [f['name'] for f in FormList(test_table(),form_name,['R'])] == ['id','type','form']
    assert [f['name'] for f in FormList(test_table(),form_name,['r'])] == ['active', 'created', 'updated']
    assert [f['name'] for f in FormList(test_table(),form_name,['r','R'])] == ['id','type','form','active', 'created', 'updated']
    '''
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()