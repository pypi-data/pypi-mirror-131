class projectsController:
    """Projects Controller"""

    _controller_name = "projectsController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, name, **kwargs):
        """

        Args:
            isRunning: (boolean): isRunning
            name: (string): name
            pipelineId: (string): If left blank, the default pipeline will be used.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clone(self, id, name):
        """

        Args:
            id: (string): id
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/clone'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): id
            isRunning: (boolean): isRunning
            name: (string): name
            pipelineId: (string): If left blank, the default pipeline will be used.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def processFile(self, file, projectId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            file: (file): file
            filterFields: (string): CSV of fields to show, default shows all. See https://github.com/bohnman/squiggly for usage
            languageId: (string): empty - AutoDetect language from text.
            logging: (boolean): logging
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            performTextExtract: (boolean): true - Extract text from file by Tika, false - Process file as plain text in UTF-8 encoding.
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'performTextExtract': {'name': 'performTextExtract', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/processFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def processText(self, projectId, text, **kwargs):
        """

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            fileExt: (string): fileExt
            fileName: (string): fileName
            filterFields: (string): CSV of fields to show, default shows all. See https://github.com/bohnman/squiggly for usage
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            mimeType: (string): mimeType
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            text: (type): text

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'fileExt': {'name': 'fileExt', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}}
        parameters_names_map = {}
        api = '/projects/processText'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
