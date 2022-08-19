#!/bin/bash
#Script to provision Cognitive Services account
grn=$'\e[1;32m'
end=$'\e[0m'

# Start of script
SECONDS=0
printf "${grn}Starting creation of backup resources for ingestion client...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Create the resource group, location
number=$[ ( $RANDOM % 10000 ) + 1 ]
resourcegroup='cs'$number
location='eastus'
textanalyticsservice='cs'$number'text'
speechservice='cs'$number'speech'
#dbservername='cs'$number'dbserver'
storageaccount='storagestt'$number
#dbname='db'$number
adminusername='adminuser'$number
adminpassword=$(uuidgen)

printf "${grn}Starting creation of the resource group...${end}\n"
rgCreate=$(az group create --name $resourcegroup --location $location)
printf "Result of resource group create:\n $rgCreate \n"

## Create speech service
printf "${grn}Creating the text analytics resource...${end}\n"
textanalyticsserviceCreate=$(az cognitiveservices account create \
	--name $textanalyticsservice \
	-g $resourcegroup \
	--kind 'TextAnalytics' \
	--sku S \
	--location $location \
	--yes)
printf "Result of text analytics create:\n $textanalyticsserviceCreate \n"

## Retrieve key from cognitive services
printf "${grn}Retrieve the keys and endpoint of the text analytics resource...${end}\n"
textKey=$(az cognitiveservices account keys list -g $resourcegroup --name $textanalyticsservice --query "key1")
textEndpoint=$(az cognitiveservices account show -g $resourcegroup --n $textanalyticsservice --query "properties.endpoint")

## Create speech service
printf "${grn}Creating the speech resource...${end}\n"
speechServiceCreate=$(az cognitiveservices account create \
	--name $speechservice \
	-g $resourcegroup \
	--kind 'SpeechServices' \
	--sku S0 \
	--location $location \
	--yes)
printf "Result of speech service create:\n $speechServiceCreate \n"

## Retrieve key from cognitive services
printf "${grn}Retrieve the keys and endpoint of the speech resource...${end}\n"
speechKey=$(az cognitiveservices account keys list -g $resourcegroup --name $speechservice --query "key1")
speechEndpoint=$(az cognitiveservices account show -g $resourcegroup --n $speechservice --query "properties.endpoint")

## Create Azure SQL Server 
#printf "${grn}Starting creation of Azure SQL Server...${end}\n"
#result=$(az sql server create \
#	--name $dbservername \
#	--resource-group $resourcegroup \
#	--location $location \
#	--admin-user $adminusername \
#	--admin-password $adminpassword)
#printf "Result of Azure SQL Server create:\n $result \n"
#sleep 40
#
## Configure a firewall rule on Azure SQL Server 
#echo "Guessing your external IP address from ipinfo.io"
#IP=$(curl -s ipinfo.io/ip)
#
#printf "${grn}Starting creation of Azure SQL Server firewall rule...${end}\n"
#sqlserverdetails=$(az sql server firewall-rule create \
#	--resource-group $resourcegroup \
#	--server $dbservername \
#	--n 'AllowYourIp' \
#	--start-ip-address $IP \
#	--end-ip-address $IP
#)
#printf "Result of Azure SQL Server Firewall create:\n $sqlserverdetails \n"
#sleep 25
#
## Create SQL Database
#printf "${grn}Starting creation of Azure SQL Database...${end}\n"
#result=$(az sql db create \
#	--name $dbname \
#	--resource-group $resourcegroup \
#	--server $dbservername \
#	--edition 'Basic' \
#)
#printf "Result of Azure SQL Database create:\n $result \n"

# Create from ARM deployment
printf "${grn}Triggering the ARM deployment...${end}\n"
params="StorageAccount=$storageaccount \
	AzureSpeechServicesKey=$speechKey \
	AzureSpeechServicesRegion=$location \
	TextAnalyticsKey=$textKey \
	TextAnalyticsRegion=$location \
	SentimentAnalysis=UtteranceLevel \
	PiiRedaction=UtteranceAndAudioLevel \
	SqlAdministratorLogin=$adminusername \
	SqlAdministratorLoginPassword=$adminpassword"
result=$(az deployment group create\
	--name "BatchDeployment"\
	--resource-group $resourcegroup\
	--template-uri "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-speech-sdk/master/samples/ingestion/ingestion-client/Setup/ArmTemplateBatch.json"\
	--parameters $params)
printf "Result of ARM deployment:\n $result \n"

# Remove double-quotes in key
textKey=$(sed -e 's/^"//' -e 's/"$//' <<<"$textKey")
speechKey=$(sed -e 's/^"//' -e 's/"$//' <<<"$speechKey")

# Create environment file 
printf "${grn}Writing out environment variables...${end}\n"
configFile='variables.env'
printf "RESOURCE_GROUP=$resourcegroup \n"> $configFile
printf "LOCATION=$location \n">> $configFile
printf "TEXT_ANALYTICS_KEY=$textKey \n">> $configFile
printf "SPEECH_ENDPOINT=$speechEndpoint \n">> $configFile
printf "SPEECH_KEY=$speechKey \n">> $configFile
printf "TEXT_ANALYTICS_ENDPOINT=$textEndpoint \n">> $configFile
#printf "HOST=$dbservername.database.windows.net \n" >> $configFile
#printf "DATABASE=$dbname \n" >> $configFile
printf "DB_USER=$adminusername \n" >> $configFile
printf "DB_PWD=$adminpassword \n" >> $configFile
