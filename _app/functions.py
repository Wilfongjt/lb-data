deprecated
'''

Function are applied to templates
a Function implements the swappinig of function tags for values within the template
'''
from list_fields import FieldList
from context_dict import ContextDict, ContextKey
from templatize import Templatize, TemplatizedLine
from forms import FormKeyList, FormList
from list_fields import FieldList
import json
import re
import itertools
#from helper_where_clause_format import HelperWhereClauseFormat
from list_parse import MultiList_WhereClause
from pprint import pprint
from const import Const
'''
Functions 
* accumulate output as a list
* the calling program is responcible for assembly

'''
class dep_depWeld(list):
    def __init__(self):
        #print('weld')
        self.prev = None
        self.next = None

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def add(self, link):
        # add to last item in list
        link.prev = self
        if self.next == None: # add to the end and return
            #link.setNo(1)
            self.next = link
        else:
            #link.setNo(1)
            self.next.add(link)

        return self

class dep_Function(list):
    # Base Class
    def __init__(self, dictionary, tmpl_line=''):
        super().__init__()
        self.dictionary = dictionary
        #self.template_list = template_list # a template list
        self.tmpl_line = tmpl_line
        self.error_no = 0
        self.context_dictionary=None
        #self.process()
        self.join_del = ' '

    def getClassName(self):
        return self.__class__.__name__

    def run(self):
        # pull data forward

        self.process()




    def process(self):
        self.append('-- i am a little teapot. {}'.format(self.getClassName()))
        return self

    def join(self):
        return self.join_del.join(self)
    '''
    def templatize(self, template_line, temp_dictionary=None):
        print('templateize 3')
        if temp_dictionary == None:
            temp_dictionary = self.dictionary

        for key_ in temp_dictionary:
            v = temp_dictionary[key_]
            if type(v) != list and type(v) != dict:
                #print('process key', key_, ' v ', v)
                template_line = template_line.replace('[[{}]]'.format(key_), v)

        if 'type' in temp_dictionary and temp_dictionary['type']== 'table':
            template_line = self.templatizeFields(template_line)

        #print('template', template_line)
        return template_line
    '''
    def templatizeFields(self, template_line):
        for f in FieldList(self.dictionary):
            template_line = self.templatize(template_line, f)
        return template_line

    def getErrorResult(self):
        self.error_no -= 1
        return '{}-{}'.format(self.getClassName(),str(self.error_no))

class dep_Function_NoTag(Function):
    # allow lines without tags into template output
    def process(self):
        if '[[' not in self.tmpl_line:
            self.append(self.tmpl_line) # use for testing
            self.template_list.append(self.tmpl_line)

class dep_Function_DeclareUpsert(Function):
    '''
    create declartaion statements for an upsert function
    CREATE OR REPLACE FUNCTION
                [[LB_DB_PREFIX]]_schema.[[api-name]](_token TEXT, _json JSONB) RETURNS JSONB
                AS $$
                    Declare rc jsonb;
                    Declare _cur_row JSONB;

                    Declare _anonymous JSONB;
                    Declare _registrant JSONB;
                    Declare _app_id TEXT;

                    [[declare-upsert]]  <<<<<<<<<<<<<<<<< here
    '''
    def process(self):
        #print('Function_DeclareUpsert A {} {} '.format(self.tmpl_line, '[[declare-upsert]]'),  '[[declare-upsert]]' in self.tmpl_line )
        if '[[declare-upsert]]' in self.tmpl_line:
            print('hi')
            declarations = ['Declare _{} {};'.format(f['name'], f['type']) for f in FieldList(self.dictionary)]

            for d in declarations: self.append(d)
            #print('Function_DeclareUpsert B', '\n'.join(self))
            self.template_list.append('\n'.join(self))
            #self.template_list.append('----------')
            #print('last', self.template_list[len(self.template_list)-1])
        return self

'''
not used
class dep_Function_DeleteParameterTypes(Function):
    def process(self):
        if '[[delete-parameter-types]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. T')
            self.template.append('-- i am still a little teapot. C')
            #
            for f in FieldList(self.dictionary,['D','R']):
'''


class dep_Function_Extentions(Function):
    def process(self):
        if '[[db-extensions]]' in self.tmpl_line:
            # self.template.append('-- i am still a little teapot. A')
            #for ln in ['CREATE EXTENSION IF NOT EXISTS "{}";'.format(n) for n in self.dictionary['db-extensions']]:
            #    self.append(ln)
            #pprint(self.dictionary)
            lst =  ['CREATE EXTENSION IF NOT EXISTS "{}";'.format(n) for n in self.dictionary['db-extensions']]
            for l in lst: self.append(l)
            #self.append('\n'.join(lst))
            self.template_list.append('\n'.join(self))


class dep_Function_TableFields(Function):
    def process(self):
        if '[[fields]]' in self.tmpl_line:
            #self.template.append('-- i am still a little teapot. D')
            context = ContextDict()
            #print('context', context)
            #print('field', FieldList(self.dictionary))
            # swap in field names using just a field from "tbl-fields" sub dict
            lst = [self.templatize(context.get(ContextKey('context', f)),f) for f in FieldList(self.dictionary)]

            # swap in table values using the whole dictioary
            lst = [self.templatize(ln) for ln in lst]
            #print('context keys', lst)

            for l in lst: self.append(l)
            self.template_list.append('\n'.join(self))


class dep_Function_DeleteParameterTypes(Function):
    def process(self):
        if '[[delete-parameter-types]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. E')
            self.template_list.append('-- i am still a little teapot. E')

class dep_Function_InsertSyncJSONValues(Function):
    """
     -- sync json values to table values
                [[insert-sync-json-values]]
    """
    def getRowField(self):
        return FieldList(self.dictionary, ['F'])[0]

    def getPasswordField(self):
        return [f for f in self.dictionary['tbl-fields'] if 'password' in f['context']][0]

    def process(self):
        if '[[insert-sync-json-values]]' in self.tmpl_line:
            #self.template.append('-- i am still a little teapot. F')
            sp2 = '  '
            msg = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
            msg += '-- required sync assignments'
            self.append(msg)
            # for f in self.getRequiredFields():
            for f in FieldList(self.dictionary,['C']): # required
                cond = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
                cond += 'if _json ? \'{}\' then _{} := _json ->> \'{}\'; else return \'{{"result":"{}"}}\'::JSONB; end if;' \
                    .format(f['name'], f['name'], f['name'], self.getErrorResult())
                self.append(cond)
            msg = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
            msg += '-- sync attributes to object'
            self.append(msg)
            cond = sp2 + sp2 + sp2 + sp2 + sp2 + sp2
            cond += '_{} := _json - \'{}\';'.format(self.getRowField()['name'], self.getPasswordField()['name'])

            self.append(cond)
            self.template_list.append('\n'.join(self))

# '[[insert-columns]]'
class dep_Function_InsertColumns(Function):
    """
                INSERT
                  INTO [[LB_DB_PREFIX]]_schema.[[tbl-name]]
                  (
                    [[insert-columns]]
                  ) VALUES (
                    [[insert-values]]
                  );
    """
    def process(self):
        if '[[insert-columns]]' in self.tmpl_line:
            #self.template_list.append('-- i am still a little teapot. G')

            prefix = self.dictionary['tbl-prefix']
            lines = ['{}_{}'.format(prefix, f['name'])
                     for f in FieldList(self.dictionary, ['C', 'c', 'F'])]

            for ln in lines: self.append(ln)

            self.template_list.append('                {}'.format(', '.join(self)))
            #self.template_list.append('-----------E')


# '[[insert-parameters]]'
class dep_Function_InsertParameters(Function):
    def process(self):
        if '[[insert-parameters]]' in self.tmpl_line:
            #self.template.append('-- i am still a little teapot. I')
            lines = [' _{} {}'.format(f['name'], f['type']) for f in FieldList(self.dictionary, ['c', 'C', 'F'])];
            for ln in lines: self.append(ln)
        self.template_list.append(', '.join(self))

# '[[insert-parameter-types]]'
class dep_Function_InsertParameterTypes(Function):
    def process(self):
        if '[[insert-parameter-types]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. J')
            self.template_list.append('-- i am still a little teapot. J')


# '[[insert-values]]'
class dep_Function_InsertValues(Function):
    """
      INSERT
                  INTO [[LB_DB_PREFIX]]_schema.[[tbl-name]]
                  (
                    [[insert-columns]]
                  ) VALUES (
                    [[insert-values]]
                  );
    """
    def process(self):
        if '[[insert-values]]' in self.tmpl_line:
            #self.template.append('-- i am still a little teapot. K')
            prefix = self.dictionary['tbl-prefix']
            # lines = HelperInsertColumnsFormat().set_dictionary(self.getConfigFile()).format()
            lines = ['{}_{}'.format(prefix, f['name'])
                     for f in FieldList(self.dictionary, ['C', 'c', 'F'])]
            for ln in lines: self.append(ln)
            #lines = ['                {}'.format(', '.join(lines))]
            self.template_list.append('                {}'.format(', '.join(self)))


# '[[required_insert_inputs]]'
class dep_Function_RequiredInsertInputs(Function):
    """
                -- check required attributes by type
                [[required_insert_inputs]]
    """
    def process(self):
        if '[[required_insert_inputs]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. L')
            self.template_list.append('-- i am still a little teapot. L')

'''
            if _json ? 'type' then
              if _json ->> 'type' = [[api-name]] then
                  -- expected form values on insert
                  if not(
                    [[expected-attributes-insert]]
                  ) then return '{"result":"-3.1"}'::JSONB; end if;
                  -- if not(_json ? 'type' and _json ? 'app-name' and _json ? 'version' and _json ? 'username' and _json ? 'password') then return '{"result":"-2"}'::JSONB; end if;
                  -- required insert columns
                  if not(
                    [[required-attributes-insert]]
                  )then return '{"result":"-3.2"}'::JSONB; end if;
                  --if not(_json ? 'type' and _json ? 'password') then return '{"result":"-3"}'::JSONB; end if;

              else
                 return '{"result":"-3.3"}'::JSONB;
              end if;
            else
                 return '{"result":"-3.4"}'::JSONB;
            end if;
'''

# '[[required_update_inputs]]'
class dep_Function_RequiredUpdateInputs(Function):
    """
    -- check required attributes by type
                [[required_update_inputs]]
    """
    def process(self):
        if '[[required_update_inputs]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. M')
            self.template_list.append('-- i am still a little teapot. M')
# '[[select-columns]]'
class dep_Function_SelectColumns(Function):
    def process(self):
        if '[[select-columns]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. N')
            self.template_list.append('-- i am still a little teapot. N')
# '[[select-parameter-types]]'
class dep_Function_SelectParameterTypes(Function):
    def process(self):
        if '[[select-parameter-types]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. O')
            self.template_list.append('-- i am still a little teapot. O')
# '[[set-defaults]]'
class dep_Function_SetDefaults(Function):
    def process(self):
        if '[[set-defaults]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. P')
            self.template_list.append('-- i am still a little teapot. P')
# '[[update-parameter-types]]'
class dep_Function_UpdateParameterTypes(Function):
    def process(self):
        if '[[update-parameter-types]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. Q')
            self.template_list.append('-- i am still a little teapot. Q')
# '[[update-sync-json-values]]'
class dep_Function_UpdateSyncJSONValues(Function):
    """
     -- sync-json-values to table values
                [[update-sync-json-values]]
    """
    def process(self):
        if '[[update-sync-json-values]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. R')
            self.template_list.append('-- i am still a little teapot. R')
# '[[update-columns]]'
class dep_Function_UpdateColumns(Function):
    def process(self):
        if '[[update-columns]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. S')
            self.template_list.append('-- i am still a little teapot. S')
# '[[update_combos_format]]'
'''
class dep_Function_UpdateCombosFormat(Function):
    """
                 -- all possible update combinations of updatable fields
                [[update_combos_format]]
    """
    def process(self):
        #print('hi A ************** {}'.format(self.tmpl_line))
        if '[[update_combos_format]]' in self.tmpl_line:
            print('hi B **************')
            self.append('-- i am still a little teapot. T')
            self.template_list.append('-- i am still a little teapot. T')
'''
# '[[where-clause]]'
class dep_Function_WhereClause(Function):
    def process(self):
        if '[[where-clause]]' in self.tmpl_line:
            self.append('-- i am still a little teapot. U')
            self.template_list.append('-- i am still a little teapot. U')



'''
assert 'Declare _id UUID;' in
Declare _type TEXT;
Declare _form JSONB;
Declare _password TEXT;
Declare _active BOOLEAN;
Declare _created TIMESTAMP;
Declare _updated TIMESTAMP;
'''
"""
class dep_Function_Reference(Function):
    # allow lines without tags into template output

    def setTag(self, tag):
        self.tag = tag
        return self

    def getTag(self):
        return self.tag

    def parse(self, group):
        parts = group.replace('[[', '').replace(']]', '').split('.')  # ['aaa','bbb:ccc','ddd']
        parts = [p.split(':') for p in parts]  # [['aaa'], ['bbb','ccc'], ['ddd']]

        return parts

    def getListKey(self, parts):
        # [['aaa'], ['bbb','ccc'], ['ddd']]
        return ''.join(parts[0])# aaa

    def getTmpl(self, parts):
        return parts[2][0]

    def getValueProcess(self, search_val):
        rc = Const().passthrough
        if '(' in search_val:  # '(ccc)' to ['c','c','c']
            rc = Const().convert_to_array
        return rc

    def getValue(self, group):
        # [['aaa'], ['bbb','ccc'], ['{{ddd}}']]
        # [['aaa'], ['bbb','(ccc)'], ['{{ddd}}']]
        # * 'ccc' implies equals: for f in table_dict if 'ccc' in f['bbb'],
        # * '(ccc) defines an in 'ccc' contains: f in table_dict if 'ccc' in f['bbb']
        #['c','c','c']
        parts = self.parse(group)
        #print('parts', parts)
        ######
        list_key = self.getListKey(parts)  # aaa
        att_tmpl = self.getTmpl(parts)  # {{ddd}}

        search_key = ''.join(parts[1][0])  # bbb
        search_val = ''.join(parts[1][1])  # ccc
        # discover how to process the search valu
        val_process = self.getValueProcess(search_val)
        if val_process == Const().convert_to_array: # convert to array
            search_val = search_val.replace('(', '').replace(')', '')
            search_val = list(search_val)
        else: # passthrough unchanged
            search_val = search_val

        # llook for field in template
        p = re.compile('{{[a-z]+}}')
        s = p.search(att_tmpl)

        rpl_att_key = s.group()
        att_key = rpl_att_key.replace('{', '').replace('}', '')

        #print('att_tmpl', att_tmpl)
        #print('search_val', search_val)
        #print('rpl_att_key', rpl_att_key)
        lst = []
        if list_key == 'tbl-fields': # fields
            #print('process fields')
            if val_process == Const().passthrough:
                lst = [att_tmpl.replace(rpl_att_key, f[att_key]) for f in self.dictionary[list_key] if
                       search_val in f[search_key]]
                if len(lst) != 1:
                    raise Exception('Expected only a single value but found: {}'.format((len(lst))))
                val = ''.join(lst)
            elif val_process == Const().convert_to_array:
                lst = [att_tmpl.replace(rpl_att_key, f[att_key]) for f in FieldList(self.dictionary, search_val)]
                if len(lst) == 0:
                    raise Exception('Expected at least 1 value but found: {}'.format((len(lst))))
                val = ' and '.join(lst)
        else: # interface
            #print('process interface')
            if val_process == Const().passthrough:
                #print('search_key',search_key)
                #print('search_val',search_val)

                lst = [att_tmpl.replace(rpl_att_key, f[att_key])
                       for f in self.dictionary[list_key]
                            if search_val == f[search_key]]
                if len(lst) != 1:
                    #print('lst',lst)
                    raise Exception('Expected only a single value but found: {}'.format((len(lst))))
                val = ''.join(lst)
            elif val_process == Const().convert_to_array:
                lst = [att_tmpl.replace(rpl_att_key, f[att_key])
                       for f in FormList(self.dictionary, self.dictionary['api-name'], search_val)]
                if len(lst) == 0:
                    raise Exception('Expected at least 1 value but found: {}'.format((len(lst))))
                val = ' and '.join(lst)

        # lst = [f[att_key] for f in self.dictionary[list_key] if search_val in f[search_key]]
        #lst = [att_tmpl.replace(rpl_att_key, f[att_key]) for f in self.dictionary[list_key] if search_val in f[search_key]]
        # should only be one value in list
        #if len(lst) != 1:
        #    raise Exception('Expected only a single value but found: {}'.format((len(lst))))

        #val = ''.join(lst)
        return val

    def templatize(self, template_line):
        for key_ in self.dictionary:
            v = self.dictionary[key_]
            if type(v) != list and type(v) != dict:
                # print('process key', key_, ' v ', v)
                template_line = template_line.replace('[[{}]]'.format(key_), v)
                # print('templ', template_line)

        return template_line

    def process(self):
        # pattern [[abc.bbb:ccc.{{ddd}}]]
        # example [[tbl-fields.context:pk.{{name}}]]
        # meaning look in fields list for field with context == pk and return the att-value for name
        # p = re.compile('\[\[[a-z\-]+[\.][a-z\-]+[:][a-z\-]+[\.][a-z\-]+\]\]')
        p = re.compile( '\[\[[a-z\-]+[\.][a-z\-]+[:][A-Za-z\-]+[\.][{}()a-z\-]+\]\]'
                       '|\[\[[a-z\-]+[\.][a-z\-]+[:][()A-Za-z\-]+[\.][\'\s?{}_()a-z\-]+[\.][and]+\]\]')
        #print('tmpl_line', self.tmpl_line)
        all_occ = p.findall(self.tmpl_line)
        #print('findall', all_occ)
        if len(all_occ) > 0:
            for group in all_occ: self.append(group) # stash for test

            for group in self:
                val = self.getValue(group)
                self.tmpl_line = self.tmpl_line.replace(group, ''.join(val))


            self.template_line = self.templatize(self.tmpl_line)
        self.template_list.append(self.tmpl_line)

        return self
"""
'''
def test_reference(dictionary_tbl):
    print('-------------------------- A')
    # single tag with first field list value

    ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.context:pk.{{name}}]]yyy',[])
    print('ref', ref)
    assert ref == ['[[tbl-fields.context:pk.{{name}}]]']
    assert  ref.template_list == ['xxxidyyy']
    print('-------------------------- B')
    # single tag with last field list value

    ref = Function_Reference(dictionary_tbl, 'aaaa [[tbl-fields.context:updated.{{name}}]] bbb',[])
    assert ref == ['[[tbl-fields.context:updated.{{name}}]]']
    assert ref.template_list == ['aaaa updated bbb']
    print('-------------------------- C')
    # single tag within a string first field list value

    ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.context:pk.aaa{{name}}bbb]]yyy', [])
    print('ref', ref)
    assert ref == ['[[tbl-fields.context:pk.aaa{{name}}bbb]]']
    assert ref.template_list == ['xxxaaaidbbbyyy']

    print('-------------------------- D')
    # single tag within a code like string first field list value

    ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.context:pk.length({{name}})]] < 8', [])
    print('ref', ref)
    assert ref == ['[[tbl-fields.context:pk.length({{name}})]]']
    assert ref.template_list == ['xxxlength(id) < 8']

    print('-------------------------- E')
    # multiple tags of same return value

    ref = Function_Reference(dictionary_tbl, 'aaaa [[tbl-fields.context:updated.{{name}}]] bbb aaaa [[tbl-fields.context:updated.{{name}}]] bbb', [])
    assert ref == ['[[tbl-fields.context:updated.{{name}}]]', '[[tbl-fields.context:updated.{{name}}]]']
    assert ref.template_list == ['aaaa updated bbb aaaa updated bbb']

    print('-------------------------- F')
    # multiple tags with diff return values

    ref = Function_Reference(dictionary_tbl, 'aaaa [[tbl-fields.context:updated.{{name}}]] bbb aaaa [[tbl-fields.context:pk.{{name}}]] bbb', [])
    assert ref == ['[[tbl-fields.context:updated.{{name}}]]', '[[tbl-fields.context:pk.{{name}}]]']
    assert ref.template_list == ['aaaa updated bbb aaaa id bbb']

    print('-------------------------- G.1')
    # concatination delemeter
    # single tag within a code like string first field list value
    # pk is only in fields once so 'and' will not appear in list
    ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.context:pk.length({{name}}).and]]yyy', [])
    print('* ref', ref)
    assert ref == ['[[tbl-fields.context:pk.length({{name}}).and]]']
    print('* ref.template_list', ref.template_list)
    assert ref.template_list == ['xxxlength(id)yyy']

    print('-------------------------- G.2')
    # concatination delemeter
    # single tag within a template string with a list of one Field
    # crud:C  has several fields so templat and template ...
    #ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.crud:(C). {{name}}).and]]yyy', [])
    ref = Function_Reference(dictionary_tbl, "xxx[[tbl-fields.crud:(C)._json ? '{{name}}'.and]]yyy", [])

    print('* ref', ref)
    assert ref == ["[[tbl-fields.crud:(C)._json ? '{{name}}'.and]]"]

    print('* ref.template_list', ref.template_list)
    assert ref.template_list == ["xxx_json ? 'type' and _json ? 'password'yyy"]

    print('-------------------------- G.2')
    # concatination delemeter
    # single tag within a template string with a list of one Field
    # crud:C  has several fields so templat and template ...
    #ref = Function_Reference(dictionary_tbl, 'xxx[[tbl-fields.crud:(C). {{name}}).and]]yyy', [])
    ref = Function_Reference(dictionary_tbl, "xxx[[api-form.json:(C)._json ? '{{name}}'.and]]yyy", [])

    print('* ref', ref)
    assert ref == ["[[api-form.json:(C)._json ? '{{name}}'.and]]"]
    print('', [f['name'] for f in FormList(dictionary_tbl, 'app' ,['C'])] )
    print('* ref.template_list', ref.template_list)
    assert ref.template_list == ["xxx_json ? 'type' and _json ? 'app-name' and _json ? 'version' and _json ? 'username' and _json ? 'password'yyy"]
'''

def test_decalare_upsert(dictionary_tbl):
    print('test_decalare_upsert start')

    func = Function_DeclareUpsert(dictionary_tbl, '[[declare-upsert]]', [])
    assert 'Declare _id UUID;' in func
    assert 'Declare _id UUID;' in func.template_list[0]

    print('test_decalare_upsert end')
'''
def test_Function_update_combination_code(dictionary_tbl):
    print('test')
    func = Function_UpdateCombinationCode(dictionary_tbl,'[[update-combination-code]]',[])
    #assert func[0].startswith('            if _json ? \'password\'') and func[len(func)-1].endswith('end if;')
    print('test_Function_update_combination_code', func)
    #assert func[len(func)-1].endswith('end if;')

    #print('Function_UpdateCombinationCode A', func)
    print('Function_UpdateCombinationCode B', func.template_list[0])
    #assert func.template_list[0].startswith('            if _json ? \'password\'') and func.template_list[0].endswith('end if;')
'''
def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os
    from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    dictionary_db = InterfaceConfiguration('app').load(test_db())
    template = []

    func = Function(dictionary_tbl,'-- gen from default tmpl')
    func.run()
    #    .add()
    

    print('Function_NoTag', Function_NoTag(dictionary_tbl,'-- gen from default tmpl'))
    assert '-- gen from default tmpl' in Function_NoTag(dictionary_tbl,'-- gen from default tmpl')
    #assert 'Declare _id UUID;' in Function_DeclareUpsert(dictionary_tbl, '[[declare-upsert]]', [])
    assert 'CREATE EXTENSION IF NOT EXISTS "pgcrypto";' in Function_Extentions(dictionary_db, '[[db-extensions]]', [])

    # print('Function_TableFields',Function_TableFields(dictionary_tbl, '[[tbl-fields]]', template))
    assert 'reg_id uuid PRIMARY KEY DEFAULT uuid_generate_v4 ()' in Function_TableFields(dictionary_tbl, '[[tbl-fields]]', [])
    assert '            -- required sync assignments' in Function_InsertSyncJSONValues(dictionary_tbl, '[[insert-sync-json-values]]', [])

    #print('fn',Function_InsertColumns(dictionary_tbl, '[[insert-columns]]', template))
    assert Function_InsertColumns(dictionary_tbl, '[[insert-columns]]', [])==['reg_type', 'reg_form', 'reg_password']
    #print('fn', Function_InsertParameters(dictionary_tbl, '[[insert-parameters]]', []).template)
    assert  Function_InsertParameters(dictionary_tbl, '[[insert-parameters]]', []) == [' _type TEXT', ' _form JSONB', ' _password TEXT']

    #print('fu', Function_InsertValues(dictionary_tbl, '[[insert-values]]', template))
    assert Function_InsertValues(dictionary_tbl, '[[insert-values]]', []) == ['reg_type', 'reg_form', 'reg_password']
    assert Function_RequiredInsertInputs(dictionary_tbl, '[[required_insert_inputs]]', []) == ['-- i am still a little teapot. L']

    test_reference(dictionary_tbl)

    test_decalare_upsert(dictionary_tbl)
    
    test_Function_update_combination_code(dictionary_tbl)

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
