import logging
from datetime import datetime

from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests import Timeout
from requests_oauthlib.oauth2_session import OAuth2Session

__author__ = 'Luis Maia <luis.maia@xfel.eu>'


# requests_oauthlib supports automatically *refreshing* a token, an OAuth
# feature that doesn't require going through the full flow again.
# The XFEL services don't seem to allow this, but because we are using
# the backend flow, with no user interaction, it's relatively easy to get
# a brand new token.
# We are borrowing the parent class' auto_refresh_kwargs attribute to use
# for this purpose. refresh_token is disabled to avoid confusion.
class AutoRenewingOAuthSession(OAuth2Session):
    """OAuth session which automatically gets a new token on expiry
    """

    def request(self, method, url, *args, **kwargs):
        try:
            return super().request(method, url, *args, **kwargs)
        except TokenExpiredError:
            self.fetch_token(**self.auto_refresh_kwargs)
            return super().request(method, url, *args, **kwargs)

    def refresh_token(self, *args, **kwargs):
        raise NotImplementedError(
            "Get a new token with fetch_token instead of refreshing it"
        )


class Oauth2ClientBackend(object):
    # Parameter that will store the session used to "invoke" the API's
    session = None

    # Number of retries allowed before deal with the consequences!
    timeout = 3
    max_retries = 3

    def __init__(self, client_id, client_secret, scope, token_url,
                 refresh_url=None, auth_url=None, session_token=None):

        self.client_secret = client_secret
        self.scope = scope
        self.token_url = token_url
        # These are not currently used:
        self.refresh_url = refresh_url
        self.auth_url = auth_url

        # Check if Certificate should be checked!
        cert_url = 'https://in.xfel.eu'
        self.ssl_verify = token_url.startswith(cert_url)

        self.fetch_token_kwargs = dict(
            token_url=self.token_url,
            client_secret=self.client_secret,
            timeout=self.timeout,
            verify=self.ssl_verify
        )

        # Configure client using "Backend Application Flow" Oauth 2.0 strategy
        self.client = BackendApplicationClient(client_id)

        # Negotiate with the server and obtains a valid session_token
        # after this self.session can be used to 'invoke' API's
        self.auth_session(session_token=session_token)

    def auth_session(self, session_token=None):
        # If a session token was passed in & it's still valid,
        # create a session using it.
        if self.is_session_token_dt_valid(session_token):
            self._re_used_existing_session_token(session_token)

        # Otherwise, try to get a new session token.
        else:
            retries = self.max_retries
            while True:
                try:
                    logging.debug('Will try to create a new session token')
                    self._create_new_session_token()

                except Timeout:
                    logging.debug('Token request timed out', exc_info=True)
                    retries -= 1
                    if retries <= 0:
                        raise
                else:
                    logging.debug('Got a new session token successfully')
                    break

        return True

    def _re_used_existing_session_token(self, session_token):
        self.session = AutoRenewingOAuthSession(
            client=self.client,
            scope=self.scope,
            token=session_token,
            auto_refresh_kwargs=self.fetch_token_kwargs,
        )

    def _create_new_session_token(self):
        self.session = AutoRenewingOAuthSession(
            client=self.client,
            scope=self.scope,
            auto_refresh_kwargs=self.fetch_token_kwargs,
        )

        self.session.fetch_token(**self.fetch_token_kwargs)

    def check_session_token(self):
        if not self.is_session_token_valid():
            self.auth_session()  # Get a new session & a new token

    def get_session_token(self):
        return self.session.token

    @property
    def headers(self):
        # This isn't needed - the session automatically adds this header to
        # requests. But downstream code may expect it to exist.
        auth_token_val = 'Bearer ' + self.session.token['access_token']
        return {'Authorization': auth_token_val}

    @property
    def oauth_token(self):
        tok = self.session.token.copy()
        # Convert expires_at to a datetime object, keeping previous interface
        tok['expires_at'] = datetime.fromtimestamp(tok['expires_at'])
        return tok

    def is_session_token_valid(self):
        current_token = self.get_session_token()
        return Oauth2ClientBackend.is_session_token_dt_valid(current_token)

    @staticmethod
    def is_session_token_dt_valid(session_token, dt=None):
        # Check session_token hash
        if session_token and 'expires_at' in session_token:
            # Convert Unix timestamp (seconds from the epoch) to datetime
            expires_dt = datetime.fromtimestamp(session_token['expires_at'])

            if dt is None:
                dt = datetime.now()

            # return True:
            # 1) If expire datetime is in future (token is still valid)
            # return False:
            # 1) If expire datetime is in past (a new token must be generated)
            return expires_dt > dt

        return False
