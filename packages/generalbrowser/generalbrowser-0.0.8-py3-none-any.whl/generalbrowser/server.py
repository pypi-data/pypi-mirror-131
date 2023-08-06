
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from dill import dumps

from generalbrowser.shared import _GeneralShared
from generallibrary import deco_optional_suppress


class GeneralServer(_GeneralShared):
    """ Server methods to talk to client. """
    _error = ValidationError

    @property
    def data(self):
        """ :param rest_framework.views.APIView or GeneralServer self: """
        return self.request.POST.dict()

    def extract_data(self, *keys, default=...):
        """ Returns tuple if any key is given, otherwise a dict. """
        if default is Ellipsis:
            return tuple(self.data[key] for key in keys)
        else:
            return tuple(self.data.get(key, default) for key in keys)

    def serialize(self, *models):
        """ Todo: Send client models in header instead? That way we can serialize inside success method instead.
            Convert django models to client models defined in generalmainframe. """
        client_models = [model.client_model() for model in models]
        return HttpResponse(dumps(client_models), content_type="application/octet-stream", headers={"testing": 5})

    def success(self, msg=None, files=None, code=None):
        if files:
            filename, file = next(iter(files.items()))
            response = HttpResponse(file, content_type="application/octet-stream")
            response["Content-Disposition"] = f'attachment; filename={filename}'
        else:
            response = Response(msg)
        if code is not None:
            response.status_code = code
        return response

    def fail(self, msg=None):
        # return Response(f"Fail: {msg}")
        raise self._error(msg)

    @deco_optional_suppress(_error)
    def _scrub(self, value, error, method):
        """ Raise ValidationError if not passing. """
        validation = method(value)
        if not validation:
            self.fail(msg=validation)
        return validation

    def scrub_email(self, email, error=True):
        return self._scrub(value=email, error=error, method=self.validate_email)

    def scrub_password(self, password, error=True):
        return self._scrub(value=password, error=error, method=self.validate_password)