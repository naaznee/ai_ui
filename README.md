# Age, Gender and Ethnicity Estimation in Facial Image Analysis

## Installation

Install this library in a virtualenv using pip. virtualenv is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.

### Supported Python Versions
Our client libraries are compatible with all current active and maintenance versions of Python.

Python >= 3.7

### Mac/Linux
```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install -r requirements-macos.txt
```
### Windows
```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install -r requirements.txt
```

## Run the application

After activating the virtualenv as instructed above you can run the following.
```
python3 main.py
```
This will run your application on port 5000
Open a browser and go to `http://127.0.0.1:5000` to access the main page.

## Next Steps
* You can add new models to the `models` folder and restart the application to see the results.
