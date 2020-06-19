"""
from helper import Helper
from app_settings import AppSettings
import itertools
from helper_where_clause_format import HelperWhereClauseFormat
from list_fields import FieldList
'''
if all atts
elsif combinations
elsif
else
end if;
(a,b,c) (a,b) (a,c) (b,c), (a), (b), (c)
['_{} := _json ->> {}'.format(f['name'],self.f['name']) for f in FieldList(self.dictionary, ['u', 'U'])]
_id := _json ->> cast(_json::jsonb ->> 'uuid' as UUID)
_password := _json ->> 'password' 
_active := _json ->> 'active'
_form := _json - 'password'

tbl_prefix = self.dictionary['tbl-prefix']
if _json
    update reg_schema.register
        set
            reg_password = _password,  reg_active = _active, reg_form = _form 
        where
            reg_id='<uuid>' and reg_type='<type>'     

        set 
            [[update-columns]]
        where
           ' and '.join(['{}_{} = _{}'.format(tbl_prefix, f['name'],f['name']) for f in Fields(dict, ['I'])])
'''
class HelperUpdateCombosFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        self.dictionary = None
        self.lines=[]

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):
        self.process()
        return self.lines

    def process(self):
        '''
        generates a list of
        :return:
        '''
        rc = []
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        fieldname_combos = self.get_fieldname_combos()

        rows = self.get_rownames()
        #
        i = 0
        for name_list in fieldname_combos:
            d = ['_json ? \'{}\''.format(n) for n in name_list]

            if i == 0:
                self.lines.append('        '
                                  ''
                                  ''
                                  '    if {} then'.format(' and '.join(d)))
            else:
                self.lines.append('            elsif {} then'.format(' and '.join(d)))

            self.add_update_template(list(name_list)+rows)
            i += 1

        self.lines.append('            else')
        for name_list in rows[::-1]:
            #self.lines.append('            else')
            self.add_update_template([name_list])
        self.lines.append('            end if;')

        return self

    def get_rownames(self):

        row_names = [f['name'] for f in FieldList(self.dictionary,['F'])]
        #row_names = [f['name'] for f in self.dictionary['fields']
        #             if 'crud' in f and 'row' in f['context']]
        if len(row_names) < 1:
            raise Exception('No json role defined!')
        if len(row_names) > 1:
            raise Exception('Only 1 "form" context field allowed!')
        return row_names
    #def getRequired(self):


    def get_fieldname_combos(self):

        #names = ['_json ? \'{}\''.format(f['name']) for f in self.dictionary['fields'] if 'crud' in f and 'json' in f and 'c' in f['crud']]
        #names = [f['name'] for f in self.dictionary['fields']
        #         if 'crud' in f and 'u' in f['crud'] and 'row' not in f['context']]

        names = [f ['name'] for f in FieldList(self.dictionary,['u']) if 'row' not in f['context']]

        all_combinations = []
        for r in range(len(names) + 1):
            combinations_object = itertools.combinations(names, r)
            combinations_list = list(combinations_object)
            all_combinations += combinations_list

        r = [f for f in reversed(all_combinations)]
        r = r[:len(r)-1]
        return r

    def add_update_template(self, name_list):
        tblpfx = self.dictionary['tbl-prefix']
        set_names = [' {}_{} = _{}'.format(tblpfx, nm,nm) for nm in name_list]
        #set_rows = [' {}_{} = _{}'.format(tblpfx, nm, nm) for nm in self.get_rownames() ]
        #set_names.append('{}_{} = _{}'.format(tblpfx, ))
        #set_names = set_names + set_rows
        pfx = self.dictionary['LB_DB_PREFIX']
        tblname = self.dictionary['tbl-name']
        #where_lines = HelperWhereClauseFormat().set_dictionary(self.getConfigFile()).format()
        where_lines = HelperWhereClauseFormat().set_dictionary(self.dictionary).format()

        #self.lines.append('              update  ')
        self.lines.append('               update {}_schema.{}'.format(pfx, tblname))
        #self.lines.append('                set ')
        self.lines.append('                set {} '.format(', '.join(set_names)))
        self.lines.append('                where ')

        for w in where_lines:
            self.lines.append('       {}'.format(w))

        return self

def main():
    import pprint
    import os

    from test_func import test_table
    os.environ['LB-TESTING'] = '1'

    helper = HelperUpdateCombosFormat().set_dictionary(test_table())

    lines = helper.format()
    #print('get_fieldname_combos', helper.get_fieldname_combos())
    assert (type(lines)==list) # is a list

    pprint.pprint(lines)
    #print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
"""