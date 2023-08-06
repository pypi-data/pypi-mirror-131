class persistController:
    """Persist Controller"""

    _controller_name = "persistController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, dbHostname, dbName, dbPassword, dbPortNumber, dbType, dbUsername, name, **kwargs):
        """

        Args:
            dbHostname: (string): dbHostname
            dbName: (string): dbName
            dbPassword: (string): dbPassword
            dbPortNumber: (integer): dbPortNumber
            dbType: (string): dbType
            dbUsername: (string): dbUsername
            enabled: (boolean): enabled
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dbHostname': {'name': 'dbHostname', 'required': True, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': True, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': True, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': True, 'in': 'query'}, 'dbType': {'name': 'dbType', 'required': True, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': True, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createAttributeFilter(self, attribute, id, includeExclude, values):
        """

        Args:
            attribute: (string): attribute
            id: (string): id
            includeExclude: (string): includeExclude
            values: (array): values

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'attribute': {'name': 'attribute', 'required': True, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeExclude': {'name': 'includeExclude', 'required': True, 'in': 'query'}, 'values': {'name': 'values', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createAttributeFilter'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createES(self, **kwargs):
        """

        Args:
            enabled: (boolean): enabled

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createES'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createMetadataFilter(self, id, includeExclude, metadataKey, type, values):
        """

        Args:
            id: (string): id
            includeExclude: (string): includeExclude
            metadataKey: (string): metadataKey
            type: (string): type
            values: (array): values

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeExclude': {'name': 'includeExclude', 'required': True, 'in': 'query'}, 'metadataKey': {'name': 'metadataKey', 'required': True, 'in': 'query'}, 'type': {'name': 'type', 'required': True, 'in': 'query'}, 'values': {'name': 'values', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createMetadataFilter'
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
        api = '/persist/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteDocuments(self, id, **kwargs):
        """

        Args:
            id: (string): id
            metaName: (string): metaName
            metaValue: (string): metaValue
            projectName: (string): projectName

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'metaName': {'name': 'metaName', 'required': False, 'in': 'query'}, 'metaValue': {'name': 'metaValue', 'required': False, 'in': 'query'}, 'projectName': {'name': 'projectName', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/deleteDocuments'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteES(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/persist/deleteES'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            dbHostname: (string): dbHostname
            dbName: (string): dbName
            dbPassword: (string): dbPassword
            dbPortNumber: (integer): dbPortNumber
            dbUsername: (string): dbUsername
            enabled: (boolean): enabled
            id: (string): id
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dbHostname': {'name': 'dbHostname', 'required': False, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': False, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': False, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': False, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def enableES(self, enabled):
        """

        Args:
            enabled: (boolean): enabled

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/enableES'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getFilters(self, id):
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
        api = '/persist/getFilters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/persist/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeFilter(self, filterId):
        """

        Args:
            filterId: (string): filterId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'filterId': {'name': 'filterId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/removeFilter'
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
        api = '/persist/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
