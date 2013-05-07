import os
import sys
import shutil
import subprocess
import pipes
import xmltodict
from jinja2 import Environment, FileSystemLoader
import jinja2.ext

from datetime import datetime
from datetime import timedelta

mavensmate_app_path = os.path.dirname(os.path.dirname(__file__))
mavensmate_base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

env = Environment(loader=FileSystemLoader(mavensmate_app_path+"/build"),trim_blocks=True)

if os.path.exists(mavensmate_app_path+"/dist/MavensMate.app"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/dist/MavensMate.app"))
if os.path.exists(mavensmate_app_path+"/dist/MavensMate.zip"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/dist/MavensMate.zip"))
if os.path.exists(mavensmate_app_path+"/release/MavensMate.zip"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/release/MavensMate.zip"))
if os.path.exists(mavensmate_app_path+"/release/appcast.xml"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/release/appcast.xml"))


##TODO: build mm
# os.chdir(mavensmate_base_path+"/mm/build")
# mm_build_script = 'freeze_osx.py'
# process = subprocess.Popen(['/Library/Frameworks/Python.framework/Versions/2.7/bin/python',mm_build_script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
# mm_build_response = None
# if process.stdout is not None: 
#     mm_build_response = process.stdout.readlines()
# elif process.stderr is not None:
#     mm_build_response = process.stderr.readlines()
# mm_build_response = '\n'.join(mm_build_response)
# mm_build_response = mm_build_response.rstrip()
# print 'mm build response: ' + mm_build_response


os.chdir(mavensmate_app_path)
build_command = '/usr/bin/xcodebuild -target MavensMate -scheme MavensMate archive'
os.system(build_command)
os.chdir(mavensmate_app_path+"/dist")
shutil.make_archive(mavensmate_app_path+'/release/MavensMate', 'zip', root_dir = mavensmate_app_path+'/dist')

release_info_plist_path = mavensmate_app_path+"/dist/MavensMate.app/Contents/Info.plist"
xml_data = open(release_info_plist_path)
data = xmltodict.parse(xml_data)
xml_data.close()

##get release version number
plist_dict = data['plist']['dict']
bundle_index = None
for i,f in enumerate(plist_dict['key']):
    if f == 'CFBundleVersion':
        bundle_index = i

version_number = None
for i,f in enumerate(plist_dict['string']):
    if i == bundle_index:
        version_number = f

##sign release
os.chdir(mavensmate_app_path+"/build")
sign_script_location = mavensmate_app_path+"/build/sign_update.rb"
private_key_location = os.path.expanduser("~/Dropbox/Development/MavensMate/dsa_priv.pem")
release_zip_location = mavensmate_app_path+"/release/MavensMate.zip"
process = subprocess.Popen(['/usr/bin/ruby',sign_script_location,release_zip_location,private_key_location], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
sign_response = None
if process.stdout is not None: 
    sign_response = process.stdout.readlines()
elif process.stderr is not None:
    sign_response = process.stderr.readlines()
sign_response_body = '\n'.join(sign_response)
sign_response_body = sign_response_body.rstrip()
print 'sign response: ' + sign_response_body

##todo: set availability? 30 mins from now?
pub_date = datetime.now().strftime("%a, %d %B %Y %H:%M:%S +0000")

##write new appcast.xml
appcast = open(mavensmate_app_path+"/release/appcast.xml", "w")
template = env.get_template('appcast.html')
file_body = template.render(version_number=version_number,signature=sign_response_body,pub_date=pub_date)
appcast.write(file_body)
appcast.close()