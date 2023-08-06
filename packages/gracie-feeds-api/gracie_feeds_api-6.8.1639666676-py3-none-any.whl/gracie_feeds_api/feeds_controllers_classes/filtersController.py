class filtersController:
    """Filters management."""

    _controller_name = "filtersController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def getFiltersTree(self, alertRuleId):
        """

        Args:
            alertRuleId: (string): alertRuleId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/getFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeFiltersTree(self, alertRuleId):
        """

        Args:
            alertRuleId: (string): alertRuleId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/removeFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def setFiltersTree(self, alertRuleId, filters):
        """

        Args:
            alertRuleId: (string): alertRuleId
            filters: (string): filters

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'filters': {'name': 'filters', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/setFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
