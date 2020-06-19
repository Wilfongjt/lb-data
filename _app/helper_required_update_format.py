"""
from helper import Helper
from app_settings import AppSettings
#from helper_test_object_json import HelperTestObjectJSON
import json
from helper_required import HelperRequired
from list_fields import FieldList
from list_forms import FormList
from forms import FormKeyList
'''
['U','I']
'''
class HelperRequiredUpdateFormat(HelperRequired):
    '''
    returns  conditions to evaluate requirements for INSERT
    '''
    def __init__(self, step=None):
        super().__init__(step)
        self.dictionary = None
        self.lines = []
        self.crud_list = ['U','I']

    def getErrorResult(self):
        return {"result": "-2"}

    def getColumns(self):
        return FieldList(self.dictionary, self.crud_list)

    '''
    def getColumns(self):
        bigU = super().getColumns(self.crud_list)
        pk =[f for f in self.dictionary['fields'] if f['context']=='pk-uuid']

        return pk + bigU
    '''

    def getForms(self, _type):
        return FormList(self.dictionary, _type, self.crud_list)
    '''
     def getForms(self, _type):
        bigU = super().getForms(_type, self.crud_value)
        pk =[f for f in self.dictionary['fields'] if f['context']=='pk-uuid']
        immuted = []
        if self.crud_value in ['u','U']:
            imuted = [f for f in self.dictionary['forms'][_type]
                        if 'json' in f
                        and 'I' in f['json']]
        return imuted + bigU
    '''
    def getOptionalAttributes(self, _type):
        crud_value = 'u'
        print('type', _type)
        imutable = [f for f in FormList(self.dictionary,_type, ['u']) ]
        '''
        #imutable = [f for f in self.dictionary['forms'][_type]
        imutable = [f for f in self.dictionary['interfaces'][_type]['form']
                    if 'json' in f
                    and crud_value in f['json']]
        '''
        return imutable

    def process(self):
        # need to ensure that input object has required attributes
        # need to ensure that input object has values for required columns
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        # structure by type
        # if type in configured list
        #   if
        #     # attribute evaluation
        #     if not(required-attribute) throw error
        #     if not(required-attribute) throw error
        #     # column evaluation
        #     if not(required-column) throw error
        #     if not(required-column) throw error

        # elsif type in configured list

        #   # attribute evaluation
        #   if not(required-attribute) throw error
        #   if not(required-attribute) throw error
        #   # column evaluation
        #   if not(required-column) throw error
        #   if not(required-column) throw error

        # else
        #   error


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

            self.formatRequiredAttributes(_type, self.crud_list)
            self.formateOneOptionalAttribute(_type)
            #self.formatColumns(_type, self.crud_value)

            self.lines.append('  ')

        # end
        self.lines.append('              else')
        self.lines.append('                   return \'{}\'::JSONB;'.format(json.dumps(self.getErrorResult())))
        self.lines.append('              end if;')
        self.lines.append('            else')
        self.lines.append('                 return \'{}\'::JSONB;'.format(json.dumps(self.getErrorResult())))
        self.lines.append('            end if;')
        return self

    #####

    def formatRequiredAttributes(self, _type, crud_value):
        required_list = self.getForms(_type)

        self.lines.append('                  -- all of these')

        first = True
        ands = ''
        for f in required_list:
            if first:
                ands += '_json ? \'{}\''.format(f['name'])
                first = False
            else:
                ands += ' and _json ? \'{}\''.format(f['name'])
        condition = '                  '
        condition += 'if not({}) then return \'{{"result":"-2"}}\'::JSONB; end if;'.format(ands)
        self.lines.append(condition)

        return self

    def formateOneOptionalAttribute(self, _type):
        opt_list = self.getOptionalAttributes( _type)

        if len(opt_list) == 0:
            self.lines.append(self.lines.append('                  -- no optional atts'))
        else:
            first = True
            and_list = ''
            for f in opt_list:
                if first:
                    and_list += '_json ? \'{}\''.format(f['name'])
                    first = False
                else:
                    and_list += ' or _json ? \'{}\''.format(f['name'])
            condition = '                  '
            condition += 'if not({}) then return \'{{"result":"-2"}}\'::JSONB; end if;'.format(and_list)
            self.lines.append('                  -- at least one of these')
            self.lines.append(condition)
        return self
    #####

    def formatColumns(self, _type, crud_value):
        column_list = self.getColumns()

        self.lines.append('                  -- values for all of these')

        for f in FieldList(self.dictionary, ['U', "I"]):
            condition = '                  '
            condition += 'if not(_json ? \'{}\') then return \'{}\'::JSONB; end if; -- Req {} attr'\
                .format(f['name'], json.dumps(self.getErrorResult()), _type)
            self.lines.append(condition)

        return self
    '''
    def formatColumns(self, _type, crud_value):
        column_list = self.getColumns()

        self.lines.append('                  -- values for all of these')

        for f in column_list:
            condition = '                  '
            condition += 'if not(_json ? \'{}\') then return \'{}\'::JSONB; end if; -- Req {} attr'\
                .format(f['name'], json.dumps(self.getErrorResult()), _type)
            self.lines.append(condition)

        return self    
    '''

def main():
    from test_func import test_table
    import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    print("###################### Update HelperRequiredUpdateFormat")
    helper = HelperRequiredUpdateFormat().set_dictionary(test_table())
    lines = helper.format()
    print('\n'.join(lines))
    #
    assert type(helper.getColumns()) == FieldList
    print('xxx',[f['name'] for f in helper.getColumns()])
    assert [f['name'] for f in helper.getColumns()] == ['id', 'type']
    #    assert [f['name'] for f in helper.getColumns()] == ['id', 'type', 'form']

    #
    assert type(helper.getForms('app')) == FormList
    print('yyy', [f['name'] for f in helper.getForms('app')])
    assert [f['name'] for f in helper.getForms('app')] == ['id','type', 'app-name']
    #
    assert type(helper.getForms('user')) == FormList
    assert [f['name'] for f in helper.getForms('user')] == ['id','type', 'app_id']
    # getOptionalAttributes
    assert type(helper.getOptionalAttributes('app')) == list
    assert [f['name'] for f in helper.getOptionalAttributes('app')] == ['username', 'password']
    # getOptionalAttributes
    assert type(helper.getOptionalAttributes('user')) == list
    assert [f['name'] for f in helper.getOptionalAttributes('user')] == ['username', 'password']

    print("######################")
    # final page
    lines = helper.format()
    assert (type(lines) == list)  # is a list
    assert ('if _json ->> \'type\' = \'app\' then'.strip() in [f.strip() for f in lines])

    #assert ('if not(_json ? \'id\' and _json ? \'type\' and _json ? \'app-name\' and _json ? \'version\') then return \'{"result":"-2"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    assert ('if not(_json ? \'username\' or _json ? \'password\') then return \'{"result":"-2"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])
    assert ('elsif _json ->> \'type\' = \'user\' then'.strip() in [f.strip() for f in lines])
    assert ('if not(_json ? \'id\' and _json ? \'type\' and _json ? \'app_id\') then return \'{"result":"-2"}\'::JSONB; end if;'.strip() in [f.strip() for f in lines])



    print("###################### Update")
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