from util import Util
import json
import os

class FileAsList(list):
    def __init__(self, folder_name, file_name):
        self.file_name = file_name
        self.folder_name = folder_name
        self.echo=False

    def getClassName(self):
        return self.__class__.__name__

    def exists(self):
        return Util().file_exists(self.getFolderName(), self.getFileName())

    def isEmpty(self):
        if len(self) == 0:
            return True
        return False

    def setEcho(self, onoff):
        self.echo = onoff
        return self

    def isEcho(self):
        return self.echo

    def setFileName(self, filename):
        self.file_name = filename
        return self

    def getFileName(self):
        if self.file_name == None :
            raise Exception('{} file name is not set!'.format(self.getClassName()) )
        return self.file_name

    def setFolderName(self, foldername):
        self.folder_name = foldername
        return self

    def getFolderName(self):
        #if self.folder_name == None:
        #    self.folder_name = None
        #    raise Exception('{} folder name is not set!'.format(self.getClassName()))

        return self.folder_name

    def append(self, item ):
        super().append(item )
        #if 'INSERT' in item:
        #    print('ailine', item)
        #    print('biline', self[len(self) - 1])
        #if 'VALUES' in item:
        #    print('aline', item)
        #    print('bline', self[len(self)-1])
        #if self.isEcho():
        #    print(self.getClassName(), item )
        return self

    def append_lines(self, line_list):

        for ln in line_list:
            self.append(ln)
        return self

    def delete(self):
        #print('delete', self.getFolderName(), self.getFileName() )
        Util().deleteFile(self.getFolderName(), self.getFileName())
        return self

    def read(self):
        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
        with open(path_filename) as f:
            for line in f:
                # self.lineList.append(line)
                line = line.rstrip()
                #line = line.replace('\n', '')
                self.append(line)

        return self

    def write(self):
        self.copy(self.getFolderName(),self.getFileName())
        return self

    def copy(self, folder, filename):
        with open('{}/{}'.format(folder, filename), 'w') as f:
            for line in self:
                #print('write', line)
                f.write('{}\n'.format(line))

        return self



class FileAsDict(dict):
    def __init__(self, folder_name, file_name):
        self.file_name = file_name
        self.folder_name = folder_name

        self.loadEnv()

    def getClassName(self):
        return self.__class__.__name__

    def setFileName(self, filename):
        self.file_name = filename
        return self

    def getFileName(self):
        return self.file_name

    def setFolderName(self, foldername):
        self.folder_name = foldername
        return self

    def getFolderName(self):
        return self.folder_name

    def delete(self):
        Util().deleteFile(self.getFolderName(), self.getFileName())
        return self

    def read(self):
        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
        #print('open file', path_filename)
        with open(path_filename) as json_file:
            configuration_dict = json.load(json_file)

        # copy to the dict
        for key in configuration_dict:
            self[key] = configuration_dict[key]
        return self

    def loadEnv(self):
        # get LB_ env vars

        for v in os.environ:
            if v.startswith('LB_'):
                self[v]= os.getenv(v)
        return self

    def write(self):
        self.copy(self.getFolderName(), self.getFileName())
        return self

    def copy(self, folder, filename):
        path_filename = '{}/{}'.format(folder, filename)

        with open(path_filename, 'w') as json_file:

            configuration_dict = json.dump(self, json_file)

        return self


def main():
    from pathlib import Path
    from util import Util

    folder = '{}/temp'.format(str(Path.home()))
    file_name = 'junk2.txt'
    print('folder',folder)
    if not Util().folder_exists(folder):
      Util().createFolder(folder)

    #print('testing FileAsList')
    fileList = FileAsList('a','b')
    fileList.append('a')
    fileList.append('b')
    fileList.append('c')

    assert(['a','b','c'] == fileList)
    assert(fileList.getFolderName()=='a')
    assert(fileList.getFileName()=='b')


    ######################################
    file_name = 'junk2.json'
    # file name trick
    expected = file_name

    # write a junk file
    print('* write file')
    os.environ['LB_'] = 'D'
    print('  - folder', folder)
    aFile = FileAsDict(folder, file_name)
    aFile['a'] = 'A'
    aFile['b'] = 'B'
    aFile['c'] = 'C'
    #aFile['LB_'] = 'D'

    aFile.write()

    assert (expected == aFile.getFileName())
    assert (Util().file_exists(folder, expected))
    #print('aFile', aFile)

    # read the junk fil* e
    print('* read file')
    aFile2 = FileAsDict(folder, file_name).read()
    print('  - aFile2', aFile2)
    #print('  - len', len(aFile2))
    assert (len(aFile2) >= 4)

    # cleanup
    aFile.delete()
    assert (not Util().file_exists(folder, expected))

if __name__ == "__main__":
    main()