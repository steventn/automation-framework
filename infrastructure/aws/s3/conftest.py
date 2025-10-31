import pytest
import os
from moto import mock_aws


@pytest.fixture
def s3_service():
    """Provide S3Service instance"""
    from .s3_service import SimpleS3Service
    return SimpleS3Service()

@pytest.fixture
def test_bucket():
    return "my-test-bucket"

@pytest.fixture
def test_file():
    return "test.txt"

@pytest.fixture
def test_content():
    return "Hello, S3 World!"

@pytest.fixture
def bucket_with_file(s3_service, test_bucket, test_file, test_content):
    """Create a bucket with a file, automatically cleaned up"""
    with mock_aws():
        s3_service.create_bucket(test_bucket)
        s3_service.upload_file(test_bucket, test_file, test_content)
        yield test_bucket
        s3_service.delete_bucket(test_bucket)

# Fixture with setup and teardown
@pytest.fixture
def pre_populated_bucket(s3_service, test_bucket, test_file, test_content):
    """Fixture that creates a bucket with a file and cleans up after"""
    with mock_aws():
        # Setup
        s3_service.create_bucket(test_bucket)
        s3_service.upload_file(test_bucket, test_file, test_content)

        yield test_bucket  # This is what tests receive

        # Teardown (runs after test completes)
        s3_service.delete_bucket(test_bucket)

@pytest.fixture(autouse=True)
def safe_aws_credentials():
    """
    SECURITY PRACTICE DEMO:
    - In production, credentials would come from AWS Secrets Manager
    - For testing, we use moto's safe test credentials
    - NEVER hardcode real AWS credentials
    """
    # Store original values
    original_env = {
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY')
    }

    # Use safe test credentials
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    yield

    # Restore original environment
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        elif key in os.environ:
            del os.environ[key]