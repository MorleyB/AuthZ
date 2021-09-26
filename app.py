import os
from flask import Flask
from flask import render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from dotenv import dotenv_values
import requests
from models.user import User

config = dotenv_values(".env")  # load environment variables from .env.
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    # get request params
    query_params = {'client_id': config.get('CLIENT_ID'),
                    'redirect_uri': config.get('REDIRECT_URI'),
                    'scope': "openid",
                    'state': config.get('APP_STATE'),
                    'nonce': config.get('NONCE'),
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request
    request_uri = "{base_url}?{query_params}".format(
        base_url=config.get('AUTH_URI'),
        query_params=requests.compat.urlencode(query_params)
    )

    # STEP 1: Redirect to the Okta sign-in page
    return redirect(request_uri)


@app.route('/authorization-code/callback')
def callback():
    try:
        # STEP 4: Okta passes the authorization code back to the app
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        ##### Validate response
        # Check for CSRF
        # breakpoint()
        code = request.args.get("code")
        if not code:
            message = 'The code was not returned or is not accessible'
            redirect(url_for('error', message=message))

        # STEP 5 & 6: Get & Receive Okta tokens
        access_token, id_token = get_tokens(request.base_url, code)
    
        # Step 7: Call Okta for user profile
        user_data = get_user_data(access_token)

        # login user
        # use flask-login to manage user session
        user = get_or_create_user(user_data)
        login_user(user)

        # Step 8: redirect to protected user profile
        return redirect(url_for("profile"))
    except Exception as e:
        print('Exception Thrown: ', e)
        return redirect(url_for('error', message=e))


def get_or_create_user(data):
    # In memory user, no db
    unique_id = data.get('sub')

    user = User(**data)

    if not User.get(unique_id):
        User.create(**data)

    return user


def get_user_data(access_token):
    response = requests.get(
        config.get('USERINFO_URI'), 
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()
    return response


def get_tokens(base_url, code):
    query_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': base_url,
    }
    query_params = requests.compat.urlencode(query_params)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    tokens = requests.post(
        config.get('TOKEN_URI'),
        headers=headers,
        data=query_params,
        auth=(config.get('CLIENT_ID'), config.get('CLIENT_SECRET'))
    ).json()

    access_token = tokens['access_token']
    id_token = tokens['id_token']
    return access_token, id_token


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/error")
def error():
    message = request.args.get('message')
    return render_template("error.html", message=message)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)