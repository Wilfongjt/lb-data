import re
import os
import json
from pprint import pprint

class ParseTagToList(list):
    """
    value tag [[name]] is short hand for [[None.None:None.{{name}}]]
    singleton '[[field.context.pk.{{name}}]]'
    multiple '[[field.crud.C.{{name}}.and]]'
    multiple '[[field.crud.(C).{{name}}.and]]'

    """

    def __init__(self, parsable ):
        self.parsable = parsable
        # print('ParseTagToList', parsable)
        # handle the [[name]] to [[None.None:None.{{}}]]
        tag_pattern = re.compile('\[\[[a-z\-]+\]\]')
        s = tag_pattern.match(parsable)
        #print('s',s)
        if s != None and s.group() == parsable:
            self.parsable = self.parsable.replace('[[','[[None.None:None.{{').replace(']]','}}]]')

        tag_pattern = re.compile('\[\[[A-Z\-_]+\]\]')
        s = tag_pattern.match(parsable)

        if s != None and s.group() == parsable:
            self.parsable = self.parsable.replace('[[', '[[None.None:None.{{').replace(']]', '}}]]')

        #print('ParseTagToList', self.parsable)


        self.process()

    def process(self):
        parts = self.parse()

        for i in parts: self.append(i)

        #print('ParseTagToList', self)


    def parse(self):
        # print('parse parsable', self.parsable)
        if '..' in self.parsable:
            parts = self.parsable.replace('[[', '').replace(']]', '').split('..')  # ['aaa','bbb:ccc','ddd']
        else:
            parts = self.parsable.replace('[[', '').replace(']]', '').split('.')  # ['aaa','bbb:ccc','ddd']

        parts[1] = parts[1].split(':')

        # filter value is array when () are present
        if '(' in parts[1][1]:
            parts[1][1] = list(parts[1][1].replace('(', '').replace(')', ''))

        return parts

    def getListKey(self):
        """ [[TBL-FIELDS.context:pk.{{name}}]]"""
        #return self[0][0]

        return self[0]

    def getFilterKey(self):
        """ [[tbl-fields.CONTEXT:pk.{{name}}]]"""
        return self[1][0]

    def getFilterValue(self):
        """ [[tbl-fields.context:PK.{{name}}]]"""
        #print('filterValue ', self[1])
        return self[1][1]

    def getAttTmpl(self):
        """ [[tbl-fields.context:pk.{{NAME}}]]"""
        #return self[2][0]
        return self[2]

    def getDelimeter(self):
        """ [[tbl-fields.context:pk.{{name}}.AND]]"""
        #print('getDelimeter 1')
        if len(self)==4:
            #print('getDelimeter 2 ',self[3])

            return self[3]
            #return self[3][0]
        #print('getDelimeter out')

        return ''

class Parse_WhereClause(ParseTagToList):
    def __init__(self):
        super().__init__("[[tbl-fields.crud:(I).{{tbl-prefix}}_{{name}} = cast(_json::jsonb ->> '{{name}}' as {{type}}). and ]]")

class MultiList(list):
    """
    create a single line template list
    """
    def __init__(self, parseTagToList, tbl_dictionary):
        self.tbl_dictionary = tbl_dictionary
        self.parseTagToList=parseTagToList

        #print('type',self.parseTagToList.getFilterValue(), '  type', type(self.parseTagToList.getFilterValue()))
        if self.parseTagToList.getListKey() == 'None':
            # [[None.None:None.{{field-key}}]] Special Case
            #print('A ')

            field_key = self.parseTagToList.getAttTmpl().replace('{', '').replace('}', '')
            value = self.parseTagToList.getAttTmpl() # assume field dictionary doesnt have this value set a passthrough value
            #print('MultiList field_key',field_key)
            #print('os.environ',os.environ)
            if field_key in tbl_dictionary:
                #print('B ')
                value = tbl_dictionary[field_key] # tbl_dictionary is really a field_dictionary ... a subset of tbl_dictionary
            elif field_key in self.tbl_dictionary: # look in root of dictionary
                #print('C ')
                value = self.tbl_dictionary[field_key]
            elif field_key in os.environ:
                #print('D')
                value = os.environ[field_key]
            else:
                #print('E dictionary', tbl_dictionary)
                _type = None
                if 'type' in self.tbl_dictionary:
                    _type = self.tbl_dictionary['type']

                raise Exception('Cannot find value for \'{}\' in "type":"{}". Add to your .env file, dictionary, initialize AppSettings object or modify template'.format(field_key, _type))
            #print('E ')
            self.append(value)

        elif self.parseTagToList.getFilterKey() == '*': # like ['*', '*']
            print('F')
            print('- F ', self.parseTagToList)
            # all fields
            # eg '[[db-extensions.*:*.CREATE EXTENSION IF NOT EXISTS {{name}}.; ]]'
            #print('getListKey', self.parseTagToList.getListKey())
            #print('dict', self.tbl_dictionary)
            #print('getAttTmpl',self.parseTagToList.getAttTmpl())
            #print('ext', ('db-extensions' in self.tbl_dictionary))
            #print('dict',self.tbl_dictionary[self.parseTagToList.getListKey()] )
            for lyttle_dictionary in [f for f in self.tbl_dictionary[self.parseTagToList.getListKey()]]:
                self.append(self.templatize(self.parseTagToList.getAttTmpl(), lyttle_dictionary))
        elif type(self.parseTagToList.getFilterValue()) == list: # like ['C']
            # eg '[[tbl-fields.crud:(C).{{tbl-prefix}}_{{name}}., ]]'
            #print('G', self.parseTagToList.getFilterValue())

            for lyttle_dictionary in [f for f in self.tbl_dictionary[self.parseTagToList.getListKey()]
                if self.parseTagToList.getFilterKey() in f and any(ele in f[self.parseTagToList.getFilterKey()] for ele in self.parseTagToList.getFilterValue())]:
                self.append(self.templatize(self.parseTagToList.getAttTmpl(), lyttle_dictionary))

        else:
            #print('H')
            # eg: select from tbl_dictionary['tbl-fields'] where has filterkey and [filterkey] == filtervalue
            # print('dictioary', self.tbl_dictionary)
            for lyttle_dictionary in [f for f in self.tbl_dictionary[self.parseTagToList.getListKey()]
                if self.parseTagToList.getFilterKey() in f and self.parseTagToList.getFilterValue() == f[self.parseTagToList.getFilterKey()]]:
                self.append(self.templatize(self.parseTagToList.getAttTmpl(), lyttle_dictionary))

    def templatize(self, template_line, lyttle_dictionary):
        #print('templateize 5 {}'.format(template_line))
        # print('lyttle_dictionary', lyttle_dictionary)
        for key_ in lyttle_dictionary:
            v = lyttle_dictionary[key_]
            # brute force the root keys, skipping values of type list and dict
            if type(v) == dict:
                #print('hi dict {}'.format(json.dumps(v)))
                k = '{{' + key_ + '}}'
                template_line = template_line.replace(k, json.dumps(v))

            elif type(v) != list:
                #print('A process key', key_, ' v ', v)
                k = '{{' + key_ + '}}'
                template_line = template_line.replace(k, str(v))
        # take care of {{}} wrapped values
        if '{{' in template_line: # didnt match so look in root...brute force
            for key_ in self.tbl_dictionary:
                v = self.tbl_dictionary[key_]
                if type(v) != list and type(v) != dict:
                    #print('B process key', key_, ' v ', v)
                    k = '{{' + key_ + '}}'
                    template_line = template_line.replace(k, str(v))
        if '{{' in template_line: # may ref something in memory
            for key_ in os.environ:
                if key_.startswith('LB_'):
                    v = os.environ[key_]
                    k = '{{' + key_ + '}}'
                    template_line = template_line.replace(k, str(v))
        if '{{' in template_line:
            raise Exception('Undefined tag {}'.format(template_line))
        #print('template_line', template_line)
        return template_line

    def toString(self):
        return self.parseTagToList.getDelimeter().join(self)

#ParseTagToList("[[tbl-fields.crud:(R).{{tbl-prefix}}_{{name}} = cast(_json::jsonb ->> '{{name}}' as {{type}}). and ]]")
class MultiList_WhereClause(MultiList): #{{tbl-prefix}}_{{name}} = cast(_json::jsonb ->> '{{name}}' as {{type}}
    def __init__(self, tbl_dictionary):
        super().__init__(Parse_WhereClause(), tbl_dictionary)


def main():
    from test_func import test_table, test_db
    from app_settings import AppSettingsTest
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os
    #from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest()
    ##
    print('#########')
    parseList = ParseTagToList('[[tbl-name]]')
    print('A parseList', parseList)
    print('A multi', MultiList(parseList, test_table()))
    print('A toString', MultiList(parseList, test_table()).toString())

    assert parseList == ['None', ['None', 'None'], '{{tbl-name}}']
    assert MultiList(parseList, test_table()) == ['register']
    assert MultiList(parseList, test_table()).toString() == 'register'

    # singleton environment
    '''
    parseList = ParseTagToList('[[LB_SECRET_PASSWORD]]')
    print('K parseList', parseList)
    print('K MultiList', MultiList(parseList, test_table()))
    print('K toString', MultiList(parseList, test_table()).toString())
    assert parseList == ['None', ['None', 'None'], '{{LB_SECRET_PASSWORD}}']
    assert MultiList(parseList, test_table()) == ['PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG']
    assert MultiList(parseList, test_table()).toString() == 'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG'
    '''
    print('#########')
    ## singleton
    parseList = ParseTagToList('[[tbl-fields.context:pk.{{name}}]]')
    print('A parseList', parseList)
    print('A multi', MultiList(parseList, test_table()))
    print('A toString', MultiList(parseList, test_table()).toString() )

    assert parseList == ['tbl-fields', ['context', 'pk'], '{{name}}']
    assert MultiList(parseList, test_table()) == ['id']
    assert MultiList(parseList, test_table()).toString() == 'id'

    print('#########')
    ## singleton
    parseList = ParseTagToList('[[tbl-fields.context:type.{{context}}-{{type}}]]')
    print('B parseList', parseList)
    print('B multi', MultiList(parseList, test_table()))
    print('B toString', MultiList(parseList, test_table()).toString() )
    assert parseList == ['tbl-fields', ['context', 'type'], '{{context}}-{{type}}']
    assert MultiList(parseList, test_table()) == ['type-TEXT']
    assert MultiList(parseList, test_table()).toString() == 'type-TEXT'
    print('#########')
    ## singleton with multiple attributes
    parseList = ParseTagToList('[[tbl-fields.context:pk.{{name}}-{{type}}]]')
    print('C parseList', parseList)
    print('C MultiList',MultiList(parseList, test_table()) )
    print('C toString', MultiList(parseList, test_table()).toString() )

    assert parseList == ['tbl-fields', ['context', 'pk'], '{{name}}-{{type}}']
    assert MultiList(parseList, test_table()) == ['id-TEXT']
    assert MultiList(parseList, test_table()).toString() == 'id-TEXT'
    print('#########')
    ## multi with array value
    parseList = ParseTagToList('[[tbl-fields.crud:(C).{{name}}. and ]]')
    print('D parseList', parseList)
    print('D getFilterValue', parseList.getFilterValue())
    print('D MultiList', MultiList(parseList, test_table()) )
    print('D toString', MultiList(parseList, test_table()).toString() )
    assert parseList == ['tbl-fields', ['crud', ['C']], '{{name}}', ' and ']
    assert MultiList(parseList, test_table()) == ['type', 'password']
    assert MultiList(parseList, test_table()).toString() == 'type and password'

    print('#########')
    ## multi with array value
    parseList = ParseTagToList('[[tbl-fields.crud:(Cc).{{name}}. and ]]')
    print('E parseList', parseList)
    print('E MultiList',MultiList(parseList, test_table()) )
    print('E toString', MultiList(parseList, test_table()).toString() )
    assert parseList == ['tbl-fields', ['crud', ['C','c']], '{{name}}', ' and ']
    assert MultiList(parseList, test_table()) == ['type', 'password']
    assert MultiList(parseList, test_table()).toString() == 'type and password'
    print('#########')
    ##
    parseList = ParseTagToList("[[tbl-fields.crud:(Cc).json ? '{{name}}'. or ]]")
    print('F parseList', parseList)
    print('F MultiList',MultiList(parseList, test_table()) )
    print('F toString', MultiList(parseList, test_table()).toString() )
    assert parseList == ['tbl-fields', ['crud', ['C', 'c']], "json ? '{{name}}'", ' or ']
    assert MultiList(parseList, test_table()) == ["json ? 'type'", "json ? 'password'"]
    assert MultiList(parseList, test_table()).toString() == "json ? 'type' or json ? 'password'"
    print('#########')
    ##
    parseList = ParseTagToList("[[tbl-fields.crud:(Cc).json ? '{{context}}-{{type}}'. and ]]")
    print('G parseList', parseList)
    print('G MultiList',MultiList(parseList, test_table()) )
    print('G toString', MultiList(parseList, test_table()).toString() )

    assert parseList == ['tbl-fields', ['crud', ['C', 'c']], "json ? '{{context}}-{{type}}'", ' and ']
    assert MultiList(parseList, test_table()) == ["json ? 'type-TEXT'", "json ? 'password-TEXT'"]
    assert MultiList(parseList, test_table()).toString() == "json ? 'type-TEXT' and json ? 'password-TEXT'"

    print('#########')
    ##
    parseList = ParseTagToList('[[tbl-fields.*:*.Declare _{{name}} {{type}}; ]]')
    print('H parseList', parseList)
    print('H MultiList', MultiList(parseList, test_table()))
    print('H toString', MultiList(parseList, test_table()).toString())

    assert parseList == ['tbl-fields', ['*', '*'], "Declare _{{name}} {{type}}; "]
    assert MultiList(parseList, test_table()) == ['Declare _id TEXT; ', 'Declare _type TEXT; ', 'Declare _form JSONB; ', 'Declare _password TEXT; ', 'Declare _active BOOLEAN; ', 'Declare _created TIMESTAMP; ', 'Declare _updated TIMESTAMP; ']
    assert MultiList(parseList, test_table()).toString() == 'Declare _id TEXT; Declare _type TEXT; Declare _form JSONB; Declare _password TEXT; Declare _active BOOLEAN; Declare _created TIMESTAMP; Declare _updated TIMESTAMP; '

    print('#########')
    #"[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]"
    ##
    parseList = ParseTagToList('[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]')
    print('I parseList', parseList)
    print('I MultiList', MultiList(parseList, test_table()))
    print('I toString', MultiList(parseList, test_table()).toString())

    assert parseList == ['tbl-fields', ['crud', ['C', 'c']], '{{tbl-prefix}}_{{name}}', ', ']
    assert MultiList(parseList, test_table()) == ['reg_type', 'reg_password']
    assert MultiList(parseList, test_table()).toString() == 'reg_type, reg_password'

    print('#########')


    # '[[db-extensions.*:*.create extension IF NOT EXISTS {{name}}.; ]]'
    #pprint(test_db())
    parseList = ParseTagToList('[[db-extensions.*:*.create extension IF NOT EXISTS {{name}};.; ]]')
    print('J parseList', parseList)
    print('J MultiList', MultiList(parseList, test_db()))
    print('J toString', MultiList(parseList, test_db()).toString())

    assert parseList == ['db-extensions', ['*', '*'], 'create extension IF NOT EXISTS {{name}};', '; ']
    assert MultiList(parseList, test_db()) == ['create extension IF NOT EXISTS pgcrypto;', 'create extension IF NOT EXISTS pgtap;', 'create extension IF NOT EXISTS pgjwt;', 'create extension IF NOT EXISTS "uuid-ossp";']
    assert MultiList(parseList, test_db()).toString() == 'create extension IF NOT EXISTS pgcrypto;; create extension IF NOT EXISTS pgtap;; create extension IF NOT EXISTS pgjwt;; create extension IF NOT EXISTS "uuid-ossp";'

    print('#########')
    print('K Parse_WhereClause',Parse_WhereClause())
    print('K MultiList_WhereClause(MultiList)', MultiList_WhereClause(test_table()))
    print('K toString', MultiList_WhereClause(test_table()).toString())

    assert Parse_WhereClause() == ['tbl-fields', ['crud', ['I']], "{{tbl-prefix}}_{{name}} = cast(_json::jsonb ->> '{{name}}' as {{type}})", ' and ']
    assert MultiList_WhereClause(test_table()) == ["reg_id = cast(_json::jsonb ->> 'id' as TEXT)", "reg_type = cast(_json::jsonb ->> 'type' as TEXT)"]
    assert MultiList_WhereClause(test_table()).toString() == "reg_id = cast(_json::jsonb ->> 'id' as TEXT) and reg_type = cast(_json::jsonb ->> 'type' as TEXT)"

    print('#########')
    #"[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]"
    ##
    parseList = ParseTagToList('[[api-test-forms..type:insert..select {{LB_DB_PREFIX}}_schema.{{api-name}}(\'{{form}}\'::TEXT);]]')
    print('L parseList', parseList)
    print('L MultiList', MultiList(parseList, InterfaceConfiguration('app').load(test_table())))
    print('L toString',  MultiList(parseList, InterfaceConfiguration('app').load(test_table())).toString())

    assert parseList == ['api-test-forms', ['type', 'insert'], 'select {{LB_DB_PREFIX}}_schema.{{api-name}}(\'{{form}}\'::TEXT);']

    #                                                                                 ['select reg_schema.app(\'{                           "type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}\'::TEXT);']
    assert MultiList(parseList, InterfaceConfiguration('app').load(test_table())) == ['select reg_schema.app(\'{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}\'::TEXT);']

    assert MultiList(parseList, InterfaceConfiguration('app').load(test_table())).toString() == 'select reg_schema.app(\'{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}\'::TEXT);'

    print('#########')
    #"[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]"
    ##
    parseList = ParseTagToList('[[models.*:*.ALTER DATABASE {{LB_DB_PREFIX}}_db SET "{{app-key}}" TO \'{{model}}\';]]')
    print('M parseList', parseList)
    print('M MultiList', MultiList(parseList, test_db()))
    print('M toString',  MultiList(parseList, test_db()).toString())

    # assert parseList == ['model', ['*', '*'], 'ALTER DATABASE {{LB_DB_PREFIX}}_db SET "{{app-key}}" TO \'{{LB_JWT_PASSWORD}}\';']
    #assert parseList == ['models', ['*', '*'], 'ALTER DATABASE {{LB_DB_PREFIX}}_db SET "{{app-key}}" TO \'{{model}}\';']
    assert parseList == ['models', ['*', '*'], 'ALTER DATABASE {{LB_DB_PREFIX}}_db SET "{{app-key}}" TO \'{{model}}\';']

    #assert MultiList(parseList, test_db()) == ['ALTER DATABASE reg_db SET "app.jwt_secret" TO \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';']

    #assert MultiList(parseList, test_db()).toString() == 'ALTER DATABASE reg_db SET "app.jwt_secret" TO \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';'
    print('#########')

    ##
    parseList = ParseTagToList('[[api-privileges..type:FUNCTION..GRANT {{privilege}} ON {{type}} {{LB_DB_PREFIX}}_schema.{{api-name}} ({{parameters}}) TO {{role}};]]')
    print('N parseList', parseList)
    print('N MultiList', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ))
    print('N toString', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString())

    assert parseList == ['api-privileges', ['type', 'FUNCTION'], 'GRANT {{privilege}} ON {{type}} {{LB_DB_PREFIX}}_schema.{{api-name}} ({{parameters}}) TO {{role}};']
    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ) == ['GRANT EXECUTE ON FUNCTION reg_schema.app (JSONB) TO anonymous;']
    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString() == 'GRANT EXECUTE ON FUNCTION reg_schema.app (JSONB) TO anonymous;'

    print('#########')

    ##
    parseList = ParseTagToList('[[api-test-forms..type:insert..{{pattern}}]]')
    print('O parseList', parseList)
    print('O MultiList', MultiList(parseList, InterfaceConfiguration('user').load(test_table()) ))
    print('O toString', MultiList(parseList, InterfaceConfiguration('user').load(test_table()) ).toString())

    assert parseList == ['api-test-forms', ['type', 'insert'], '{{pattern}}']
    assert  MultiList(parseList, InterfaceConfiguration('user').load(test_table()) ) == ['{"username": "testuser@register.com", "role": "anonymous"}']
    assert  MultiList(parseList, InterfaceConfiguration('user').load(test_table()) ).toString() == '{"username": "testuser@register.com", "role": "anonymous"}'

    print('#########')

    ##
    parseList = ParseTagToList("[[api-test-forms..type:select..( matches( {{db-prefix}}_schema.{{api-name}}( {{token}}, {{form}} )::JSONB, {{expected}}, {{description}} )::JSONB ->> 'result' ) ->> 'token']]")
    print('P parseList', parseList)
    print('P MultiList', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ))
    print('P toString', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString())

    assert parseList == ['api-test-forms', ['type', 'select'], "( matches( {{db-prefix}}_schema.{{api-name}}( {{token}}, {{form}} )::JSONB, {{expected}}, {{description}} )::JSONB ->> 'result' ) ->> 'token'"]
    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ) == ['( matches( reg_schema.app( sign(\'{"username": "testuser@register.com", "role": "anonymous"}\', current_setting(\'app.jwt_secret\') ), {"id": "my-test-app@1.0.0"} )::JSONB, [a-zA-Z\\.0-9_]+, app - select and check token )::JSONB ->> \'result\' ) ->> \'token\'']
    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString() == '( matches( reg_schema.app( sign(\'{"username": "testuser@register.com", "role": "anonymous"}\', current_setting(\'app.jwt_secret\') ), {"id": "my-test-app@1.0.0"} )::JSONB, [a-zA-Z\.0-9_]+, app - select and check token )::JSONB ->> \'result\' ) ->> \'token\''
    print('#########')

    ##
    parseList = ParseTagToList("[[api-test-forms..type:insert..is ( {{db-prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]")
    print('Q parseList', parseList)
    print('Q MultiList', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ))
    print('Q toString', MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString())

    assert parseList == ['api-test-forms', ['type', 'insert'], "is ( {{db-prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );"]

    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ) == ['is ( reg_schema.app( sign(\'{"username": "testuser@register.com", "role": "anonymous"}\', current_setting(\'app.jwt_secret\')), \'{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}\'::JSONB )::JSONB, \'{"status": "200", "msg": "ok"}\'::JSONB, \'app - insert test\'::TEXT );']

    assert  MultiList(parseList, InterfaceConfiguration('app').load(test_table()) ).toString() == 'is ( reg_schema.app( sign(\'{"username": "testuser@register.com", "role": "anonymous"}\', current_setting(\'app.jwt_secret\')), \'{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}\'::JSONB )::JSONB, \'{"status": "200", "msg": "ok"}\'::JSONB, \'app - insert test\'::TEXT );'


if __name__ == "__main__":
    main()