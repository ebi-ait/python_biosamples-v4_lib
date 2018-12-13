import requests
import os


def _ensure_output_uniqueness(file):
    """
    Given a file path, verifies file doesn't exist
    :param file: the file path to check
    :raises FileExistsError if the provided path already exists
    """
    if file:
        if os.path.isfile(file):
            raise FileExistsError('Output file already exists! Rename the file or use a different output file')


class Utilities:
    @staticmethod
    def convert_json_matrix_to_sampletab(json_matrix):
        return os.linesep.join(['\t'.join(line) for line in json_matrix])

    @staticmethod
    def sampletab_to_json_matrix(sampletab_file):
        json_matrix = list()
        for line in sampletab_file:
            json_line = line.replace('\n', '').split("\t")
            json_matrix.append(json_line)
        return json_matrix


class BaseClient:

    def __init__(self, url):
        if url is None:
            raise Exception('You must provide the base url for the client to work')
        self._baseurl = url

    @property
    def url(self):
        return "{}/api/v1/file/{}".format(self._baseurl, self._endpoint())

    def submit(self, **kwargs):
        if kwargs.get('file'):
            input_file = kwargs.pop('file')
            with open(input_file, 'rb') as fin:
                return self._submit(fin, **kwargs)

        elif kwargs.get('json'):
            json_content = kwargs.pop('json')
            content = Utilities.convert_json_matrix_to_sampletab(json_content)
            return self._submit(content, **kwargs)

        elif kwargs.get('content'):
            content = kwargs.pop('content')
            return self._submit(content, **kwargs)

        else:
            raise ValueError('file|json|content argument are missing')

    def _submit(self, content, **kwargs):
        output_file = kwargs.get('output_file', None)
        apikey = kwargs.get('apikey', None)

        self._check_apikey(apikey)

        _ensure_output_uniqueness(output_file)

        files = {'file': content}
        params = dict()
        if apikey:
            params['apikey'] = apikey

        res = self._send(files, params=params)
        if res.ok:
            submission_errors = res.json().get('errors')
            if len(submission_errors) > 0:
                raise ValueError('Some errors occurred while sumbitting sampletab', submission_errors)

            final_sampletab = res.json().get('sampletab')

            if output_file:
                BaseClient._save_sampletab_to_file(final_sampletab, output_file)

            return res.json()

        else:
            res.raise_for_status()

    def _send(self, files, **kwargs):
        return requests.post(self.url, files=files, params=kwargs.get('params'))

    def _endpoint(self):
        raise NotImplementedError("This method need to be implemented in a subclass")

    def _check_apikey(self, apikey):
        if apikey and isinstance(apikey, str):
            return
        raise ValueError("You need to provide an apikey")

    @staticmethod
    def _save_sampletab_to_file(sampletab_json, output_file):
        with open(output_file, 'w', encoding='utf-8') as file_out:
            file_out.write(Utilities.convert_json_matrix_to_sampletab(sampletab_json))


class ValidationClient(BaseClient):

    def _check_apikey(self, apikey):
        pass

    def _endpoint(self):
        return "va"


class SubmissionClient(BaseClient):

    def _endpoint(self):
        return "sb"


class AccessionClient(BaseClient):

    def _endpoint(self):
        return "ac"
