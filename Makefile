infra:
	./setup/text-analytics-resource.sh
ingestion:
	./setup/ingestion-client-backup.sh
install:
	#conda create -n language python=3.8 -y; conda activate language
	pip install python-dotenv
	pip install requests
	#pip install pylint
