import os, json, time, requests
from dotenv import load_dotenv

class textAnalytics:
    def __init__(self):
        self.access_variables = self.__load_variables()
        self.endpoint = self.access_variables['text_endpoint']
        self.standard_path = f'{self.endpoint}language/:analyze-text?api-version=2022-05-01'
        self.document_path = f'{self.endpoint}text/analytics/v3.2-preview.1/analyze'
        self.headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key':self.access_variables['text_key']}

    # Load sub, tenant ID variables 
    def __load_variables(self):
        """Load access variables"""
        env_var=load_dotenv('./variables.env')
        auth_dict = {
                "text_key":os.environ['TEXT_ANALYTICS_KEY'],
                "text_endpoint":os.environ['TEXT_ANALYTICS_ENDPOINT'],
                "text_location":os.environ['TEXT_ANALYTICS_LOCATION'],
                }
        return auth_dict

    def __load_file(self, source=None, document=False):
        if not document:
            with open(source, 'r') as f:
                data = f.read().splitlines()
                documents = []
                for i,v in enumerate(data):
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

    def entity_recognition(self, use_file=False, free_text=None):
        if use_file:
            documents = self.__load_file(source='./text-data/entity-recognition.txt')
        elif free_text is not None:
            documents = [{"id":"1", "language":"en","text": str(free_text)}]
        else:
            documents = [{"id":"1", "language":"en","text": "I had a wonderful trip to Seattle."}]

        path = self.standard_path
        body = {
                 "kind": "EntityRecognition",
                 "parameters":{"modelVersion":"latest"},
                 "analysisInput":{
                     "documents": documents
                     }
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def sentiment(self, use_file=False, free_text=None):
        if use_file:
            documents = self.__load_file(source='./text-data/sentiment.txt')
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

    def key_phrase_extraction(self, use_file=False, free_text=None):
        if use_file:
            documents = self.__load_file(source='./text-data/key-phrases.txt')
        elif free_text is not None:
            documents = [{"id":"1", "language":"en","text": str(free_text)}]
        else:
            documents = [{"id":"1", "language":"en","text": "Dr. Smith has a very modern medical office, and she has great staff."}]
        path = self.standard_path
        body = {
                 "kind": "KeyPhraseExtraction",
                 "parameters":{
                     "modelVersion":"latest"
                     },
                 "analysisInput":{
                     "documents": documents
                     }
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def pii_data(self, use_file=False, free_text=None):
        if use_file:
            documents = self.__load_file(source='./text-data/pii.txt')
        elif free_text is not None:
            documents = [{"id":"1", "language":"en","text": str(free_text)}]
        else:
            documents = [{"id":"1", "language":"en","text": "Call our office at 312-555-1234, or send an email to support@contoso.com."}]
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
        documents = self.__load_file(source='./text-data/document.txt', document=True)
        path = self.document_path
        body = {"analysisInput":{"documents":[{"id":"1", "language":"en", "text":documents}]},
                 "tasks":{"extractiveSummarizationTasks":[
                         {
                             "parameters":{
                                 "model-version":"latest",
                                 "sentenceCount":3,
                                 "sortBy":"Offset"
                                 }
                             }
                         ]
                     }
                 }
        self.rest_api_request(path = path, headers= self.headers, json=body)

    def rest_api_request(self, path=None, headers=None, json=None):
        response = requests.post(url=path, headers=headers, json=json)
        status, reason, resp_headers, resp_text = response.status_code, response.reason, response.headers, response.text
        if status == 200:
            #print(f"response status code: {status}")
            #print(f"response status: {reason}")
            #print(f"response headers: {resp_headers}")
            print(f"response text: {resp_text}\n")
        elif status == 202: # document summarization
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
    t = textAnalytics()

    #print(f"Entity recognition:\n")
    #t.entity_recognition(use_file=True)
    #t.entity_recognition(free_text="There are so many things to see in Portland! For example, I ate sushi for the first time!")
    #t.entity_recognition()

    #print(f"Sentiment:\n")
    #t.sentiment(use_file=True)
    #t.sentiment(free_text="I wish that this call would get over faster!")
    #t.sentiment()

    #print(f"Key Phrase extraction:\n")
    #t.key_phrase_extraction(use_file=True)
    #t.key_phrase_extraction(free_text="In this place there are so many different species of birds!")
    #t.key_phrase_extraction()
    #
    #print(f"PII data:\n")
    #t.pii_data(use_file=True)
    #t.pii_data(free_text="Yes, my VISA credit card is 2222-4422-2422-1987 with a CVV of 763 and my social security number is 234-12-1111.")
    #t.pii_data()

    #print(f"Document summarization:\n")
    #t.document_summarization()
