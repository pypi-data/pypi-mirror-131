import json
from unittest import mock

from b_aws_cf_response.cfresponse import CfResponse


@mock.patch('urllib3.PoolManager')
def test_FUNC_respond_WITH_valid_resource_provider_event_EXPECT_response_successful(mock_cfresponse) -> None:
    class CustomResourceContext:
        """
        Dummy custom resource context object with the property log_stream_name.
        """
        @property
        def log_stream_name(self):
            return 'fake_log_stream_name'

    # Dummy custom resource creation request event.
    custom_resource_event = {
        'RequestType': 'Create',
        'ResponseURL': 'http://pre-signed-S3-url-for-response',
        'StackId': 'arn:aws:cloudformation:eu-central-1:123456789012:stack/stack-name/guid',
        'RequestId': 'unique id for this create request',
        'ResourceType': 'Custom::TestResource',
        'LogicalResourceId': 'MyTestResource',
        'ResourceProperties': {
            'Name': 'Value',
            'List': [1, 2, 3]
        }
    }

    # Creating dummy resource.
    customer_resource_context = CustomResourceContext()
    resource_id = 'unique-id-of-created-dummy-resource'
    resource_data = {
        'name': 'value',
        'list': [1, 2, 3]
    }

    # Instantiating a CfResponse class with dummy custom resource event and dummy context object.
    response = CfResponse(custom_resource_event, customer_resource_context)

    # Trying to send response about successful dummy resource creation.
    response.respond(
        status=CfResponse.CfResponseStatus.SUCCESS,
        resource_id=resource_id,
        data=resource_data
    )

    # Expected response body to be sent.
    expected_response_body = {
        'Status': 'SUCCESS',
        'Reason': f'See the details in CloudWatch: {customer_resource_context.log_stream_name}.',
        'PhysicalResourceId': resource_id,
        'StackId': custom_resource_event['StackId'],
        'RequestId': custom_resource_event['RequestId'],
        'LogicalResourceId': custom_resource_event['LogicalResourceId'],
        'NoEcho': False,
        'Data': resource_data
    }

    cfresponse = mock_cfresponse.return_value

    # Checking does CfResponse http request was called with expected parameters.
    cfresponse.request.assert_called_with(
        'PUT',
        custom_resource_event['ResponseURL'],
        body=json.dumps(expected_response_body),
        headers={'Content-Type': 'application/json'}
    )
