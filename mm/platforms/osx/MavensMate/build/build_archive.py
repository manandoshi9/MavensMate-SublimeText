import os
import sys
import shutil
import subprocess
import pipes
import xmltodict
from jinja2 import Environment, FileSystemLoader
import jinja2.ext
import ftplib

mavensmate_app_path = os.path.dirname(os.path.dirname(__file__))

env = Environment(loader=FileSystemLoader(mavensmate_app_path+"/build"),trim_blocks=True)

if os.path.exists(mavensmate_app_path+"/dist/MavensMate.app"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/dist/MavensMate.app"))
if os.path.exists(mavensmate_app_path+"/dist/MavensMate.zip"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/dist/MavensMate.zip"))
if os.path.exists(mavensmate_app_path+"/release/MavensMate.zip"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/release/MavensMate.zip"))
if os.path.exists(mavensmate_app_path+"/release/appcast.xml"):
    os.system("rm -rf {0}".format(mavensmate_app_path+"/release/appcast.xml"))

os.chdir(mavensmate_app_path)
build_command = '/usr/bin/xcodebuild -target MavensMate -scheme MavensMate archive'
os.system(build_command)
os.chdir(mavensmate_app_path+"/dist")
shutil.make_archive(mavensmate_app_path+'/release/MavensMate', 'zip', root_dir = mavensmate_app_path+'/dist')