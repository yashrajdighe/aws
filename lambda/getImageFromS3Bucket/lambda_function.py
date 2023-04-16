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


# TODO Rename this here and in `lambda_handler`
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
            "Content-Type": "image/jpg" # application/pdf
            # "Content-Disposition": "attachment; filename={}".format(file_name),
        },
        "body": base64.b64encode(file_content),
        "isBase64Encoded": True,
    }
