# Report Automation Documentation

_Welcome Folks!_ The purpose of this project is to automate the monthly reports. 

## How to Run Code

In a very general way. There are template reports made for every single client with information in the file 
client_information/client_information.json. These reports should be shared with you on Google Slides. You should be logged into a google
account and be inside of my virtual environment (requirements.txt). Great, so now open up a separate terminal using finder. The terminal icon looks like this

![picture alt](https://cdn.dribbble.com/users/559169/screenshots/2456814/02-terminal_1x.png)

The terminal should look like this

![picture alt](https://www.imore.com/sites/imore.com/files/styles/xlarge/public/field/image/2016/02/say-terminal-command-screenshot.jpg?itok=jOSHQLCF)

Make sure you are in the correct directory. For me that looks like ~/dev/googleslidesapi. You can change your directory by typing in cd and then your file path. So, I would type in cd ~/dev/googleslides api to get to my project located at Users/sarahpolzer/dev/googleslidesapi. Then I would make sure that I am in a virtual environment with all of the necessary packages, if pip, virtualenv,virtualenvwrapper are already installed on your computer, type in mkvirtuaenv googleslides api, and then type in pip install -r requirements.txt. Great, you should be ready. In the separate terminal, type in python flask_master_script.py, and follow directions for User inputs.

The separate terminal should say that it is Running on http://127.0.0.1:5005/ 

Now go to VSCode in the project folder. At the top of the page, you should see a dropdown entitled View. Click on it and then press integrated terminal. The integrated terminal looks like this.

![picture alt](http://keysandstrokes.info/wp-content/uploads/2016/10/Visual-Studio-Code-Integrated-terminal.png)


 Make sure you are in the correct directory, and that you are in the correct virtual environment (type workon googleslidesapi). Ok now type into the terminal master_script.py.

The code should run and you should see that the report for the client that you selected will be automated with charts, dates, logos, and more!!


## How to regenerate client template reports and update client information

Ok cool so located in the client_information directory ~/dev/googleslidesapi/client_data_list there is a script to generate client data and new template reports named after each client. There is a file called client_information.json that contains a clients dictionary. This dictionary has client names, and domain names, google analytics ids, what converts ids, organization logos, presentation ids. If you need to update any of these values just go into the file and update it. If you need to generate new template client reports, move the file client_data_list.py into the ~/dev/googleslides directory, and then run it by typing into cd ~/dev/googleslidesapi and python client_data_list.py. It will generate a new client dictionary (client_information.json) and new client template reports in Google Drive. After this process has completed, move client_data_list.py and client_information.json into the client_information directory ~/dev/googleslidesapi/client_information.





