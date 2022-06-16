from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_kinesisfirehose as firehose,
    aws_lambda as _lambda

)

import path as path
import aws_cdk.aws_kinesisfirehose_alpha as firehose
import aws_cdk.aws_kms as kms
import aws_cdk.aws_lambda_nodejs as lambdanodejs
import aws_cdk.aws_logs as logs
import aws_cdk.aws_s3 as s3
import aws_cdk as cdk
import aws_cdk.aws_kinesisfirehose_destinations_alpha as destinations

from constructs import Construct


class FirehoseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "PII-Bucket",
                           removal_policy=cdk.RemovalPolicy.DESTROY,
                           auto_delete_objects=True
                           )

        backup_bucket = s3.Bucket(self, "PII-BackupBucket",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  auto_delete_objects=True
                                  )
        log_group = logs.LogGroup(stack, "PII-LogGroup",
                                  removal_policy=cdk.RemovalPolicy.DESTROY
                                  )

        # The code that defines your stack goes here
        layer = _lambda.LayerVersion(self, 'lambda-lib',
                                     code=_lambda.Code.from_asset('code/common_lib/'),
                                     compatible_runtimes=[_lambda.Runtime.PYTHON_3_8])

        data_processor_function = _lambda.Function(self, 'pii_checker_func',
                                                   code=_lambda.Code.from_asset('code/pii_checker'),
                                                   handler='pii_checker.handler',
                                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                                   function_name='pii_checker_func',
                                                   layers=[layer]
                                                   )

        processor = firehose.LambdaFunctionProcessor(data_processor_function,
                                                     buffer_interval=cdk.Duration.seconds(60),
                                                     buffer_size=cdk.Size.mebibytes(1),
                                                     retries=1
                                                     )

        key = kms.Key(self, "PII-Key",
                      removal_policy=cdk.RemovalPolicy.DESTROY
                      )

        backup_key = kms.Key(self, "PII-BackupKey",
                             removal_policy=cdk.RemovalPolicy.DESTROY
                             )

        firehose.DeliveryStream(self, "PII-Delivery Stream",
                                destinations=[destinations.S3Bucket(bucket,
                                                                    logging=True,
                                                                    log_group=log_group,
                                                                    processor=processor,
                                                                    compression=destinations.Compression.GZIP,
                                                                    data_output_prefix="regularPrefix",
                                                                    error_output_prefix="errorPrefix",
                                                                    buffering_interval=cdk.Duration.seconds(60),
                                                                    buffering_size=cdk.Size.mebibytes(1),
                                                                    encryption_key=key,
                                                                    s3_backup=destinations.DestinationS3BackupProps(
                                                                        mode=destinations.BackupMode.ALL,
                                                                        bucket=backup_bucket,
                                                                        compression=destinations.Compression.ZIP,
                                                                        data_output_prefix="backupPrefix",
                                                                        error_output_prefix="backupErrorPrefix",
                                                                        buffering_interval=cdk.Duration.seconds(60),
                                                                        buffering_size=cdk.Size.mebibytes(1),
                                                                        encryption_key=backup_key
                                                                    )
                                                                    )]
                                )
