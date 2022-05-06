# FastAPI with Google Oauth Login

The objective of this repo is to help developers who need to add the Login with Google functionality to their app.

There are some environment variables needed in order to make the app working, use the .env.example as a template. (rename it to .env and set the values).

To create the Oauth variables (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET), follow the next steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/home/dashboard)

2. Select the option to [create a new Project](https://console.cloud.google.com/projectcreate)

3. Go to Credentials on side panel or click [here](https://console.cloud.google.com/apis/credentials)

4. Go to Create Credentials -> OAuth client ID

5. Set the "User type" to "External"

6. Set up the App Name and Support Email, the Logo is optional

7. On the "Scopes" screen, select userinfo.email, userinfo.profile, openid -> Save and continue.

8. On the "Test Users" screen, add your email as a test user to start testing the application.

9. After the consent screen is ready we can finally create the OAuth client id. So we go to Credentials -> Create Credentials -> OAuth client ID

10. Set up the OAuth client ID:

  - Application Type: Web Application
  - Name: Choose a nice name for your app
  - Authorized JavaScript origins: http://localhost:8000
  - Authorized redirect URIs: http://localhost:8000/callback (This endpoint is on our main.py file)

** OBS: These urls should be modified to allow requests from your domain when the app is hosted in a server

After creating the client, a modal with your client ID and client secret will appear, copy these information to your .env file

Now you can run your app with the command: `uvicorn main.app --reload`

