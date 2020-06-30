#!/usr/bin/env python3

from aws_cdk import core

# from aws_cdk.aws_cdk_stack import AwsCdkStack
from aws_cdk.cdk_vpc_stack import CdkVpcStack
from aws_cdk.cdk_ec2_stack import CdkEc2Stack
from aws_cdk.cdk_vpc_ec2_stack import CdkVpcEc2Stack
# from aws_cdk.cdk_ec2 import AppStack
from aws_cdk.cdk_rds import CdkRdsStack
from aws_cdk.cdk_redis import CdkRedisStack
from aws_cdk.cdk_ecs import MyEcsConstructStack
from aws_cdk.cdk_rds_stack import CdkRDSStack

env = core.Environment(account="456843195142", region="us-east-1")

app = core.App()
# AwsCdkStack(app, "aws-cdk")
vpc_stack = CdkVpcStack(app, "cdk-vpc")
rds_stack = CdkRDSStack(app, "cdk-rds",vpc=vpc_stack.vpc,public_subnet_a=vpc_stack.public_subnet_a,public_subnet_c=vpc_stack.public_subnet_c,public_subnet_d=vpc_stack.public_subnet_d)
# rds_stack = CdkRdsStack(app, "cdk-rds")
# ecs_stack = MyEcsConstructStack(app, "cdk-ecs")
# redis_stack = CdkRedisStack(app, "cdk-redis")
ec2_stack = CdkEc2Stack(app, "cdk-ec2",vpc=vpc_stack.vpc,subnet_id=vpc_stack.public_subnet_a)
# ec2_stack = CdkVpcEc2Stack(app, "cdk-ec2", env=env)
# AppStack(app, "ec2", env=env)



app.synth()
