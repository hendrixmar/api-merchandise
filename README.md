# Merchandise Sales API




This API that can be use for building point of sale completely serverless it is build with
the following cloud technologies

- AWS
- Lambda
- API Gateway
- RDS PostgreSql
- Secret manager
-

## Credentials
Before you can deploy an application, be sure you have credentials configured. If you have previously configured your machine to run boto3 (the AWS SDK for Python) or the AWS CLI then you can skip this section.

If this is your first time configuring credentials for AWS you can follow these steps to quickly get started:
```sh
$ mkdir ~/.aws
$ cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as us-west-2, us-west-1, etc)
```

## Quickstart



First, you'll need to install the AWS CDK if you haven't already.
The CDK requires Node.js and npm to run.

```sh
$ npm install -g aws-cdk
```

Next you'll need to install the requirements for the project.

```
$ pip install -r requirements.txt
```

There's also separate requirements files in the `infrastructure`
and `backend` directories if you'd prefer to have separate virtual
environments for your CDK and Chalice app.


To deploy the application, `cd` to the `infrastructure` directory.
If this is you're first time using the CDK you'll need to bootstrap
your environment.

```
$ cdk bootstrap
```

Then you can deploy your infrastructure using the CDK.

```
$ cdk deploy
```

Now `cd` into the `backend` folder and then you can deploy your application using Chalice.

```
$ chalice deploy --stage prod
```
