import requests
from urllib.parse import urljoin
from typing import Optional, Dict, Any

from qmenta.core.errors import (
    ActionFailedError,
    ConnectionError,
    InvalidResponseError,
)


class InvalidLoginError(ActionFailedError):
    """
    When the provided credentials are incorrect, or when the used token
    is not valid.
    """
    pass


class Needs2FAError(ActionFailedError):
    """
    When a 2FA code must to be provided to log in.
    """
    pass


class Auth:
    """
    Class for authenticating to the platform.
    Do not use the constructor directly, but use the login() function to
    create a new authentication

    Attributes
    ----------
    base_url : str
        The base URL of the platform. Example: 'https://platform.qmenta.com'
    token : str
        The authentication token, returned by the platform when logging in.
    """
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self._session: Optional[requests.Session] = None

    @classmethod
    def login(cls, username: str, password: str,
              code_2fa: Optional[str] = None,
              ask_for_2fa_input: bool = False,
              base_url: str = 'https://platform.qmenta.com') -> 'Auth':
        """
        Authenticate to the platform using username and password.

        Parameters
        ----------
        username : str
            The username to log in on the platform. For all new platform
            accounts, this is the e-mail address of the user.
            Example: 'example@qmenta.com'
        password : str
            The QMENTA platform password of the user.
        code_2fa : str
            The 2FA code that was sent to your phone (optional).
        ask_for_2fa_input: bool
            When set to True, the user is asked input the 2FA code
            in the command-line interface when it is needed. If the user does
            not have 2FA enabled, no input is requested.
            This is useful for scripts.
            When set to False, a Needs2FAError exception is raised when
            a 2FA code is needed. This is useful for GUIs.
            Default value: False
        base_url : str
            The URL of the platform to connect to.
            Default value: 'https://platform.qmenta.com'

        Returns
        -------
        Auth
            The Auth object that was logged in with.

        Raises
        ------
        ConnectionError
            If there was a problem setting up the network connection with the
            platform.
        InvalidResponseError
            If the platform returned an invalid response.
        InvalidLoginError
            If the login was invalid. This can happen when the
            username/password combination is incorrect, or when the account is
            not active or 2FA is required to be set up.
        Needs2FAError
            When a login attempt was done without a valid 2FA code.
            The 2FA code has been sent to your phone, and must be provided
            in the next call to the login function.
        """
        url: str = urljoin(base_url, '/login')

        try:
            r: requests.Response = requests.post(
                url, data={
                    'username': username, 'password': password,
                    'code_2fa': code_2fa
                }
            )
        except requests.RequestException as e:
            raise ConnectionError(str(e))

        try:
            d: Dict[str, Any] = r.json()
        except ValueError:
            raise InvalidResponseError(
                f'Could not decode JSON for response {r}')

        try:
            if d["success"] != 1:
                # Login was not successful
                if 'account_state' in d and d['account_state'] == '2fa_need':
                    if ask_for_2fa_input:
                        input_2fa = input("Please enter your 2FA code: ")
                        return Auth.login(
                            username, password, code_2fa=input_2fa,
                            ask_for_2fa_input=True, base_url=base_url
                        )
                    else:
                        raise Needs2FAError(
                            'Provide the 2FA code sent to your phone, '
                            'or set the ask_for_2fa_input parameter'
                        )
                else:
                    raise InvalidLoginError(d['error'])

            token: str = d['token']
        except KeyError as e:
            raise InvalidResponseError(f'Missing key: {e}')

        return cls(base_url, token)

    def get_session(self) -> requests.Session:
        if not self._session:
            self._session = requests.Session()

            # Session may store other cookies such as 'route'
            auth_cookie = requests.cookies.create_cookie(
                name='AUTH_COOKIE', value=self.token
            )
            # Add or update it
            self._session.cookies.set_cookie(auth_cookie)
            self._session.headers.update(self._headers())

        return self._session

    def _headers(self):
        h = {
            'Mint-Api-Call': '1'
        }
        return h
