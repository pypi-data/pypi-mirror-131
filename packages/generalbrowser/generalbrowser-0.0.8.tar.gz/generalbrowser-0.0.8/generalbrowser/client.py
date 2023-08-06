
from requests import Session, Response, exceptions
import webbrowser
import re
from unittest.mock import Mock
from dill import loads

from generalbrowser.shared import _GeneralShared
from generalfile import Path


class GeneralClient(_GeneralShared):
    """ Client methods to talk to server. """
    session_path = Path.get_cache_dir() / "generalbrowser/session.txt"
    debug = False

    def __init__(self, domain):
        self.domain = domain

        stored_session = self.session_path.pickle.read(default=None)
        self.session = stored_session or Session()

    def url(self, endpoint):
        return f"{self.domain}/api/{endpoint}"

    def store_session(self):
        self.session_path.pickle.write(self.session, overwrite=True)

    def _request(self, method, endpoint, filepath=None, **data):
        """ :rtype: Response """
        url = self.url(endpoint=endpoint)

        try:
            if filepath is not None:
                path = Path(filepath)
                with open(path, "rb") as file:
                    files = {path.name(): file}
                    response = method(url=url, files=files, data=data)
            else:
                response = method(url=url, data=data)
        except exceptions.ConnectionError as e:
            response = Mock(spec=Response, status_code=400, text=f"Connection failed for {self.domain}")
        
        else:  # Don't think we should update session on connection fail
            self.store_session()

        # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        if self.debug and str(response.status_code)[0] != "2":
            self.render_response(response)
        
        return response

    def post(self, endpoint, filepath=None, **data):
        """ :param endpoint: 
            :param filepath: Path to file or None. """
        return self._request(method=self.session.post, endpoint=endpoint, filepath=filepath, **data)

    def get(self, endpoint, filepath=None, **data):
        """ :param endpoint: 
            :param filepath: Path to file or None. """
        return self._request(method=self.session.get, endpoint=endpoint, filepath=filepath, **data)

    def deserialize(self, response):
        """ Return list of client models. """
        return loads(response.content)

    @staticmethod
    def render_response(response):
        """ Open response in browser. """
        path = Path.get_cache_dir() / "python/response.htm"  # type: Path
        path.text.write(response.text, overwrite=True)
        webbrowser.open(str(path))

    @staticmethod
    def response_to_file(response, path):
        """ Write a file from response to path. """
        name = re.findall("filename=(.+)", response.headers['content-disposition'])[0]
        path = Path(path) / name

        with open(path, "wb") as file:
            file.write(response.content)


