# smts Backend

Here all data handling happens. The backend of the "Wheres My Thief" consists of a main.py, which is the main program, and the models *users* and *devices*.

## Installation
 
If you want to install the backend server as standalone follow the steps:

1. Make sure you have recent version of Python and MongoDB installed on your machine.
2. Clone the repository, open a console and cd into this directory.
3. In the console run the command 
```
python -m pip install -r requirements.txt 
```
4. Now set your environment variables *FLASK_APP* to the main program
```
export FLASK_APP=main.py
```

## Usage
Run the flask server, a port can be specified because default is 0.0.0.0
```
flask run --port=8008
``
