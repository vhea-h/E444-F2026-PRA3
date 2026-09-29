import re
from datetime import datetime, timezone
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
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
app.config['SECRET_KEY'] = 'potato_totter_tater_tooter'

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        # Check any name changes
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        # Check email changes
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        # Validate UofT domain on submitted email
        if 'utoronto' not in form.email.data.lower():
            flash('Please fill in a UofT Email!!')
            return redirect(url_for('index'))

        # Store in session and redirect directly to chatbot
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('chat_page'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email'),
    )


# actual display page for the chat 
@app.route('/chat_page')
def chat_page():
    # Require name & email submission before accessing chatbot
    if not session.get('name') or not session.get('email'):
        flash('Please submit your name and UofT email first.')
        return redirect(url_for('index'))

    return render_template(
        'chat.html', name=session.get('name'), email=session.get('email')
    )

# specifically displays chat box 
@app.route('/chat', methods=['POST'])
def chat():
    # Check JSON payload exists
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    msg_lower = message.lower()

    # Initialize memory dictionary in session if not present
    if 'chat_memory' not in session:
        session['chat_memory'] = {}

    memory = session['chat_memory']

    # Detect user introducing their name (e.g., "My name is Alice")
    name_match = re.search(r'my name is\s+([a-zA-Z]+)', message, re.IGNORECASE)

    if name_match:
        extracted_name = name_match.group(1).capitalize()
        memory['user_name'] = extracted_name
        session.modified = True  # Tell Flask the session dictionary changed
        reply = f'Nice to meet you, {extracted_name}!'

    # Respond to "What is my name?"
    elif 'what is my name' in msg_lower or 'what\'s my name' in msg_lower:
        if 'user_name' in memory:
            reply = f"Your name is {memory['user_name']}."
        else:
            reply = "I don't know your name yet! You can tell me by saying 'My name is [Name]'."

    # greeting check
    elif 'hello' in msg_lower or 'hi' in msg_lower:
        reply = 'Hello!'

    # Default response
    else:
        reply = "I don't understand."

    return jsonify({'reply': reply})


@app.route('/logout')
def logout():
    # Clear session data to forget saved information :)
    session.clear()
    flash('You have been logged out and memory cleared.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)