from AppManager import Manager
from lib.other.ClickUpAPI import ClickUp
from lib.other.LocalmetricManager import Localmetric
from credentials.config import Config
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle




def getCredentials(config):
    creds = None
    if os.path.exists(config.TokenPath):
        with open(config.TokenPath, 'rb') as token:
            creds = pickle.load(token)    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(config.CredentialsPath, config.Scopes)
            creds = flow.run_local_server(port=0)
        with open(config.TokenPath, 'wb') as token:
            pickle.dump(creds, token)
    return creds

settings = Config()
creds = getCredentials(settings)

manager = Manager(
    Localmetric(settings, creds),
    ClickUp(settings),
)