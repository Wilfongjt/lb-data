from function_weld import Function
from list_fields import FieldList
import itertools
from list_parse import MultiList_WhereClause
from context_dict import ContextDict, ContextKey
from pprint import pprint

# '<<table-fields>>'
class Function_TableFieldCode(Function):
    '''
    generates a list of table field definitions
    '''

    def __init__(self,dictionary={}, tmpl_line=''):
        super().__init__(dictionary, tmpl_line=tmpl_line)
        # dictionary is loaded by adding Function_TableFieldCode to Function_Anchor

    def process(self):
        '''
        generates a list of table field definitions
        '''

        if '<<table-fields>>' in self.tmpl_line:
            #print('found <<table-fields>>')
            # self.template.append('-- i am still a little teapot. D')
            context = ContextDict()
            # print('context', context)
            # print('field', FieldList(self.dictionary))
            # swap in field names using just a field from "tbl-fields" sub dict
            lst = [self.templatize(context.get(ContextKey('context', f)), f) for f in FieldList(self.dictionary)]
            #pprint(lst)
            # swap in table values using the whole dictioary
            #lst = [self.templatize(ln) for ln in lst]
            # print('context keys', lst)

            for l in lst:
                if l not in self:
                    self.append(l)

            #self.append(','.join(self))
            #print('self', self)
            self.tmpl_line = ',\n'.join(self)
            #print('toString', self.toString())
        return self

    def toString(self):
        if self.getNext() == None:
            return ',\n'.join(self)
        return self.getNext().toString()

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
    nxt = Function_TableFieldCode()
    tmpl_line = "<<table-fields>>"
    func =  Function_Anchor(dictionary_tbl, tmpl_line) \
            .add(nxt)
    print('toString', func.toString())
    assert func.toString().startswith('[[tbl-prefix]]_id TEXT PRIMARY KEY DEFAULT uuid_generate_v4 (),' )

    print('toString',func.toString())
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()