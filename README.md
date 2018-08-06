# Report Automation Documentation :star:

_Welcome Folks!_ The purpose of this project is to automate the monthly reports. 

## How to Run Code

In a very general way. There are template reports made for every single client with information in the file 
client_information/client_information.json. These reports should be shared with you on Google Slides. You should be logged into a google
account and be inside of my virtual environment (requirements.txt). Great, so now open up a separate terminal using finder. The terminal icon looks like this

![picture alt](https://cdn.dribbble.com/users/559169/screenshots/2456814/02-terminal_1x.png)

The terminal should look like this

![picture alt](https://www.imore.com/sites/imore.com/files/styles/xlarge/public/field/image/2016/02/say-terminal-command-screenshot.jpg?itok=jOSHQLCF)

Make sure you are in the correct directory. For me that looks like ~/dev/googleslidesapi. You can change your directory by typing in cd and then your file path. So, I would type in cd ~/dev/googleslides api to get to my project located at Users/sarahpolzer/dev/googleslidesapi. 

![cd](screenshots_for_instructions/cd.png)

Then I would make sure that I am in a virtual environment with all of the necessary packages, if pip, virtualenv,virtualenvwrapper are already installed on your computer, type in mkvirtuaenv googleslidesapi.

![mkvirtualenv](screenshots_for_instructions/mkvirtualenv.png)

Then type in workon googleslidesapi

![workon](screenshots_for_instructions/workon.png)


Finally, type in pip install -r requirements.txt. Great, you should be ready. 

![requirements](screenshots_for_instructions/requirements.png)


In the separate terminal, type in python flask_master_script.py, and follow directions for User inputs.

![flaskmasterscript](screenshots_for_instructions/flask_master_script.png)


Wait a couple seconds. The separate terminal should now look like this. Leave it alone for now.

![runningon](screenshots_for_instructions/running_on.png)

Now go to VSCode in the project folder. At the top of the page, you should see a dropdown entitled View. Click on it and then press integrated terminal. The integrated terminal looks like this.

![picture alt](http://keysandstrokes.info/wp-content/uploads/2016/10/Visual-Studio-Code-Integrated-terminal.png)


 Make sure you are in the correct directory, and that you are in the correct virtual environment (type workon googleslidesapi). Ok now type into the terminal master_script.py.

The code should run and you should see that the report for the client that you selected will be automated with charts, dates, logos, and more!!


## How to regenerate client template reports and update client information

Ok cool so located in the client_information directory ~/dev/googleslidesapi/client_data_list there is a script to generate client data and new template reports named after each client. There is a file called client_information.json that contains a clients dictionary. This dictionary has client names, and domain names, google analytics ids, what converts ids, organization logos, presentation ids. If you need to update any of these values just go into the file and update it. If you need to generate new template client reports, move the file client_data_list.py into the ~/dev/googleslides directory, and then run it by typing into cd ~/dev/googleslidesapi and python client_data_list.py. It will generate a new client dictionary (client_information.json) and new client template reports in Google Drive. After this process has completed, move client_data_list.py and client_information.json into the client_information directory ~/dev/googleslidesapi/client_information. :star:


 ### Updating presentation IDs.

 Lets say that you want to make a new template report for a client without having to make template presentations for all clients by running client_data_list.py. Theres an easy solution. Just make a copy of the google presentation in your drive entitled template, and then rename it the name of the client. Then find its presentation id based on the presentations URL.


![picture alt](https://i.ytimg.com/vi/VSz0WxdF0eM/maxresdefault.jpg)

Above is a Google Presentation. In its URL, between presentation/d/ and /edit is a long sequence of letters and numbers. This is your presentation ID. Copy this sequence, and paste it into client_information.json next to "presentation_id": for the client. Make sure it is a string, or is enclosed by quotations. For example "presentation_id" : "1234567gfderfdgbrh3eteh"

### Updating Domain Name, WhatConvers, Organization Logo, or Google Analytics Information for a Single Client

The same can be done if the organization logo, the WhatConverts ID, the domain name, or the Google Analytics ID of any one client changes. Just overwrite the old inforamtion in client_information.json with new client information. For example, if client_information.json says that the domain name for Beyond Exteriors is beyond_exteriors.org like this "Beyond Exteriors" : "beyond_exteriors.org", and the domain name has been changed to "beyond_exteriors.com", just overwrite the old dictionary value with "beyond_exteriors.com". 

"Beyond Exteriors" : "beyond_exteriors.org" is now "Beyond Exteriors" : "beyond_exteriors.com"









