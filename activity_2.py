from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField(
        'What is your UofT Email address?', validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'toodalooo'

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        # Check name changes
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        # Check email changes
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        # Validate UofT domain on submitted email
        if 'utoronto' not in form.email.data:
            flash('Please fill in a UofT Email!!')
        else:
            session['name'] = form.name.data
            session['email'] = form.email.data

        return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email'),
    )


@app.route('/user/<name>')
def user(name):
    return render_template(
        'user.html', name=name, current_time=datetime.now(timezone.utc)
    )


if __name__ == '__main__':
    app.run(debug=True)