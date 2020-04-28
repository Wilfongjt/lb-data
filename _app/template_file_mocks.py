from template_file import TemplateFile
from app_settings import AppSettings, AppSettingsTest
import os
from util import Util

class TemplateFileMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        # read from code folders
        self.setFolderName(AppSettings().getResourceFolder('templates'))

    def write(self):
        # write to examples
        self.copy(
            AppSettingsTest().getFolder('temp-lates-folder'),
            self.getFileName())
        return self

    def mockup(self):
        self.read()
        self.write()
        return self

class TemplateFileCreateDatabaseMock(TemplateFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = AppSettingsTest().getFolder('temp-lates-folder')

        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('database.pg.tmpl')

        self.add([
            '\c postgres',
            'DROP DATABASE IF EXISTS [[db-prefix]]_db;',
            'CREATE DATABASE [[db-prefix]]_db;',
            '\c [[db-prefix]]_db',
            'create schema if not exists [[db-prefix]]_schema;',
            '[[extensions]]',
            'SET search_path TO [[db-prefix]]_schema, public; -- put everything in [[db-prefix]]_schema;'
        ])

class TemplateFileCreateTableMock(TemplateFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = AppSettingsTest().getFolder('temp-lates-folder')

        if foldername == None:
            self.setFolderName(self.default_folder)

        if filename == None:
            self.setFileName('db-api-table-table.pg.tmpl')

        self.add([
            '\c [[db-prefix]]_db',
            'create db-table if not exists',
            '[[db-prefix]]_schema.[[tbl-name]] (',
            '  [[fields]]',
            ');',
            'CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[db-prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id int4_ops);'
        ])

class TemplateFileTableApiInsertMock(TemplateFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = AppSettingsTest().getFolder('temp-lates-folder')

        if foldername == None:
            self.setFolderName(self.default_folder)

        if filename == None:
            self.setFileName('table-api-insert.pg.tmpl')

        self.add(
            [
                '\c [[db-prefix]]_db',
                '-------------------------------',
                '-- INSERT',
                '---------',
                'CREATE OR REPLACE FUNCTION',
                '[[db-prefix]]_schema.[[api-name]](',
                '  _token TEXT,',
                '  [[insert-parameters]]',
                ') RETURNS TEXT',
                'AS $$',
                '    Declare rc TEXT;',
                '    Declare role TEXT;',
                '    Declare id int;',
                '  BEGIN',
                '    rc := \'{"result", -1}\';',
                '    role := [[db-prefix]]_schema.get_role(_token);',

                '    BEGIN',
                '      if [[db-prefix]]_schema.is_valid_token(_token,\'[[tbl - role]]\') then',
                '        rc := \'{"result", -2}\';',
                '        INSERT INTO api_schema.users',
                '          ([[insert-columns]])',
                '          VALUES',
                '          ([[insert-values]]);',
                '          rc := \'{"result": 1}\';',
                '      end if;',
                '    EXCEPTION WHEN unique_violation THEN',
                '      rc := \'{"result", -3}\';',
                '    END;',
                '    RETURN rc;',
                '  END;',
                '$$ LANGUAGE plpgsql;'
            ]
        )


class TemplateFileTableApiSelectMock(TemplateFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = AppSettingsTest().getFolder('temp-lates-folder')

        if foldername == None:
            self.setFolderName(self.default_folder)

        if filename == None:
            self.setFileName('table-api-select.pg.tmpl')

        self.add(
            [
                '\c [[db-prefix]]_db',
                '-------------------------------',
                '-- Select',
                '---------',
                'CREATE OR REPLACE FUNCTION',
                '[[db-prefix]]_schema.[[tbl-name]](_token text, id int) RETURNS TEXT',
                'AS $$',
                '  DECLARE rc TEXT;',
                '  DECLARE secret TEXT;',
                'BEGIN',
                '  -- returns a single user\'s info',
                '  -- need to figure out postgres environment variables',

                '  rc := \'{"result":-1}\';',

                '  if [[db-prefix]]_schema.is_valid_token(_token) then',
                '    select',
                '    \'{\' || [[select-columns]] || \'}\'',
                '    into rc from',
                '    [[db-prefix]]_schema.[[tbl-name]]',
                '    where [[tbl-prefix]]_id=id;',
                '    if rc is NULL then',
                '      rc := \'{"result":-1}\';',
                '    end if;',
                '  end if;',

                '  RETURN rc;',
                'END;  $$ LANGUAGE plpgsql;',
            ]
        )

class TemplateFileTableApiUpdateMock(TemplateFile):

    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)

        self.default_folder = AppSettingsTest().getFolder('temp-lates-folder')

        if foldername == None:
            self.setFolderName(self.default_folder)

        if filename == None:
            self.setFileName('table-api-update.pg.tmpl')

        self.add(
            [

                '\c [[db-prefix]]_db',
                '-------------------------------',
                '-- Update',
                '---------',
                'CREATE OR REPLACE FUNCTION',
                '[[db-prefix]]_schema.[[api-name]](_token text, [[update-parameters]]) RETURNS TEXT',
                'AS $$',
                '    Declare rc TEXT;',
                '  BEGIN',
                '    rc := \'{"result": -1}\';',
                '    if [[db-prefix]]_schema.is_valid_token(_token, \'[[tbl - role]]\') then',
                '      rc := \'{"result": -2}\';',
                '      rc := format(\'{"result": "%s"}\',[[db-prefix]]_schema.get_username(_token));',
                '      update [[db-prefix]]_schema.[[tbl-name]]',
                '        set',
                '          [[update-columns]]',
                '          ,[[tbl-prefix]]_updated=CURRENT_DATE',
                '        where [[tbl-prefix]]_id=id;',
                '      if FOUND then',
                '        rc := \'{"result": 1}\';',
                '      end if;',
                '    end if;',
                '    RETURN rc;',
                '  END;',
                '$$ LANGUAGE plpgsql;'
            ]
        )


class TemplateMockups():
    def mockups(self):
        os.environ['LB-TESTING'] = '1'
        appSettings = AppSettingsTest().createFolders()
        filelist = Util().getFileList(appSettings.getResourceFolder('templates'))
        #print('filelist', filelist)
        folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder())

        for fn in filelist:
            #print('filename ', fn)
            if '.DS_Store' not in fn:
                TemplateFileMock(appSettings.getResourceFolder('templates'), fn) \
                    .mockup()


def main():
    import os
    from util import Util

    os.environ['LB-TESTING'] = '1'
    appSettings = AppSettingsTest().createFolders()
    filelist = Util().getFileList(appSettings.getResourceFolder('templates'))
    print('filelist', filelist)
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )

    for fn in filelist:
        print('filename ', fn)
        if '.DS_Store' not in fn:
            TemplateFileMock(appSettings.getResourceFolder('templates'), fn )\
                .mockup()
            assert (Util().folder_exists(folder))
            assert (Util().file_exists(folder, fn))
    appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'

    appSettings.createFolders()
    ###################################################
    # write a junk file to temp folder
    aFile = TemplateFileCreateDatabaseMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )
    file = 'database.pg.tmpl'

    assert(Util().folder_exists(folder))
    assert(Util().file_exists(folder, file))

    ##################################################
    # write a junk file to temp folder
    aFile = TemplateFileCreateTableMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )
    file = 'db-api-table-table.pg.tmpl'

    assert(Util().folder_exists(folder))
    assert(Util().file_exists(folder, file))

    ##################################################
    # write a junk file to temp folder
    aFile = TemplateFileTableApiInsertMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )
    file = 'table-api-insert.pg.tmpl'

    assert (Util().folder_exists(folder))
    assert (Util().file_exists(folder, file))

    ##################################################
    # write a junk file to temp folder
    aFile = TemplateFileTableApiSelectMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )
    file = 'table-api-select.pg.tmpl'

    assert (Util().folder_exists(folder))
    assert (Util().file_exists(folder, file))

   ##################################################
    # write a junk file to temp folder
    aFile = TemplateFileTableApiUpdateMock().write()
    folder = '{}/..LyttleBit/testing/projects/example-dev/templates'.format(appSettings.getHomeFolder() )
    file = 'table-api-update.pg.tmpl'

    assert (Util().folder_exists(folder))
    assert (Util().file_exists(folder, file))
    ##################################################

    appSettings.removeFolders()
    os.environ['LB-TESTING'] = '0'


if __name__ == "__main__":
    main()