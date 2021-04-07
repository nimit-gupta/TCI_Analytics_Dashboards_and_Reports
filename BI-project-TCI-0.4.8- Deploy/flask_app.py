from flask import Flask, redirect, render_template

flask_app = Flask(__name__, template_folder='template', static_folder = 'static')

@flask_app.route('/')
def index():
   return render_template('index.html')

