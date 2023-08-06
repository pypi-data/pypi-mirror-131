# B.AwsCfResponse

A python based library to send response back to
AWS Cloud Formation service after processing of
custom resource request.

#### Description

Sometimes a necessity to write custom AWS resource provisioning logic arises. After processing of
custom resource requests, a resource provider must send the standardized response back to
AWS CloudFormation service. This package makes a response message from a custom resource provider
event and sends a callback to AWS CloudFormation service.

#### Remarks

[Biomapas](https://biomapas.com) aims to modernize life-science
industry by sharing its IT knowledge with other companies and
the community. This is an open source library intended to be used
by anyone. Improvements and pull requests are welcome.

#### Related technology

- Python 3
- AWS CloudFormation

#### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS and CloudFormation.

#### Useful sources

- Read more about Cloud Formation:<br>
  https://docs.aws.amazon.com/cloudformation/index.html

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b-aws-cf-response
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

Create **CfResponse** object using event and context of custom resource provider:

```python
from b_aws_cf_response.cfresponse import CfResponse

response = CfResponse(event, context)
```

After successful provision of custom resource, initiate SUCCESS response. The response can include data from the custom resource provider. For example, created resource name.

```python
# Custom resource provider defined name-value pairs to send with response.
custom_resource_data = {
  'IndexName': 'opensearch-index-name'
}

response.respond(
  status=CfResponse.CfResponseStatus.SUCCESS,
  data=custom_resource_data,
  resource_id=custom_resource_id
)
```

Initiate FAILED response if custom resource provisioning failed.

```python
response.respond(
  status=CfResponse.CfResponseStatus.FAILED,
  status_reason=error_message
)
```

#### Testing

The project has tests that can be run. Simply run:

```
pytest
```

#### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
