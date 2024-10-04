import unittest
from moto import mock_secretsmanager, mock_rds
import boto3
import json
from aws_utils import discover_rds_secret_name, get_rds_credentials, get_rds_endpoint_and_dbname

class TestAWSUtils(unittest.TestCase):

    @mock_secretsmanager
    def test_discover_rds_secret_name(self):
        """Test the discovery of the RDS secret name."""
        # Create a mock Secrets Manager client
        client = boto3.client("secretsmanager", region_name="us-east-1")
        
        # Mock secret creation in Secrets Manager
        secret_name = "rds/test-secret"
        db_instance_identifier = "test-db-instance"
        client.create_secret(Name=secret_name, SecretString=json.dumps({"username": "test", "password": "test"}), Description=db_instance_identifier)

        # Call the function to test
        discovered_secret = discover_rds_secret_name(db_instance_identifier)
        self.assertEqual(discovered_secret, secret_name)

    @mock_secretsmanager
    def test_get_rds_credentials(self):
        """Test fetching RDS credentials from Secrets Manager."""
        # Create a mock Secrets Manager client
        client = boto3.client("secretsmanager", region_name="us-east-1")
        
        # Mock secret creation in Secrets Manager
        secret_name = "rds/test-secret"
        secret_value = json.dumps({"username": "test", "password": "test"})
        client.create_secret(Name=secret_name, SecretString=secret_value)

        # Call the function to test
        credentials = get_rds_credentials(secret_name)
        self.assertEqual(credentials["username"], "test")
        self.assertEqual(credentials["password"], "test")

    @mock_rds
    def test_get_rds_endpoint_and_dbname(self):
        """Test fetching the RDS endpoint and DB name."""
        # Create a mock RDS client with a supported region
        client = boto3.client("rds", region_name="us-east-1")
    
        # Mock RDS instance creation
        db_instance_identifier = "test-db-instance"
        client.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass='db.t2.micro',
            Engine='postgres',
            DBName='testdb',
            MasterUsername='test',
            MasterUserPassword='password',
            AllocatedStorage=20  # This is required for the mock to succeed
        )
    
        # Call the function to test
        endpoint, db_name = get_rds_endpoint_and_dbname(db_instance_identifier)
    
        # Assertions
        self.assertTrue(endpoint.startswith('test-db-instance'))
        self.assertIn('.rds.amazonaws.com', endpoint)
        self.assertEqual(db_name, 'testdb')


if __name__ == '__main__':
    unittest.main()