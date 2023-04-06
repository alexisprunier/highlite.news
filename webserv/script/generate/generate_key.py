import os
from utils.config import PROJECT_PATH
import json
import google_auth_oauthlib.flow
import webbrowser


class GenerateKey:

    def run(self):

        CLIENT_SECRETS_FILE = os.path.join(PROJECT_PATH, "credentials", "client_secret.json")
        GOOGLE_CREDENTIALS_FILE = os.path.join(PROJECT_PATH, "credentials", "google_credentials.json")
        SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]

        f = open(CLIENT_SECRETS_FILE, "r")
        client_secret = f.read()
        f.close()

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPE)
        flow.redirect_uri = "http://localhost"

        user_authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt=None,
            login_hint='highlitedotnews@gmail.com'
        )

        webbrowser.open(user_authorization_url, new=0, autoraise=True)

        code = input()
        state = input()
        scope = input()
        url = input()

        credential_content = {
            "state": state,
            "code": code,
            "scope": scope
        }

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=credential_content['scope'],
            state=credential_content["state"]
        )
        flow.redirect_uri = "http://localhost"

        authorization_response = url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        temp = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'id_token': credentials.id_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': [credentials.scopes]
        }

        file_content = json.dumps(temp, indent=4)
        f = open(GOOGLE_CREDENTIALS_FILE, "w")
        f.write(file_content)
        f.close()
