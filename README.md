# snazzy

VISIT OUR WEBSITE AT:
http://ec2-13-211-252-85.ap-southeast-2.compute.amazonaws.com:8000/

RMIT Programming Project by Geek Bank group.
Snazzy is an e-commerce website focusing on marketing apparels.

Github repository url: https://github.com/rmit-s3652122-adam-anis/snazzy

Below are the instructions for contributors to set up the project environment
NOTE: project is still in development phase with various cloud service integrated using private keys. 
Please contact email s3652122@student.rmit.edu.au to attain the list of keys used to set up the project environment later on at step 5 and 6

How to get get started:
1. Install the latest python 3 from https://www.python.org/downloads/
    
    For Windows Users:
        - Ensure python is added into environment path. Refer https://www.howtogeek.com/197947/how-to-install-python-on-windows/

2. Install PostgreSQL from https://www.postgresql.org/download/. Once installed, open pgAdmin(or other similar GUI) and create a new database called "snazzydb"

    For Windows Users: 
        - refer http://www.postgresqltutorial.com/install-postgresql/
        
3. (Optional) Once python 3 has successfully installed, install virtualenv package using pip. Then, create a virtualenv inside the working directory (/snazzy) called "snazzyenv" and use the virtualenv. Refer https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

4. Using terminal, inside the working directory (/snazzy) run the command line : 
windows:
pip install -r requirements.txt
mac/linux:
pip install -r requirements_mac.txt

5. This project used google cloud sql to manage the database. If desired to connect to own local database, refer the most upvote answer in https://stackoverflow.com/questions/5394331/how-to-set-up-a-postgresql-database-in-django on configuring the database. However, to connect to the google cloud sql database locally:
    1. email s3652122@student.rmit.edu.au to attain access to the project cloud (Google Cloud)
    2. refer to https://cloud.google.com/sql/docs/postgres/quickstart-proxy-test to set up proxy server to connect to the cloud database

6. This project used google cloud services and requires private access keys and key files, to set up:
    1. email s3652122@student.rmit.edu.au to attain access keys and key files
    2. (for windows machine only) using terminal, navigate inside the snazzysite folder (snazzy/snazzysite), run command python manage.py runserver, it will prompt user to input secret key values of the environment. Input the access key values/key file directory path as prompted
    3. (for mac/linux machine only) You have to set up the credentials which are access keys and key files into the os environment variables. Users can refer to this website for guidelines how to do:
        https://askubuntu.com/questions/58814/how-do-i-add-environment-variables
    OR users can simply follow these steps:
        1. Navigate to the bin file in the virtual environment (snazzyenv/bin/)
        2. add the following 2 lines of code inside the activate file:-
            GOOGLE_APPLICATION_CREDENTIALS = filepath
            export GOOGLE_APPLICATION_CREDENTIALS
    4. go and edit snazzysite/snazzysite/settings.py file at line 187 to 191. There listed whether a user is using a windows machine or mac/linux machine. Uncomment line 189 if using a windows machine. Else, uncomment line 191 if using a linux/mac machine

6. Test if able to run the website. Using terminal, inside the site folder (snazzysite) run the command lines: 
python manage.py migrate (to update website settings)
python manage.py createsuperuser (everytime a new database is created, need to add a new superuser/admin)
python manage.py runserver (to run our website)

Any issues, please contact email address below:
s3652122@student.rmit.edu.au
