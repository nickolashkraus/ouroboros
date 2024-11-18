# Ouroboros

Ouroboros (ˌyo͝orəˈbôrəs) simplifies AWS Lambda function deployments.

>The ouroboros is an ancient symbol depicting a serpent or dragon eating its own tail. Originating in ancient Egyptian iconography, the ouroboros entered western tradition via Greek magical tradition and was adopted as a symbol in Gnosticism and Hermeticism and most notably in alchemy. The term derives from Ancient Greek: οὐροβόρος, from οὐρά (oura), "tail" + βορά (bora), "food", from βιβρώσκω (bibrōskō), "I eat".

## Overview

Ouroboros solves a common problem:

>*It is impossible to deploy a Lambda function and the S3 bucket where it is located in the same CloudFormation template at the same time.*

## A classic chicken and egg problem

There are two ways to deploy a Lambda function using CloudFormation:

1. Inline
2. Using Amazon S3

### Inline

For Node.js and Python functions, you can specify the function code inline in the template. This can be accomplished by using the [*literal style*](https://yaml.org/spec/1.2/spec.html#id2795688) block indicator (`|`).

### Using Amazon S3

Additionally, you can specify the location of a deployment package in Amazon S3. This is where a Lambda deployment can become cumbersome, as it is impossible to define a Lambda function resource *and* the S3 bucket from which the Lambda function deployment package is retrieved in the same CloudFormation template.

Instead, you must first deploy the CloudFormation stack with the S3 bucket, put the Lambda function deployment package in the S3 bucket, then specify the S3 bucket and object key in the CloudFormation template for the Lambda function resource before deploying the template again.

## Solutions

### The Wrong Way

In the past, I solved this problem using the following methodology:

1. Create an AWS Lambda function using [`Zipfile`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile) and the deployment S3 bucket:

```bash
LambdaFunction:
  Type: AWS::Lambda::Function
  Properties:
    Code:
      # S3Bucket: !Ref LambdaS3Bucket
      # S3Key: 'lambda_function.zip'
      # Use ZipFile to address 'chicken and egg' problem
      ZipFile: |
        def handler(event, context):
          return

LambdaS3Bucket:
  Type: AWS::S3::Bucket
  Properties:
    AccessControl: AuthenticatedRead
    BucketName: '${AWS::StackName}-lambda'
    VersioningConfiguration:
      Status: Enabled
```

**Note**: The deployment S3 bucket is commented out for the first deployment.

2. Deploy the CloudFormation stack:

```bash
aws cloudformation deploy \
--stack-name $STACK_NAME \
--template-file template.yaml \
--parameter-overrides $(cat parameters.properties)
```

3. Deploy the AWS Lambda function to the deployment S3 bucket:

```bash
aws s3api put-object \
--body lambda_function.zip \
--bucket $STACK_NAME-lambda \
--key lambda_function.zip
```

4. Uncomment the deployment S3 bucket ([`S3Bucket`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3bucket)) in the Lambda function, comment out the `Zipfile`:

```bash
LambdaFunction:
  Type: AWS::Lambda::Function
  Properties:
    Code:
      S3Bucket: !Ref LambdaS3Bucket
      S3Key: 'lambda_function.zip'
      # Use ZipFile to address 'chicken and egg' problem
      # ZipFile: |
      #   def handler(event, context):
      #     return
```

5. Redeploy the CloudFormation stack.

### The Right Way

Just use [Serverless](https://serverless.com)!

## Serverless

Serverless uses the same methodology, but in a seamless, deterministic way. There is no need to execute two initial deploys, Serverless handles this maladroit process transparently for the user.

1. Serverless creates a CloudFormation template with only the deployment S3 bucket and deploys the CloudFormation stack:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
CloudFormation - CREATE_IN_PROGRESS - AWS::CloudFormation::Stack - ouroboros-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::CloudFormation::Stack - ouroboros-dev
Serverless: Stack create finished...
```

2. Serverless packages the AWS Lambda function and uploads the deployment package to S3:

```bash
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service ouroboros.zip file to S3 (11.35 KB)...
```

3. Any IAM Roles, Functions, Events and Resources are added to the AWS CloudFormation template and the CloudFormation stack is updated:

```bash
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
CloudFormation - CREATE_COMPLETE - AWS::CloudFormation::Stack - ouroboros-dev
CloudFormation - UPDATE_IN_PROGRESS - AWS::CloudFormation::Stack - ouroboros-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - MainLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - MainLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - MainLogGroup
CloudFormation - CREATE_COMPLETE - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - MainLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - MainLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - MainLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - MainLambdaVersion5fX9BH08tSq4n71MXtUupggMMFhtLiQsdItUppmFQ
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - MainLambdaVersion5fX9BH08tSq4n71MXtUupggMMFhtLiQsdItUppmFQ
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - MainLambdaVersion5fX9BH08tSq4n71MXtUupggMMFhtLiQsdItUppmFQ
CloudFormation - UPDATE_COMPLETE_CLEANUP_IN_PROGRESS - AWS::CloudFormation::Stack - ouroboros-dev
CloudFormation - UPDATE_COMPLETE - AWS::CloudFormation::Stack - ouroboros-dev
Serverless: Stack update finished...
Service Information
service: ouroboros
stage: dev
region: us-east-1
stack: ouroboros-dev
resources: 5
api keys:
  None
endpoints:
  None
functions:
  main: ouroboros-dev-main
layers:
  None

Stack Outputs
MainLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:185444048157:function:ouroboros-dev-main:2
ServerlessDeploymentBucketName: ouroboros-dev-serverlessdeploymentbucket-1xz8z3cefcmfg

Serverless: Run the "serverless" command to setup monitoring, troubleshooting and testing.
```

Voilà! Painless AWS Lambda function deploys!

## Development

### Installation

#### Serverless

Install Node.js and NPM:

```bash
brew install node
```

Install the Serverless Framework open-source CLI:

```bash
npm install -g serverless
```

#### Python

Create a new virtual environment:

```bash
mkvirtualenv ouroboros
```

Install requirements:

```bash
pip install -r ouroboros/requirements_dev.txt
```

### Deployment

Deploy Ouroboros:

```bash
serverless deploy -v
```

Use [bumpversion](https://pypi.org/project/bumpversion/) to increment the current version:

```
cd ouroboros
bumpversion <major | minor | patch>
```
