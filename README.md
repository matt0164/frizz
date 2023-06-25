Frizz-Wiz Application Documentation
Version 0.02 running with GPS as of 6/24/23 and without slider 
Overview
Frizz-Wiz is a web application running on an Nginx server. The application is configured to be accessible from the internet via app.frizz-wiz.com with the domain names frizz-wiz.com and www.frizz-wiz.com.
The Application Code
The Components
1.	Python Scripts: Two Python scripts are used in the Frizz Wiz application. These scripts include functions for retrieving weather data and geolocation information. They interact with an external APIs, OpenWeatherMap, to fetch weather data and geolocation details. The scripts are called by the Flask application to provide the necessary data for rendering the web pages.
2.	HTML Template: The HTML template defines the structure and content of the web pages displayed to users. It utilizes template engines to dynamically insert data retrieved from the Python scripts. The template displays weather results, and renders images and text based on the weather conditions (humidity and dew point impacting a user’s hair). It is formatted based on a css style template.
3.	JavaScript: Two JavaScript files are used to handle the UI interactivity, geolocation functionality, and to make AJAX requests to the server. fetch_forecast.js fetches weather data, and location.js gets the current latitude and longitude using browser's GPS.
4.	Gunicorn Configuration and Error Logs: Gunicorn is a Python WSGI HTTP Server that serves the Flask application. The configuration file specifies server settings such as the number of worker processes, bind address, and log file locations. The error logs capture any errors or exceptions that occur during the server's operation, providing valuable information for debugging and troubleshooting.
5.	Flask Application: The Flask application is the core of the Frizz Wiz web server. It handles incoming HTTP requests and generates appropriate responses. The application consists of routes that define the URL endpoints and associated functions to handle the requests. It also utilizes templates to render dynamic HTML pages and JavaScript files for the interactivity of the pages. The application interacts with the Gunicorn server to serve the web pages to clients.
6.	Gunicorn Server: Gunicorn is responsible for running the Flask application as a web server. It listens for incoming requests and dispatches them to the appropriate Flask route for processing. The server configuration determines how the server operates, including the number of worker processes, concurrency model, and network settings.
 
By combining these components, the Frizz Wiz application functions as a web server that receives user input, retrieves weather data, and dynamically renders HTML pages with the corresponding information. The server (Gunicorn) listens for incoming requests and directs them to the Flask application, which utilizes Python scripts and HTML templates to process the requests and generate the appropriate responses. The end result is a user-friendly interface where users can retrieve weather information based on zip codes or their current location.

[graphic available in word file]

1.	web_app.py: This Python file serves as the entry point for the Flask application. It imports the necessary modules, sets up the Flask app, defines the routes, and handles the logic for retrieving weather data based on location. The routes interact with the HTML templates by rendering them and passing data from the Python scripts to be displayed dynamically. Additionally, it interacts with JavaScript files by receiving data via AJAX requests and triggering updates on the web page.
2.	weather_fetch.py: This Python file contains functions for fetching weather data from external APIs based on location coordinates and time selection. The get_weather() function retrieves weather data using the OpenWeatherMap API and performs calculations to determine the weather forecast. The function returns the weather result and photo URL to be displayed in the HTML templates.
3.	frizz_landing.html: This HTML template is the main page of the Frizz Wiz application. It includes a form where a user can click a button to use geolocation. It also includes placeholders for displaying the weather result, photo, and dynamically generated colors. The template interacts with the Python script web_app.py by receiving the weather result and photo data to be rendered in the appropriate sections.
4.	fetch_forecast.js: This JavaScript file sends the chosen time range and location details (GPS coordinates) to the Flask app via an AJAX POST request. Upon receiving a successful response, it updates the weather forecast and the photo on the page. It interacts with both web_app.py and weather_fetch.py to fetch and display updated weather forecasts.
5.	location.js: This JavaScript file is responsible for handling geolocation functionality in the web page. It checks if the browser supports geolocation and, if so, retrieves the current latitude and longitude coordinates. It then sends this data to the server using an AJAX request to the /weather route. Upon receiving a successful response (status code 200), it triggers a fetch for updated weather information based on the current location. This file interacts with web_app.py and weather_fetch.py through the AJAX request and response handling.
6.	style.css: This is a stylesheet that dictates the aesthetic and layout for the Frizz Wiz web app. It defines styles for various elements, such as the body and header, to ensure an intuitive and visually appealing user interface. Customizations include font family, background, and flex container setup for the entire application, and layout dimensions.
These files work together to create a seamless user experience. The Python scripts fetch weather data and perform calculations, the JavaScript files handle geolocation functionality and user-selected time ranges, and the HTML template displays the content dynamically based on user input and retrieved data from the Python scripts.

Updating Application Code
To update the application, you commit your changes to a version control system (like Git), then pull or checkout the updated code on the server.
Depending on the nature of the updates, you may need to restart the application or the Nginx server for the changes to take effect.
Uploading Code to the Server
You can upload code to the server using scp (secure copy), rsync, or any other file transfer method. If you use Git, you can simply git pull the latest version of your code on the server.
 
web_app.py
This module serves as the main entry point for a Flask-based web application, which fetches weather data based on user-inputted parameters. It supports both POST and GET requests on multiple endpoints. The web_app.py file is designed to be run on a web server.
1.	The / route serves the homepage, handles POST requests to fetch weather data based on coordinates, and stores fetched data in session variables. The page background color is randomly generated.
2.	The /weather route takes POST requests and fetches weather data based on lat long coordinates. It returns error messages for missing or invalid parameters.
If the module is run as the main script, the Flask application is started.
The external function used in this module is get_weather from a module named weather_fetch.py.
The application requires two environment variables - a "SECRET_KEY" used by Flask for session management and potentially a "SESSION_KEY" - although the code does not seem to use the latter. If the environment variables are not found, a fallback value is used for the "SECRET_KEY".
In summary, web_app.py defines routes and their corresponding functions for handling requests. It interacts with the weather_fetch module to retrieve weather data based on user input and renders the HTML template "frizz_landing.html" with the results and dynamically generated colors.
 
weather_fetch.py

his script, weather_fetch.py, handles fetching weather data from the OpenWeatherMap API and implements the core logic for processing the fetched data.
The script starts by loading environment variables from a .env file, which includes an "API_KEY" for the OpenWeatherMap API. It also sets up the base URL for the OpenWeatherMap API.
There is one primary function in this script: 
1.	get_weather: The get_weather function fetches weather data based on latitude (lat) and longitude (lon) coordinates. It makes a GET request to the One Call API, passing the coordinates and API key as parameters. If the GET request is successful (status code 200), it retrieves the JSON data from the response and extracts the hourly forecast data. The function then calculates the average humidity and dew point during the specified core hours of the day (default 10 AM to 3 PM). It also determines if there are hours with high humidity or dew point above predefined thresholds. Based on the average humidity and dew point, the function provides a forecast and advice for hair care, selecting an appropriate photo based on the forecast conditions. If the GET request is unsuccessful, it prints the status code and returns an error message along with a default photo. The function returns a dictionary containing the photo URL and the forecast result.
The script also employs logging to record the URLs it fetches data from, the received data, and any errors that occur.
 
location.js

This code is responsible for getting the user's current location using the browser's geolocation API and sending it to the server for further processing. Let's break it down:
1.	function handleGpsFailure() : This is a JavaScript function that is called when the Geolocation API fails to get the user's current position. It logs an error message to the console for debugging purposes.
2.	function getLocation() {...}: This is a JavaScript function that is triggered when the user clicks the element with the ID location-btn.
3.	if (navigator.geolocation) {...}: This condition checks if the browser supports the geolocation API.
4.	navigator.geolocation.getCurrentPosition(function(position) {...}): If geolocation is supported, this line retrieves the current position (latitude and longitude) of the user.
5.	Inside the callback function, the latitude and longitude values are extracted from the position object.
6.	An AJAX request is sent to the server using the XMLHttpRequest object (xhr). The request is sent as a POST request to the /weather endpoint with the latitude and longitude data included in the request payload as JSON.
7.	xhr.onload is an event listener that triggers when the AJAX request has completed. If the status code of the response is 200 (indicating a successful request), the page is reloaded using location.reload(). This is typically done to update the page with new data received from the server.
8.	If the browser doesn't support geolocation, an alert is shown indicating that geolocation is not supported.
9.	window.addEventListener('load', function() {...}): This event listener waits for the page to finish loading. Once loaded, it attaches an event listener to the element with the ID location-btn and calls the getLocation() function when that element is clicked.
In summary, this code allows the user to click a button (with ID location-btn) to obtain their current location using the browser's geolocation API. The obtained latitude and longitude coordinates are then sent to the server for further processing, potentially retrieving weather information or performing other location-based tasks.
Flask's url_for function is intelligent enough to find the static files. As long as the location.js file is in a directory named static at the same level as your templates directory, Flask will be able to locate the file. The project structure should look something like this:
frizz/
  static/
    location.js
  templates/
    frizz_landing.html
  app.py 
frizz_landing.html

This is an HTML page that represents the user interface for the Frizz Wiz application. It is saved locally in a test environment in C:\Users\matta\PycharmProjects\frizz\templates and on the Ubuntu Unix server in /var/www/frizz/templates/ whereas all of the other files are in the \frizz (/frizz) directory.  Let's go through its structure and elements:
The document structure can be broken down into two main parts: the head and the body.
In the head:
•	It declares the HTML document's language (lang="en"), character encoding (charset="UTF-8"), and viewport settings for responsive design (name="viewport").
•	The title tag sets the webpage title as " The Frizz Wiz – Alpha [with version #]".
•	The style tag includes CSS styles for various elements on the webpage such as body, form, div, img, and several specific elements with IDs like 'location-btn', 'submit-btn', 'weather_photo', and 'resultDiv'. This styling is responsible for the look and layout of the webpage.
•	The head also includes scripts for jQuery and jQuery UI, useful for handling events, creating animations, and adding other interactive features.
•	It links to a CSS file named styles.css from the application's static files.
In the body:
•	There's a top-level heading (h1) "The Frizz Wiz".
•	A form (id="locationForm") which includes two hidden input fields for latitude and longitude, and a button to get the hair forecast.
•	A div (id="resultDiv") which is hidden by default, and presumably displayed after a successful fetch of the hair forecast. This div includes a heading, paragraph for displaying results, and an image element for displaying a weather photo.
•	At the end, two JavaScript files named jquery.min.js and location.js are linked from the web and the application's static files. These scripts contain JavaScript functionality for the webpage such as fetching the hair forecast using Ajax and getting the user's location.
Key elements and attributes such as {{ color1 }}, {{ color2 }}, {{ url_for('static', filename='css/new_slider.css') }}, etc. are placeholders which will be filled in with actual data when the HTML is rendered by a web server (like Flask). The placeholder notation {{ ... }} is common in web frameworks to signify dynamic content.
The whole webpage is designed for the user to get their hair forecast based on their location and a chosen time range. The forecast results and a corresponding photo will be displayed on the webpage after they have been fetched from the server.


fetch_forecast.js
fetch_forecast.js, is a JavaScript code that fetches weather forecast data from a Flask web application and updates the webpage's content based on the returned forecast. Here's what each part of the script does:
Let's break down the functions:
1.	pad(number): This function pads a number with a leading zero if it is less than 10.
2.	window.fetchWeatherForecast(startHourValue, endHourValue): This function is called to fetch the weather forecast. It retrieves the GPS coordinates from the HTML elements with IDs 'lat' and 'lon'. It prepares the data to be sent in the AJAX request, including the latitude, longitude, start hour, and end hour. It sets up the URL for the Flask app's endpoint. Then, it fetches the weather forecast from the Flask app using the POST method and JSON data. If the response is successful, it updates the forecast and displays any associated photo in the appropriate HTML elements. If there is an error, it displays an error message.
3.	handleButtonClick(): This function is called when the 'Get My Hair Forecast' button is clicked. It retrieves the start and end hours from a slider, logs them, and calls the fetchWeatherForecast function with the start and end hour values.
4.	Event listener: This event listener waits for the DOM to finish loading. Once loaded, it adds a click event listener to the 'Get My Hair Forecast' button, calling the handleButtonClick function when clicked.
In summary, the code allows the user to fetch the weather forecast based on their GPS coordinates and a specified time period. When the 'Get My Hair Forecast' button is clicked, the start and end hours are retrieved from the slider, and the fetchWeatherForecast function is called to fetch and display the weather forecast.


 
Firewall & Other Tools
Firewall (UFW) 
The server uses a firewall to limit the rate of incoming connections to the SSH port. UFW is the program
1.	If it needs to be reinstalled: sudo apt install ufw
2.	It can be enabled with sudo ufw enable
3.	By default it blocks all SSH incoming connections and allows all outgoing. To allow incoming connections: sudo ufw allow ssh
4.	To check the status of ufw, sudo ufw status verbose
5.	To open a port on uft, sudo ufw allow 22
6.	To deny connections on uft, sudo ufw deny 22
7.	This will prevent all connections including Putty

Allowing SSH access to your server from the internet can be a security risk. Ensure that you're following best practices for securing SSH, such as using key-based authentication, disallowing root login, and potentially using a non-standard port.

Key-based authentication has been used. My identification has been saved in C:\Users\matta/.ssh/id_rsa.
Your public key has been saved in C:\Users\matta/.ssh/id_rsa.pub.
The key fingerprint is:
[ommited for security reasons]

2.	Fail2Ban: Fail2Ban is a tool that can automatically update firewall rules to ban IP addresses that make too many failed login attempts. 
1.	If it needs to be reinstalled: sudo apt install fail2ban
2.	To start and enable it: sudo systemctl start fail2ban and sudo systemctl enable fail2ban
3.	Because of attempts to guess the login password (server might be under a brute-force attack, where an attacker is trying to guess your root password), the root login has been disabled. 
1.	To change this, edit the SSH config file: sudo nano /etc/ssh/sshd_config
2.	Find the line that says PermitRootLogin and it was changed to no. If the line doesn't exist, you can add it to the file. Then save and exit the file.
3.	Then, restart SSHD: sudo systemctl restart ssh
We created a new user with sudo privileges before disabling root login, and tested logging in as this user in a new terminal session before closing the current one. The new user is matt0164.
These steps should help increase the security of your server and might alleviate the load that these failed login attempts are putting on your server, allowing you to restart Nginx and check its status.

Virtual Environment
A virtual environment is an isolated environment where you can install Python packages without interfering with packages installed in other environments or the system's global Python environment. This can be especially useful when different projects require different versions of the same package.

To start using a virtual environment, you have to activate it. You can do that using the following command:

1.	Activate the virtual environment: source /var/www/frizz/venv/bin/activate
Here is how to create a new virtual environment:
1.	Navigate to your project directory (e.g., /var/www/frizz).
2.	Create a new virtual environment: python3 -m venv venv
3.	This will create a new directory named venv in the current directory.
After doing this, the correct path for the Environment directive should be /var/www/frizz/venv/bin.
Also, please note that in the ExecStart directive, the Gunicorn executable is being referenced from /usr/local/bin/gunicorn. However, when using a virtual environment, Gunicorn should be installed in the virtual environment and the path should be the one inside the virtual environment. So it should be something like /var/www/frizz/venv/bin/gunicorn.
If you need to re-install gunicorn, it should be done within the virtual environment using the following command:
1.	Create a new virtual environment
python3 -m venv /path/to/new/virtual/environment
2.	Install Gunicorn: 
pip install gunicorn

 
The Algorithm
1.	Determining the Forecast Period:
•	By default, the program will provide a weather forecast for the 'upcoming day' based on the time the user checks the app.
•	The app will provide a forecast from 10 AM that day to 3 PM of the same day.
•	Future version of the program will also provide a 48-hour forecast, allowing users to select a different day or time period and visualize the weather conditions during the upcoming day.
2.	Highlighting Critical Periods:
•	The app will analyze the forecast data for the next 24 (and 72 hours in future versions) to identify any 'critical periods' - times when humidity or dew point (and later wind speed) will be extremely high or low.
•	Users will be notified about these critical periods, which can help them plan their hair care and styling accordingly.
3.	Weekly Snapshot (future versions):
•	In addition to the daily forecast, the app will provide a snapshot for the next 5 to 7 days.
•	This snapshot will highlight any particularly good or bad days for certain hairstyles based on the expected humidity and wind speed.
•	For example, it could tell a user "next Tuesday will be a great day for straight hair" or "next Thursday will be a very tough day for straight hair due to high humidity and wind speeds".
4.	User-Centric Customizations (future versions):
•	Users can adjust their 'hair check' times according to their routine, enabling the app to provide a more personalized forecast.
•	Based on the forecast and the user's specified schedule, the app will offer custom recommendations on the optimal hair care/styling for that day.
 
Quick tasks
1.	To switch to the main directory
cd /var/www/frizz
2.	To activate the virtual environment
source /var/www/frizz/venv/bin/activate
3.	To edit the service file that starts gunicorn
sudo nano /etc/systemd/system/frizzapp.service
4.	To restart the gunicorn frizz.service
sudo systemctl restart frizzapp.service
5.	To check the status of the service to ensure it's running in bash: 
sudo systemctl status frizzapp.service
6.	To review the status of the gunicorn service
sudo journalctl -u frizzapp.service --since "2 minutes ago"
7.	To edit nginx config
sudo nano /etc/nginx/sites-available/default
8.	To restart ngnix and test its status
sudo systemctl restart nginx
sudo nginx -t
9.	To clone the latest branch from Github
cd /var/www/frizz
git clone git@github.com:matt0164/frizz.git
git fetch origin
git reset --hard origin/latest

DO NOT USE: git clone -b latest git@github.com:matt0164/frizz.git

10.	To check that files were updated (replace filename)
ls -l --time=status web_app.py

 
Configuration & Troubleshooting
Gunicorn
Gunicorn is installed on the server (using sudo pip3 install gunicorn)
in the following path /usr/local/bin/gunicorn (to check, run which gunicorn)

To test Gunicorn :

1.	Activate the virtual environment: 

source /var/www/frizz/venv/bin/activate

2.	Navigate to the project directory:
cd /var/www/frizz/

3.	Test gunicorn
gunicorn wsgi:app 
note: leave off the .py when running web_app using gunicorn


Gunicorn should run and show some output like this:
[2023-05-17 08:27:27 +0000] [42262] [INFO] Starting gunicorn 20.1.0
[2023-05-17 08:27:27 +0000] [42262] [INFO] Listening at: http://127.0.0.1:8000 (42262)
[2023-05-17 08:27:27 +0000] [42262] [INFO] Using worker: sync
[2023-05-17 08:27:27 +0000] [42263] [INFO] Booting worker with pid: 42263

If there are errors, it can often be the following:
1.	Permission errors to ensure that Gunicorn can log errors. If you get this, change the ownership of the directory and the file to:
sudo chown frizzwizceo:frizzwizceo /var/www/frizz/logs -R

This command will recursively (-R) change the ownership of the directory /var/www/frizz/logs and its contents to the user frizzwizceo and the group frizzwizceo. Now try starting your Gunicorn process again.
2.	When you run the system process, sometimes the system can't find Gunicorn at the specified location /var/www/frizz/venv/bin/gunicorn

Here are a few troubleshooting steps:
A.	Ensure that the virtual environment has been activated before running Gunicorn. If it hasn't been, then Gunicorn might not be available in the shell's PATH.
B.	Verify that Gunicorn is installed in the virtual environment. You can do this by activating the virtual environment and running which gunicorn:
This command will print the path to the Gunicorn executable if it's installed.
If Gunicorn is not installed, you can install it using pip within your virtual environment:
source /var/www/frizz/venv/bin/activate pip install gunicorn 

C.	If Gunicorn is installed but the path is different from what's in the frizzapp.service file, then you'll need to update the service file with the correct path.
You can edit the frizzapp.service file using a text editor like nano:
sudo nano /etc/systemd/system/frizzapp.service 
In the file, change the path in the line that starts with ExecStart to match the path returned by the which gunicorn command, then save and exit the file. After this, reload the systemd daemon and restart your service:
sudo systemctl daemon-reload sudo systemctl restart frizzapp.service 

D.	Make sure the permissions on the venv directory allow the frizzwizceo user to read and execute files. You can ensure this with the following command:

sudo chmod -R 755 /var/www/frizz/venv 
This command will recursively (-R) change the permissions of the directory /var/www/frizz/venv and its contents to allow read, write, and execute permissions for the owner, and read and execute permissions for the group and others.
3.	The error Connection in use: ('127.0.0.1', 8000) indicates that the port 8000 is currently being used by another process.
a.	You can use the following command to find out what process is using port 8000:
sudo lsof -i :8000

b.	This command will show you a list of all processes using the port. The output will look something like this:

COMMAND     PID        USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
gunicorn 138412 frizzwizceo    5u  IPv4 1515041      0t0  TCP localhost:8000 (LISTEN)
gunicorn 138413 frizzwizceo    5u  IPv4 1515041      0t0  TCP localhost:8000 (LISTEN)

c.	In this output, the second column (PID) shows the process ID of the process that's using the port. You can stop this process using the kill command and the PID:

sudo kill -9 <PID>

Replace <PID> with the process ID from the output of the lsof command.
After killing the process, try restarting the frizzapp.service again.


You can paste any errors into Chat GPT to troubleshoot further.

1.	you can stop it with Ctrl+C and proceed to the next step.
2.	Create a Gunicorn systemd Service File: We have created a systemd service file to start and manage the Gunicorn process. First, we created the file:

To edit the Gunicorn system file, 

SSH:
sudo nano /etc/systemd/system/frizzapp.service 

This file should contain the following:

[Unit]
Description=Gunicorn instance to serve frizzapp
After=network.target

[Service]
User=frizzwizceo
Group=www-data
WorkingDirectory=/var/www/frizz/
Environment="PATH=/var/www/frizz/venv/bin/"
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 wsgi:app --access-logfile '-' --error-logfile '-'

[Install]
WantedBy=multi-user.target

If you make any changes, run:
sudo systemctl daemon-reload
sudo systemctl restart frizzapp.service 
Then check the status of the service:
sudo systemctl status frizzapp.service
To stop any running Gunicorn and Nginx processes, you can use the following commands. Note that you'll need to have superuser privileges to run these commands, which usually means you'll need to include sudo at the beginning of each command.
sudo systemctl stop frizz.service
sudo systemctl stop nginx
Once you've stopped these services, you can check the status of the ports to see if they're ready to listen. You can use the ss command to do this:
sudo ss -tuln
The command options -tuln are for:
•	t: TCP ports
•	u: UDP ports
•	l: only services which are listening on some port
•	n: show port number, don't try to resolve the service name
After you run this command, you should see a list of ports and the services that are using them. Look for ports 80 and 8000, they should be free now that we have stopped Nginx and Gunicorn.
Check the service file by opening it in nano:
sudo nano  /etc/systemd/system/frizzapp.service
A backup of this file will contain the correct configuration (see page 18)
Then activate the virtual environement
If you need to make any changes, reload the system daemon to apply the changes and restart and check the service.
 
Nginx
Basic Guide to Nginx Configuration
1.	Understand Nginx Configuration File Structure: Nginx configuration files are typically stored in /etc/nginx. Here are the key files and directories:
•	nginx.conf: This is the main Nginx configuration file.
•	sites-available: This directory contains configuration files for each server block (i.e., website) you want to host.
•	sites-enabled: This directory contains links to the configuration files for the server blocks (websites) you want to enable.
•	conf.d: This directory is used to store additional configuration files.
•	mime.types: This file maps file extensions to their MIME type.
2.	Edit Configuration Files: The configuration files can be edited using any text editor such as nano, vim, etc. Always use 'sudo' to ensure you have the necessary permissions.
sudo nano /etc/nginx/sites-available/default
3.	Check Configuration for Errors: Always check your configuration for any errors before you try to restart or reload Nginx. You can do this using the -t flag:
sudo nginx -t
If there are no errors, you should see the message "configuration file /etc/nginx/nginx.conf test is successful".
4.	Apply Configuration Changes: After editing the configuration and checking for errors, you need to reload or restart Nginx to apply the changes. This can be done using the systemctl command:
sudo systemctl reload nginx
or
sudo systemctl restart nginx
Troubleshooting Common Nginx Configuration Issues
1.	403 Forbidden Error: This usually indicates a permissions problem. Check that Nginx has read access to the files and directories in your website's root directory. Also, ensure that the directory itself is executable.
2.	502 Bad Gateway Error: This error can occur if Nginx is unable to communicate with your Flask app or any other upstream server it's proxying requests to. Check that your upstream servers are running and that the proxy settings in your Nginx configuration are correct.
3.	"Failed to read PID from file" Error: This error can occur if Nginx is unable to write to the PID file specified in your nginx.conf file. Check that the directory where the PID file is located exists and that Nginx has write access to it.
4.	Changes Not Applied: If you made changes to your configuration and they don't seem to be applied, check that you edited the correct configuration file and that you reloaded or restarted Nginx afterwards. Also, use sudo nginx -t to check for syntax errors in your configuration files.
5.	Nginx Doesn't Start After Reboot: This can happen if Nginx isn't enabled to start at boot. You can fix this by running sudo systemctl enable nginx.
6.	Check Nginx/Aplication Logs: When encountering issues, checking Nginx logs (/var/log/nginx/error.log or /var/log/nginx/access.log) and your application logs could provide useful insight into the cause of the issue.
Remember to keep backups of your original configuration files before making any changes, as it can help revert any undesired changes. Always test new configuration files before applying them.
 
Frizz App Nginx Configuration
The Nginx configuration for the application is stored in the file /etc/nginx/sites-available/default and /etc/nginx/nginx.conf. The file has include statements that also reference /etc/nginx/mime.types; /etc/nginx/conf.d/*.conf; and /etc/nginx/sites-enabled/*; These configuration files specify how incoming HTTP requests are handled by the server.
The server listens on port 80, and it is configured to proxy requests to the application running on localhost (127.0.0.1) port 8000. It also includes headers to provide information about the original client request, as it proxies the request to the application.
The server is also configured to serve the directory /.well-known/acme-challenge/ from /var/www/html, which is used for the Let's Encrypt SSL certificate verification process.
The nginx config file should contain the following:
server {
    listen 80;
    server_name app.frizz-wiz.com;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name app.frizz-wiz.com;

    ssl_certificate /etc/letsencrypt/live/app.frizz-wiz.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.frizz-wiz.com/privkey.pem;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/frizz/frizz.sock;
    }
    
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/frizz;
    }
}  
Changing the Configuration
If you need to change the server configuration, edit the file /etc/nginx/sites-available/default with a text editor (like nano or vim). See the section called nginx config for the current/correct config. You'll need sudo privileges to edit this file. After making changes, save the file and exit the text editor.
sudo nano /etc/nginx/sites-available/default
Next, test the new configuration by running sudo nginx -t. If this command reports that the configuration is okay, reload the Nginx configuration by running sudo systemctl reload nginx.
To view the error log in nginx, you can 
1.	Open SSH log in and enter this command:
sudo nano /var/log/nginx/error.log


SSL Certificate
The application uses an SSL certificate to secure connections. This certificate is provided by Let's Encrypt, a free, automated, and open certificate authority. The certificate needs to be renewed every 90 days.
If you encounter any issues while renewing the certificate or if the SSL certificate was purchased from a different provider (like GoDaddy), follow the certificate provider's instructions for renewal and installation.
Location of key files:
frizz_landing.html 	/var/www/frizz/web_app/templates
The code can be updated via Git using a public/private key. The key is saved in /home/frizzwizceo/.ssh/id_rsa as first-key.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDC1UTLqblrHtgdLm4tNACjaOIg5dHR90ek3OleYn3>

 
Encapsulated Summary (for ChatGPT – requires update)
Frizz-Wiz is a web application running on an Nginx server. The application is configured to be accessible from the internet via the domain names frizz-wiz.com and www.frizz-wiz.com.
Nginx Configuration is stored in the file /etc/nginx/sites-available/default and /etc/nginx/nginx.conf. The file has include statements that also reference /etc/nginx/mime.types; /etc/nginx/conf.d/*.conf; and /etc/nginx/sites-enabled/*; These configuration files specify how incoming HTTP requests are handled by the server. The server listens on port 80, and it is configured to proxy requests to the application running on localhost (127.0.0.1) port 8000. It also includes headers to provide information about the original client request, as it proxies the request to the application. The server is also configured to serve the directory /.well-known/acme-challenge/ from /var/www/html, which is used for the Let's Encrypt SSL certificate verification process.

My flask web_app
Various Python scripts are used in the Frizz Wiz application to handle different tasks. These scripts include functions for retrieving weather data, geolocation information, and generating random colors. They interact with external APIs, such as OpenWeatherMap and IPinfo, to fetch weather data and geolocation details. The scripts are called by the Flask application to provide the necessary data for rendering the web pages.
The HTML templates define the structure and content of the web pages displayed to users. They utilize template engines, such as Jinja2, to dynamically insert data retrieved from the Python scripts. The templates include forms for user input, display weather results, and render appropriate images based on weather conditions. JavaScript is also used to handle geolocation functionality and make AJAX requests to the server.
The Flask application is the core of the Frizz Wiz web server. The application interacts with the Gunicorn server to serve the web pages to clients. Gunicorn is responsible for running the Flask application as a web server.  By combining these components, the Frizz Wiz application functions as a web server that receives user input, retrieves weather data, and dynamically renders HTML pages with the corresponding information. 

The project is saved locally at C:/Users/matta/PycharmProjects/frizz/
The project is served from my GoDaddy VPS server with an IP address is 186.184.30.145
I am running Ubuntu 22.04 and the project is served from /var/www/frizz

Nginx is installed in /usr/sbin/nginx /usr/lib/nginx /etc/nginx /usr/share/nginx /usr/share/man/man8/nginx.8.gz
Gunicorn is installed in /var/www/frizz/
My systemmd service file for gunicorn should be: /etc/systemd/system/frizz.service 
My nginx error log is in /var/log/nginx/error.log
The application uses an SSL certificate to secure connections. This certificate is provided by Let's Encrypt
Location of key files:
frizz_landing.html 	/var/www/frizz/web_app/templates
My code can be updated via Git using a public/private key. The key is saved in /home/frizzwizceo/.ssh/id_rsa as first-key.pub and the key is:
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDC1UTLqblrHtgdLm4tNACjaOIg5dHR90ek3OleYn3>

1.	web_app.py: This Python file serves as the entry point for the Flask application. It imports the necessary modules, sets up the Flask app, defines the routes, and handles the logic for retrieving weather data based on zip code or location. The routes interact with the HTML templates by rendering them and passing data from the Python scripts to be displayed dynamically. Additionally, it interacts with the JavaScript file location.js by receiving geolocation data via AJAX requests and triggering a page reload after processing.
2.	web_main.py: This Python file contains functions for fetching weather data from external APIs based on zip codes, location coordinates, or city names. The get_weather_by_zip() function retrieves weather data using the OpenWeatherMap API and performs calculations to determine if it's a good or bad hair day. The get_weather_by_lat_lng() function does the same but uses latitude and longitude coordinates. These functions return the weather result and photo URL to be displayed in the HTML templates.
3. 	wsgi.py: This Python file is the entry point for the application when it's run with a WSGI server like Gunicorn. It imports the Flask application instance (app) from the web_app module. This app is expected to be a Flask instance. It checks if this script is being run directly or being imported. The code inside this block runs only when the script is run directly. It starts the Flask's built-in development server. 
4.	location.js: This JavaScript file is responsible for handling geolocation functionality in the web page. It checks if the browser supports geolocation and, if so, retrieves the current latitude and longitude coordinates. It then sends this data to the server using an AJAX request to the /location route. Upon receiving a successful response (status code 200), it triggers a page reload to display the updated weather information. This file connects with the Python script web_app.py through the AJAX request and response handling.
5.	frizz_landing.html: This HTML template is the main page of the Frizz Wiz application. It includes a form where users can enter a zip code or click a button to use geolocation. The form submits a POST request to the / route in the Flask application. It also includes placeholders for displaying the weather result, photo, and dynamically generated colors. The template interacts with the Python script web_app.py by receiving the weather result and photo data to be rendered in the appropriate sections.
