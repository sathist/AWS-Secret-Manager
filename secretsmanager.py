import boto3
import sys
from botocore.exceptions import ClientError

"Secret Name and Application profile fetch from environment variable"

SECRET_NAME = sys.argv[1]
FILE_NAME = sys.argv[2]

def get_secrets():
    "Get Evironment Key and Value from AWS Secret Manager Service"
    client = boto3.client('secretsmanager')

    try:
        response = client.get_secret_value(SecretId = SECRET_NAME)

        try:
            #Convert unicode to Dict
            #Store the key and value pairs in file
            file = open(FILE_NAME, "w")
            e_variables = (response['SecretString'])
            file_content = str(e_variables)
            file.write(file_content)
            print ("Fetched secret Values from " + sys.argv[1])
            return True
        except Exception as error:
            print(error)
            return False

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Requested AWS Secrets Manager " + SECRET_NAME + " was not found")
            return False
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("Request AWS Secrets Manager was invalid due to:\n", str(e))
            return False
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("Request AWS Secrets Manager had invalid params:\n", str(e))
            return False
        elif e.response['Error']['Code'] == 'DecryptionFailureException':
            print ("Reques AWS Secrets Manager had DecryptionFailureException:\n", str(e))
            return False
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            print ("Request AWS Secrets Manager had InternalServiceErrorException:\n", str(e))
            return False
        else:
            print("Unexpected error: %s" % str(e))
            return False
 
def main():
    if not get_secrets():
        sys.exit(1)

if __name__ == "__main__":
    main()