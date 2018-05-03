import requests
import os

class BaseClient:

    def __init__(self, url):
        if url is None:
            raise Exception('You must provide the base url for the client to work')
        self._baseurl = url

    @property
    def url(self):
        return "{}/api/v1/file/{}".format(self._baseurl, self._endpoint())

    def submit(self, input_file, **kwargs):
        output_file = kwargs.get('output_file', None)
        apikey = kwargs.get('apikey', None)

        self._check_apikey(apikey)

        BaseClient._ensure_output_uniqueness(output_file)

        with open(input_file, 'rb') as sampletab_file:
            files = {'file': sampletab_file}
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
        return requests.post(self.url, files=files, **kwargs)

    def _endpoint(self):
        raise NotImplementedError("This method need to be implemented in a subclass")

    def _check_apikey(self, apikey):
        if apikey and isinstance(apikey, str):
            return
        raise ValueError("You need to provide an apikey")

    @staticmethod
    def _save_sampletab_to_file(sampletab_json, output_file):
        with open(output_file, 'w') as file_out:
            for line in BaseClient.convert_json_matrix_to_sampletab(sampletab_json):
                file_out.write("{}{}".format(line, os.linesep))

    @staticmethod
    def _ensure_output_uniqueness(file):
        if file:
            if os.path.isfile(file):
                raise FileExistsError('Output file already exists! Rename the file or use a different output file')

    @staticmethod
    def convert_json_matrix_to_sampletab(json_matrix):
        return ['\t'.join(line) for line in json_matrix]


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

# def submit(self, input_file, apikey, output_file=None):
#
#     Client._ensure_output_uniqueness(output_file)
#
#     if apikey is None:
#         raise ValueError('You must provide an apikey to submit a sampletab')
#     with open(input_file, 'rb') as sampletab_file:
#         files = {
#             'file': sampletab_file
#         }
#         params = {
#             'apikey': apikey
#         }
#         res = requests.post(self._submit_url, files=files, params=params)
#         if res.ok:
#             submission_errors = res.json().get('errors')
#             if len(submission_errors) > 0:
#                 raise ValueError('Some errors occurred while sumbitting sampletab', submission_errors)
#
#             final_sampletab = res.json().get('sampletab')
#
#             if output_file:
#                 Client._save_sampletab_to_file(final_sampletab, output_file)
#
#             return res.json()
#         else:
#             res.raise_for_status()
#
# def accession(self, input_file, apikey, output_file=None):
#     '''
#     Assigns accessions to samples; This does not submit any sample metadata but
#     returns the assigned accessions immediately
#     :param input_file: path to the input file
#     :type input_file: str
#     :param apikey: apikey to use for the sumbission
#     :type apikey: str
#     :param output_file: path to the output file
#     :type output_file: str
#     :raise
#     :return:
#     '''
#
#     Client._ensure_output_uniqueness(output_file)
#
#     if apikey is None:
#         raise ValueError('You must provide an apikey to submit a sampletab')
#     with open(input_file, 'rb') as sampletab_file:
#         files = {
#             'file': sampletab_file
#         }
#         params = {
#             'apikey': apikey
#         }
#         res = requests.post(self._accession_url, files=files, params=params)
#         if res.ok:
#             submission_errors = res.json().get('errors')
#             if len(submission_errors) > 0:
#                 raise ValueError('Some errors occurred while sumbitting sampletab', submission_errors)
#
#             final_sampletab = res.json().get('sampletab')
#
#             if output_file:
#                 Client._save_sampletab_to_file(final_sampletab, output_file)
#
#             return res.json()
#         else:
#             res.raise_for_status()
