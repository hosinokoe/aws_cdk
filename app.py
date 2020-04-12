#!/usr/bin/env python3

from aws_cdk import core

# from aws_cdk.aws_cdk_stack import AwsCdkStack
from aws_cdk.cdk_vpc_stack import CdkVpcStack


app = core.App()
# AwsCdkStack(app, "aws-cdk")
vpc_stack = CdkVpcStack(app, "cdk-vpc")

app.synth()
