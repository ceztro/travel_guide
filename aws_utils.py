import boto3
import json
import os

def discover_rds_secret_name(db_instance_identifier, region_name="us-east-1"):
    """
    Discovers the name of the AWS-managed RDS secret by filtering for 'rds' and the db_instance_identifier.

    :param db_instance_identifier: The DB instance identifier of the RDS instance.
    :param region_name: The AWS region where the secret is stored.
    :return: The name of the AWS-managed RDS secret.
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Search for secrets that contain "rds" in the name and the db_instance_identifier
        response = client.list_secrets(
            Filters=[
                {"Key": "name", "Values": ["rds"]}
            ]
        )
        
        # Filter the list of secrets to find the one that matches the db_instance_identifier
        for secret in response["SecretList"]:
            if db_instance_identifier in secret["Description"]:
                return secret["Name"]
        
        # Raise an exception if no secret is found
        raise Exception(f"No secret found for RDS instance: {db_instance_identifier}")
    
    except Exception as e:
        print(f"Failed to discover RDS secret name: {e}")
        raise


def get_rds_credentials(secret_name, region_name="us-east-1"):
    """
    Fetches RDS credentials (username, password) from AWS Secrets Manager.

    :param secret_name: The name of the AWS-managed secret stored in Secrets Manager.
    :param region_name: The AWS region where the secret is stored.
    :return: A dictionary containing the RDS credentials (username and password).
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)
    except Exception as e:
        print(f"Failed to retrieve secret: {e}")
        raise


def get_rds_endpoint_and_dbname(db_instance_identifier, region_name="us-east-1"):
    """
    Fetches the endpoint (host) and DB name of the RDS instance using boto3.

    :param db_instance_identifier: The DB instance identifier of the RDS instance.
    :param region_name: The AWS region where the RDS instance is running.
    :return: A tuple containing the endpoint (host) and the database name.
    """
    session = boto3.session.Session()
    client = session.client(service_name="rds", region_name=region_name)

    try:
        response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        endpoint = response["DBInstances"][0]["Endpoint"]["Address"]
        db_name = response["DBInstances"][0].get("DBName", "postgres")  # Default to 'postgres' if DBName is not set
        return endpoint, db_name
    except Exception as e:
        print(f"Failed to retrieve RDS endpoint or DB name: {e}")
        raise