from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticache as redis,
    core,
)


class CdkREDISStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, public_subnet_a, public_subnet_c, public_subnet_d, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prefix = "test"

    # RedisSecurityGroup
        redis_security_group = ec2.CfnSecurityGroup(self, "RedisSecurityGroup",
          group_name = "stg-test-redis01",
          group_description =  "HTTP traffic",
          vpc_id = vpc.ref,
          security_group_ingress = [
            {
              "ipProtocol" : "tcp",
              "fromPort" : 6379,
              "toPort" : 6379,
              "cidrIp" : "192.168.0.0/16"
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
        redis_subnet_group = redis.CfnSubnetGroup(self, "RedisSubnetGroup",
            cache_subnet_group_name = "stg-test-redis01",
            description = "stg-test-redis01",
            subnet_ids = [
                    public_subnet_a.ref,
                    public_subnet_c.ref,
                    public_subnet_d.ref
            ]
        )
        redis_params = {
            'auto_minor_version_upgrade': True,
            'engine': 'redis',
            'at_rest_encryption_enabled': True,
            'automatic_failover_enabled': False,
            'engine_version': '4.0.10',
            'cache_node_type': 'cache.t3.micro',
            'num_cache_clusters': 1,
            'replication_group_description': "stg-test-redis01",
            'replication_group_id': "stg-test-redis01",
            'security_group_ids': [redis_security_group.ref],
            'cache_subnet_group_name': redis_subnet_group.ref
        }

        self.redis = redis.CfnReplicationGroup(self, 'stg-test-redis01', **redis_params
        )

        core.CfnOutput(self, "OutputVpc",
                       value=vpc.ref)
        core.CfnOutput(self, "OutputRedis",
                       value=self.redis.ref)