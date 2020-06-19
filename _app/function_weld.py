
'''
Function are applied to templates
a Function implements the swappinig of function tags for values within the template
'''
from list_fields import FieldList
from context_dict import ContextDict, ContextKey
#from templatize import Templatize, TemplatizedLine
from forms import FormKeyList, FormList
from list_fields import FieldList
import json
import re
import itertools
# from helper_where_clause_format import HelperWhereClauseFormat
from pprint import pprint
from const import Const
from list_parse import ParseTagToList, MultiList
import os

'''
Functions 
* accumulate output as a list
* the calling program is responcible for assembly

'''
class Weld(list):
    def __init__(self):
        #print('weld')
        self.prev = None
        self.next = None

    def getClassName(self):
        return self.__class__.__name__

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

    def run(self):
        # pull data forward
        if self.getPrev() != None:
            self.tmpl_line = self.getPrev().tmpl_line
            self.dictionary = self.getPrev().dictionary
            self.context_dictionary = self.getPrev().context_dictionary

        self.process()

        if self.getNext() != None:
            self.getNext().run()

        return self

class Function(Weld):
    """
    Base Class
    .run() is called when functions are added
    call .run() once instansated

    """
    #def __init__(self, dictionary={}, tmpl_line=''):
    def __init__(self, dictionary, tmpl_line=''):
    #def __init__(self, dictionary, parseTagToList):
        super().__init__()
        self.dictionary = dictionary
        #self.template_list = template_list # a template list
        self.tmpl_line = tmpl_line
        #self.parseTagToList = parseTagToList
        self.error_no = 0
        self.context_dictionary=None
        #self.process()
        self.join_del = ' '
        #self.run()

    def add(self, func):
        super().add(func)
        func.run()
        return self

    def process(self):
        """
        process a single line of template
        append template updates to self
        before end gather results into the tmpl_line
        """

        if '[[' not in self.tmpl_line and '<<' not in self.tmpl_line:
            self.append(self.templatize(self.tmpl_line))
        else:
            self.append(self.templatize(self.tmpl_line))
        return self


    '''
    def templatize(self, template_line, lyttle_dictionary):
        print('templateize 5')
        for key_ in lyttle_dictionary:
            v = lyttle_dictionary[key_]
            if type(v) == dict: # brute force the root keys, skipping values of type list and dict
                #print('hi dict {}'.format(json.dumps(v)))
                k = '{{' + key_ + '}}'
                template_line = template_line.replace(k, json.dumps(v))

            elif type(v) != list:
                #print('A process key', key_, ' v ', v)
                k = '{{' + key_ + '}}'
                template_line = template_line.replace(k, str(v))

        if '{{' in template_line: # take care of {{}} wrapped values
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

        #print('template_line', template_line)
        return template_line
    '''
    def templatize(self, template_line, temp_dictionary=None):
        # print('templateize 4')
        if temp_dictionary == None:
            temp_dictionary = self.dictionary
        for key_ in temp_dictionary:# brute force through all the root keys
            v = temp_dictionary[key_]
            if type(v) != list and type(v) != dict:
                #print('process key', key_, ' v ', v)
                if '[[' in template_line: # lookup
                    template_line = template_line.replace('[[{}]]'.format(key_), v)
                elif '<<' in template_line: # run some code
                    template_line = template_line.replace('<<{}>>'.format(key_), v)
        return template_line

    def getErrorResult(self):
        self.error_no -= 1
        return '{}-{}'.format(self.getClassName(),str(self.error_no))

    def getTemplateLine(self):
        """
        get the last result in the sequence
        """
        if self.getNext() == None:
            return self.tmpl_line
        return self.getNext().getTemplateLine()

    def toString(self):
        if self.getNext() == None:
            return '\n'.join(self)
        return self.getNext().toString()


def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os
    from list_forms import FormList

    os.environ['LB-TESTING'] = '1'
    #print('Function', Function(test_table(),'[[type]]'))
    #print('toString', Function(test_table(), '[[type]]').toString())
    # [[type]] applies to all templates
    func = Function(test_table(), '-- test comment').run()
    assert func == ['-- test comment']
    func = Function(test_table(), '[[type]]').run()
    assert func == ['table']
    assert func.toString() == 'table'
    print('getTemplateLine', func.getTemplateLine)

    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()