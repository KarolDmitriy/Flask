import export as export
from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm
from models import User, db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the Registration Form App!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.cli.command("init-db")
def init_db():
    db.create_all()
print('OK')


if __name__ == '__main__':
    app.run(debug=True)
