# Lambda function to extract image from S3 bucket

## Steps

1. Create a basic execution role [[**Steps**]](https://github.com/yashrajdighe/aws/tree/main/lambda#to-create-a-basic-lambda-execution-role-follow-the-below-steps-or-click-here)
2. Add the **AmazonS3ReadOnlyAccess** permission policy in the above role to provide the S3 Read Only Access to lambda function.
3. Open [[AWS Lambda]](https://us-east-1.console.aws.amazon.com/lambda/) console.
4. Click on **Create Function**.
5. Select **Author from scratch**.
6. Enter **Function name**.
7. Select **Runtime** to **python 3.9**.
8. Select **Architecture** as **arm64**.
9. In **Permissions** section, select **Use an existing role** and select the role you created above for this lambda function.
10. Finally click on **Create Function**.
11. In the code editor shown  on next screen, paste the below code
    ```python
    import os
    import json
    import base64
    import boto3

    def lambda_handler(event, context):
        try:
            bucket_name = event["queryStringParameters"]["BUCKET_NAME"]
            if event and bucket_name:
                return extract_image_from_s3_bucket(event, bucket_name)
            else:
                return {
                    "statusCode": 500,
                    "body": json.dumps("Invalid invocation or Bucket name is not defined!"),
                }

        except Exception as e:
            return {"statusCode": 500, "body": json.dumps("Error processing the request!")}


    def extract_image_from_s3_bucket(event, bucket_name):
        s3 = boto3.client("s3")
        folder_name = event["queryStringParameters"]["FOLDER_NAME"]
        file_name = event["queryStringParameters"]["IMAGE_NAME"]

        fileObj = s3.get_object(
            Bucket=bucket_name, Key=f"{folder_name}/{file_name}"
        )
        file_content = fileObj["Body"].read()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/jpg"
                # "Content-Disposition": "attachment; filename={}".format(file_name),
            },
            "body": base64.b64encode(file_content),
            "isBase64Encoded": True,
        }

    ```
    #### Note: In the above code, if you want the image should be downloaded instead of rendered in browser page, you can uncomment the **Content-Deposition** header in return statement.
12. Click on **Deploy**.
13. After the function is deployed, click on **Configurations** tab.
14. Click on **Function URL**.
15. Click on **Create Function URL**.
16. For this function, select **Auth type** as **NONE**, and click on **SAVE**
17. Now your function is deployed and ready to be tested.
18. Copy the **Function URL** and add the params (BUCKET_NAME, FOLDER_NAME and IMAGE_NAME) in url as below and update the params as per your need:
    ```console
    https://kdpqevgf5d2dcgedicjswnnlbu0pqnrk.lambda-url.us-east-1.on.aws/?BUCKET_NAME=aws-lambda-images-s3&FOLDER_NAME=public-images&IMAGE_NAME=code.jpg
    ```