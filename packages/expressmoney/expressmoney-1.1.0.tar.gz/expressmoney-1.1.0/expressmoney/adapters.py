import datetime
import io
import json
import os

import requests
from google.cloud.exceptions import NotFound
from google.protobuf import timestamp_pb2
from google.cloud import pubsub_v1, storage, secretmanager, secretmanager_v1
from google.cloud import tasks_v2
from google.cloud import error_reporting


report = error_reporting.Client()
client = secretmanager.SecretManagerServiceClient()
access_secret_version = secretmanager_v1.types.service.AccessSecretVersionRequest()


class PubSub:
    """ Google Cloud PubSub Adapter"""

    __publisher = pubsub_v1.PublisherClient()

    def __init__(self, topic_id: str, access_token: str = None, project='expressmoney'):
        self.__topic_path = self.__publisher.topic_path(project, topic_id)
        self.__access_token = str(access_token)

    def publish(self, payload: dict = None):
        attrs = {'topic': self.__topic_path, }

        if payload and not isinstance(payload, dict):
            raise TypeError('Payload should be dict type')

        if payload:
            if self.__access_token:
                payload.update({'access_token': self.__access_token})
        else:
            if self.__access_token:
                payload = {'access_token': self.__access_token}
        if payload:
            attrs.update({'data': json.dumps(payload, ensure_ascii=False).encode('UTF-8')})

        self.__publisher.publish(**attrs)


class Tasks:
    """ Google Cloud Tasks Adapter"""

    _client = tasks_v2.CloudTasksClient()

    def __init__(self,
                 access_token: str = None,
                 queue: str = 'attempts-1',
                 location: str = 'europe-west1',
                 project: str = 'expressmoney',
                 in_seconds: int = None,
                 ):
        """
        CloudTasks client
        Args:
            access_token: 'Bearer DFD4345345D'
            queue: 'my-appengine-queue'
            location: 'europe-west1'
            project: 'expressmoney'
            in_seconds: None
        """

        self._project = project
        self._in_seconds = in_seconds
        self._parent = self._client.queue_path(self._project, location, queue)
        self._uri = None
        self._payload = None
        self._update = False
        self._service = None
        self._access_token = access_token

    def run(self,
            service: str,
            uri: str,
            payload: dict = None,
            update: bool = False,
            ):
        """
        Start service execution
        Args:
            service: service name of App Engine
            uri: '/example_task_handler'
            payload: {'param': 'value'}
            update: True - PUT method
        """
        self._service = service
        self._uri = uri
        self._payload = payload
        self._update = update
        task = self._create_task()
        task = self._add_payload(task)
        task = self._convert_in_seconds(task)
        task = self._add_authorization(task)
        task = self._remove_empty_headers(task)
        self._client.create_task(parent=self._parent, task=task)

    def _create_task(self):
        task = {
            'app_engine_http_request': {
                'http_method': self._http_method,
                'relative_uri': self._uri,
                'headers': {},
                'app_engine_routing': {
                    'service': self._service,
                    'version': '',
                    'instance': '',
                    'host': '',

                }
            },
        }

        return task

    def _add_authorization(self, task):
        if self._access_token:
            task["app_engine_http_request"]["headers"]['X-Forwarded-Authorization'] = f'Bearer {self._access_token}'
        return task

    def _add_payload(self, task):
        if self._payload is not None:
            if not isinstance(self._payload, dict):
                raise TypeError('Payload should be dict type')
            payload = json.dumps(self._payload, ensure_ascii=False).encode('utf-8')
            task["app_engine_http_request"]["body"] = payload
            task["app_engine_http_request"]["headers"]['Content-Type'] = 'application/json'
        return task

    def _convert_in_seconds(self, task):
        if self._in_seconds is not None:
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=self._in_seconds)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
            task['schedule_time'] = timestamp
        return task

    @staticmethod
    def _remove_empty_headers(task):
        if len(task['app_engine_http_request']['headers']) == 0:
            del task['app_engine_http_request']['headers']
        return task

    @property
    def _http_method(self):
        if self._update:
            return tasks_v2.HttpMethod.PUT
        else:
            return tasks_v2.HttpMethod.GET if self._payload is None else tasks_v2.HttpMethod.POST


class Storage:
    """ Google Cloud Storage Adapter"""

    def __init__(self, bucket_name='expressmoney'):
        self._bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self._bucket_name)

    def upload_blob(self, source_file_name, destination_blob_name, type_file='pdf'):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(source_file_name, content_type=f'application/{type_file}')

    def delete_blob(self, blob_name):
        """Deletes a blob from the bucket."""
        blob = self.bucket.blob(blob_name)
        blob.delete()

    def get_blob(self, path_to_file):
        """ Upload a file from the bucket. """
        blob = self.bucket.blob(path_to_file)
        try:
            file = io.BytesIO(blob.download_as_bytes())
            return file
        except NotFound:
            return None


class VertexAI:
    """Google Cloud VertexAI Adapter"""

    REGION = 'us-central1'
    PROJECT_ID = '1086735462412'

    def __init__(self, endpoint_id, instance_dict: dict, action='predict'):
        self._action = action
        self.endpoint_id = endpoint_id
        self.url = f'https://{self.REGION}-aiplatform.googleapis.com/v1/projects/{self.PROJECT_ID}/locations/' \
                   f'{self.REGION}/endpoints/{self.endpoint_id}:{action}'
        self.bearer = self._get_token()
        self._instance_dict = instance_dict
        self.__response = None

    @property
    def _response(self):

        if self.__response is None:
            # preparing data for google service
            data = dict()
            data['instances'] = []
            data['instances'].append(self._instance_dict)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.bearer}',
            }

            # self.__response = RequestService.request(method='POST', data=data, headers=headers, url=self.url)

            self.__response = requests.post(self.url, json=data, headers=headers)

            if self.__response.status_code != 200:
                error = f'Не удалось получить prediction из VertexAI: {self.__response.status_code}'
                report.report(error)
                raise Exception(error)

        return self.__response

    def get_score(self):
        predictions = self._response
        predictions = predictions.json().get('predictions')[0]
        for target_index, target_value in enumerate(predictions['classes']):
            if target_value == '1':
                score = predictions.get('scores')[target_index]
                return score

        raise Exception("Not found target '1' in prediction result")

    def get_explanations(self):
        """Получить весовые значения фичей"""
        if self._action != 'explain':
            return None
        target_name = self._response.json().get('explanations')[0].get('attributions')[0].get('outputDisplayName')
        explanations = self._response.json().get('explanations')[0].get('attributions')[0].get('featureAttributions')
        multiplier = 1000 if int(target_name) == 1 else -1000
        explanations = {key: multiplier * value for key, value in explanations.items()}
        return explanations

    @staticmethod
    def _get_token():
        if os.getenv('GAE_APPLICATION'):
            # when we are in GAE env:
            metadata_url = 'http://metadata.google.internal/computeMetadata/v1/'
            metadata_headers = {'Metadata-Flavor': 'Google'}
            service_account = 'default'

            url = '{}instance/service-accounts/{}/token'.format(
                metadata_url, service_account)

            # Request an access token from the metadata server.
            r = requests.get(url, headers=metadata_headers)
            r.raise_for_status()

            # Extract the access token from the response.
            access_token = r.json()['access_token']
        else:
            # when running locally:
            stream = os.popen('gcloud auth application-default print-access-token')
            access_token = stream.read().strip()

        return access_token


class Request:
    """Sync http request"""

    requests = requests

    def __init__(self, service: str = None, path: str = '/', access_token: str = None, project: str = 'expressmoney',
                 timeout: tuple = (30, 30)):
        self.__path = path
        self.__service = service
        self.__access_token = str(access_token)
        self.__project = project
        self.__timeout = timeout

    def run(self, payload: dict = None, update=False):
        if update:
            response = requests.put(self._uri, json=payload if payload else {}, headers=self._headers,
                                    timeout=self.__timeout)
        elif payload:
            response = requests.post(self._uri, json=payload, headers=self._headers, timeout=self.__timeout)
        else:
            response = requests.get(self._uri, headers=self._headers, timeout=self.__timeout)
        if response.status_code == 403:
            raise Exception('Service account does not have permission '
                            'to access the IAP-protected application.')
        elif response.status_code not in (200, 201):
            raise Exception('Bad response from application: {!r} / {!r} / {!r}'.format(
                response.status_code, response.headers, response.text))
        return response

    @property
    def _uri(self):
        local_url = 'http://127.0.0.1:8000'
        url = f'https://{self.__service}-dot-{self.__project}.appspot.com' if self.__service else local_url
        return f'{url}{self.__path}'

    @property
    def _headers(self):
        headers = dict()
        headers.update(self._get_authorization())
        return headers

    def _get_authorization(self) -> dict:
        return {'X-Forwarded-Authorization': f'Bearer {self.__access_token}'} if self.__access_token else {}

    @property
    def _aud(self):
        secrets = {
            'expressmoney': 'projects/1086735462412/secrets/IAP_CLIENT_ID/versions/1',
            'expressmoney-dev': 'projects/13337168308/secrets/IAP_CLIENT_ID/versions/1',
            'loans-russia': 'projects/70455559151/secrets/IAP_CLIENT_ID/versions/1',
        }
        access_secret_version.name = secrets.get(self.__project, None)
        return client.access_secret_version(request=access_secret_version).payload.data.decode("utf-8")
