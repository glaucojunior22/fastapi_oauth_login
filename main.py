import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from starlette.config import Config
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

load_dotenv()

app = FastAPI()

# Middleware
SECRET_KEY = os.getenv('SECRET_KEY', 'my_super_secret_key')
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise BaseException('Missing environment variables!')

config_data = {
    'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
metadata_url = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=metadata_url,
    client_kwargs={'scope': 'openid email profile'}, # scopes selected on GCP
)


@app.get('/', response_class=HTMLResponse)
def index():
    return '<h1>Index Page</h1><div><a href=/login>Login</a></div>'


@app.route('/login')
async def login(request: Request):
    # This creates the url for the /callback endpoint
    redirect_uri = request.url_for('callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/callback')
async def callback(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    request.session['user'] = dict(access_token['userinfo'])
    return RedirectResponse(url='/restricted')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.get('/restricted', response_class=HTMLResponse)
def restricted(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        email = user.get('email')
        return f'<p>Hello {name} ({email})!</p><a href=/logout>Logout</a>'
    return RedirectResponse(url='/')