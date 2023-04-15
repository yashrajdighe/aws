# AWS Lambda Function

### Pre-requisites of creating a lambda function
- Create a basic execution role for lambda function (this role allows lambda to upload logs to AWS Cloudwatch)
- Knowledge of creating a function or api using the supported programming languages by AWS Lambda
  - Node Js
  - Typescript
  - Python
  - Java
  - Ruby
  - Go
  - C#
  - Powershell

### To Create a basic lambda execution role, follow the below steps or ([Click Here](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)):
1. Open the **IAM Roles** page in AWS Console
2. Choose **Create Role**
3. Under  **Use Case**, choose **Lambda**
4. Choose **NEXT**
5. Select AWS managed policies **AWSLambdaBasicExecutionRole** and **AWSXRayDaemonWriteAccess**
6. Choose **NEXT**
7. Enter the **Role Name** and choose **Create Role**