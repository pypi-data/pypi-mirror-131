class bulkProcessingController:
    """Bulk Processing Controller"""

    _controller_name = "bulkProcessingController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def cancel(self, documentId):
        """

        Args:
            documentId: (string): documentId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'documentId': {'name': 'documentId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/cancel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def cancelAll(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/cancelAll'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clearErrors(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/clearErrors'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deletePerformanceStats(self, **kwargs):
        """

        Args:
            olderThan: (string): olderThan
            reportType: (string): reportType

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'olderThan': {'name': 'olderThan', 'required': False, 'in': 'query'}, 'reportType': {'name': 'reportType', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/deletePerformanceStats'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """Change BulkProcessing configuration parameters

        Args:
            chunkSize: (integer): chunkSize
            maxChunks: (integer): maxChunks
            minChunkSize: (integer): minChunkSize
            numThreads: (integer): numThreads

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'chunkSize': {'name': 'chunkSize', 'required': False, 'in': 'query'}, 'maxChunks': {'name': 'maxChunks', 'required': False, 'in': 'query'}, 'minChunkSize': {'name': 'minChunkSize', 'required': False, 'in': 'query'}, 'numThreads': {'name': 'numThreads', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getErrors(self, **kwargs):
        """

        Args:
            pageNum: (integer): pageNum
            pageSize: (integer): pageSize

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'pageNum': {'name': 'pageNum', 'required': False, 'in': 'query'}, 'pageSize': {'name': 'pageSize', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/getErrors'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listUploads(self, **kwargs):
        """

        Args:
            pageNum: (integer): pageNum
            pageSize: (integer): pageSize

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'pageNum': {'name': 'pageNum', 'required': False, 'in': 'query'}, 'pageSize': {'name': 'pageSize', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/listUploads'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def pause(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/pause'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def performanceStats(self, **kwargs):
        """

        Args:
            onlySince: (string): onlySince
            reportType: (string): reportType

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'onlySince': {'name': 'onlySince', 'required': False, 'in': 'query'}, 'reportType': {'name': 'reportType', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/performanceStats'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def resume(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/resume'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def stats(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/stats'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def uploadFiles(self, files, projectId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            filePath: (string): filePath
            files: (array): files
            languageId: (string): empty - AutoDetect language from text.
            performTextExtract: (boolean): true - Extract text from file by Tika, false - Process file as plain text in UTF-8 encoding.
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            userMetadata: (string): userMetadata

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'filePath': {'name': 'filePath', 'required': False, 'in': 'query'}, 'files': {'name': 'files', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'performTextExtract': {'name': 'performTextExtract', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'userMetadata': {'name': 'userMetadata', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadFiles'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def uploadText(self, projectId, text, **kwargs):
        """

        Args:
            fileName: (string): fileName
            languageId: (string): empty - AutoDetect.
            mimeType: (string): mimeType
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            text: (type): text
            userMetadata: (string): userMetadata

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}, 'userMetadata': {'name': 'userMetadata', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadText'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def uploadZip(self, file, projectId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            file: (file): file
            languageId: (string): empty - AutoDetect language from text.
            performTextExtract: (boolean): true - Extract text from file by Tika, false - Process file as plain text in UTF-8 encoding.
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            userMetadata: (string): userMetadata

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'performTextExtract': {'name': 'performTextExtract', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'userMetadata': {'name': 'userMetadata', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadZip'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
