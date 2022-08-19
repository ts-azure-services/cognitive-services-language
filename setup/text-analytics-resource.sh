#!/bin/bash
#Script to provision Cognitive Services account
grn=$'\e[1;32m'
end=$'\e[0m'

# Start of script
SECONDS=0
printf "${grn}STARTING CREATION OF TEXT ANALYTICS RESOURCE...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Create the resource group, location
number=$[ ( $RANDOM % 10000 ) + 1 ]
resourcegroup='cs'$number
textanalyticsservice='cs'$number'text'
location='westus2'

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
Key=$(az cognitiveservices account keys list -g $resourcegroup --name $textanalyticsservice --query "key1")
Endpoint=$(az cognitiveservices account show -g $resourcegroup --n $textanalyticsservice --query "properties.endpoint")

# Remove double-quotes in key
Key=$(sed -e 's/^"//' -e 's/"$//' <<<"$Key")

# Create environment file 
printf "${grn}Writing out environment variables...${end}\n"
configFile='variables.env'
printf "RESOURCE_GROUP=$resourcegroup \n"> $configFile
printf "TEXT_ANALYTICS_KEY=$Key \n">> $configFile
printf "TEXT_ANALYTICS_LOCATION=$location \n">> $configFile
printf "TEXT_ANALYTICS_ENDPOINT=$Endpoint \n">> $configFile
