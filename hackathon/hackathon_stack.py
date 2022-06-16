from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_apigatewayv2_alpha as gateway,
    aws_apigatewayv2_integrations_alpha as lambda_integration,
    aws_lambda as _lambda,
    aws_iam

)
from constructs import Construct


class HackathonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        layer = _lambda.LayerVersion(self, 'lambda-lib',
                                     code=_lambda.Code.from_asset('code/common_lib/'),
                                     compatible_runtimes=[_lambda.Runtime.PYTHON_3_8])

        comprehend_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                'comprehend:*',
            ],
            resources=["*"]
        )

        pii_checker = _lambda.Function(self, 'pii_checker_func',
                                       code=_lambda.Code.from_asset('code/pii_checker'),
                                       handler='pii_checker.handler',
                                       runtime=_lambda.Runtime.PYTHON_3_8,
                                       function_name='pii_checker_func',
                                       layers=[layer],
                                       initial_policy=[comprehend_policy]
                                       )

        pii_integration = lambda_integration.HttpLambdaIntegration(
            'pii_function_integration',
            handler=pii_checker
        )

        pii_gateway = gateway.HttpApi(self, "PIIGateway",
                                      cors_preflight=gateway.CorsPreflightOptions(
                                          allow_headers=['Content-Type', 'Authorization'],
                                          allow_methods=[gateway.HttpMethod.POST, gateway.HttpMethod.GET,
                                                         gateway.HttpMethod.PUT, gateway.HttpMethod.OPTIONS,
                                                         gateway.HttpMethod.DELETE],
                                          # allow_origins=['http://localhost.com']
                                      ))
        pii_gateway.add_routes(
            path="/pii/check",
            methods=[gateway.HttpMethod.POST],
            integration=pii_integration
        )
