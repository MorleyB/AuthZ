# AuthZ
===
A small app to demonstrate the Auth Code Grant (RFC 6749 section 4)

Resources
===
https://www.oauth.com/playground/authorization-code.html
https://developer.okta.com/docs/guides/implement-grant-type/authcode/main/
https://datatracker.ietf.org/doc/html/rfc6749


Grant-Type Flow
===

The browser hits the /login route and the app server sends a request to Okta.


Okta redirects the user to it's authentication url.


Upon successful authentication, Okta will redirect the user to the app server's callback route, where the server will request tokens and then use the token to request the user's Okta profile.


The profile page is a restricted resource.




Dev Installation
===
Activate virtual environment
`source env/bin/activate`

Install packages
`pip install -r requirements.txt`

Configure application secrets
`cp .env.example .env`
- Create Otaku Developer Account
- Update OKTA_DOMAIN, CLIENT_ID, CLIENT_SECRET in the .env file
- Create a random & secret key
`import uuid`
` uuid.uuid4().hex`

Run application
===
`python app.py`
