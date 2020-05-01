from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class AppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lets create couple of instances to test
        vpc = ec2.Vpc(
                self, "abacVPC",
                cidr="10.13.0.0/21",
                max_azs=2,
                nat_gateways=0,
                subnet_configuration=[
                    ec2.SubnetConfiguration(name="pubSubnet", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC)
                ]
            )
        
        # Tag all VPC Resources
        core.Tag.add(vpc,key="Owner",value="KonStone",include_resource_types=[])
        core.Tag.add(vpc,key="teamName",value="teamUnicorn",include_resource_types=[])

        # We are using the latest AMAZON LINUX AMI
        ami_id = ec2.AmazonLinuxImage(generation = ec2.AmazonLinuxGeneration.AMAZON_LINUX_2).get_image(self).image_id
        
        red_web_inst = ec2.CfnInstance(self,
            "redWebInstance01",
            image_id = ami_id,
            instance_type = "t2.micro",
            monitoring = False,
            tags = [
                { "key": "teamName", "value": "teamUnicorn" },
                { "key": "projectName", "value": "projectRed" },
                { "key": "Name", "value": "projectRed-Web" }
            ],
            network_interfaces = [{
                "deviceIndex": "0",
                "associatePublicIpAddress": True,
                "subnetId": vpc.public_subnets[0].subnet_id,
                # "groupSet": [web_sg.security_group_id]
            }], #https: //github.com/aws/aws-cdk/issues/3419
        )
        # core.Tag.add(red_web_inst,key="Owner",value="KonStone",include_resource_types=[])