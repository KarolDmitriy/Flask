from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('user_data', f'{name}:{email}')
        return resp
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    user_data = request.cookies.get('user_data')
    if user_data:
        name, _ = user_data.split(':')
        return render_template('welcome.html', name=name)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('user_data')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
