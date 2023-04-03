import os

from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway)
from aws_cdk import aws_ssm as ssm
from aws_cdk.aws_apigateway import (
    ApiKey,
    UsagePlan,
    RestApi,
    ThrottleSettings,
    LambdaIntegration)
from aws_cdk.aws_ecr import Repository
from constructs import Construct


class {{ cookiecutter.application_name }}Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        image_tag = os.getenv("IMAGE_TAG", "latest")
        {{ cookiecutter.safe_name }}_ecr_image = _lambda.DockerImageCode.from_ecr(
            repository=Repository.from_repository_name(self,
                                                       "{{ cookiecutter.lambda_slug }}-repository",
                                                       "{{ cookiecutter.lambda_slug }}"),
            tag_or_digest=image_tag
        )
        {{ cookiecutter.safe_name }}_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="{{ cookiecutter.lambda_slug }}-lambda",
            # Function name on AWS
            function_name="{{ cookiecutter.lambda_slug }}",
            # Use aws_cdk.aws_lambda.DockerImageCode.from_image_asset to build
            # a docker image on deployment
            code={{ cookiecutter.safe_name }}_ecr_image,
        )

        {{ cookiecutter.safe_name }}_api = apigateway.LambdaRestApi(self, "{{ cookiecutter.lambda_slug }}-api",
                                                        rest_api_name="{{ cookiecutter.lambda_name }}",
                                                        handler={{ cookiecutter.safe_name }}_lambda,
                                                        proxy=False)

        {{ cookiecutter.safe_name }}_resource = {{ cookiecutter.safe_name }}_api.root.add_resource("/")
        {{ cookiecutter.safe_name }}_resource.add_method("GET")
