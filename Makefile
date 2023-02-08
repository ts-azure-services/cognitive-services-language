infra:
	./setup/text-analytics-resource.sh

ingestion:
	./setup/ingestion-client-backup.sh

install:
	#conda create -n language python=3.8 -y; conda activate language
	pip install python-dotenv
	pip install requests
	pip install flake8

entity_test:
	python ./analytics.py -er 
	python ./analytics.py -er --file "./entity-recognition/sample.txt"
	python ./analytics.py -er --free_text "We went to Venice."

sentiment_test:
	python ./analytics.py -s
	python ./analytics.py -s --file "./sentiment/sample.txt"
	python ./analytics.py -s --free_text "We went to Venice."

key_phrase_test:
	python ./analytics.py -ex
	python ./analytics.py -ex --file "./key-phrase/sample.txt"
	python ./analytics.py -ex --free_text "We went to Venice."

pii_test:
	python ./analytics.py -pii
	python ./analytics.py -pii --file "./pii/sample.txt"
	python ./analytics.py -pii --free_text "We went to Venice."

doc_summarization_test:
	python ./analytics.py -ds
