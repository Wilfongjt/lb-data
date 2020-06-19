"""
from helper import Helper
from app_settings import AppSettings
import json
from list_fields import FieldList
# [[insert-sync-json-values]]
class HelperInsertSyncJSONValuesFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.dictionary = None
        self.lines=[]
        self.error_no = -20

    def getErrorResult(self):
        self.error_no -= 1
        #return {"result": str(self.error_no)}
        return str(self.error_no)

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def getRowField(self):
        #print('getRowField', self.dictionary)
        #return [f for f in self.dictionary['tbl-fields'] if 'row' in f['context']][0]
        #print('getRowField',FieldList(self.dictionary, ['F']))
        return FieldList(self.dictionary, ['F'])[0]

    def getPasswordField(self):
        return [f for f in self.dictionary['tbl-fields'] if 'password' in f['context']][0]

    def getForms(self):
        return [f for f in self.dictionary['forms']]

    def format(self):

        self.process()

        return self.lines

    '''
                types       types
    fields      app         user
    ------      --------    --------
    id          id          id
    type        type        type
                app-name    app_id
                version
                username    username
    pass-word   password    password
                app-token
    attributes
    created
    updated
    active
    '''
    def getRequiredFields(self):
        return [f
                for f in self.dictionary['tbl-fields']
                if 'crud' in f
                and 'C' in f['crud']]
                #and 'JSONB' not in f['type']]

    def getOptionalFields(self):
        return [f for f in self.dictionary['tbl-fields']
                if 'crud in f'
                and 'c' in f['crud']]

    def formatObject(self):
        return ['_{} := _json-\'password\';\n'.format(f['name'], f['name'])
                            for f in self.dictionary['fields']
                            if 'crud' in f
                            and ('c' in f['crud'] or 'C' in f['crud'])
                            and 'JSONB' in f['type']
                            and 'row' in f['context']]

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')


        #json_assignments = ['_{} := _json-\'password\';\n'.format(f['name'], f['name'])
        #               for f in self.dictionary['fields']
        #               if 'crud' in f and ('c' in f['crud'] or 'C' in f['crud']) and 'JSONB' in f['type'] and 'row' in f['context']]
        #first = True
        sp2 = '  '
        msg = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
        msg += '-- required sync assignments'
        self.lines.append(msg)
        for f in self.getRequiredFields():
            cond = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
            cond += 'if _json ? \'{}\' then _{} := _json ->> \'{}\'; else return \'{{"result":"{}"}}\'::JSONB; end if;'\
            .format(f['name'],f['name'], f['name'], self.getErrorResult())
            self.lines.append(cond)
        msg = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
        msg += '-- sync attributes to object'
        self.lines.append(msg)
        cond = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
        cond += '_{} := _json - \'{}\';'.format(self.getRowField()['name'],self.getPasswordField()['name'])
        self.lines.append(cond)
        return self

class HelperUpdateSyncJSONValuesFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.dictionary = None
        self.lines = []

    def set_dictionary(self, table_dictionary):
        self.dictionary = table_dictionary
        return self

    def getInputPassword(self, _type):
        return [f for f in self.dictionary['forms'][_type]
                if 'json' in f
                and ('u' in f['json'] or 'U' in f['json'])
                and 'password' in f['context']]

    def getRequiredFields(self):
        return [f for f in self.dictionary['fields']
                if 'crud' in f
                and ('u' in f['crud'] or 'U' in f['crud'])
                and 'JSONB' not in f['type']]

    def getForms(self, _type):
        return [f for f in self.dictionary['forms'][type]
                if 'json' in f
                and ('c' in f['json'] or 'C' in f['json'])
                and 'JSONB' in f['type']
                and 'row' in f['context']]

    def formatObject(self, _type):
        # sample: _attribute := _cur_row || (_json - 'password')
        rc = ['-- code incomplete']


        return rc
    def format(self):

        self.process()

        return self.lines

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

def testUpdate():
    import test_func
    import os

    os.environ['LB-TESTING'] = '1'
    print('* Update')
    helper = HelperUpdateSyncJSONValuesFormat().set_dictionary(test_func.test_table())

    print('password', helper.formatObject('app'))

    print('fields', [f['name'] for f in helper.getRequiredFields()])

    assert [f['name'] for f in helper.getRequiredFields()] == ['password', 'active']
    #assert == ['_attribute := ']
    lines = helper.format()
    assert (type(lines) == list)  # is a list

    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '1'

def testInsert():
    from test_func import test_table
    import os
    os.environ['LB-TESTING'] = '1'

    print('* Insert')
    helper = HelperInsertSyncJSONValuesFormat().set_dictionary(test_table())
    print('fields', [f['name'] for f in helper.getRequiredFields()])
    assert [f['name'] for f in helper.getRequiredFields()] == ['type', 'password']
    #assert [f['name'] for f in helper.getRequiredFields()] == ['type', 'form', 'password']

    #assert [f['name'] for f in helper.getOptionalFields()] == []

    lines = helper.format()
    assert (type(lines)==list) # is a list

    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'

def main():
    import os

    os.environ['LB-TESTING'] = '1'
    testInsert()
    testUpdate()


    #pprint.pprint(lines)
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()


"""