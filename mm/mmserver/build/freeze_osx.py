#this scripts freezes mm.py and places it in the dist directory
import sys
import argparse
import shutil
import os
import subprocess
import pipes
sys.path.append('../')
import util

mavensmate_path         = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
pyinstaller_path        = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"/tools/pyinstaller-dev"
mmserver_path           = os.path.dirname(os.path.dirname(__file__))
mmserver_build_path     = os.path.dirname(__file__)
build_settings          = util.parse_json_from_file('build_settings.json')

def main():
    #remove dist directory
    if os.path.exists("{0}/dist".format(mmserver_path)):
        shutil.rmtree("{0}/dist".format(mmserver_path))
    
    #remove mm directory from pyinstaller
    if os.path.exists("{0}/mmserver".format(pyinstaller_path)):
        shutil.rmtree("{0}/mmserver".format(pyinstaller_path))

    #run pyinstaller on mm.py
    os.chdir(pyinstaller_path)
    pyinstaller_command = "'{0}' pyinstaller.py '{1}/mmserver.py' --onedir '{2}/mmserver.spec'".format(
        build_settings['python_location'], 
        mmserver_path, 
        mmserver_path)

    print '>>>> ', pyinstaller_command
    p = subprocess.Popen(pyinstaller_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if p.stdout is not None : 
        for line in p.stdout.readlines():
            print line
    elif p.stderr is not None :
        print "****ERROR****"
        for line in p.stderr.readlines():
            print line

    #copy frozen mm to mm dist path
    shutil.copytree("{0}/mmserver/dist".format(pyinstaller_path), "{0}/dist".format(mmserver_path))
    
    #copy mm lib contents to mm/dist/mm/lib
    os.rename("{0}/dist/mmserver/lib".format(mmserver_path), "{0}/dist/mmserver/lib2".format(mmserver_path))
    shutil.copytree("{0}/lib".format(mmserver_path), "{0}/dist/mmserver/lib".format(mmserver_path))
    shutil.copytree("{0}/dist/mmserver/lib2/python2.7".format(mmserver_path), "{0}/dist/mmserver/lib/python2.7".format(mmserver_path))
    shutil.rmtree("{0}/dist/mmserver/lib2".format(mmserver_path))

    #run install_name_tool on libpython2.7.dylib
    # os.chdir("{0}/dist/mmserver".format(mmserver_path))
    # point_to_dylib_command = "/usr/bin/install_name_tool -change /usr/lib/libSystem.B.dylib {0} libpython2.7.dylib".format(
    #     pipes.quote("@loader_path/lib/dyn/libSystem.B.dylib"))

    # print '>>>> ', point_to_dylib_command 
    # p = subprocess.Popen(point_to_dylib_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # if p.stdout is not None : 
    #     for line in p.stdout.readlines():
    #         print line
    # elif p.stderr is not None :
    #     print "****ERROR****"
    #     for line in p.stderr.readlines():
    #         print line

if  __name__ == '__main__':
    main()