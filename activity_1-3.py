from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
from datetime import datetime, timezone
from flask_moment import Moment 

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.now(timezone.utc))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', 
                           name=name,
                           current_time=datetime.now(timezone.utc))


# app.add_url_rule('/', 'index', index)

# if __name__ == '__main__':
#     app.run()