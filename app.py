from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





# Dashboard Route
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Settings Route
@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'POST':
        # Logic to update user settings can go here
        pass
    return render_template('setting.html')



if __name__ == '__main__':
    app.run(debug=True)
