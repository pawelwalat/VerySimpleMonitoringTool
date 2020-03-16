Very Simple Monitoring Tool (VSMT)
========================

This is a tool for simple monitoring activities.

---------------
1. Purpose
Very Simple Monitoring Tool (VSMT) is home made tool to monitor various systems like IoT, Internet connection, websites.

2. OS and requirements
This tool will work on Linux OS only.
The main reason is that it is extendly using linux command line tools like 'ping' and this behavior on windows is different.
Other requirements are stored in the requirements.txt file.

3. How it works

Sensors - is a base object in the VSMT. Handles monitoring activities like ping, ssh connection, http request etc.
Availabe sensor types:
- ping

Database - Stores logs of sensors activities. As for now only SQLite database is available.

Notification - 
