from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cdn,
    aws_route53 as r53,
    aws_ssm as ssm,
    core
) 


class CdkCDNStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # MyCfnId
        self.cfn_access_id = cdn.CfnCloudFrontOriginAccessIdentity(self, "cfn_access_id",
            cloud_front_origin_access_identity_config={'comment':'access-id-s3-test'}
        )
        # MyCfn
        self.cfn = cdn.CfnDistribution(self, "cfn",
            distribution_config={
                'aliases': ['mst-test.codefirefly.com'],
                'enabled': True,
                'defaultCacheBehavior': {
                    'forwardedValues': {
                        'queryString': False,
                        'cookies': {'forward': 'none'}
                    },
                    'allowed_methods': ['GET','HEAD'],
                    # 'lambdaFunctionAssociations': [{
                    #     'eventType': 'viewer-request',
                    #     'lambdaFunctionArn': checkConditionsFunctionVersion.function_arn
                    # }],
                    'targetOriginId': 'myS3Origin',
                    'viewerProtocolPolicy': 'allow-all',
                    'compress': True
                },
                'ipv6Enabled': False,
                # 'logging': {
                #     'bucket': self.node.try_get_context('distribution_log_bucket'),
                #     'prefix': "logs/"
                # },
                'origins': [{
                    'domainName': 'mst-test.s3.amazonaws.com',
                    'id': "myS3Origin",
                    's3OriginConfig': {
                        'originAccessIdentity': 'origin-access-identity/cloudfront/'+self.cfn_access_id.ref
                    }
                }],
                'comment': 'mst-test',
                # 'priceClass': 'PriceClass_All',
                'viewerCertificate': {
                    'acmCertificateArn': 'arn:aws:acm:us-east-1:456843195142:certificate/31c9c3b3-af3e-4155-9ad8-ebbf1186284e',
                    'sslSupportMethod': 'sni-only'
                }
            }
        )
        # MyRoute53
        record = r53.CfnRecordSet(self,'route53',
            name='mst-test.codefirefly.com',
            hosted_zone_id='Z2787K6CO94PK7',
            # comment='public dns for myDistribution',
            type='A',
            alias_target=r53.CfnRecordSet.AliasTargetProperty(
                dns_name=self.cfn.attr_domain_name,
                hosted_zone_id='Z2FDTNDATAQYW2'
            )
        )