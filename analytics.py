import os
import argparse
import json
import time
import requests
from dotenv import load_dotenv
# from pprint import pprint as pp


class textAnalytics:
    def __init__(self):
        self.access_variables = self.__load_variables()
        self.endpoint = self.access_variables['text_endpoint']
        self.standard_path = f'{self.endpoint}language/:analyze-text?api-version=2022-05-01'
        self.document_path = f'{self.endpoint}text/analytics/v3.2-preview.1/analyze'
        self.headers = {'Content-Type': 'application/json',
                        'Ocp-Apim-Subscription-Key': self.access_variables['text_key']
                        }

    # Load sub, tenant ID variables
    def __load_variables(self):
        """Load access variables"""
        load_dotenv('./variables.env')
        auth_dict = {
                "text_key": os.environ['TEXT_ANALYTICS_KEY'],
                "text_endpoint": os.environ['TEXT_ANALYTICS_ENDPOINT'],
                "text_location": os.environ['TEXT_ANALYTICS_LOCATION'],
                }
        return auth_dict

    def __load_file(self, source=None, document=False):
        if not document:
            with open(source, 'r') as f:
                data = f.read().splitlines()
                documents = []
                for i, v in enumerate(data):
                    temp_dict = {}
                    temp_dict['id'] = i+1
                    temp_dict['language'] = 'en'
                    temp_dict['text'] = v
                    documents.append(temp_dict)
            return documents
        else:
            with open(source, 'r') as f:
                data = f.read().splitlines()
            return data[0]

    def entity_recognition(self, file=None, free_text=None):
        if file is not None:
            documents = self.__load_file(source=file)
        elif free_text is not None:
            documents = [{"id": "1",
                          "language": "en",
                          "text": str(free_text)}]
        else:
            documents = [{"id": "1",
                          "language": "en",
                          "text": "I had a wonderful trip to Seattle."}]

        path = self.standard_path
        body = {
                 "kind": "EntityRecognition",
                 "parameters": {"modelVersion": "latest"},
                 "analysisInput": {"documents": documents}
                 }
        self.rest_api_request(path=path, headers=self.headers, json=body)

    def sentiment(self, file=None, free_text=None):
        if file is not None:
            documents = self.__load_file(source=file)
        elif free_text is not None:
            documents = [{"id":"1", "language":"en","text": str(free_text)}]
        else:
            documents = [{"id":"1", "language":"en","text": "The food and service were unacceptable. The concierge was nice, however."}]
        path = self.standard_path
        body = {
                 "kind": "SentimentAnalysis",
                 "parameters":{
                     "modelVersion":"latest",
                     "opinionMining":"True"},
                 "analysisInput":{
                     "documents":documents}
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def key_phrase_extraction(self, file=None, free_text=None):
        if file is not None:
            documents = self.__load_file(source=file)
        elif free_text is not None:
            documents = [{"id": "1", 
                          "language": "en",
                          "text": str(free_text)}]
        else:
            documents = [{"id":"1", 
                          "language":"en",
                          "text": "Dr. Smith has a very modern medical office, and she has great staff."}]
        path = self.standard_path
        body = {
                 "kind": "KeyPhraseExtraction",
                 "parameters": {
                     "modelVersion":"latest"
                     },
                 "analysisInput": {
                     "documents": documents
                     }
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def pii_data(self, file=None, free_text=None):
        if file is not None:
            documents = self.__load_file(source=file)
        elif free_text is not None:
            documents = [{"id": "1",
                          "language": "en",
                          "text": str(free_text)}]
        else:
            documents = [{"id": "1",
                          "language": "en",
                          "text": "Call our office at 312-555-1234, or send an email to support@contoso.com."}]
        path = self.standard_path
        body = {
                 "kind": "PiiEntityRecognition",
                 "parameters":{
                     "modelVersion":"latest"
                     },
                 "analysisInput":{
                     "documents":documents
                     }
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def document_summarization(self):
        documents = self.__load_file(source='./document-summarization/sample.txt', document=True)
        path = self.document_path
        body = {"analysisInput":
                {"documents":
                 [{"id": "1", "language": "en", "text": documents}]},
                "tasks":{"extractiveSummarizationTasks":[
                         {
                             "parameters": {
                                 "model-version": "latest",
                                 "sentenceCount": 3,
                                 "sortBy": "Offset"
                                 }
                             }
                         ]
                     }
                }
        self.rest_api_request(path=path, headers=self.headers, json=body)

    def rest_api_request(self, path=None, headers=None, json=None):
        response = requests.post(url=path, headers=headers, json=json)
        status, reason, resp_headers, resp_text = response.status_code, response.reason, response.headers, response.text
        if status == 200:
            # print(f"response status code: {status}")
            # print(f"response status: {reason}")
            # print(f"response headers: {resp_headers}")
            print(f"response text: {resp_text}\n")
        elif status == 202:  # document summarization
            print(f"response status: {reason}")
            print(f"response headers: {resp_headers}")
            resp_headers_dict = dict(resp_headers)
            request_id = resp_headers_dict['operation-location'].split('/jobs/')[1]
            print(f"Request: {request_id} initiated.")
            print("Waiting for 20 seconds for request to process...")
            time.sleep(20)
            self.get_batch_request(request_id=request_id)
        else:
            print("No response.")

    def get_batch_request(self, request_id=None):
        """Get document summarization result"""
        path = self.document_path + '/jobs/' + str(request_id)
        response = requests.get(path, headers=self.headers)
        status, reason, resp_headers, resp_content = response.status_code, response.reason, response.headers, response.content
        print(f"response status code: {status}")
        print(f"response status: {reason}")
        print(f"response headers: {resp_headers}")
        print(f"response content: {resp_content}")
        resp_content_json = json.loads(resp_content.decode('utf-8'))
        print(resp_content_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-er", action='store_true', default=False)
    parser.add_argument("-s", action='store_true', default=False)
    parser.add_argument("-ex", action='store_true', default=False)
    parser.add_argument("-pii", action='store_true', default=False)
    parser.add_argument("-ds", action='store_true', default=False)
    parser.add_argument("--file", type=str, required=False)
    parser.add_argument("--free_text", type=str, required=False)
    args = parser.parse_args()

    # Instantiate the text object
    t = textAnalytics()

    # Entity recognition
    if args.er:
        if args.file:
            t.entity_recognition(file=args.file)
        elif args.free_text:
            t.entity_recognition(free_text=args.free_text)
        else:
            t.entity_recognition()

    # Sentiment
    if args.s:
        if args.file:
            t.sentiment(file=args.file)
        elif args.free_text:
            t.sentiment(free_text=args.free_text)
        else:
            t.sentiment()

    # Key phrase extraction
    if args.ex:
        if args.file:
            t.key_phrase_extraction(file=args.file)
        elif args.free_text:
            t.key_phrase_extraction(free_text=args.free_text)
        else:
            t.key_phrase_extraction()

    # PII information
    if args.pii:
        if args.file:
            t.pii_data(file=args.file)
        elif args.free_text:
            t.pii_data(free_text=args.free_text)
        else:
            t.pii_data()

    # Document summarization
    if args.ds:
        t.document_summarization()
