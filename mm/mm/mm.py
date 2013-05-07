#!/usr/bin/env python

import os.path
import sys
import argparse
import traceback
import json
import lib.config as config
import lib.mm_util as util
import time #TODO: remove
import urllib
from suds.client import Client
from lib.mm_connection import MavensMatePluginConnection
from lib.mm_client import MavensMateClient

request_payload = util.get_request_payload()
config.logger.debug('\n\n\n>>>>>>>>\nhandling request with payload >>>>>')
config.logger.debug(request_payload)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation') #name of the operation being requested
    parser.add_argument('-c', '--client') #name of the plugin client ("SUBLIME_TEXT_2", "SUBLIME_TEXT_3", "TEXTMATE", "NOTEPAD_PLUS_PLUS", "BB_EDIT", etc.)
    parser.add_argument('-p', '--projectname') #name of the project
    parser.add_argument('-d', '--projectdirectory') #name of the project
    parser.add_argument('--callback') #some terminal script to run upon completion of a command
    parser.add_argument('--ui', action='store_true', default=False, 
        dest='ui_switch', help='Include flag to launch the default UI for the operation')
    parser.add_argument('--html', action='store_true', default=False, 
        dest='respond_with_html', help='Include flag if you want the response in HTML')
    args = parser.parse_args()
    operation = args.operation
    
    try:
        setup_connection(args)
    except Exception as e:
        print util.generate_error_response(e.message)
        return

    #if the arg switch argument is included, the request is to launch the out of box
    #MavensMate UI, so we generate the HTML for the UI and launch the process
    #example: mm -o new_project --ui
    if args.ui_switch == True:
        #os.system('killAll MavensMateWindowServer') #TODO: try/except?
        tmp_html_file = util.generate_ui(operation,request_payload)
        print tmp_html_file
        util.launch_ui(tmp_html_file, config.connection.chrome )
        print tmp_html_file
        print util.generate_success_response('UI Generated Successfully')
    else:        
        if operation == 'new_project':
            new_project()
        elif operation == 'edit_project':
            edit_project()    
        elif operation == 'upgrade_project':
            upgrade_project()     
        elif operation == 'checkout_project':
            checkout_project()
        elif operation == 'compile_project':
            compile_project()
        elif operation == 'new_metadata':
            new_metadata()
        elif operation == 'clean_project':
            clean_project()
        elif operation == 'refresh':
            refresh()
        elif operation == 'compile':
            compile_selected_metadata()
        elif operation == 'delete':
            delete_selected_metadata()
        elif operation == 'get_active_session':
            get_active_session()
        elif operation == 'update_credentials':
            update_credentials()
        elif operation == 'execute_apex':
            execute_apex()
        elif operation == 'deploy_to_server' or operation == 'deploy':
            deploy_to_server(args)
        elif operation == 'unit_test' or operation == 'test':
            run_unit_tests(args)
        elif operation == 'list_metadata':
            list_metadata()
        elif operation == 'index_metadata':
            index_metadata(args)    
        elif operation == 'list_connections':
            list_connections()
        elif operation == 'new_connection':
            new_connection()
        elif operation == 'delete_connection':
            delete_connection()
        elif operation == 'index_apex_overlays':
            index_apex_overlays()
        elif operation == 'new_apex_overlay':
            new_apex_overlay()
        elif operation == 'delete_apex_overlay':
            delete_apex_overlay()
        elif operation == 'fetch_logs':
            fetch_logs()
        elif operation == 'new_project_from_existing_directory':
            new_project_from_existing_directory()
        elif operation == 'debug_log':
            TODO()
        elif operation == 'open_sfdc_url':
            open_sfdc_url()
        else:
            print util.generate_error_response('Invalid operation requested')

    if args.callback != None:
        os.system(args.callback)

# each operation sets up a single connection
# the connection holds information about the plugin running it
# and establishes a project object
def setup_connection(args):
    if 'project_name' in request_payload or 'project_directory' in request_payload:
        #project_name        = request_payload.get('project_name', args.projectname)
        #project_directory   = request_payload.get('project_directory', args.projectdirectory)
        config.connection = MavensMatePluginConnection(
            client=args.client or 'SUBLIME_TEXT_2',
            ui=args.ui_switch,
            params=request_payload,
            operation=args.operation)
    else:
        config.connection = MavensMatePluginConnection(
            client=args.client or 'SUBLIME_TEXT_2',
            params=request_payload,
            operation=args.operation)

# echo '{ "username" : "joeferraro4@force.com", "password" : "352198", "metadata_type" : "ApexClass" ' | joey2 mavensmate.py -o 'list_metadata'
def list_metadata():
    client = MavensMateClient(credentials={
        "sid"                   : request_payload.get('sid', None),
        "metadata_server_url"   : urllib.unquote(request_payload.get('metadata_server_url', None)),
        "server_url"            : urllib.unquote(request_payload.get('server_url', None)),
    }) 
    print json.dumps(client.list_metadata(request_payload['metadata_type']))

def open_sfdc_url():
    print config.connection.project.open_selected_metadata(request_payload);

def list_connections():
    print config.connection.project.get_org_connections()

def new_connection():
    print config.connection.project.new_org_connection(request_payload)

def delete_connection():
    print config.connection.project.delete_org_connection(request_payload)

def compile_selected_metadata():
    print config.connection.project.compile_selected_metadata(request_payload)

def delete_selected_metadata():
    print config.connection.project.delete_selected_metadata(request_payload)

def index_metadata(args):
    index_result = config.connection.project.index_metadata()
    if args.respond_with_html == True:
        html = util.generate_html_response(args.operation, index_result, request_payload)
        print util.generate_success_response(html, "html")
    else:
        print index_result

def new_project():
    print config.connection.new_project(request_payload,action='new')

def new_project_from_existing_directory():
    print config.connection.new_project(request_payload,action='existing')

def edit_project():
    print config.connection.project.edit(request_payload)

def upgrade_project():
    print config.connection.project.upgrade()
    
def checkout_project():
    print config.connection.new_project(request_payload,action='checkout')

def compile_project():
    print config.connection.project.compile()

def clean_project():
    print config.connection.project.clean()

def refresh():
    print config.connection.project.refresh_selected_metadata(request_payload)

def new_metadata():
    print config.connection.project.new_metadata(request_payload)

def execute_apex():
    print config.connection.project.execute_apex(request_payload)

def fetch_logs():
    print config.connection.project.fetch_logs(request_payload)

# echo '{ "project_name" : "bloat", "classes" : [ "MyTester" ] }' | joey2 mavensmate.py -o 'test'
def run_unit_tests(args):
    test_result = config.connection.project.run_unit_tests(request_payload)
    if args.respond_with_html ==  True:
        html = util.generate_html_response(args.operation, test_result, request_payload)
        print util.generate_success_response(html, "html")
    else:
        print test_result

def deploy_to_server(args):
    deploy_result = config.connection.project.deploy_to_server(request_payload)
    if args.respond_with_html == True:
        html = util.generate_html_response(args.operation, deploy_result, request_payload)
        print util.generate_success_response(html, "html")
    else:
        print deploy_result

# echo '{ "username" : "mm@force.com", "password" : "force", "org_type" : "developer" }' | joey2 mavensmate.py -o 'get_active_session'
def get_active_session():
    try:
        client = MavensMateClient(credentials={
            "username" : request_payload['username'],
            "password" : request_payload['password'],
            "org_type" : request_payload['org_type']
        }) 
        
        response = {
            "sid"                   : client.sid,
            "user_id"               : client.user_id,
            "metadata_server_url"   : client.metadata_server_url,
            "server_url"            : client.server_url,
            "metadata"              : client.get_org_metadata(),
            "success"               : True
        }
        print util.generate_response(response)
    except BaseException, e:
        print util.generate_error_response(e.message)

def index_apex_overlays():
    print config.connection.project.index_apex_overlays(request_payload)

def new_apex_overlay():
    print config.connection.project.new_apex_overlay(request_payload)

def delete_apex_overlay():
    print config.connection.project.delete_apex_overlay(request_payload)

def update_credentials():
    try:
        config.connection.project.username = request_payload['username']
        config.connection.project.password = request_payload['password']
        config.connection.project.org_type = request_payload['org_type']
        config.connection.project.update_credentials()
        print util.generate_success_response('Your credentials were updated successfully')
    except BaseException, e:
        print util.generate_error_response(e.message)

if  __name__ == '__main__':
    main()