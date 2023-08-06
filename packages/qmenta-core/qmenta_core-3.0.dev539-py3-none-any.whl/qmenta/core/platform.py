import requests
from urllib.parse import urljoin
from typing import Dict, Any

from qmenta.core.auth import Auth
from qmenta.core.errors import (
    ActionFailedError,
    ConnectionError,
    InvalidResponseError,
)

"""
Handles all the communication with the QMENTA platform.
"""


class ChooseDataError(ActionFailedError):
    """
    When a trying to start an analysis, but data has to be chosen

    Parameters
    ----------
    warning : str
        Warning message returned by the platform
    data_to_choose : str
        Specification of the data to choose returned by the platform
    analysis_id : int
        The ID of the analysis for which data needs to be chosen,
        returned by the platform.
    """
    def __init__(self, warning: str, data_to_choose: str,
                 analysis_id: int) -> None:
        self.warning: str = warning
        self.data_to_choose: str = data_to_choose
        self.analysis_id: int = analysis_id


def parse_response(response: requests.Response) -> Any:
    """
    Convert a platform response to JSON and check that it is valid.
    This function should be applied to the output of post().

    Parameters
    ----------
    response : requests.Response
        The response from the platform

    Raises
    ------
    InvalidResponseError
        When the response of the platform cannot be converted to JSON,
        or when it has unexpected values or missing keys.
    ActionFailedError
        When the requested action could not be performed by the platform
    ChooseDataError
        When a POST was done to start an analysis, but data needs to be
        chosen before the analysis can be started.

    Returns
    -------
    dict or list
        When the platform returns a response with a list in the JSON, it
        is returned. Otherwise, it is assumed that the returned value is a
        dict. In case the dict has a 'data' key, the value of data in the
        dict is returned, otherwise the full dict is returned.
    """
    try:
        d: Any = response.json()
    except ValueError:
        raise InvalidResponseError(
            'Could not decode JSON for response {}'.format(response))

    if isinstance(d, dict):
        try:
            success: int
            errmsg: str

            success = d['success']
            if success == 0:
                errmsg = d['error']
                raise ActionFailedError(errmsg)
            elif success == 1:
                # Good!
                pass
            elif success == 2:
                # You have to choose data
                raise ChooseDataError(
                    warning=d['warning'],
                    data_to_choose=d['data_to_choose'],
                    analysis_id=d['analysis_id']
                )
            elif success == 3:
                errmsg = d['message']
                raise ActionFailedError(errmsg)
            else:
                raise InvalidResponseError(
                    'Unexpected value for success: {}'.format(success)
                )
        except KeyError as e:
            raise InvalidResponseError('Missing key: {}'.format(e))

        try:
            result = d['data']
        except KeyError:
            result = d

    elif isinstance(d, list):
        # In some cases, the platform does not return a dict with additional
        #   information, but only a list with the results.
        result = d
    else:
        raise InvalidResponseError(
            'Response is not a dict or list: {}'.format(response.text))

    return result


def post(auth: Auth, endpoint: str, data: Dict[str, Any] = {},
         headers: Dict[str, Any] = {}, stream: bool = False,
         timeout: float = 30.0) -> requests.Response:
    """
    Post the given data and headers to the specified platform's endpoint.

    Parameters
    ----------
    auth : qmenta.core.platform.Auth
        Auth object that was used to authenticate to the QMENTA platform
    endpoint : str
        The end-point in the platform to post to
    data : dict
        The data to post
    headers : dict
        The headers to post
    stream : bool
        Stream the response. This is used when downloading files.
        Default value: False.
    timeout : float
        Timeout in seconds. If no bytes have been received within this time,
        an exception is raised. Default value: 30.

    Raises
    ------
    qmenta.core.errors.ConnectionError
        When there is a problem connecting to the QMENTA platform

    Returns
    -------
    requests.Response
        The response object returned by the request.
    """
    url: str = urljoin(auth.base_url, endpoint)
    try:
        r = auth.get_session().post(
            url=url,
            data=data,
            headers=headers,
            stream=stream,
            timeout=timeout
        )
    except requests.RequestException as e:
        raise ConnectionError(str(e))

    return r
