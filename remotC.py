"""remote controller for presentation."""
from flask import Flask, render_template, request, redirect
from pykeyboard import PyKeyboard
import os

app = Flask(__name__)
k = PyKeyboard()


@app.route('/', methods=['POST', 'GET'])
def index():
    """index."""
    if request.method == "POST":
        action = request.form.get('key')
        if action:
            if action == "F5":
                key = k.function_keys[5]
            elif action == "page_down":
                key = k.page_down_key
            elif action == "page_up":
                key = k.page_up_key
            elif action == "Esc":
                key = k.escape_key
            k.press_key(key)
            k.release_key(key)
    return render_template('index.html')


@app.route('/file_manager', methods=['POST', 'GET'])
def file_manager():
    """openfile view."""
    pwd = request.args.get('path', os.getcwd())
    print pwd
    pwd = os.path.realpath(pwd)
    pr_pwd = os.path.realpath(os.path.join(pwd, '..'))
    print pwd
    dir_list = os.listdir(pwd)
    print dir_list
    dir_dict = {
        'pr_pwd': pr_pwd,
        'files': [],
        'dirs': []
    }
    for item in dir_list:
        if item.startswith('.'):
            continue
        path = os.path.join(pwd, item)
        if os.path.isfile(path):
            dir_dict['files'].append((path, item))
        elif os.path.isdir(path):
            dir_dict['dirs'].append((path, item))
    if request.method == "POST":
        action = request.form.get('filename')
        apps = request.form.get('apps')
        if action:
            os.system('export DISPLAY=":0";{} {}&'.format(apps, action))
            return redirect('/')
    return render_template('file_manager.html', **dir_dict)


@app.route('/open_file', methods=['POST', 'GET'])
def openfile():
    """open file."""
    file_name = request.args.get('path')
    if request.method == "POST":
        apps = request.form.get('apps')
        if file_name:
            os.system('export DISPLAY=":0";{} "{}"&'.format(apps, file_name))
            return redirect('/')
    return render_template('openfile.html', file_name=file_name)


app.run(host="0.0.0.0")
