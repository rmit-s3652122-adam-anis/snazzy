# snazzy
RMIT Programming Project by Geek Bank group.
Snazzy is an e-commerce website focusing on marketing apparels.

How to get started:
1. Install the latest python 3 from https://www.python.org/downloads/
    
    For Windows Users:
        - Ensure python is added into environment path. Refer https://www.howtogeek.com/197947/how-to-install-python-on-windows/

2. Install PostgreSQL from https://www.postgresql.org/download/. Once installed, open pgAdmin(or other similar GUI) and create a new database called "snazzydb"

    For Windows Users: 
        - refer http://www.postgresqltutorial.com/install-postgresql/
        
3. (Optional) Once python 3 has successfully installed, install virtualenv package using pip. Then, create a virtualenv inside the working directory (/snazzy) called "snazzyenv" and use the virtualenv. Refer https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

4. Using terminal, inside the working directory (/snazzy) run the command line : pip install -r requirements.txt

5. Test if able to run the website. Using terminal, inside the site folder (snazzysite) run the command lines: 
python manage.py migrate (to update website settings)
python manage.py runserver (to run our website)

Any issues, please contact email address below:
s3652122@student.rmit.edu.au
