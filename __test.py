import sys

import os
from pathlib import Path

import settings
#import __mockups as mockups
#import mockups as mockups_generate


import util as util
import file as file
import link as link
import step as step
import script_file as script_file
import template_file as template_file
import configuration_file as configuration_file
import context_dict as context_dict
#import copy_file as copy_file
import logger as logger

import app_settings as app_settings
import app_environment as app_environment
import app_initialize as app_initialize
import app_create_folders as app_create_folders
import forms as forms

'''
import helper_copy_file as helper_copy_file
#import helper_declare_upsert_format as helper_declare_upsert_format
#import helper_configuration_generate_api as helper_configuration_generate_api
#import helper_script_generate as helper_script_generate
#import helper_template_compile as helper_template_compile
#import helper_template_merge as helper_template_merge
#import helper_temporary_file as helper_temporary_file
#import helper_declare_upsert_format as helper_declare_upsert_format
#import helper_fields_format as helper_fields_format
#import helper_insert_columns_format as helper_insert_columns_format
#import helper_insert_values_format as helper_insert_values_format
import helper_required as helper_required
import helper_required_insert_attributes_format as helper_required_insert_attributes_format
import helper_required_insert_format as helper_required_insert_format
import helper_required_update_format as helper_required_update_format
#import helper_script_generate as helper_script_generate
import helper_set_clause_format as helper_set_clause_format
import helper_set_defaults_format as helper_set_defaults_format
import helper_sync_json_values_format as helper_sync_json_values_format
import helper_test_api_template as helper_test_api_template
import helper_test_object_json as helper_test_object_json
import helper_update_combos_format as helper_update_combos_format
import helper_where_clause_format as helper_where_clause_format
'''
#import functions as functions
import function_weld as function_weld
import function_update_combination_code as function_update_combination_code
import templates as templates

import project_environment as project_environment
import project_create_folders as project_create_folders
import project_initialize as project_initialize
import project_compile as project_compile
import project_merge as project_merge
import project_organize_files as project_organize_files
import project_cleanup as project_cleanup
import project_move_to_sql as project_move_to_sql
import app as app

#os.environ['LB-TESTING'] = '1'

# setup files
# store testing copies in temp/ folder
#ConfigurationDictFileDatabaseMock().write()
#ConfigurationDictFileTableMock().write()
#TemplateFileCreateTableMock().write()

# Mockups
#mockups_generate.main()
#mockups.main()


# util classes
util.main()
app_settings.main() # this runs AppSettingsTests

#
link.main()

step.main()


# helper

# file classes
file.main()

script_file.main()

#template_file.main()
templates.main()
configuration_file.main()

context_dict.main()

logger.main()

forms.main()

# helper classes
'''
helper_declare_upsert_format.main()
#helper_fields_format.main()
#helper_insert_columns_format.main()
#helper_insert_values_format.main()
helper_required.main()
helper_required_insert_attributes_format.main()
helper_required_insert_format.main()
helper_required_update_format.main()
# dep helper_script_generate.main()
helper_set_clause_format.main()
helper_set_defaults_format.main()
helper_sync_json_values_format.main()

helper_update_combos_format.main()
#helper_test_object_json.main()
helper_where_clause_format.main()
helper_test_api_template.main()
'''

#functions.main()
function_weld.main()
function_update_combination_code.main()
# Step classes
#copy_file.main()
app_environment.main()

app_create_folders.main()

app_initialize.main()

# project classes
project_environment.main()

project_create_folders.main()
# delete project_configuration_initialize.main()
# delete project_template_initialize.main()
project_initialize.main()

# project_configuration_generate_api.main()
#project_generate_api.main()

project_compile.main()

project_merge.main()

project_move_to_sql.main()
exit(0)

#project_organize_files.main()

project_cleanup.main()

exit(0)
#application class
#app.main()
