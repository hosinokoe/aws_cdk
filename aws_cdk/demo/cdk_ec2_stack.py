from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_cloudwatch as cw,
    core,
)

# ec2_type = "t3a.nano"
key_name = "stg-intrinio-www01"  # Setup key_name for EC2 instance login 
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class CdkEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prefix = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        volumne_size = self.node.try_get_context("volumne_size")
        ec2_type = self.node.try_get_context("ec2_type")
        # read parameters from SSM
        vpcid = ssm.StringParameter.value_from_lookup(self, "/cdk/ec2/vpc_id")
        # Get the existing VPC
        my_vpc = ec2.Vpc.from_lookup(
            self,
            "VPC",
            vpc_id=vpcid
        )
        
        # self.security_group = ec2.CfnSecurityGroup(
        #     self,
        #     id="web_server_sg",
        #     vpc_id=vpc.ref,
        #     group_name=env_name+'-'+prefix+'-www01',
        #     group_description="Web server security group",
        #     # security_group_ingress=[ingress_ssh],
        #     # security_group_egress=[egress_all],
        #     tags = [core.CfnTag(key="Name", value=env_name+'-'+prefix+'-www01')]
        # )
        
        # public Ingress
        # ec2.CfnSecurityGroupIngress(self, 'publicsecuritygroupingress01', group_id=self.security_group.ref, ip_protocol='tcp', cidr_ip='0.0.0.0/0', description='http', from_port=80, to_port=80)
        # ec2.CfnSecurityGroupIngress(self, 'publicsecuritygroupingress02', group_id=self.security_group.ref, ip_protocol='tcp', cidr_ip='0.0.0.0/0', description='ssh', from_port=22, to_port=22)
        # # public Egress
        # ec2.CfnSecurityGroupEgress(
        #     self, 
        #     'publicsecuritygroupegress01', 
        #     group_id=self.security_group.ref, 
        #     ip_protocol='-1', 
        #     cidr_ip='0.0.0.0/0'
        # destination_security_group_id=privatesecuritygroup01.ref, 
        # description='for private', 
        # from_port=22, to_port=22
        # )
        # private Ingress

        image_id=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2).get_image(self).image_id

        # Create an EC2 instance with the above configuration
        ec2_instance = ec2.Instance(
            self, "my_ec2_instance",
            # instance_type=_ec2.InstanceType(
                # instance_type_identifier=instance_type),
            # machine_image=_ec2.MachineImage.latest_amazon_linux(),
            vpc=my_vpc, instance_name="MyInstance",
            # key_name=key_name, security_group=my_security_group,
            # role=my_session_mgmt_role,
            # user_data=_ec2.UserData.custom(user_data)
        )
        # host.add_property_override("credit_specification", { "cpu_credits" : "standard" })
        # ec2.Instance has no property of BlockDeviceMappings, add via lower layer cdk api:
        # host.instance.add_property_override("BlockDeviceMappings", [{
        #     "DeviceName": "/dev/xvda",
        #     "Ebs": {
        #         "VolumeSize": "10",
        #         "VolumeType": "io1",
        #         "Iops": "150",
        #         "DeleteOnTermination": "true"
        #     }
        # }, {
        #     "DeviceName": "/dev/sdb",
        #     "Ebs": {"VolumeSize": "30"}
        # }
        # ])  # by default VolumeType is gp2, VolumeSize 8GB
        # host.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(22), "Allow ssh from internet")
        # host.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(80), "Allow ssh from internet")

        # core.CfnOutput(self, "Output",
        #                value=host.instance_public_ip)