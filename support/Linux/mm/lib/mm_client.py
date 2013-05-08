import datetime
import re
import string
import sys
import unittest
import traceback
import json
import os
import yaml
import mm_util
import shutil
import config
import xmltodict
import requests
from operator import itemgetter
sys.path.append('../')

from sforce.base import SforceBaseClient
from suds import WebFault
from sforce.partner import SforcePartnerClient
from sforce.metadata import SforceMetadataClient
from sforce.apex import SforceApexClient
from sforce.tooling import SforceToolingClient

wsdl_path = config.base_path + "/lib/wsdl"
#if config.frozen:
#   wsdl_path = config.base_path

class MavensMateClient(object):

    def __init__(self, **kwargs):
        self.credentials            = kwargs.get('credentials', None)
        self.override_session       = kwargs.get('override_session', False)

        self.reset_creds            = False #set flag to true to have MavensMateProject restore creds

        self.username               = None
        self.password               = None
        self.sid                    = None
        self.user_id                = None
        self.server_url             = None
        self.metadata_server_url    = None
        self.endpoint               = None
        self.pod                    = None

        #salesforce connection bindings
        self.pclient                = None
        self.mclient                = None
        self.aclient                = None
        self.tclient                = None

        #print self.credentials

        if self.credentials != None:
            self.username               = self.credentials['username']              if 'username' in self.credentials else None
            self.password               = self.credentials['password']              if 'password' in self.credentials else None
            self.sid                    = self.credentials['sid']                   if 'sid' in self.credentials else None
            self.user_id                = self.credentials['user_id']               if 'user_id' in self.credentials else None
            self.metadata_server_url    = self.credentials['metadata_server_url']   if 'metadata_server_url' in self.credentials else None
            self.server_url             = self.credentials['server_url']            if 'server_url' in self.credentials else None
            self.org_type               = self.credentials['org_type']              if 'org_type' in self.credentials else 'production'
            self.endpoint               = self.credentials['endpoint']              if 'endpoint' in self.credentials else mm_util.get_sfdc_endpoint_by_type(self.org_type)

        #we do this to prevent an unnecessary "login" call
        #if the getUserInfo call fails, we catch it and reset our class variables 
        if self.override_session == False and self.sid != None and self.user_id != None and self.metadata_server_url != None and self.endpoint != None and self.server_url != None:
            self.pclient = self.__get_partner_client()
            self.pclient._setEndpoint(self.server_url)

            header = self.pclient.generateHeader('SessionHeader')
            header.sessionId = self.sid
            self.pclient.setSessionHeader(header)
            self.pclient._setHeaders('')

            result = None
            try:
                config.logger.debug('GETTING USER INFO')
                result = self.pclient.getUserInfo()
                config.logger.debug(result)
            except WebFault, e:
                #exception here means most likely that cached auth creds are no longer valid
                #we're ok with this, the script will attempt another login
                self.sid = None
        elif self.server_url == None:
            self.pclient = self.__get_partner_client()
            self.login()
            self.reset_creds = True  

        #if the cached creds didnt work & username/password/endpoint are not provided, get them from keyring
        if self.sid == None or self.override_session == True:
            self.pclient = self.__get_partner_client()
            self.login()   
            self.reset_creds = True

    def login(self):
        result = None
        try:
            result = self.pclient.login(self.username, self.password, '')
        except WebFault, e:
            raise e
        config.logger.debug('LOGIN RESULT')
        config.logger.debug(result)
        self.metadata_server_url    = result.metadataServerUrl
        self.sid                    = result.sessionId
        self.user_id                = result.userId
        self.server_url             = result.serverUrl
        #TODO: do need to reset clients here now?

    def is_connection_alive(self):
        try:
            #print self.sid
            result = self.pclient.getUserInfo()
        except WebFault, e:
            #print 'connection dead!'
            #print e
            return False
        return True

    def compile_apex(self, type, body, **kwargs):
        ac = self.__get_apex_client()
        compile_result = None
        if type == 'class' or type == 'ApexClass':
            compile_result = ac.compileClasses(body, **kwargs)
        elif type == 'trigger' or type == 'ApexTrigger':
            compile_result = ac.compileTriggers(body, **kwargs)
        return compile_result

    def execute_apex(self, params):
        ac = self.__get_apex_client()
        execute_apex_result = ac.executeAnonymous(params)
        return execute_apex_result

    def describeMetadata(self, **kwargs):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        return self.mclient.describeMetadata(**kwargs)

    def get_org_metadata(self, as_dict=True):
        describe_result = self.describeMetadata()
        d = xmltodict.parse(describe_result,postprocessor=mm_util.xmltodict_postprocessor)
        if as_dict:
            result = d["soapenv:Envelope"]["soapenv:Body"]["describeMetadataResponse"]["result"]
            sorted_list = sorted(result['metadataObjects'], key=itemgetter('xmlName')) 
            result['metadataObjects'] = sorted_list
            return result
        else:
            return json.dumps(d["soapenv:Envelope"]["soapenv:Body"]["describeMetadataResponse"]["result"], sort_keys=True, indent=4)

    def retrieve(self, **kwargs):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        return self.mclient.retrieve(**kwargs)

    def deploy(self, params, **kwargs):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        return self.mclient.deploy(params, **kwargs)

    def delete(self, params, **kwargs):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        return self.mclient.deploy(params, **kwargs)

    def run_tests(self, params):
        if self.aclient == None:
            self.aclient = self.__get_apex_client()
        params['namespace'] = self.get_org_namespace()
        return self.aclient.runTests(params)

    def get_org_namespace(self):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        return self.mclient.getOrgNamespace() 

    def does_metadata_exist(self, **kwargs):
        if self.pclient == None:
            self.pclient = self.__get_partner_client()
        query_result = self.pclient.query('select count() From '+kwargs['object_type']+' Where Name = \''+kwargs['name']+'\' AND NamespacePrefix = \''+self.get_org_namespace()+'\'')
        return True if query_result.size > 0 else False

    def execute_query(self, soql):
        if self.pclient == None:
            self.pclient = self.__get_partner_client()
        query_result = self.pclient.query(soql)
        return query_result

    def get_apex_entity_id_by_name(self, **kwargs):
        if self.pclient == None:
            self.pclient = self.__get_partner_client()
        query_result = self.pclient.query('select Id From '+kwargs['object_type']+' Where Name = \''+kwargs['name']+'\'')
        record_id = None
        try:
            record_id = query_result.records[0].Id
        except:
            pass
        return record_id

    def list_metadata_basic(self, request):
        if self.mclient == None:
            self.mclient = self.__get_metadata_client()
        list_response = self.mclient.listMetadata(request, True, config.connection.sfdc_api_version) 
        return list_response

    def list_metadata(self, metadata_type):
        try:
            if self.mclient == None:
                self.mclient = self.__get_metadata_client()
            metadata_type_def = mm_util.get_meta_type_by_name(metadata_type)
            has_children_metadata = False
            if 'childXmlNames' in metadata_type_def and type(metadata_type_def['childXmlNames']) is list:
                has_children_metadata = True
            is_folder_metadata = metadata_type_def['inFolder']
            if is_folder_metadata == True:
                metadata_request_type = metadata_type+"Folder"
            else:
                metadata_request_type = metadata_type
            if metadata_request_type == "EmailTemplateFolder":
                metadata_request_type = "EmailFolder"
            list_response = self.mclient.listMetadata(metadata_request_type, True, mm_util.SFDC_API_VERSION) 
            if type(list_response) is not list:
                list_response = [list_response]
            #print list_response
            object_hash = {} #=> {"Account" => [ {"fields" => ["foo", "bar"]}, "listviews" => ["foo", "bar"] ], "Contact" => ... }

            if has_children_metadata == True and len(list_response) > 0: #metadata objects like customobject, workflow, etc.
                request_names = []
                for element in list_response:
                    request_names.append(element['fullName'])
                retrieve_result = self.retrieve(package={
                    metadata_request_type : request_names
                })
                #print retrieve_result
                tmp = mm_util.put_tmp_directory_on_disk()
                mm_util.extract_base64_encoded_zip(retrieve_result.zipFile, tmp)

                #iterate extracted directory
                for dirname, dirnames, filenames in os.walk(tmp+"/unpackaged/"+metadata_type_def['directoryName']):
                    for f in filenames:
                        #f => Account.object
                        full_file_path = os.path.join(dirname, f)
                        data = mm_util.parse_xml_from_file(full_file_path)
                        c_hash = {}
                        for child_type in metadata_type_def['childXmlNames']:
                            #print 'processing child type >>>>> ', child_type
                            child_type_def = mm_util.get_meta_type_by_name(child_type)
                            if child_type_def == None: #TODO handle newer child types
                                continue
                            tag_name = child_type_def['tagName']
                            items = []
                            try:
                                for i, val in enumerate(data['CustomObject'][tag_name]):
                                    #print val['fullName']
                                    items.append(val['fullName'])
                            except BaseException, e:
                                #print 'exception >>>> ', e.message
                                pass

                            c_hash[tag_name] = items

                        base_name = f.split(".")[0]
                        object_hash[base_name] = c_hash

                shutil.rmtree(tmp)

            return_elements = []

            for element in list_response:
                children = []
                full_name = element['fullName']
                if full_name == "PersonAccount":
                    full_name = "Account" 
                #print 'processing: ', element
                if has_children_metadata == True:
                    object_detail = object_hash[full_name]
                    if object_detail == None:
                        continue

                    for child in metadata_type_def['childXmlNames']:
                        child_type_def = mm_util.get_meta_type_by_name(child)
                        if child_type_def == None: #TODO: handle more complex types
                            continue
                        tag_name = child_type_def['tagName']
                        if len(object_detail[tag_name]) > 0:
                            gchildren = []
                            for gchild_el in object_detail[tag_name]:
                                gchildren.append({
                                    "title"       : gchild_el,
                                    "key"         : gchild_el,
                                    "isLazy"      : False,
                                    "isFolder"    : False,
                                    "selected"    : False
                                })
                                children = sorted(children, key=itemgetter('title')) 
                          
                            children.append({
                                "title"     : child_type_def['tagName'],
                                "key"       : child_type_def['tagName'],
                                "isLazy"    : False,
                                "isFolder"  : True,
                                "children"  : gchildren,
                                "selected"  : False
                            })
                            children = sorted(children, key=itemgetter('title')) 

                #if this type has folders, run queries to grab all metadata in the folders
                if is_folder_metadata == True:
                    if element["manageableState"] != "unmanaged":
                        continue

                    list_basic_response = self.list_metadata_basic({
                            "type"      : metadata_type,
                            "folder"    : element["fullName"]
                    })

                    if type(list_basic_response) is not list:
                        list_basic_response = [list_basic_response]

                    for folder_element in list_basic_response:
                        children.append({
                            "title"     : folder_element['fullName'].split("/")[1],
                            "key"       : folder_element['fullName'],
                            "isLazy"    : False,
                            "isFolder"  : False,
                            "selected"  : False
                        })
                        children = sorted(children, key=itemgetter('title')) 

                return_elements.append({
                    "title"     : element['fullName'],
                    "key"       : element['fullName'],
                    "isLazy"    : is_folder_metadata or has_children_metadata,
                    "isFolder"  : is_folder_metadata or has_children_metadata,
                    "children"  : children,
                    "selected"  : False
                })
                return_elements = sorted(return_elements, key=itemgetter('title')) 

            # if list_response == []:
            #     return list_response

            # return list_response
            return return_elements
        except BaseException, e:
            if 'INVALID_TYPE: Unknown type' in e.message:
                return None
            else:
                #print traceback.print_exc()
                raise e

    def get_overlay_actions(self, **kwargs):        
        if 'file_path' in kwargs:
            id = kwargs.get('id', None)
            file_path = kwargs.get('file_path', None)
            if id == None:
                ext = mm_util.get_file_extension_no_period(file_path)
                api_name = mm_util.get_file_name_no_extension(file_path)
                mtype = mm_util.get_meta_type_by_suffix(ext)
                id = self.get_apex_entity_id_by_name(object_type=mtype['xmlName'], name=api_name)
            query_string = "Select Id, Line, Iteration, ExpirationDate, IsDumpingHeap from ApexExecutionOverlayAction Where ExecutableEntityId = '{0}'".format(id)
            payload = { 'q' : query_string }
            r = requests.get(self.get_tooling_url()+"/query/", params=payload, headers=self.get_rest_headers(), verify=False)
            return mm_util.parse_rest_response(r.text)
        else:
            query_string = "Select Id, ScopeId, ExecutableEntityId, Line, Iteration, ExpirationDate, IsDumpingHeap from ApexExecutionOverlayAction limit 5000"
            payload = { 'q' : query_string }
            r = requests.get(self.get_tooling_url()+"/query/", params=payload, headers=self.get_rest_headers(), verify=False)
            return mm_util.parse_rest_response(r.text)

    def get_trace_flags(self, **kwargs):        
        query_string = "Select Id, ScopeId, TracedEntityId, ExpirationDate from TraceFlag limit 5000"
        payload = { 'q' : query_string }
        r = requests.get(self.get_tooling_url()+"/query/", params=payload, headers=self.get_rest_headers(), verify=False)
        return mm_util.parse_rest_response(r.text)    

    def create_trace_flag(self, payload):
        if 'ScopeId' not in payload:
            payload['ScopeId'] = self.user_id
        payload = json.dumps(payload)
        r = requests.post(self.get_tooling_url()+"/sobjects/TraceFlag", data=payload, headers=self.get_rest_headers('POST'), verify=False)
        return mm_util.parse_rest_response(r.text)

    #TODO: support in the future
    def run_async_apex_tests(self, payload):
        payload = json.dumps(payload)
        r = requests.post(self.get_tooling_url()+"/sobjects/ApexTestQueueItem", data=payload, headers=self.get_rest_headers('POST'), verify=False)
        return mm_util.parse_rest_response(r.text)

    def create_overlay_action(self, payload):
        if 'ScopeId' not in payload:
            payload['ScopeId'] = self.user_id
        if 'API_Name' in payload:
            payload['ExecutableEntityId'] = self.get_apex_entity_id_by_name(object_type=payload['Object_Type'], name=payload['API_Name'])
            payload.pop('Object_Type', None)
            payload.pop('API_Name', None)

        payload = json.dumps(payload)
        r = requests.post(self.get_tooling_url()+"/sobjects/ApexExecutionOverlayAction", data=payload, headers=self.get_rest_headers('POST'), verify=False)
        return mm_util.parse_rest_response(r.text)

    def remove_overlay_action(self, **kwargs):
        if 'overlay_id' in kwargs:
            r = requests.delete(self.get_tooling_url()+"/sobjects/ApexExecutionOverlayAction/{0}".format(kwargs['overlay_id']), headers=self.get_rest_headers(), verify=False)
            r.raise_for_status()
            return mm_util.generate_success_response('OK')
        else:
            id = kwargs.get('id', None)
            file_path = kwargs.get('file_path', None)
            line_number = kwargs.get('line_number', None)
            if id == None:
                ext = mm_util.get_file_extension_no_period(file_path)
                api_name = mm_util.get_file_name_no_extension(file_path)
                mtype = mm_util.get_meta_type_by_suffix(ext)
                id = self.get_apex_entity_id_by_name(object_type=mtype['xmlName'], name=api_name)
            
            query_string = "Select Id from ApexExecutionOverlayAction Where ExecutableEntityId = '{0}' AND Line = {1}".format(id, line_number)
            r = requests.get(self.get_tooling_url()+"/query/", params={'q':query_string}, headers=self.get_rest_headers(), verify=False)
            r.raise_for_status()
            query_result = mm_util.parse_rest_response(r.text)
            overlay_id = query_result['records'][0]['Id']
            r = requests.delete(self.get_tooling_url()+"/sobjects/ApexExecutionOverlayAction/{0}".format(overlay_id), headers=self.get_rest_headers(), verify=False)
            r.raise_for_status()
            return mm_util.generate_success_response('OK')

    def download_log(self, id):
        pod = self.metadata_server_url.replace("https://", "").split("-")[0]
        log_endpoint = "https://{0}.salesforce.com/apexdebug/traceDownload.apexp".format(pod)
        r = requests.get(log_endpoint, params={"id":id}, headers=self.get_rest_headers(), verify=False)
        return r.text

    def download_checkpoint(self, id):
        pod = self.metadata_server_url.replace("https://", "").split("-")[0]
        checkpoint_endpoint = "https://{0}.salesforce.com/servlet/debug/apex/ApexCSIJsonServlet".format(pod)
        r = requests.get(checkpoint_endpoint, params={"log":id,"extent":"fewmet","doDelete":False,"page":1,"start":0,"limit":25}, headers=self.get_rest_headers(), verify=False)
        return r.text

    def get_rest_headers(self, method='GET'):
        headers = {}
        headers['Authorization'] = 'Bearer '+self.sid
        if method == 'POST':
            headers['Content-Type'] = 'application/json'
        return headers

    def get_tooling_url(self):
        pod = self.metadata_server_url.replace("https://", "").split("-")[0]
        return "https://{0}.salesforce.com/services/data/v{1}/tooling".format(pod, mm_util.SFDC_API_VERSION)

    def __get_partner_client(self):
        return SforcePartnerClient(
            wsdl_path+'/partner.xml', 
            apiVersion=mm_util.SFDC_API_VERSION, 
            environment=self.org_type, 
            sid=self.sid, 
            metadata_server_url=self.metadata_server_url, 
            server_url=self.endpoint)

    def __get_metadata_client(self):
        return SforceMetadataClient(
            wsdl_path+'/metadata.xml', 
            apiVersion=mm_util.SFDC_API_VERSION, 
            environment=self.org_type, 
            sid=self.sid, 
            url=self.metadata_server_url, 
            server_url=self.endpoint)

    def __get_apex_client(self):
        return SforceApexClient(
            wsdl_path+'/apex.xml', 
            apiVersion=mm_util.SFDC_API_VERSION, 
            environment=self.org_type, 
            sid=self.sid, 
            metadata_server_url=self.metadata_server_url, 
            server_url=self.endpoint)

    def __get_tooling_client(self):
        return SforceToolingClient(
            wsdl_path+'/tooling.xml', 
            apiVersion=mm_util.SFDC_API_VERSION, 
            environment=self.org_type, 
            sid=self.sid, 
            metadata_server_url=self.metadata_server_url, 
            server_url=self.endpoint)


