#!/usr/bin/env python3

from aws_cdk import core

# from aws_cdk.aws_cdk_stack import AwsCdkStack
from aws_cdk.cdk_vpc_stack import CdkVpcStack
# from aws_cdk.cdk_ec2_stack import CdkEc2Stack
from aws_cdk.cdk_vpc_ec2_stack import CdkVpcEc2Stack
# from aws_cdk.cdk_ec2 import AppStack
from aws_cdk.cdk_rds import CdkRdsStack

env = core.Environment(account="456843195142", region="us-east-1")

app = core.App()
# AwsCdkStack(app, "aws-cdk")
# vpc_stack = CdkVpcStack(app, "cdk-vpc")
rds_stack = CdkRdsStack(app, "cdk-rds")
# ec2_stack = CdkEc2Stack(app, "cdk-ec2",vpc=vpc_stack.vpc,subnet_id=vpc_stack.public_subnet_a)
# ec2_stack = CdkVpcEc2Stack(app, "cdk-ec2", env=env)
# AppStack(app, "ec2", env=env)



app.synth()
