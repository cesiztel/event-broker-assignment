#!/bin/bash

echo "Creating the infrastructure for the Event broker architecture (dev environment)"
echo "Step 1: Creating schema backup bucket"
cd event-schemas-backup-service 
cdk deploy --require-approval never 
cd ..
echo "Step 2: Creating the storage for the components deployment configuration"
cd components-configuration-storage-service
cdk deploy --require-approval never 
cd ..
echo "Step 3: Create the main API for injection events and custom event bus"
cd event-broker-infrastructure
cdk deploy EventBrokerApiStackAppStack
cdk deploy EventBrokerBusStackAppStack
cd ..
echo "Step 4: Deploy the self service portal"
cd self-service-portal
sam build && sam validate && sam deploy --no-confirm-changeset
echo "End: System ready to use"