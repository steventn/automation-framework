import pytest
from moto import mock_aws
from .s3_service import SimpleS3Service

# Fixtures
@pytest.fixture
def aws_credentials():
    """Mock AWS credentials for moto"""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture
def s3_service(aws_credentials):
    """Provide S3Service instance"""
    return SimpleS3Service()


@pytest.fixture
def test_bucket():
    """Test bucket name"""
    return "my-test-bucket"


@pytest.fixture
def test_file():
    """Test file name"""
    return "test.txt"


@pytest.fixture
def test_content():
    """Test file content"""
    return "Hello, S3 World!"


# Test Class using Fixtures
@mock_aws
class TestS3WithFixtures:

    def test_create_bucket_success(self, s3_service, test_bucket):
        """Test creating a bucket works"""
        result = s3_service.create_bucket(test_bucket)
        assert result is True

        # Check bucket exists in list
        buckets = s3_service.list_buckets()
        assert test_bucket in buckets

    def test_upload_and_download_file(self, s3_service, test_bucket, test_file, test_content):
        """Test uploading and downloading a file"""
        # Create bucket first
        s3_service.create_bucket(test_bucket)

        # Upload file
        upload_result = s3_service.upload_file(test_bucket, test_file, test_content)
        assert upload_result is True

        # Download and verify content
        downloaded_content = s3_service.download_file(test_bucket, test_file)
        assert downloaded_content == test_content

    def test_download_nonexistent_file(self, s3_service, test_bucket):
        """Test downloading a file that doesn't exist"""
        s3_service.create_bucket(test_bucket)

        result = s3_service.download_file(test_bucket, "ghost-file.txt")
        assert result is None

    def test_list_buckets(self, s3_service):
        """Test listing multiple buckets"""
        # Create several buckets
        buckets = ["bucket-a", "bucket-b", "bucket-c"]
        for bucket in buckets:
            s3_service.create_bucket(bucket)

        # List and verify
        bucket_list = s3_service.list_buckets()
        for bucket in buckets:
            assert bucket in bucket_list

    def test_delete_bucket(self, s3_service, test_bucket, test_file, test_content):
        """Test bucket deletion"""
        # Create bucket with a file
        s3_service.create_bucket(test_bucket)
        s3_service.upload_file(test_bucket, test_file, test_content)

        # Delete bucket
        result = s3_service.delete_bucket(test_bucket)
        assert result is True

        # Verify it's gone
        buckets = s3_service.list_buckets()
        assert test_bucket not in buckets

    def test_upload_to_nonexistent_bucket(self, s3_service, test_file, test_content):
        """Test uploading to a bucket that doesn't exist"""
        result = s3_service.upload_file("non-existent-bucket", test_file, test_content)
        assert result is False


# Function-style tests with fixtures
@mock_aws
def test_simple_workflow_with_fixtures(s3_service, test_bucket, test_file, test_content):
    """Test complete S3 workflow using fixtures"""
    # Create bucket
    assert s3_service.create_bucket(test_bucket) is True

    # Upload file
    assert s3_service.upload_file(test_bucket, test_file, test_content) is True

    # Download file
    content = s3_service.download_file(test_bucket, test_file)
    assert content == test_content

    # Clean up
    assert s3_service.delete_bucket(test_bucket) is True


@mock_aws
def test_multiple_files_same_bucket(s3_service, test_bucket):
    """Test multiple files in the same bucket"""
    s3_service.create_bucket(test_bucket)

    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    # Upload all files
    for filename, content in files.items():
        assert s3_service.upload_file(test_bucket, filename, content) is True

    # Verify all files
    for filename, expected_content in files.items():
        downloaded = s3_service.download_file(test_bucket, filename)
        assert downloaded == expected_content


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


@mock_aws
def test_with_pre_populated_bucket(s3_service, pre_populated_bucket, test_file, test_content):
    """Test using a pre-populated bucket fixture"""
    bucket_name = pre_populated_bucket

    # Bucket should already exist with our file
    content = s3_service.download_file(bucket_name, test_file)
    assert content == test_content

    # We can also add more files
    assert s3_service.upload_file(bucket_name, "new_file.txt", "new content") is True


if __name__ == "__main__":
    # You can still run this directly
    print("Running S3 tests with fixtures...")

    # Test the fixtures manually
    with mock_aws():
        # Create fixtures manually
        import os

        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'

        service = SimpleS3Service()
        bucket = "manual-test-bucket"
        service.create_bucket(bucket)
        service.upload_file(bucket, "manual.txt", "Manual test content")
        content = service.download_file(bucket, "manual.txt")
        print(f"Downloaded content: {content}")
        service.delete_bucket(bucket)

        print("✅ All fixture tests passed!")