# Solution architecture for event broker system

The presented projects represents the solution architecture to create a self-servive event broker system
in AWS using event-driven approach with Amazon EventBridge.

Following you can see the diagram of the propose solution without including the list of the improvements that
can be applied to the architecture. You can read about the improvements not included on the solution design on the
"Solution architecture improvements" on the below section.

![alt text](documents/postnl-event-broker-assessment.png "Solution architecture")

## Architectural components

- **_Self-service portal_**: The back-end service that supports the possibility manage events (create, update, delete, subscribe, list). The
  managers of the events can be also consumers of that events. This back-end is built using [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) and uses the services: AWS APIGateway, AWS Lambda and AWS DynamoDB.

- **_Event Broker infrastructure_**: Infrastructure project which create a stack where includes a AWS APIGateway for producers and a custom event bus on EventBridge. The AWS APIGateway does not include any endpoint becauser all the endpoints will be deployed independently based on producer demand when an even is created (see more details on Producer components generator section)

- **_Event schema backup_**: All the events will be send to EventBridge registery so can be discover by consumers, but they also are saved as json format on a Amazon S3 backup, so we avoid that EventBridge registry is the single point of faiure and we can recreate the registry if it's required.

- **_Componets configuration storage service_**: When a event is created or some consumer subscribe to even through the self service portal, it will generate a deployment file with all the information required to build the components required by producers and consumers. Each of producers and consumers will have specific bucket. All the deployment json files will be use to trigger a new deployment of components. Bellow is detail which compoments are created based on deployment.

- **_Producer components generator_**: [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) app which creates a stack of constructs with the main components for producers. There are two main types of producers: HTTPProducer and SQSProducer.

- **_Consumer components generator_**: [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) app which creates a stack of cosntructs with the main components for consumers. Possible Consumers are: LambdaConsumer, SQSConsumer, HTTPConsumer.

# How to install

In the main path of the projects you can find a script called `local_deploy.sh` that will help you to make the local deployment
of all the components in your own AWS Account:

- Initial requirements:
  - Make sure you have an AWS Account create
  - Make sure that you have a IAM profile setup in your local machine
  - Run `chmod +x local_eploy.sh` to make the file executabler
  - Make sure that you have install in you local machine SAM CLI and CDK CLI.

## Deployment script steps

General notes:

- All the stacks and services follow the same naming convention. On company environment the name can be more fine grane created
  adding the system, subsystem and team owner of the service. In this case for simplicity, the environment and dash for each component
  the name.

### Step 1: Creating schema backup bucket

The first step of the script is created an auxiliary bucket to store the events created on the service portal. Thisis created
just as support mechanism in case on disaster, so the registry is deleted and needs to be recreated with all the events.

**_Artifacts created_**:

- Stack name: `{enviroment}-event-schemas-backup-service`
- Bucket name: `{enviroment}-event-schemas-backup-bucket`

Notes:

- Name of those buckets are not dynamic except of the environment, so can be use the same name for other services.
- After using the self-service portal if you want to restart the infrastructure from scratch you will need to
  to delete first all its content

### Step 2: Creating configuration storage buckets

In the second step of the script is created a stack that contains two buckets which will contain the deployment configuration for the
components the architecture will create automatically for consumers and producers after a producer creates an event or a consumer
subscribe to an event through the service portal

**_Artifacts created_**:

- Stack name: `{enviroment}-components-configuration-storage-service`
- Bucket name for procuders: `{enviroment}-publisher-components-bucket`
- Bucket name for consumers: `{enviroment}-subscriber-components-bucket`

Notes:

- Name of those buckets are not dynamic except of the environment, so can be use the same name for other services.
- After using the self-service portal if you want to restart the infrastructure from scratch you will need to
  to delete first all its content

### Step 3: Event broker insfrastructure

In the third step we are going to create the infrastructure to insject events via API Gateway and one
custom event bus to inject all our events. The current implementation supports HTTP producers. One of the
improvements to be done is to add another type of producers

**_Artifacts created_**:

Stack name for the API Gateway: `{enviroment}-event-broker-api-service`
Stack name for event bus: `{environment}-event-broker-bus`
Broker bus: `{environment}.custom.events.bus`
API Gateway + Lamda injector: `{environment}-event-broker-api`

Notes:

- API Gateway does not have any resource associated because all the producers will create their own
  set of components base on the creation of the events on the self sevice portal.

### Step 4: Deploy the Self service portal

In the fourth step we need to depoy the service that interacts with the users to manage their events.
This application used AWS SAM and uses the buckets and objects that we created on the previous steps

**_Artifact created_**:

Stack name: `{enviroment}-self-service-portal`
API Gateway: `{environment}-self-service-portal-api`
DynamoDBTable: `{environment}-self-service-events-table`

## Full demo example

1. The first step is the self service portal. We can create an event with the following endpoint:

### Create events

- Request: `POST /events`
- Request Payload:
  - application (str): Application that creates the request
  - event_type (str): Short representation of the event
  - description (str): Human representation of the event
  - connection_type (enum): The type of the connection of the producer. Allow types HTTPS, SQS
  - data: JSON Schema representation of the content. that data will be wrap by an envelop before to be store

Example request

```
{
    "application": "demo",
    "event_type": "scanned_parcel",
    "description": "Scanned parcel on the workshop",
    "connection_type": "HTTPS",
    "data": {
        "type": "object",
        "properties": {
            "dest_postal_code": {
                "type": "string"
            },
            "dest_house": {
                "type": "integer"
            },
            "parcel_weight": {
                "type": "number"
            }
        },
        "required": ["dest_postal_code", "dest_house", "parcel_weight"]
    }
}
```

Notes:

- For simplicity it was not taken in consideration authentication of users across the application.
- Before save the event, the self service logic will wrap the content of the event on a full
  JSON Schema with a predifine envolope. This is done because, the only one that should be aware
  about the envolope is the self-service portal. No other application require to know about it. So
  Producers and consumers just consume the events assuming the full schema schema including the envelope.

2. The logic after sending the request is the following:

- The API Gateway validates the body with the mandatory fields
- The data of the event is wrapped on an enveloped.
- Lambda recieve the event and store on the database
- Event is store on the registry. The first creation of the event is always version 1.
- Event is store on the backup
- Event generates the `deploy` script for the producers.

3. Now we can deploy the producer components:

- Download the `deploy.json` script from the producer bucket.
- Copy that file on the `config/` folder on the `producer-components-generator`.
- The stack requires the API_GATEWAY_ID and API_GATEWAY_ROOT_ID of the event broker api
  as parameters of the `cdk deploy`
- This will deploy a stack where contains:

```
HTTP Procesor components

HTTP Model - that corresponds to the JSON Schema of the event
HTTP Resource - /{event_type}/{version}
HTTP Request Validator - All the requests that does not match the schema will be rejected
so we do not need to add extra latency to validate the schema inside of the lambda.
```

After the deployment we will see how we can run the request:

POST {event_broker_api}/scanned_parcel/1
The request payload will need to match the JSON Schema created

If the request is successfull the Lambda will redirect the event to the EventBridge bus

5. Now consumers can subscribe to the `scanned_parcel` event:

### Subscribe event

- Request: `POST /subscriptions`
- Request Payload:
  - event_type (str): Short representation of the event
  - version (str): Version of the event
  - target_unit (str): Unit or department that we want to make sure the event is deliver. This is because
    we do not want to depend only on the event data rules matching. In case that the event is really big
    we do not want to rely on that.
  - connection_type (enum): The type of the connection of the consumer. Allow types HTTPS, LAMBDA, SQS
  - connection_string: ARN of the LAMBA/SQS to send the event. Can be also HTTPS endpoint

Example request

```
{
    "event_type": "scanned_parcel",
    "version": "1",
    "target_unit": "u2",
    "connection_type": "LAMBDA",
    "connection_string": "arn:aws:lambda:{REGION}:{ACCOUNT}:function:my-target-lambda-processor"
}
```

6. The logic after sending the request is the following:

- The API Gateway validates the body with the mandatory fields
- The configuration of the subscription is store on the database. It is not taken in consideration validation against
  event existance
- Generates the `deploy` script for the consumer.

7. Now we can deploy the producer components:

- Download the `deploy.json` script from the consumer bucket.
- Copy that file on the `config/` folder on the `consumer-components-generator`.
- The stack requires the ACCOUNT, REGION, EVENT_BUS_NAME as parameters of the `cdk deploy`
- This will deploy a stack where contains:

```
Lambda Consumer components

EventBrige rule - matches the target on the detail of the event and the detail_type. The detail type will contain
embeed the version of the event.
Lambda target of the rule - If the event matches the rule the event is redirect to the lambda
```

8. Finally we can go to the event broker API and produce events with POST /scanned/parcel that should
   with the full payload of the event. The event should pass the JSON Schema validation and should also
   match the rules of any consumer for EventBridge to redirect the event

## Considerations

- This solution design does not take in consideration certain things for simplicity:
  - It does not include a build pipelie for the components. The ideal candidate is when the event is generated, call a Step Functions
    workflow where one of the steps is the cdk project of the consumer or the producer. The projects are already
    prepare for that since we have the deploy json and the process of using it. Ideally the build process needs to be done
    on the AWS Code build.
- Authorization of the API's (broker and self service): Both API can be added authorization with Custom Lambda
  Authorizers or using Cognito as authentication provider.
- Event Bridge can process top 10.000 events per second. In order to manage a peak of 20.000 we can do:
  - Create a SQS queue for injection of messsages. This will increase the latency of the events on peak times,
    but it will not throttle the system. We need to take in consideration as well increasing the concurrency of the lambda
    injector.
- Another aspect to take in consideration is the payload of the event. This solution desing does not includes
  the case that the payload is bigger than 256 KB which is the quota of the limit of the event. In that case the lambda
  injector will need to send the payload to the S3 and replace the content of the data payload for a S3 link. The consumers
  does not rely on the data for the event matching but on the target, so, they can open the S3 and enrich the event on
  consumption time.
- Monitoring. The monitoring can be seen on the main matrics on thje CloudWatch since we can see the bus and the rule for
  certain event and version. It's important to take in account the limit of 100 rules per bus and limit of 300 buses. Depending
  on the use case we need to go for a multi bus model and the architecture will need to include a way to integrate different
  buses on the flow.

## Pricing

### Self-Service portal

For simplicty we will assume that we will receive 1000 million requests month:

**_API Gateway_**
Depending on the number of requests base on changes on the events. The standard price for a REST API is:
First 333 million / month -> $3.50. Because is unlikely that the self service portal pass the quote, the total
price will be $3.50
**_Lambda executions (each lambda will receive an average of 300k requests)._**
We have 3 lambdas

- Monthly compute charges. We assume that we assign to the lambda 1536MB
  The monthly compute price is $0.0000166667 per GB-s and the free tier provides 400,000 GB-s.
Total compute (seconds) = 0.3 million * 120ms = 36,000 seconds
Total compute (GB-s) = 36,000 * 1536MB/1024 MB = 35,000 GB-s
Total compute – Free tier compute = monthly billable compute GB- s
35,000 GB-s – 400,000 free tier GB-s = Part of the free tier
Monthly compute charges = Part of free tier so 0$
- Monthly request charges
  The monthly request price is $0.20 per one million requests and the free tier provides 1 million requests per month.
Total requests – Free tier requests = monthly billable requests
0.3 million requests – 1 million free tier requests = We will still be in free tier so 0$
- DynamoDB
  We can assume that we use eventual consistency requests for WCU and RCU
  The payload is not going to exceed on the 1MB
  For simplicity, assume that your consumed capacity remains constant at 80 RCUs and 80 WCUs. Your table also remains provisioned for 114 WCUs and 114 RCUs, with a daily charge of $2.1341, broken out as:
  114 WCUs x $0.00065 per hour x 24 hours = $1.7784
  114 RCUs x $0.00013 per hour x 24 hours = $0.3557
  For the month, you are charged $64.04
  The AWS Free Tier includes 25 WCUs and 25 RCUs for tables using the DynamoDB Standard table class, reducing your monthly bill by $14.04:
  25 WCUs x $0.00065 per hour x 24 hours x 30 days = $11.70
  25 RCUs x $0.00013 per hour x 24 hours x 30 days = $2.34
  Data storage: Assume your table occupies 25 GB of storage at the beginning of the month and grows to 29 GB by the end of the month, averaging 27 GB based on the continuous monitoring of your table size. Since your table class is set to DynamoDB Standard, the first 25 GB of storage are included in the AWS Free Tier. The remaining 2 GB of storage are charged at $0.25 per GB, resulting in a table storage cost of $0.50 for the month.
  Total = $64.04 - ($11.70 + $2.34) + $0.50

### Buckets (schema backup and deployment configuration)

We have three S3 buckets:
Storage will be close 0 becaause the json files will be very small
For put and get objects wher have:
PUT - (per 1,000 requests) - $0.0053
GET - (per 1,000 requests) - $0.00042
For the backup will pay for the puts but not for gets at less we have some disaster recovery

### Event Bridge

**_API Gateway of the broker_**
In the peak we have 20k per second -> 1.2M per minute -> 72M per hour -> 1728M month
First 333 million $3.50
Next 667 million $3.33
So the price will start from $3.50 and going down to $3.33

**_Lambda injestor_**
Monthly compute charges

The monthly compute price is $0.0000166667 per GB-s and the free tier provides 400,000 GB-s.
Total compute (seconds) = 1728M million _ 120ms = 207,360 seconds
Total compute (GB-s) = 207,360 _ 1536MB/1024 MB = 311,040 GB-s
Total compute – Free tier compute = monthly billable compute GB- s
311,040 GB-s – 400,000 free tier GB-s = Part of the free tier

Monthly request charges

The monthly request price is $0.20 per one million requests and the free tier provides 1 million requests per month.
Total requests – Free tier requests = monthly billable requests
1728M requests – 1 million free tier requests = 1727M million monthly billable requests
Monthly request charges = 1727M \* $0.2/M = $345

Total monthly charges
Total charges = Compute charges + Request charges = $345 per month

**\*Event bridge**
Monthly events = 1727M events (all equal to or less than 64 KB each) Assuming each request transform in an event
Monthly events charges = 1727M \* $1.00/M = $1727 per month
