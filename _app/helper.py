"""
from pathlib import Path
from context_dict import ContextDict

class Helper():

    def __init__(self, step=None):
        self.temporaryFile=None
        self.templateFile = None
        self.configurationFile = None
        self.mergeFile = None
        #self.data = None
        self.step = step
        self.default_folder = '{}/temp'.format(str(Path.home()))
        self.object_types = ['JSONB']
        self.unquoted_types = ['INTEGER', 'BOOLEAN']
        self.quoted_types = ['TEXT', 'TIMESTAMP']
        self.dictionary = None
        self.context = None

    def set_dictionary(self, table_dictionary ):
        if 'interfaces' not in table_dictionary:
            raise Exception('table dictionary missing interfaces')
        self.dictionary = table_dictionary
        return self

    '''
    def setData(self, data):
        self.data = data
        return self

    def getData(self):
        if self.data == None:
            raise Exception('{} data is not set!'.format(self.getClassName()))
        return self.data
    '''
    '''
    def getFieldList(self):
        if self.field_list == None:
            self.field_list = FieldList()
    '''
    def getContext(self):
        if self.context == None:
            self.context = ContextDict().read()
        return self.context
    '''
    def get_context_dictionary(self):
        if self.context_dictionary == None:
            self.context_dictionary = ContextDict().read()
        return self.context_dictionary
    '''
    def getData(self):
        if self.step != None:
            return self.step.getData()
        return {}

    def getFolder(self, key):
        if 'project-folders' in self.getData():
            if key in self.getData()['project-folders']:
                return self.getData()['project-folders'][key]
        return self.default_folder # used for testing

    def setTemporaryFile(self,temporaryFile):
        #print('setTemporaryFile', temporaryFile)
        self.temporaryFile = temporaryFile
        return self

    def getTemporaryFile(self):
        if self.temporaryFile == None:
            raise Exception('{} temporaryFile is not set!'.format(self.getClassName()))
        return self.temporaryFile

    def setTemplateFile(self,scriptFile):
        self.templateFile = scriptFile
        return self

    def getTemplateFile(self):
        if self.templateFile == None:
            raise Exception('{} templateFile is not set!'.format(self.getClassName()))
        return self.templateFile

    def setConfigurationFile(self, confFile):
        self.configurationFile=confFile
        return self

    def getConfigurationFile(self):
        if self.configurationFile == None:
            raise Exception('{} configurationFile is not set!'.format(self.getClassName()))
        return self.configurationFile

    def setMergeFile(self, tempFile):
        self.mergeFile = tempFile
        return self

    def getMergeFile(self):
        if self.mergeFile == None:
            raise Exception('{} mergeFile is not set!'.format(self.getClassName()))
        return self.mergeFile

    def run(self):
        self.process()
        return self

    def getClassName(self):
        return self.__class__.__name__

    def process(self):
        raise Exception('{} Overload process'.format(self.getClassName()))
"""