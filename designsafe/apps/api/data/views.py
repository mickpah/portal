from designsafe.apps.api.views import BaseApiView
from designsafe.apps.api.mixins import JSONResponseMixin, SecureMixin

from designsafe.apps.api.data.agave.filemanager import FileManager as AgaveFileManager
from designsafe.apps.api.data.agave.public_filemanager import FileManager as PublicFileManager
from designsafe.apps.api.data.box.filemanager import FileManager as BoxFileManager

import logging
import json

logger = logging.getLogger(__name__)

class BaseDataView(SecureMixin, JSONResponseMixin, BaseApiView):
    """
    Base View which to instatiate corresponding file manager
    and execute correct operation.
    """
    #TODO: More elegant meta-programming.
    #TODO: Better way to check if it's an operation not permitted and to add operations.
    def _get_file_manager(self, request, resource, **kwargs):
        """
        Instantiates the correct file manager class
        
        Args:
            request: Request object. Used to get the user object.
            resource: Resource name to decide which class to instantiate.
        """
        user_obj = request.user
        if resource == 'default':
            return AgaveFileManager(user_obj, resource = resource, **kwargs)
        elif resource == 'public':
            return PublicFileManager(user_obj, resource = resource, **kwargs)
        elif resource == 'box':
            return BoxFileManager(user_obj, resource = resource, **kwargs)

    def _execute_operation(self, request, operation, **kwargs):
        """
        Executes operation of a file manager object.

        Args:
            request: Request object. Used to get the body of a post request and file array.
            operation: Operation to execute.
        """
        fm = self._get_file_manager(request, **kwargs)
        op = getattr(fm, operation)
        try:
            body_json = json.loads(request.body)
        except ValueError:
            body_json = {}
        files = request.FILES or []
        d = body_json
        d.update({'files': files})
        d.update(kwargs)
        resp = op(**kwargs)
        return resp

class DataView(BaseDataView):
    """
    Data View to handle listing of a file or folder. GET HTTP Request.
    """
    def get(self, request, *args, **kwargs):
        resp = self._execute_operation(request, 'listing', **kwargs)        
        return self.render_to_json_response(resp)

class DataFileManageView(BaseDataView):
    """
    Data View to handle file management. POST, PUT and DELETE Requests.

    If the request is POST or PUT it is expecting a JSON object in the body.
    The body JSON object should have at least these keys:
    - action: Operation to execute in the file manager.
    - path: File path on which the operation should be executed.

    The entire request body will be passed onto the file manager operation being executed as a python dictionary as well as the uploaded file array if present.
    """
    def _execute_post_operation(request, **kwargs):
        body_json = json.loads(request.body)
        operation = body_json.get('action')
        resp = self._execute_operation(request, operation, **kwargs)
        return self.render_to_json_response(resp.to_dict())

    def post(self, request, *args, **kwargs):
        self._execute_post_operation(request, **kwargs)

    def put(self, request, *args, **kwargs):
        self._execute_post_operation(request, **kwargs)

    def delete(self, request, *args, **kwargs):
        resp = self._execute_operation(request, 'delete', **kwargs)        
        return self.render_to_json_response(resp.to_dict())

class DataSearchView(BaseDataView):
    """
    Data view to handle search.
    It will pass all the keyword arguments as well as the Query String parameters as a dictionary on to the `search` method of the file manager class.
    """
    def get(self, request, *args, **kwargs):
        fm = self._get_file_manager(request, **kwargs)
        d = {}
        d.update(kwargs)
        d.update(request.GET)
        resp = fm.search(**kwargs)
        return self.render_to_json_response([o.to_dict() for o in resp])