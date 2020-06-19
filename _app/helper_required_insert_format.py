"""
from helper import Helper
from app_settings import AppSettings
#from helper_test_object_json import HelperTestObjectJSON
import json
from helper_required import HelperRequired
from forms import FormKeyList, FormList


class HelperRequiredInsertFormat(HelperRequired):
    '''
    returns  conditions to evaluate requirements for INSERT
    '''
    def __init__(self, step=None):
        super().__init__(step)
        self.dictionary = None
        self.lines = []
        self.crud_value = 'C'
        self.error_no = -1

    def getErrorResult(self):
        self.error_no -= 1
        #return {"result": str(self.error_no)}
        return str(self.error_no)

    def getColumns(self):
        return super().getColumns(self.crud_value)

    def getForms(self, _type):
        return super().getForms(_type, self.crud_value)

    def getTypeField(self):
        lst = [f for f in self.dictionary['fields'] if 'context' in f and 'type' in f['context']]
        return lst[0]

    def process(self):
        # need to ensure that input object has required attributes
        # need to ensure that input object has values for required columns
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        # structure by type
        # if type in configured list
        #   # attribute evaluation
        #   if not(required-attribute) throw error
        #   if not(required-attribute) throw error
        #   # column evaluation
        #   if not(required-column) throw error
        #   if not(required-column) throw error
        # elsif type in configured list
        #   # attribute evaluation
        #   if not(required-attribute) throw error
        #   if not(required-attribute) throw error
        #   # column evaluation
        #   if not(required-column) throw error
        #   if not(required-column) throw error
        # else
        #   error

        crud_value = 'C'
        first = True

        condition = 'if _json ? \'type\' then'
        self.lines.append( '            {}'.format(condition ))

        #for _type in self.getTypes():

        for _type in FormKeyList(self.dictionary):
            condition = 'if _json ->> \'type\' = \'{}\' then'.format(_type)

            if not first:
                condition = 'els' + condition
            first = False
            self.lines.append('              {}'.format(condition))
            self.lines.append('  ')

            self.formatRequiredAttributes(_type, crud_value)

            self.formatColumns(_type, crud_value)
            self.lines.append('  ')

        # end
        self.lines.append('              else')
        self.lines.append('                 return \'{{"result":{}}}\'::JSONB;'.format(json.dumps(self.getErrorResult())))
        self.lines.append('              end if;')
        self.lines.append('            else')
        self.lines.append('                 return \'{{"result":{}}}\'::JSONB;'.format(json.dumps(self.getErrorResult())))
        self.lines.append('            end if;')
        return self

    #####

    def formatRequiredAttributes(self, _type, crud_value):

        #required_list = self.getForms(_type) # FormList(self.dictionary, _type, crud_list)
        required_list = FormList(self.dictionary, _type, ['C'])
        self.lines.append('                  -- expected form values on insert')

        first = True
        ands = ''
        for f in required_list:
            if first:
                ands += '_json ? \'{}\''.format(f['name'])
                first = False
            else:
                ands += ' and _json ? \'{}\''.format(f['name'])
        condition = '                  '
        condition += 'if not({}) then return \'{{"result":"{}"}}\'::JSONB; end if;'.format(ands, self.getErrorResult())
        self.lines.append(condition)

        return self
    '''
    def formatRequiredAttributes(self, _type, crud_value):
        #attribute_list = self.getForms(_type, crud_value)
        attribute_list = self.getForms(_type)
        self.lines.append('                -- Required {} Attributes'.format(self.expand[crud_value]))
        self.lines.append('                -- MAO: {}'.format(

        HelperTestObjectJSON(attribute_list, crud_value).json()))
        for f in attribute_list:
            condition = '                '
            condition += 'if not(_json ? \'{}\') then return \'{{"result":"{}"}}\'::JSONB; end if; -- req attr in {}-object'\
                .format(f['name'], self.getErrorResult(), _type)
            self.lines.append(condition)

        return self
    '''
    #####

    '''
    def formatValidateColumns(self, crud_value):
        self.lines.append('              -- * validation is future need')
        return self
    '''

    def formatColumns(self, _type, crud_value):
        # column_list = self.getColumns(crud_value)
        required_list = self.getColumns()

        # self.lines.append('              -- expected: {}'.format(HelperTestObjectJSON(required, crud_value ).json()) )
        self.lines.append('                  -- required insert columns')
        first = True
        ands = ''
        for f in required_list:
            if first:
                ands += '_json ? \'{}\''.format(f['name'])
                first = False
            else:
                ands += ' and _json ? \'{}\''.format(f['name'])
        condition = '                  '
        condition += 'if not({}) then return \'{{"result":"{}"}}\'::JSONB; end if;'.format(ands,self.getErrorResult())
        self.lines.append(condition)
        '''
        for f in required_list:
            condition = '                  '
            condition += 'if not(_json ? \'{}\') then return \'{}\'::JSONB; end if;  -- Req {} col'\
                .format(f['name'], json.dumps(self.getErrorResult()), _type)
            self.lines.append(condition)
        '''
        return self
'''

'''

def main():
    from test_func import test_table
    import pprint
    import os
    from list_fields import FieldList
    from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    print("###################### Insert")
    helper = HelperRequiredInsertFormat().set_dictionary(test_table())
    #assert type(helper.getColumns('C')) == list
    #assert len(helper.getColumns('C')) == 2
    #assert type(helper.getForms('app','C')) == list
    #assert type(helper.getForms('user','C')) == list
    print([f['name'] for f in helper.getColumns()])

    # getTypeField
    #print('type', helper.getTypeField())
    assert type(helper.getTypeField()) == dict
    assert helper.getTypeField()['context'] == 'type'
    # getColumns
    assert type(helper.getColumns()) == FieldList
    print('xxx', [f['name'] for f in helper.getColumns()] )
    assert [f['name'] for f in helper.getColumns()] == ['type', 'password']
    #assert [f['name'] for f in helper.getColumns()] == ['type', 'form','password']

    # getForms
    assert type(helper.getForms('app')) == FormList
    print('yyy', [f['name'] for f in helper.getForms('app')])
    assert [f['name'] for f in helper.getForms('app')] == ['type', 'app-name', 'version', 'username', 'password']

    assert type(helper.getForms('user')) == FormList
    #print('zzz',[f['name'] for f in helper.getForms('user')])
    assert [f['name'] for f in helper.getForms('user')] == ['type', 'app_id','username','password']

    print("######################")
    # final page
    lines = helper.format()
    assert (type(lines) == list)  # is a list

    print('\n'.join(lines))
    assert (type(lines) == list)  # is a list
    # look for line in lines
    assert ('if _json ->> \'type\' = \'app\' then'.strip() in [f.strip() for f in lines])
    # required insert form fields app
    #assert ('if not(_json ? \'type\' and _json ? \'app-name\' and _json ? \'version\' and _json ? \'username\' and _json ? \'password\') then return \'{"result":"-1"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    # reqired insert user form fields
    #assert ('if not(_json ? \'type\' and _json ? \'app_id\' and _json ? \'username\' and _json ? \'password\') then return \'{"result":"-1"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])

    assert ('elsif _json ->> \'type\' = \'user\' then'.strip() in [f.strip() for f in lines])
    #assert ('if not(_json ? \'type\' and _json ? \'app_id\' and _json ? \'username\' and _json ? \'password\') then return \'{"result":"-1"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    #assert ('if not(_json ? \'type\' and _json ? \'password\') then return \'{"result":"-1"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    #assert ('if not(_json ? \'type\' and _json ? \'form\' and _json ? \'password\') then return \'{"result":"-1"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    # assert ('_json := _json - \'password\''.strip() in [f.strip() for f in lines])

    print('\n'.join(lines))

    print("###################### insert")
    '''
    helper = HelperRequiredUpdateFormat().set_dictionary(test_func.test_table())

    # final page
    lines = helper.format()
    assert (type(lines) == list)  # is a list
    print('\n'.join(lines))
    '''
    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()
"""