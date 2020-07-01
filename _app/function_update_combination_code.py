from function_weld import Function
from list_fields import FieldList
import itertools
from list_parse import MultiList_WhereClause
import os

# '[[update-combination-code]]'
class Function_UpdateCombinationCode(Function):
    '''
    detect the expected possible form attribute combinations
    given: _form = {"id":1, "type":"app", "f1":"abc", "f2":"efg"}
    output:
    if _json ? 'f1' and _json ? 'f2' then
               update reg_schema.register
                set  reg_f1 = _f1,  reg_f2 = _f2,  reg_form = _form
                where
                   reg_id= cast(_json::jsonb ->> 'id' as UUID) and reg_type= cast(_json::jsonb ->> 'type' as TEXT)
                   ;
            elsif _json ? 'f2' then
               update reg_schema.register
                set  reg_f2 = _f2,  reg_form = _form
                where
                   reg_id= cast(_json::jsonb ->> 'id' as UUID) and reg_type= cast(_json::jsonb ->> 'type' as TEXT)
                   ;
            elsif _json ? 'f1' then
               update reg_schema.register
                set  reg_f1 = _f1,  reg_form = _form
                where
                   reg_id= cast(_json::jsonb ->> 'id' as UUID) and reg_type= cast(_json::jsonb ->> 'type' as TEXT)
                   ;
            else
               update reg_schema.register
                set  reg_form = _form
                where
                   reg_id= cast(_json::jsonb ->> 'id' as UUID) and reg_type= cast(_json::jsonb ->> 'type' as TEXT)
                   ;
            end if;
    '''

    def __init__(self,dictionary={}, tmpl_line=''):
        super().__init__(dictionary, tmpl_line=tmpl_line)
        # dictionary is loaded by adding Function_SimpleTemplatize to Function_Anchor

    def process(self):
        '''
        generates a list of

        '''
        #print('Function_UpdateCombinationCode 1')
        # load up a temporary template so we can templateize it before final assembly
        if '<<update-combination-code>>' not in self.tmpl_line:
            #print('Function_UpdateCombinationCode 1 out')
            return self
        if 'tbl-fields' not in self.dictionary:
            raise Exception('Found <<update-combination-code>> template but missing "tbl-fields" in dictionary')

        #print('at <<update-combination-code>>')
        # wrangel data
        fieldname_combos = self.get_fieldname_combos() # List of possible combinations
        rows = self.get_rownames() # all rows that can be updated
        # first pass to compile the template, append everything to self

        i = 0

        for name_list in fieldname_combos:
            d = ['_json ? \'{}\''.format(n) for n in name_list]
            if i == 0:
                self.append('            if {} then'.format(' and '.join(d)))
            else:
                self.append('            elsif {} then'.format(' and '.join(d)))
            self.add_update_template(list(name_list)+rows)
            i += 1

        self.append('            else')
        for name_list in rows[::-1]:
            self.add_update_template([name_list])
        self.append('            end if;')

        # pull everything together and put in template_list

        #self.template_list.append(' \n'.join(self))
        self.tmpl_line = '\n'.join(self)
        #print('join','\n'.join(self))

        return self

    def get_template(self, contextKey):
        # the key might be code

        rc = self.get_context_dictionary().get(contextKey)

        if rc == None: # key might be code so return it if not found
            return 'context-key {} {} not found!'.format(contextKey['name'], contextKey['key'])

        return rc

    def get_context_dictionary(self):
        if self.context_dictionary == None:
            self.context_dictionary = ContextDict().read()

        return self.context_dictionary

    def get_fieldname_combos(self):

        names = [f ['name'] for f in FieldList(self.dictionary,['u']) if 'row' not in f['context']]

        all_combinations = []
        for r in range(len(names) + 1):
            combinations_object = itertools.combinations(names, r)
            combinations_list = list(combinations_object)
            all_combinations += combinations_list

        r = [f for f in reversed(all_combinations)]
        r = r[:len(r)-1]
        return r

    def get_rownames(self):

        row_names = [f['name'] for f in FieldList(self.dictionary,['F'])]
        #row_names = [f['name'] for f in self.dictionary['tbl-fields']
        #             if 'crud' in f and 'row' in f['context']]
        if len(row_names) < 1:
            raise Exception('No json role defined!')
        if len(row_names) > 1:
            raise Exception('Only 1 "form" context field allowed!')
        return row_names

    def add_update_template(self, name_list):
        tblpfx = self.dictionary['tbl-prefix']
        set_names = [' {}_{} = _{}'.format(tblpfx, nm,nm) for nm in name_list]

        #pfx = self.dictionary['LB_PROJECT_prefix']
        pfx = os.environ['LB_PROJECT_prefix']

        tblname = self.dictionary['tbl-name']
        #where_lines = HelperWhereClauseFormat().set_dictionary(self.dictionary).format()
        wh = MultiList_WhereClause(self.dictionary).toString()
        #print('MultiList_WhereClause(self.dictionary)', MultiList_WhereClause(self.dictionary))

        self.append('               update {}_schema.{}'.format(pfx, tblname))
        self.append('                set {} '.format(', '.join(set_names)))
        self.append('                where ')
        """
        wh = ''
        for w in where_lines:
            wh += '       {}'.format(w)

        wh = TemplatizedLine(self.dictionary, wh)[0]
        """
        self.append('{};'.format(wh))
        return self

def main():
    from function_anchor import Function_Anchor
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os
    from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    dictionary_db = InterfaceConfiguration('app').load(test_db())
    template = []

    ### F
    nxt = Function_UpdateCombinationCode()
    tmpl = "<<update-combination-code>>"
    func =  Function_Anchor(dictionary_tbl, tmpl) \
            .add(nxt)
    print('A Function nxt', nxt)
    print('A toString', func.toString())
    assert func.getTemplateLine().startswith("            if _json ? 'password' and _json ? 'active' then")


if __name__ == "__main__":
    main()