#MavensMate for Sublime Text plugin (2.0 beta)

MavensMate for Sublime Text is a plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE. Its goal is to allow developers to work inside Sublime Text for all their Force.com-related tasks.

* Create & Edit Salesforce.com projects with specific package metadata
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Play Pacman, Tetris, and Donkey Kong while your Apex unit tests and deploys run
* Deploy metadata to other Salesforce.com orgs
* Apex Execute Anonymous
* Create Apex Execution Overlay Actions (tooling API)
* Download Apex Logs (tooling API)
* Apex Code Assist (beta!!)

#Install instructions (Linux only)

 * sudo apt-get install  python git chromium-browser
 * wget https://raw.github.com/manandoshi9/MavensMate-SublimeText/2.0/install.py
 * python install.py
 * create your workspace folder e.g. /home/your_username/mm-force.com please avoid any whitespace or special characters
    start sublime text 2
 * In MavensMate -> Settings -> User set mm_workspace to your workspace folder, like /home/your_username/mm-force.com
 * In MavensMate -> Settings -> User consider changing mm_sublime
 * In MavensMate -> Settings -> User consider changing mm_chrome
 * In MavensMate -> Settings -> User consider changing mm_app_location -> this should point to the mmserver executable. The 
 	default location should be ~/.config/sublime-text-2/Packages/MavensMate/support/(linux32 or linux64 depending on your architecture)/mmserver/mmserver
 * In MavensMate -> Settings -> User consider changing mm_location -> this should point to the mm executable. The 
 	default location should be ~/.config/sublime-text-2/Packages/MavensMate/support/(linux32 or linux64 depending on your architecture)/mm/mm
    restart sublime text 2

