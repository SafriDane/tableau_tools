# -*- coding: utf-8 -*-

from tableau_tools.tableau_rest_api import *
from tableau_tools import *
import time

server = 'http://127.0.0.1'
username = ''
password = ''

new_site_content_url = 'test_site'
new_site_name = 'Sample Test Site'

# Choose the API version for your server. 10.2 = 25
default = TableauRestApiConnection26(server=server, username=username, password=password, site_content_url='default')
try:
    default.signin()
    default.create_site(new_site_name=new_site_name, new_content_url=new_site_content_url)
except AlreadyExistsException as e:
    print((e.msg))
    print("Cannot create new site, it already exists")
    exit()

time.sleep(4)


t = TableauRestApiConnection26(server=server, username=username, password=password,
                               site_content_url=new_site_content_url)
t.signin()
logger = Logger('create_site_sample.log')
# Enable logging after sign-in to hide credentials
t.enable_logging(logger)

# Create some groups
groups_to_create = ['Administrators', 'Executives', 'Managers', 'Line Level Workers']

for group in groups_to_create:
    t.create_group(group_name=group)

# Remove all permissions from Default Project
time.sleep(4)
default_proj = t.query_project(project_name_or_luid='Default')
default_proj.lock_permissions()

default_proj.clear_all_permissions() # This clears all, including the defaults


# Add in any default permissions you'd like at this point
admin_perms = default_proj.create_project_permissions_object_for_group(group_name_or_luid='Administrators',
                                                                       role='Project Leader')
default_proj.set_permissions_by_permissions_obj_list([admin_perms, ])

admin_perms = default_proj.create_workbook_permissions_object_for_group(group_name_or_luid='Administrators',
                                                                        role='Editor')
admin_perms.set_capability(capability_name='Download Full Data', mode='Deny')
default_proj.workbook_defaults.set_permissions_by_permissions_obj_list([admin_perms, ])

admin_perms = default_proj.create_datasource_permissions_object_for_group(group_name_or_luid='Administrators',
                                                                          role='Editor')
default_proj.datasource_defaults.set_permissions_by_permissions_obj_list([admin_perms, ])

# Change one of these
new_perms = default_proj.create_project_permissions_object_for_group(group_name_or_luid='Administrators',
                                                                     role='Publisher')
default_proj.set_permissions_by_permissions_obj_list([new_perms, ])

# Create Additional Projects
projects_to_create = ['Sandbox', 'Data Source Definitions', 'UAT', 'Finance', 'Real Financials']
for project in projects_to_create:
    t.create_project(project_name=project, no_return=True)

# Set any additional permissions on each project

# Add Users
users_to_add = ['user_1', 'user_2', 'user_3']
for user in users_to_add:
    t.add_user(username=user, fullname=user, site_role='Publisher')

time.sleep(3)
# Add Users to Groups
t.add_users_to_group(username_or_luid_s='user_1', group_name_or_luid='Managers')
t.add_users_to_group(username_or_luid_s='user_2', group_name_or_luid='Administrators')
t.add_users_to_group(username_or_luid_s=['user_2', 'user_3'], group_name_or_luid='Executives')
