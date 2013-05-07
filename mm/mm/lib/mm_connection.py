#when mavensmate binary is executed, a plugin connection should be created immediately
#plugin connection should have a single instance of a mm_client associated
import os
import json
import mm_util
import sys
import config
import logging
from enum import enum
from mm_project import MavensMateProject
from mm_exceptions import MMException

class MavensMatePluginConnection(object):
   
    currently_supported_clients = ['SUBLIME_TEXT_2', 'SUBLIME_TEXT_3']
    PluginClients = enum(SUBLIME_TEXT_2='SUBLIME_TEXT_2', SUBLIME_TEXT_3='SUBLIME_TEXT_3', NOTEPAD_PLUS_PLUS='NOTEPAD_PLUS_PLUS', TEXTMATE='TEXTMATE')
    
    def __init__(self, params={}, **kwargs):
        params = dict(params.items() + kwargs.items())

        self.operation              = params.get('operation', None)
        self.platform               = sys.platform
        self.plugin_client          = params.get('client', 'SUBLIME_TEXT_2') #=> "Sublime Text", "Notepad++", "TextMate"
        if self.plugin_client not in self.currently_supported_clients:
            self.plugin_client = 'SUBLIME_TEXT_2'
        
        self.plugin_client_version  = params.get('client_version', '2.0.1') #=> "1.0", "1.1.1", "v1"
        self.plugin_client_settings = self.get_plugin_client_settings()
        self.workspace              = self.get_workspace()
        self.project_name           = params.get('project_name', None)

        self.project_location       = None
        if self.project_name != None:
            self.project_location = self.workspace+"/"+self.project_name
        self.project_id             = params.get('project_id', None)
        self.project                = None
        self.sfdc_api_version       = self.get_sfdc_api_version()
        self.ui                     = params.get('ui', False) #=> whether this connection was created for the purposes of generating a UI
        self.chrome                 = self.get_chrome();
        self.setup_logging()

        if self.sfdc_api_version != None:
            mm_util.SFDC_API_VERSION = self.sfdc_api_version #setting api version based on plugin settings

        if self.operation != 'new_project' and self.operation != 'upgrade_project' and self.operation != 'new_project_from_existing_directory' and self.project_location != None:
            if not os.path.exists(self.project_location+"/config/.settings"):
                raise MMException('This does not seem to be a valid MavensMate project, missing config/.settings')
            if not os.path.exists(self.project_location+"/src/package.xml"):
                raise MMException('This does not seem to be a valid MavensMate project, missing package.xml')
      
        if self.project_name != None and self.project_name != '' and not os.path.exists(self.project_location) and self.operation != 'new_project_from_existing_directory' and self.operation != 'new_project':
            raise MMException('The project could not be found')
        elif self.project_name != None and self.project_name != '' and os.path.exists(self.workspace+"/"+self.project_name) and self.operation != 'new_project_from_existing_directory':
            params['location'] = self.project_location
            params['ui'] = self.ui
            self.project = MavensMateProject(params)
    
    def setup_logging(self):
        if self.get_log_level() != None:
            if self.get_log_location() != None:
                try:
                    config.logger.handlers = []
                    config.suds_logger.handlers = []
                    handler = logging.FileHandler(self.get_log_location()+"/mm.log")
                    config.logger.addHandler(handler)
                    config.suds_logger.addHandler(handler)
                except:
                    pass
            log_level = self.get_log_level()
            if log_level == 'CRITICAL':
                config.logger.setLevel(logging.CRITICAL)
                config.suds_logger.setLevel(logging.CRITICAL)
            elif log_level == 'ERROR':
                config.logger.setLevel(logging.ERROR)
                config.suds_logger.setLevel(logging.ERROR)
            elif log_level == 'WARNING':
                config.logger.setLevel(logging.WARNING)
                config.suds_logger.setLevel(logging.WARNING)
            elif log_level == 'DEBUG':
                config.logger.setLevel(logging.DEBUG)
                config.suds_logger.setLevel(logging.DEBUG)
            elif log_level == 'INFO':
                config.logger.setLevel(logging.INFO) 
                config.suds_logger.setLevel(logging.INFO)

    #returns the workspace for the current connection (/Users/username/Workspaces/MavensMate)
    def get_workspace(self):
        return self.plugin_client_settings['user']['mm_workspace']

    def get_chrome(self):
        return self.plugin_client_settings['user']['mm_chrome']

    #returns the MavensMate settings as a dict for the current plugin
    def get_plugin_client_settings(self):
        if self.plugin_client == self.PluginClients.SUBLIME_TEXT_2:
            if self.platform == 'darwin':
                default_settings = mm_util.parse_json_from_file(os.path.expanduser('~/Library/Application Support/Sublime Text 2/Packages/MavensMate/mavensmate.sublime-settings'))
                user_settings    = mm_util.parse_json_from_file(os.path.expanduser('~/Library/Application Support/Sublime Text 2/Packages/User/mavensmate.sublime-settings'))
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
            elif self.platform == 'win32' or self.platform == 'cygwin':
                default_settings = mm_util.parse_json_from_file(path.join(environ['APPDATA'], 'Sublime Text 2', 'Packages', 'MavensMate')+"mavensmate.sublime-settings")
                user_settings = mm_util.parse_json_from_file(path.join(environ['APPDATA'], 'Sublime Text 2', 'Packages', 'User')+"mavensmate.sublime-settings")
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
            elif self.platform == 'linux2':
                
                default_settings = mm_util.parse_json_from_file(os.path.expanduser('/home/manan/.config/sublime-text-2/Packages/MavensMate/mavensmate.sublime-settings'))
                user_settings    = mm_util.parse_json_from_file(os.path.expanduser('/home/manan/.config/sublime-text-2/Packages/User/mavensmate.sublime-settings'))
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
        elif self.plugin_client == self.PluginClients.SUBLIME_TEXT_3:
            if self.platform == 'darwin':
                default_settings = mm_util.parse_json_from_file(os.path.expanduser('~/Library/Application Support/Sublime Text 3/Packages/MavensMate/mavensmate.sublime-settings'))
                user_settings    = mm_util.parse_json_from_file(os.path.expanduser('~/Library/Application Support/Sublime Text 3/Packages/User/mavensmate.sublime-settings'))
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
            elif self.platform == 'win32' or self.platform == 'cygwin':
                default_settings = mm_util.parse_json_from_file(path.join(environ['APPDATA'], 'Sublime Text 3', 'Packages', 'MavensMate')+"mavensmate.sublime-settings")
                user_settings = mm_util.parse_json_from_file(path.join(environ['APPDATA'], 'Sublime Text 3', 'Packages', 'User')+"mavensmate.sublime-settings")
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
            elif self.platform == 'linux2':
                default_settings = mm_util.parse_json_from_file(os.path.expanduser('/home/manan/.config/sublime-text-2/Packages/MavensMate/mavensmate.sublime-settings'))
                user_settings    = mm_util.parse_json_from_file(os.path.expanduser('/home/manan/.config/sublime-text-2/Packages/Packages/User/mavensmate.sublime-settings'))
                return {
                    'user'    : user_settings,
                    'default' : default_settings
                }
        else:
            return None

    #retrieves metadata from server, creates local project
    def new_project(self, params, **kwargs):
        try:
            if 'username' not in params or params['username'] == '':
                return mm_util.generate_error_response('Please specify a username')
            if 'password' not in params or params['password'] == '':
                return mm_util.generate_error_response('Please specify a password')
            if 'project_name' not in params or params['project_name'] == '':
                return mm_util.generate_error_response('Please specify a project name')

            if ('action' in kwargs and kwargs['action'] == 'new') or 'action' not in kwargs:
                if 'package' not in params or params['package'] == []:
                    params['package'] = {
                        'ApexClass'         : '*',
                        'ApexComponent'     : '*',
                        'ApexPage'          : '*',
                        'ApexTrigger'       : '*',
                        'StaticResource'    : '*'
                    }
                self.project = MavensMateProject(params)
                result = self.project.retrieve_and_write_to_disk()
            elif 'action' in kwargs and kwargs['action'] == 'existing':
                self.project = MavensMateProject(params)
                result = self.project.retrieve_and_write_to_disk('existing')

            if json.loads(result)['success'] == True:
                #opens project based on the client
                if self.plugin_client == self.PluginClients.SUBLIME_TEXT_2:
                    if self.platform == 'darwin':
                        os.system("'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '{0}'".format(self.project.location+"/"+self.project.project_name+".sublime-project"))
                elif self.plugin_client == self.PluginClients.SUBLIME_TEXT_3:
                    if self.platform == 'darwin':
                        os.system("'/Applications/Sublime Text 3.app/Contents/SharedSupport/bin/subl' --project '{0}'".format(self.project.location+"/"+self.project.project_name+".sublime-project"))

            return result
        except BaseException, e:
            return mm_util.generate_error_response(e.message)

    def get_log_level(self):
        try:
            return self.get_plugin_client_setting('mm_log_level')
        except:
            return None

    def get_log_location(self):
        try:
            return self.get_plugin_client_setting('mm_log_location')
        except:
            return None

    def get_sfdc_api_version(self):
        try:
            return self.get_plugin_client_setting('mm_api_version')
        except:
            return None
        # if 'mm_api_version' in self.plugin_client_settings['user'] and self.plugin_client_settings['user']['mm_api_version'] != None:
        #     return self.plugin_client_settings['user']['mm_api_version']
        # else:
        #     return self.plugin_client_settings['default']['mm_api_version']

    def get_plugin_client_setting(self, setting_name):
        if setting_name in self.plugin_client_settings['user'] and self.plugin_client_settings['user'][setting_name] != None:
            return self.plugin_client_settings['user'][setting_name]
        else:
            return self.plugin_client_settings['default'][setting_name]

    # tooling_api_extensions = ['.cls', '.trigger', '.page', '.component']

    # def alert(message):
    #     return { "success" : False, "body" : message }





