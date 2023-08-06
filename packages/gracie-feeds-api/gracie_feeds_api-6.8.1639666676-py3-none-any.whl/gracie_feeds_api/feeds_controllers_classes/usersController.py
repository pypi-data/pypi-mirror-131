class usersController:
    """User - is someone who can edit data in the database.  All CRUD- operations possible to implement. """

    _controller_name = "usersController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, login, password, **kwargs):
        """

        Args:
            description: (string): description
            enabled: (boolean): enabled
            login: (string): login
            password: (string): password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'login': {'name': 'login', 'required': True, 'in': 'query'}, 'password': {'name': 'password', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            description: (string): description
            enabled: (boolean): enabled
            id: (string): id
            login: (string): login
            password: (string): password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'login': {'name': 'login', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def editUserAttributes(self, **kwargs):
        """

        Args:
            dashboardsRefreshEvery: (string): dashboardsRefreshEvery
            dashboardsRefreshRate: (integer): dashboardsRefreshRate

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dashboardsRefreshEvery': {'name': 'dashboardsRefreshEvery', 'required': False, 'in': 'query'}, 'dashboardsRefreshRate': {'name': 'dashboardsRefreshRate', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/editUserAttributes'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
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
        api = '/users/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieveUserAttributes(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/retrieveUserAttributes'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def whoAmI(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/whoAmI'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
