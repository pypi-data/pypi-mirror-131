class skillsController:
    """Skills Controller"""

    _controller_name = "skillsController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def list(self, skillsetId):
        """

        Args:
            skillsetId: (string): skillsetId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skill/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, skillId):
        """

        Args:
            skillId: (string): skillId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skill/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
