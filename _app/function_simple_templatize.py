from function_weld import Weld, Function
from function_anchor import Function_Anchor
import re
from list_parse import ParseTagToList, MultiList

class Function_SimpleTemplatize(Function):
    """
    handle tags looking for tags in first level of dictionary e.g [[tbl-name]]
    what: replace template-tags with tag-values
    how: * make list of all template-tag in template-line e.g. [[tbl-name]] or [[field.context:pk.{{name}}]]
         * find tag-values in configuration value
         * replace template-tag in original template with tag-value
             [[tbl-fields.context:pk.json ? '{{name}}']]
    [[tbl-name]]
    [[field.context:pk.{{name}}]]
    [[field.crud:(Cc).{{name}}]]

    """
    def __init__(self,dictionary={}, tmpl_line=''):
        super().__init__(dictionary, tmpl_line=tmpl_line)
        # dictionary is loaded by adding Function_SimpleTemplatize to Function_Anchor

    def process(self):
        print('Function_SimpleTemplatize')
        self.tag_pattern = re.compile('\[\[[A-Za-z:>\'\-\.\s\"{}?;_*(),]+\]\]') # yank all [[]] tags

        # handle no tag matches
        #print('tmpl_line', self.tmpl_line)
        all_occ = self.tag_pattern.findall(self.tmpl_line)
        #print('all_occ', all_occ)

        if len(all_occ) > 0:
            for group in all_occ:
                self.append(group)  # make list of all template tags

            for group in self: # apply
                value = MultiList(ParseTagToList(group), self.dictionary).toString()
                self.tmpl_line = self.tmpl_line.replace(group, value)
        elif '[[' in self.tmpl_line or '{{' in self.tmpl_line:
            raise Exception('Function_SimpleTemplatize template not recognized...{}'.format(self.tmpl_line))
        return self


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


    #### B
    nxt = Function_SimpleTemplatize()
    func =  Function_Anchor(dictionary_tbl, '-- Always start with Function_Anchor [[tbl-name]]') \
            .add(nxt)
    print('B Function', func)
    print('B getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[tbl-name]]']
    assert func.getTemplateLine() == '-- Always start with Function_Anchor register'

    ### C
    nxt = Function_SimpleTemplatize()
    func =  Function_Anchor(dictionary_tbl, '-- Always start with Function_Anchor [[tbl-name]][[tbl-name]]') \
            .add(nxt)

    print('C Function nxt', nxt)
    print('C getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[tbl-name]]','[[tbl-name]]']

    ### D
    nxt = Function_SimpleTemplatize()
    tmpl = "-- Always start with Function_Anchor [[tbl-name]] [[tbl-name]] [[tbl-fields.context:pk.json ? '{{name}}']]"
    func =  Function_Anchor(dictionary_tbl, tmpl) \
            .add(nxt)
    print('D Function nxt', nxt)
    print('D getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[tbl-name]]','[[tbl-name]]',"[[tbl-fields.context:pk.json ? '{{name}}']]"]
    assert func.getTemplateLine() == "-- Always start with Function_Anchor register register json ? 'id'"

    ### E
    nxt = Function_SimpleTemplatize()
    tmpl = "[[tbl-fields.*:*.Declare _{{name}} {{type}};]]"
    func = Function_Anchor(dictionary_tbl, tmpl) \
        .add(nxt)
    print('E Function nxt', nxt)
    print('E getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[tbl-fields.*:*.Declare _{{name}} {{type}};]]']
    assert func.getTemplateLine().startswith('Declare _id UUID;')

    ### F
    nxt = Function_SimpleTemplatize()
    tmpl = "[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]"
    func = Function_Anchor(dictionary_tbl, tmpl) \
        .add(nxt)
    print('F Function nxt', nxt)
    print('F getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[tbl-fields.crud:(Cc).{{tbl-prefix}}_{{name}}., ]]']
    assert func.getTemplateLine() == 'reg_type, reg_password'

    ### G
    nxt = Function_SimpleTemplatize()
    tmpl = "[[LB_SECRET_PASSWORD]]"
    func = Function_Anchor(dictionary_tbl, tmpl) \
        .add(nxt)
    print('G Function nxt', nxt)
    print('G getTemplateLine', func.getTemplateLine())

    assert nxt == ['[[LB_SECRET_PASSWORD]]']
    assert func.getTemplateLine() == 'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG'


    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()

