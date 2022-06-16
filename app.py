#!/usr/bin/env python3
import os

import aws_cdk as cdk

from hackathon.hackathon_stack import HackathonStack
from hackathon.firehose_stack import FirehoseStack


app = cdk.App()
HackathonStack(app, "HackathonStack")
FirehoseStack(app, "FirehoseStack")

app.synth()
