#Output a list of installed packages and their versions
pip freeze > requirements.txt

#Install dependencies
pip install -r requirements.txt