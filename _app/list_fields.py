from pathlib import Path
from context_dict import ContextDict
from pprint import pprint

'''
common lists of fields
getFields is all fields in table

'''

class FieldList(list):
    def __init__(self, tbl_dictionary, test_list=[]):
        self.tbl_dictionary = tbl_dictionary
        self.test_list = test_list
        if 'tbl-fields' not in tbl_dictionary:
            #pprint(self.tbl_dictionary)
            raise Exception('FieldList dictionary has no is "fields" key.')

        if test_list == []:
            #print('tbl_dictionary')
            #pprint(self.tbl_dictionary)
            for f in self.tbl_dictionary['tbl-fields']:
                self.append(f)
        else:
            print('FieldList ', self.tbl_dictionary)
            print('has field', 'tbl-fields' in self.tbl_dictionary )
            for k in [f for f in self.tbl_dictionary['tbl-fields']
                if 'crud' in f and any(ele in f['crud'] for ele in self.test_list) ]:
                self.append(k)
        #print('FieldList', [f['name'] for f in self])


def main():
    import pprint
    import os
    from test_func import test_table

    os.environ['LB-TESTING'] = '1'
    fields = FieldList(test_table())

    assert type(FieldList(test_table())) == FieldList
    assert len(FieldList(test_table())) > 0
    assert [f['name'] for f in FieldList(test_table())] == ['id', 'type', 'form', 'password', 'active', 'created', 'updated']
    print('required',[f['name'] for f in FieldList(test_table(),['C'])])
    assert [f['name'] for f in FieldList(test_table(),['C'])] == ['type', 'password']
    assert [f['name'] for f in FieldList(test_table(),['c'])] == []
    assert [f['name'] for f in FieldList(test_table(),['C','c'])] == ['type', 'password']
    assert [f['name'] for f in FieldList(test_table(),['I'])] == ['id', 'type']
    assert [f['name'] for f in FieldList(test_table(),['U'])] == []
    assert [f['name'] for f in FieldList(test_table(),['u'])] == ['password','active']
    assert [f['name'] for f in FieldList(test_table(),['u','U'])] == ['password','active']
    assert [f['name'] for f in FieldList(test_table(),['u','U','I'])] == ['id','type','password','active']
    assert [f['name'] for f in FieldList(test_table(),['R'])] == ['id','type','form']
    assert [f['name'] for f in FieldList(test_table(),['r'])] == ['active', 'created', 'updated']
    assert [f['name'] for f in FieldList(test_table(),['r','R'])] == ['id','type','form','active', 'created', 'updated']

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()