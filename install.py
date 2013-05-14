try:
    import os
    import sys
    import platform
    import shutil
    import argparse
    import pipes

    install_paths = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 2/Packages/MavensMate"),
        "win32"  : "",
        "cygwin" : "",
        "linux2" : os.path.expanduser("~/.config/sublime-text-2/Packages/MavensMate")
    }

    user_settings_path = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 2/Packages/User"),
        "win32"  : "",
        "cygwin" : "",
        "linux2" : os.path.expanduser("~/.config/sublime-text-2/Packages/User")
    }

    sys_platform        = sys.platform
    install_path        = install_paths[sys_platform]
    user_settings_path  = user_settings_path[sys_platform]
    branch              = None
    git_url             = pipes.quote('git://github.com/manandoshi9/MavensMate-SublimeText.git')

    def install_from_source():
        branch = '2.0'
        os.system("git clone {0} {1}".format(git_url, pipes.quote(install_path)))

    def install_user_settings():
        if os.path.isfile(user_settings_path+"/mavensmate.sublime-settings") == False:
            os.system("cp {0} {1}".format(
                pipes.quote(install_path+"/mavensmate.sublime-settings"), 
                pipes.quote(user_settings_path)
            ))

    def delete_32_or_64():
        platform_arch = platform.architecture()[0]
        if ( platform_arch == '32bit' ):
            os.system ( "rm -rf {0}".format(pipes.quote(install_path + "/support/linux64" ) ) )
        else:
            os.system ( "rm -rf {0}".format(pipes.quote(install_path + "/support/linux32" ) ) )

    def uninstall():
        os.system("rm -rf {0}".format(pipes.quote(install_path)))

    def install():
        uninstall()
        install_from_source()
        if ( sys_platform == 'linux2' ):
            delete_32_or_64()
        install_user_settings()

    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-b', '--branch') #name of the branch being requested
        args = parser.parse_args()
        if args.branch != None and args.branch != '':
            branch = args.branch
        install()
except Exception as e:
    print('install.py issue')
    print(e.message)
