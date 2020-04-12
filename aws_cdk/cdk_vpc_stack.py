from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class CdkVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # The code that defines your stack goes here
        prefix = "test"
        # def name(s): return "{0}/{1}".format(prefix, s)
        def name(s): return "{0} {1}".format(prefix, s)

        # VPC
        vpc = ec2.CfnVPC(
            self, "vpc",
            cidr_block="192.168.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags=[
                core.CfnTag(key="Name", value=name("vpc"))
            ]
        )

        # InternetGateway
        igw = ec2.CfnInternetGateway(
            self, "igw",
            tags=[
                core.CfnTag(key="Name", value=name("igw"))
            ]
        )
        igw_attachment = ec2.CfnVPCGatewayAttachment(
            self, "igw_attachment",
            vpc_id=vpc.ref,
            internet_gateway_id=igw.ref
        )
        dhcpoptions = ec2.CfnDHCPOptions(
            self, "dhcpoptions",
            domain_name="ap-northeast-1.compute.internal",
            domain_name_servers=["AmazonProvidedDNS"],
            tags=[
                core.CfnTag(key="Name", value=name("dhcpoptions"))
            ]
        )
        dhcpoptionsassociation = ec2.CfnVPCDHCPOptionsAssociation(
            self, "dhcpoptionsassociation",
            dhcp_options_id=dhcpoptions.ref,
            vpc_id=vpc.ref
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
        public_subnet_a = ec2.CfnSubnet(
            self, "public_a",
            vpc_id=vpc.ref,
            cidr_block="192.168.0.0/20",
            # availability_zone="ap-northeast-1a",
            availability_zone="us-east-1a",
            tags=[
                core.CfnTag(key="Name", value=name("public_a"))
            ]
        )
        # PublicSubnetC
        public_subnet_c = ec2.CfnSubnet(
            self, "public_c",
            vpc_id=vpc.ref,
            cidr_block="192.168.16.0/20",
            availability_zone="us-east-1c",
            tags=[
                core.CfnTag(key="Name", value=name("public_c"))
            ]
        )
        public_subnet_d = ec2.CfnSubnet(
            self, "public_d",
            vpc_id=vpc.ref,
            cidr_block="192.168.32.0/20",
            availability_zone="us-east-1d",
            tags=[
                core.CfnTag(key="Name", value=name("public_d"))
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
        #     subnet_id=public_subnet_a.ref,
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
        rtb_public_a = ec2.CfnRouteTable(
            self, "rtb_public_a",
            vpc_id=vpc.ref,
            tags=[
                core.CfnTag(key="Name", value=name("rtb_public_a"))
            ]
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_a_association",
            route_table_id=rtb_public_a.ref,
            subnet_id=public_subnet_a.ref
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_c_association",
            route_table_id=rtb_public_a.ref,
            subnet_id=public_subnet_c.ref
        )
        ec2.CfnSubnetRouteTableAssociation(
            self, "rtb_public_d_association",
            route_table_id=rtb_public_a.ref,
            subnet_id=public_subnet_d.ref
        )
        ec2.CfnRoute(
            self, "route_public_a",
            route_table_id=rtb_public_a.ref,
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
        # core.CfnOutput(self, "Output",
        #                value=self.vpc.vpc_id)
