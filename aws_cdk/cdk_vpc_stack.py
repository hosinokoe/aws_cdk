from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class CdkVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prefix = "test"
        cidr = "192.168.0.0/16"
        # def name(s): return "{0}/{1}".format(prefix, s)
        def name(s): return "{0} {1}".format(prefix, s)

        # VPC
        self.vpc = ec2.CfnVPC(
            self, "vpc",
            cidr_block=cidr,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags=[
                core.CfnTag(key="Name", value=prefix+' VPC')
            ]
        )

        # InternetGateway
        igw = ec2.CfnInternetGateway(
            self, "igw",
            tags=[
                core.CfnTag(key="Name", value=prefix+' IGW')
            ]
        )
        igw_attachment = ec2.CfnVPCGatewayAttachment(
            self, "igw_attachment",
            vpc_id=self.vpc.ref,
            internet_gateway_id=igw.ref
        )
        dhcpoptions = ec2.CfnDHCPOptions(
            self, "dhcpoptions",
            domain_name="ec2.internal "+prefix,
            domain_name_servers=["AmazonProvidedDNS"],
            tags=[
                core.CfnTag(key="Name", value=prefix)
            ]
        )
        dhcpoptionsassociation = ec2.CfnVPCDHCPOptionsAssociation(
            self, "dhcpoptionsassociation",
            dhcp_options_id=dhcpoptions.ref,
            vpc_id=self.vpc.ref
        )

        # PrivateSubnetA
        # private_subnet_a = ec2.CfnSubnet(
        #     self, "private_a",
        #     vpc_id=vpc.ref,
        #     cidr_block="192.168.0.0/24",
        #     availability_zone="ap-northeast-1a",
        #     tags=[
        #         core.CfnTag(key="Name", value=name("private_a"))
        #     ]
        # )
        # PrivateSubnetC
        # private_subnet_c = ec2.CfnSubnet(
        #     self, "private_c",
        #     vpc_id=vpc.ref,
        #     cidr_block="192.168.1.0/24",
        #     availability_zone="ap-northeast-1c",
        #     tags=[
        #         core.CfnTag(key="Name", value=name("private_c"))
        #     ]
        # )

        # PublicSubnetA
        self.public_subnet_a = ec2.CfnSubnet(
            self, "public_a",
            vpc_id=self.vpc.ref,
            cidr_block="192.168.0.0/20",
            # availability_zone="ap-northeast-1a",
            availability_zone="us-east-1a",
            tags=[
                core.CfnTag(key="Name", value=prefix+" public_a")
            ]
        )
        # PublicSubnetC
        self.public_subnet_c = ec2.CfnSubnet(
            self, "public_c",
            vpc_id=self.vpc.ref,
            cidr_block="192.168.16.0/20",
            availability_zone="us-east-1c",
            tags=[
                core.CfnTag(key="Name", value=prefix+" public_c")
            ]
        )
        self.public_subnet_d = ec2.CfnSubnet(
            self, "public_d",
            vpc_id=self.vpc.ref,
            cidr_block="192.168.32.0/20",
            availability_zone="us-east-1d",
            tags=[
                core.CfnTag(key="Name", value=prefix+" public_d")
            ]
        )

        # EIP1 (for NATGW)
        # eip1 = ec2.CfnEIP(
        #     self, "eip1",
        #     domain="vpc",
        # )
        # eip1.add_depends_on(igw_attachment)

        # EIP2 (for NATGW)
        # eip2 = ec2.CfnEIP(
        #     self, "eip2",
        #     domain="vpc",
        # )
        # eip2.add_depends_on(igw_attachment)

        # NatGatewayA
        # natgw_a = ec2.CfnNatGateway(
        #     self, "natgw_a",
        #     allocation_id=eip1.attr_allocation_id,
        #     subnet_id=self.public_subnet_a.ref,
        #     tags=[
        #         core.CfnTag(key="Name", value=name("natgw_a"))
        #     ]
        # )
        # NatGatewayC
        # natgw_c = ec2.CfnNatGateway(
        #     self, "natgw_c",
        #     allocation_id=eip2.attr_allocation_id,
        #     subnet_id=public_subnet_c.ref,
        #     tags=[
        #         core.CfnTag(key="Name", value=name("natgw_c"))
        #     ]
        # )

        # RouteTable of PrivateSubnetA
        # rtb_private_a = ec2.CfnRouteTable(
        #     self, "rtb_private_a",
        #     vpc_id=vpc.ref,
        #     tags=[
        #         core.CfnTag(key="Name", value=name("rtb_private_a"))
        #     ]
        # )
        # ec2.CfnSubnetRouteTableAssociation(
        #     self, "rtb_private_a_association",
        #     route_table_id=rtb_private_a.ref,
        #     subnet_id=private_subnet_a.ref
        # )
        # ec2.CfnRoute(
        #     self, "route_private_a",
        #     route_table_id=rtb_private_a.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     nat_gateway_id=natgw_a.ref
        # )

        # RouteTable of PrivateSubnetC
        # rtb_private_c = ec2.CfnRouteTable(
        #     self, "rtb_private_c",
        #     vpc_id=vpc.ref,
        #     tags=[
        #         core.CfnTag(key="Name", value=name("rtb_private_c"))
        #     ]
        # )
        # ec2.CfnSubnetRouteTableAssociation(
        #     self, "rtb_private_c_association",
        #     route_table_id=rtb_private_c.ref,
        #     subnet_id=private_subnet_c.ref
        # )
        # ec2.CfnRoute(
        #     self, "route_private_c",
        #     route_table_id=rtb_private_c.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     nat_gateway_id=natgw_c.ref
        # )

        # RouteTable of PublicSubnetA
        self.rtb_public_a = ec2.CfnRouteTable(
            self, "rtb_public_a",
            vpc_id=self.vpc.ref,
            tags=[
                core.CfnTag(key="Name", value=prefix+" rtb_public_a")
            ]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_a_association",
            route_table_id=self.rtb_public_a.ref,
            subnet_id=self.public_subnet_a.ref
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_c_association",
            route_table_id=self.rtb_public_a.ref,
            subnet_id=self.public_subnet_c.ref
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_d_association",
            route_table_id=self.rtb_public_a.ref,
            subnet_id=self.public_subnet_d.ref
        )
        ec2.CfnRoute(
            self, "route_public_a",
            route_table_id=self.rtb_public_a.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=igw.ref
        )

        # RouteTable of PublicSubnetC
        # rtb_public_c = ec2.CfnRouteTable(
        #     self, "rtb_public_c",
        #     vpc_id=vpc.ref,
        #     tags=[
        #         core.CfnTag(key="Name", value=name("rtb_public_c"))
        #     ]
        # )
        # ec2.CfnSubnetRouteTableAssociation(
        #     self, "rtb_public_c_association",
        #     route_table_id=rtb_public_c.ref,
        #     subnet_id=public_subnet_c.ref
        # )
        # ec2.CfnRoute(
        #     self, "route_public_c",
        #     route_table_id=rtb_public_c.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     gateway_id=igw.ref
        # )

        # ami_id = ec2.AmazonLinuxImage(generation = ec2.AmazonLinuxGeneration.AMAZON_LINUX_2).get_image(self).image_id

        # security_group = ec2.SecurityGroup(
        #     self,
        #     id='test',
        #     vpc=self.vpc,
        #     security_group_name='test-security-group'
        # )

        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.ipv4(cidr),
        #     connection=ec2.Port.tcp(22),
        # )
        
        # test_web = ec2.CfnInstance(self,
        #     "testInstance01",
        #     image_id = ami_id,
        #     instance_type = "t3a.micro",
        #     monitoring = False,
        #     key_name = "stg-intrinio-www01",
        #     security_group_ids=[security_group.security_group_id],
        #     block_device_mappings = [{
        #     "deviceName": "/dev/xvda",
        #     "ebs": {
        #         "volumeSize": 10,
        #         "volumeType": "io1",
        #         "iops": 150,
        #         "deleteOnTermination": True
        #             }
        #         }
        #     ],
        #     tags = [
        #         { "key": "Name", "value": prefix }
        #     ],
        #     network_interfaces = [{
        #         "deviceIndex": "0",
        #         "associatePublicIpAddress": True,
        #         "subnetId": self.public_subnet_a.ref,
        #         # "groupSet": [web_sg.security_group_id]
        #     }], #https: //github.com/aws/aws-cdk/issues/3419
        # )

        core.CfnOutput(self, "Output",
                       value=self.vpc.ref)
