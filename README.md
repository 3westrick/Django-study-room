# Django-study-room
This is an web application based on Django.

<img width="1252" alt="room" src="https://github.com/3westrick/Django-study-room/assets/109426803/00027ab3-977b-4845-8f56-b432dcb7347d">

## Installation
first create a main folder and another folder by the name "mysite" inside the main folder.
then open the terminal and go to the main folder.<br>
move the <strong>requirements.txt</strong> file to the main folder<br>
now we need a Virtual environment to install python packages.

```bash
python -m venv env
```
now to activate the environment (on mac)
```bash
source env/bin/activate
```
You should see "(env)" in your terminal, at the beginning of the line.<br>
Next use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements for backend.
```bash
pip install -r requirements.txt
```
And finally enter the main folder and run the server
```bash
python mysite/manage.py runserver
```
it should run on 127.0.0.1:8000<br>
<strong>DO NOT CLOSE THE TERMINAL</strong>
