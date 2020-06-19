
from list_forms import FormList
import json

class FormKeyList(list):
    def __init__(self, dictionary):
        if 'interfaces' in dictionary:
            for formkey in dictionary['interfaces']:
                self.append(formkey)
        elif 'api-form' in dictionary:
            self.append(dictionary['api-name'])

class Form(dict):
    def default(self, f):
        num_list =['INTEGER']
        if f['type'] in [any(ele in f['json'] for ele in ['INTEGER']) ]:
            rc = 0
        elif f['type'] in [any(ele in f['json'] for ele in ['JSONB','JSON']) ]:
            rc = {'na':'na'}
        else:
            rc = 'NA'
        return rc

class InsertForm(Form):
    def __init__(self, dictionary, form_key, constraints=['C','c']):
        # dictionary is table dictionary
        # form_key as found in forms
        self.dictionary = dictionary
        #contextDict = ContextDict().read()
        for f in FormList(self.dictionary, form_key, constraints):
            self[f['name']] = self.default(f)
        self['type']=form_key

class UpdateForm(Form):
    def __init__(self, dictionary, form_key, constraints=['I','U','u']):
        self.dictionary = dictionary
        #contextDict = ContextDict().read()
        for f in FormList(self.dictionary, form_key, constraints):
            self[f['name']] = self.default(f)##ContextDict(ContextKey('data-context',f))
        self['type'] = form_key

def main():
    import os
    from test_func import test_table
    from context_dict import ContextDict

    os.environ['LB-TESTING'] = '1'

    # FormKey
    assert FormKeyList(test_table()) == ['app', 'user']

    # InsertForm
    form = InsertForm(test_table(), 'app')
    assert type(form) == InsertForm
    assert form == {'type': 'app', 'app-name': 'NA', 'version': 'NA', 'username': 'NA', 'password': 'NA'}
    print('insert form', form)

    context = ContextDict().read()
    #print('context', context)
    form = context.goodify(form)
    print('context good', form)
    form = context.badify(form)
    print('context bad', form)

    # UpdateForm
    form = UpdateForm(test_table(), 'app')
    print('update form', form)
    assert type(form) == UpdateForm
    assert form == {'id': 'NA', 'type': 'app', 'app-name': 'NA', 'username': 'NA', 'password': 'NA'}
    form = context.goodify(form)
    print('context good', form)
    form = context.badify(form)
    print('context bad', form)


    form = InsertForm(test_table(), 'user')
    print('insert form', form)


    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()