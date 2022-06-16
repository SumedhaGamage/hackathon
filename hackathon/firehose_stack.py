from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_kinesisfirehose as firehose

)
from constructs import Construct


class FirehoseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Add Firehose stack code here
        