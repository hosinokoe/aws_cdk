from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)


class CdkRDSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, public_subnet_a, public_subnet_c, public_subnet_d, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prefix = "test"

    # RdsSecurityGroup
        RdsSecurityGroupStg = ec2.CfnSecurityGroup(self, "RdsSecurityGroupStg",
          group_name = 'stg-'+prefix+'-db01',
          group_description = 'stg-'+prefix+'-db01',
          vpc_id = vpc.ref,
          security_group_ingress = [
            {
              "ipProtocol" : "tcp",
              "fromPort" : 3306,
              "toPort" : 3306,
              "cidrIp" : "0.0.0.0/0"
            }
          ],
          security_group_egress = [
            {
              "ipProtocol" : "tcp",
              "fromPort" : 0,
              "toPort" : 65535,
              "cidrIp" : "0.0.0.0/0"
            }
          ],
        )
        # MyDBSubnetGroup
        rds_subnet_group = rds.CfnDBSubnetGroup(self, "DBSubnetGroup",
            db_subnet_group_description = "DBSubnetGroup",
            subnet_ids = [
                    public_subnet_a.ref,
                    public_subnet_c.ref,
                    public_subnet_d.ref
            ]
        )
        DBParameterGroupStg = rds.CfnDBParameterGroup(self, "DBParameterGroupStg",
            description = 'stg-'+prefix+'db01',
            family = "MySQL5.6",
            parameters = {
                'character_set_client': "utf8",
                'character_set_connection': "utf8",
                'character_set_database': "utf8",
                'character_set_results': "utf8",
                'character_set_server': "utf8",
                'collation_connection': "utf8_general_ci",
                'collation_server': "utf8_general_ci",
                'long_query_time': "1.2",
                'slow_query_log': "1",
                'time_zone': "Asia/Tokyo",
            },
            tags=[
                core.CfnTag(key="Name", value='stg-'+prefix+'db01')
            ]
        )
        rds_params = {
            'db_instance_identifier': "stg-test-db01",
            'engine': "mysql",
            'engine_version': '5.6.39',
            'db_instance_class': 'db.t3.micro',
            'allocated_storage': '5',
            'storage_type': 'gp2',
            'db_name': "test",
            'master_username': "test",
            'master_user_password': "zaq12wsx",
            'db_subnet_group_name' : rds_subnet_group.ref,
            'publicly_accessible': False,
            'multi_az': False,
            'preferred_backup_window': "18:00-18:30",
            'preferred_maintenance_window': "sat:19:00-sat:19:30",
            'auto_minor_version_upgrade': False,
            'db_parameter_group_name': DBParameterGroupStg.ref,
            'vpc_security_groups': [RdsSecurityGroupStg.ref],
            'copy_tags_to_snapshot': True,
            'backup_retention_period': 7,
            # 'enable_performance_insights': True,
            'delete_automated_backups': True,
            'deletion_protection': False,
            'availability_zone': "us-east-1a",
            'enable_cloudwatch_logs_exports': ["error","slowquery"]
            # 'storage_encrypted': False,
        }

        self.rds = rds.CfnDBInstance(self, 'staff-rds', **rds_params,
            tags=[
                core.CfnTag(key="Name", value='stg-'+prefix+'db01')
            ]
        )

        core.CfnOutput(self, "OutputVpc",
                       value=vpc.ref)
        core.CfnOutput(self, "OutputRds",
                       value=self.rds.ref)