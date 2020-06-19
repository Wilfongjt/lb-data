from function_weld import Weld, Function

class Function_Anchor(Function):
    """
    all function chains begin with an Function_Anchor
    """
    def __init__(self, dictionary, tmpl_line):
        super().__init__(dictionary=dictionary, tmpl_line=tmpl_line)

    def process(self):
        #self.append('-- Always start with Function_Anchor')
        #print('Function_Anchor')
        return self


def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os
    from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    #dictionary_db = InterfaceConfiguration('app').load(test_db())
    #template = []

    func =  Function_Anchor(dictionary_tbl, '-- Always start with Function_Anchor')
    print('A Function', func)
    print('A getTemplateLine', func.getTemplateLine())

    assert func == []
    assert func.getTemplateLine() == '-- Always start with Function_Anchor'

    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()