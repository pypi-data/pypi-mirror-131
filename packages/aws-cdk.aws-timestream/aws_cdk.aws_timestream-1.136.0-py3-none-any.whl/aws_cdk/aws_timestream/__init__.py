'''
# AWS::Timestream Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_timestream as timestream
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Timestream](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Timestream.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDatabase(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-timestream.CfnDatabase",
):
    '''A CloudFormation ``AWS::Timestream::Database``.

    :cloudformationResource: AWS::Timestream::Database
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_timestream as timestream
        
        cfn_database = timestream.CfnDatabase(self, "MyCfnDatabase",
            database_name="databaseName",
            kms_key_id="kmsKeyId",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: ``AWS::Timestream::Database.DatabaseName``.
        :param kms_key_id: ``AWS::Timestream::Database.KmsKeyId``.
        :param tags: ``AWS::Timestream::Database.Tags``.
        '''
        props = CfnDatabaseProps(
            database_name=database_name, kms_key_id=kms_key_id, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Database.DatabaseName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Database.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::Timestream::Database.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-timestream.CfnDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnDatabaseProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Timestream::Database``.

        :param database_name: ``AWS::Timestream::Database.DatabaseName``.
        :param kms_key_id: ``AWS::Timestream::Database.KmsKeyId``.
        :param tags: ``AWS::Timestream::Database.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_timestream as timestream
            
            cfn_database_props = timestream.CfnDatabaseProps(
                database_name="databaseName",
                kms_key_id="kmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Database.DatabaseName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Database.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::Timestream::Database.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScheduledQuery(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery",
):
    '''A CloudFormation ``AWS::Timestream::ScheduledQuery``.

    :cloudformationResource: AWS::Timestream::ScheduledQuery
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_timestream as timestream
        
        cfn_scheduled_query = timestream.CfnScheduledQuery(self, "MyCfnScheduledQuery",
            error_report_configuration=timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                    bucket_name="bucketName",
        
                    # the properties below are optional
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            ),
            notification_configuration=timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            ),
            query_string="queryString",
            schedule_configuration=timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                schedule_expression="scheduleExpression"
            ),
            scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
        
            # the properties below are optional
            client_token="clientToken",
            kms_key_id="kmsKeyId",
            scheduled_query_name="scheduledQueryName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_configuration=timestream.CfnScheduledQuery.TargetConfigurationProperty(
                timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    table_name="tableName",
                    time_column="timeColumn",
        
                    # the properties below are optional
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                        measure_value_type="measureValueType",
        
                        # the properties below are optional
                        measure_name="measureName",
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
        
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
        
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
        
                        # the properties below are optional
                        target_multi_measure_name="targetMultiMeasureName"
                    )
                )
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        client_token: typing.Optional[builtins.str] = None,
        error_report_configuration: typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", aws_cdk.core.IResolvable],
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.NotificationConfigurationProperty"],
        query_string: builtins.str,
        schedule_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.ScheduleConfigurationProperty"],
        scheduled_query_execution_role_arn: builtins.str,
        scheduled_query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        target_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TargetConfigurationProperty"]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::ScheduledQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param client_token: ``AWS::Timestream::ScheduledQuery.ClientToken``.
        :param error_report_configuration: ``AWS::Timestream::ScheduledQuery.ErrorReportConfiguration``.
        :param kms_key_id: ``AWS::Timestream::ScheduledQuery.KmsKeyId``.
        :param notification_configuration: ``AWS::Timestream::ScheduledQuery.NotificationConfiguration``.
        :param query_string: ``AWS::Timestream::ScheduledQuery.QueryString``.
        :param schedule_configuration: ``AWS::Timestream::ScheduledQuery.ScheduleConfiguration``.
        :param scheduled_query_execution_role_arn: ``AWS::Timestream::ScheduledQuery.ScheduledQueryExecutionRoleArn``.
        :param scheduled_query_name: ``AWS::Timestream::ScheduledQuery.ScheduledQueryName``.
        :param tags: ``AWS::Timestream::ScheduledQuery.Tags``.
        :param target_configuration: ``AWS::Timestream::ScheduledQuery.TargetConfiguration``.
        '''
        props = CfnScheduledQueryProps(
            client_token=client_token,
            error_report_configuration=error_report_configuration,
            kms_key_id=kms_key_id,
            notification_configuration=notification_configuration,
            query_string=query_string,
            schedule_configuration=schedule_configuration,
            scheduled_query_execution_role_arn=scheduled_query_execution_role_arn,
            scheduled_query_name=scheduled_query_name,
            tags=tags,
            target_configuration=target_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqErrorReportConfiguration")
    def attr_sq_error_report_configuration(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQErrorReportConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqErrorReportConfiguration"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqKmsKeyId")
    def attr_sq_kms_key_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQKmsKeyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqKmsKeyId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqName")
    def attr_sq_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqNotificationConfiguration")
    def attr_sq_notification_configuration(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQNotificationConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqNotificationConfiguration"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqQueryString")
    def attr_sq_query_string(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQQueryString
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqQueryString"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqScheduleConfiguration")
    def attr_sq_schedule_configuration(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQScheduleConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqScheduleConfiguration"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqScheduledQueryExecutionRoleArn")
    def attr_sq_scheduled_query_execution_role_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQScheduledQueryExecutionRoleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqScheduledQueryExecutionRoleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSqTargetConfiguration")
    def attr_sq_target_configuration(self) -> builtins.str:
        '''
        :cloudformationAttribute: SQTargetConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqTargetConfiguration"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.ClientToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientToken", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="errorReportConfiguration")
    def error_report_configuration(
        self,
    ) -> typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", aws_cdk.core.IResolvable]:
        '''``AWS::Timestream::ScheduledQuery.ErrorReportConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-errorreportconfiguration
        '''
        return typing.cast(typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", aws_cdk.core.IResolvable], jsii.get(self, "errorReportConfiguration"))

    @error_report_configuration.setter
    def error_report_configuration(
        self,
        value: typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "errorReportConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.NotificationConfigurationProperty"]:
        '''``AWS::Timestream::ScheduledQuery.NotificationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-notificationconfiguration
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.NotificationConfigurationProperty"], jsii.get(self, "notificationConfiguration"))

    @notification_configuration.setter
    def notification_configuration(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.NotificationConfigurationProperty"],
    ) -> None:
        jsii.set(self, "notificationConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''``AWS::Timestream::ScheduledQuery.QueryString``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        jsii.set(self, "queryString", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheduleConfiguration")
    def schedule_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.ScheduleConfigurationProperty"]:
        '''``AWS::Timestream::ScheduledQuery.ScheduleConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduleconfiguration
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.ScheduleConfigurationProperty"], jsii.get(self, "scheduleConfiguration"))

    @schedule_configuration.setter
    def schedule_configuration(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.ScheduleConfigurationProperty"],
    ) -> None:
        jsii.set(self, "scheduleConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheduledQueryExecutionRoleArn")
    def scheduled_query_execution_role_arn(self) -> builtins.str:
        '''``AWS::Timestream::ScheduledQuery.ScheduledQueryExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryexecutionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledQueryExecutionRoleArn"))

    @scheduled_query_execution_role_arn.setter
    def scheduled_query_execution_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "scheduledQueryExecutionRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheduledQueryName")
    def scheduled_query_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.ScheduledQueryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduledQueryName"))

    @scheduled_query_name.setter
    def scheduled_query_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheduledQueryName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::Timestream::ScheduledQuery.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetConfiguration")
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TargetConfigurationProperty"]]:
        '''``AWS::Timestream::ScheduledQuery.TargetConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-targetconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TargetConfigurationProperty"]], jsii.get(self, "targetConfiguration"))

    @target_configuration.setter
    def target_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TargetConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "targetConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.DimensionMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_value_type": "dimensionValueType", "name": "name"},
    )
    class DimensionMappingProperty:
        def __init__(
            self,
            *,
            dimension_value_type: builtins.str,
            name: builtins.str,
        ) -> None:
            '''
            :param dimension_value_type: ``CfnScheduledQuery.DimensionMappingProperty.DimensionValueType``.
            :param name: ``CfnScheduledQuery.DimensionMappingProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                dimension_mapping_property = timestream.CfnScheduledQuery.DimensionMappingProperty(
                    dimension_value_type="dimensionValueType",
                    name="name"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "dimension_value_type": dimension_value_type,
                "name": name,
            }

        @builtins.property
        def dimension_value_type(self) -> builtins.str:
            '''``CfnScheduledQuery.DimensionMappingProperty.DimensionValueType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-dimensionvaluetype
            '''
            result = self._values.get("dimension_value_type")
            assert result is not None, "Required property 'dimension_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnScheduledQuery.DimensionMappingProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.ErrorReportConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class ErrorReportConfigurationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.S3ConfigurationProperty"],
        ) -> None:
            '''
            :param s3_configuration: ``CfnScheduledQuery.ErrorReportConfigurationProperty.S3Configuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                error_report_configuration_property = timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                    s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_configuration": s3_configuration,
            }

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.S3ConfigurationProperty"]:
            '''``CfnScheduledQuery.ErrorReportConfigurationProperty.S3Configuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html#cfn-timestream-scheduledquery-errorreportconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.S3ConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorReportConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.MixedMeasureMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_name": "measureName",
            "measure_value_type": "measureValueType",
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "source_column": "sourceColumn",
            "target_measure_name": "targetMeasureName",
        },
    )
    class MixedMeasureMappingProperty:
        def __init__(
            self,
            *,
            measure_name: typing.Optional[builtins.str] = None,
            measure_value_type: builtins.str,
            multi_measure_attribute_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]]] = None,
            source_column: typing.Optional[builtins.str] = None,
            target_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param measure_name: ``CfnScheduledQuery.MixedMeasureMappingProperty.MeasureName``.
            :param measure_value_type: ``CfnScheduledQuery.MixedMeasureMappingProperty.MeasureValueType``.
            :param multi_measure_attribute_mappings: ``CfnScheduledQuery.MixedMeasureMappingProperty.MultiMeasureAttributeMappings``.
            :param source_column: ``CfnScheduledQuery.MixedMeasureMappingProperty.SourceColumn``.
            :param target_measure_name: ``CfnScheduledQuery.MixedMeasureMappingProperty.TargetMeasureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                mixed_measure_mapping_property = timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                    measure_value_type="measureValueType",
                
                    # the properties below are optional
                    measure_name="measureName",
                    multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                
                        # the properties below are optional
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                    source_column="sourceColumn",
                    target_measure_name="targetMeasureName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "measure_value_type": measure_value_type,
            }
            if measure_name is not None:
                self._values["measure_name"] = measure_name
            if multi_measure_attribute_mappings is not None:
                self._values["multi_measure_attribute_mappings"] = multi_measure_attribute_mappings
            if source_column is not None:
                self._values["source_column"] = source_column
            if target_measure_name is not None:
                self._values["target_measure_name"] = target_measure_name

        @builtins.property
        def measure_name(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.MixedMeasureMappingProperty.MeasureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurename
            '''
            result = self._values.get("measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_value_type(self) -> builtins.str:
            '''``CfnScheduledQuery.MixedMeasureMappingProperty.MeasureValueType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            assert result is not None, "Required property 'measure_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]]]:
            '''``CfnScheduledQuery.MixedMeasureMappingProperty.MultiMeasureAttributeMappings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]]], result)

        @builtins.property
        def source_column(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.MixedMeasureMappingProperty.SourceColumn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_measure_name(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.MixedMeasureMappingProperty.TargetMeasureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-targetmeasurename
            '''
            result = self._values.get("target_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MixedMeasureMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_value_type": "measureValueType",
            "source_column": "sourceColumn",
            "target_multi_measure_attribute_name": "targetMultiMeasureAttributeName",
        },
    )
    class MultiMeasureAttributeMappingProperty:
        def __init__(
            self,
            *,
            measure_value_type: builtins.str,
            source_column: builtins.str,
            target_multi_measure_attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param measure_value_type: ``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.MeasureValueType``.
            :param source_column: ``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.SourceColumn``.
            :param target_multi_measure_attribute_name: ``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.TargetMultiMeasureAttributeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                multi_measure_attribute_mapping_property = timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                    measure_value_type="measureValueType",
                    source_column="sourceColumn",
                
                    # the properties below are optional
                    target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "measure_value_type": measure_value_type,
                "source_column": source_column,
            }
            if target_multi_measure_attribute_name is not None:
                self._values["target_multi_measure_attribute_name"] = target_multi_measure_attribute_name

        @builtins.property
        def measure_value_type(self) -> builtins.str:
            '''``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.MeasureValueType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            assert result is not None, "Required property 'measure_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_column(self) -> builtins.str:
            '''``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.SourceColumn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            assert result is not None, "Required property 'source_column' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_multi_measure_attribute_name(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.MultiMeasureAttributeMappingProperty.TargetMultiMeasureAttributeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-targetmultimeasureattributename
            '''
            result = self._values.get("target_multi_measure_attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureAttributeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.MultiMeasureMappingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "target_multi_measure_name": "targetMultiMeasureName",
        },
    )
    class MultiMeasureMappingsProperty:
        def __init__(
            self,
            *,
            multi_measure_attribute_mappings: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]],
            target_multi_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param multi_measure_attribute_mappings: ``CfnScheduledQuery.MultiMeasureMappingsProperty.MultiMeasureAttributeMappings``.
            :param target_multi_measure_name: ``CfnScheduledQuery.MultiMeasureMappingsProperty.TargetMultiMeasureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                multi_measure_mappings_property = timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                    multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                
                        # the properties below are optional
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                
                    # the properties below are optional
                    target_multi_measure_name="targetMultiMeasureName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "multi_measure_attribute_mappings": multi_measure_attribute_mappings,
            }
            if target_multi_measure_name is not None:
                self._values["target_multi_measure_name"] = target_multi_measure_name

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]]:
            '''``CfnScheduledQuery.MultiMeasureMappingsProperty.MultiMeasureAttributeMappings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            assert result is not None, "Required property 'multi_measure_attribute_mappings' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureAttributeMappingProperty"]]], result)

        @builtins.property
        def target_multi_measure_name(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.MultiMeasureMappingsProperty.TargetMultiMeasureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-targetmultimeasurename
            '''
            result = self._values.get("target_multi_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureMappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"sns_configuration": "snsConfiguration"},
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            sns_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.SnsConfigurationProperty"],
        ) -> None:
            '''
            :param sns_configuration: ``CfnScheduledQuery.NotificationConfigurationProperty.SnsConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                notification_configuration_property = timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                    sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "sns_configuration": sns_configuration,
            }

        @builtins.property
        def sns_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.SnsConfigurationProperty"]:
            '''``CfnScheduledQuery.NotificationConfigurationProperty.SnsConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html#cfn-timestream-scheduledquery-notificationconfiguration-snsconfiguration
            '''
            result = self._values.get("sns_configuration")
            assert result is not None, "Required property 'sns_configuration' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.SnsConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "encryption_option": "encryptionOption",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            encryption_option: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnScheduledQuery.S3ConfigurationProperty.BucketName``.
            :param encryption_option: ``CfnScheduledQuery.S3ConfigurationProperty.EncryptionOption``.
            :param object_key_prefix: ``CfnScheduledQuery.S3ConfigurationProperty.ObjectKeyPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                s3_configuration_property = timestream.CfnScheduledQuery.S3ConfigurationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if encryption_option is not None:
                self._values["encryption_option"] = encryption_option
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnScheduledQuery.S3ConfigurationProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_option(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.S3ConfigurationProperty.EncryptionOption``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.S3ConfigurationProperty.ObjectKeyPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.ScheduleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleConfigurationProperty:
        def __init__(self, *, schedule_expression: builtins.str) -> None:
            '''
            :param schedule_expression: ``CfnScheduledQuery.ScheduleConfigurationProperty.ScheduleExpression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                schedule_configuration_property = timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''``CfnScheduledQuery.ScheduleConfigurationProperty.ScheduleExpression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html#cfn-timestream-scheduledquery-scheduleconfiguration-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.SnsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsConfigurationProperty:
        def __init__(self, *, topic_arn: builtins.str) -> None:
            '''
            :param topic_arn: ``CfnScheduledQuery.SnsConfigurationProperty.TopicArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                sns_configuration_property = timestream.CfnScheduledQuery.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "topic_arn": topic_arn,
            }

        @builtins.property
        def topic_arn(self) -> builtins.str:
            '''``CfnScheduledQuery.SnsConfigurationProperty.TopicArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html#cfn-timestream-scheduledquery-snsconfiguration-topicarn
            '''
            result = self._values.get("topic_arn")
            assert result is not None, "Required property 'topic_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"timestream_configuration": "timestreamConfiguration"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            timestream_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TimestreamConfigurationProperty"],
        ) -> None:
            '''
            :param timestream_configuration: ``CfnScheduledQuery.TargetConfigurationProperty.TimestreamConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                target_configuration_property = timestream.CfnScheduledQuery.TargetConfigurationProperty(
                    timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        table_name="tableName",
                        time_column="timeColumn",
                
                        # the properties below are optional
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                            measure_value_type="measureValueType",
                
                            # the properties below are optional
                            measure_name="measureName",
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                
                            # the properties below are optional
                            target_multi_measure_name="targetMultiMeasureName"
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "timestream_configuration": timestream_configuration,
            }

        @builtins.property
        def timestream_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TimestreamConfigurationProperty"]:
            '''``CfnScheduledQuery.TargetConfigurationProperty.TimestreamConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html#cfn-timestream-scheduledquery-targetconfiguration-timestreamconfiguration
            '''
            result = self._values.get("timestream_configuration")
            assert result is not None, "Required property 'timestream_configuration' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.TimestreamConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-timestream.CfnScheduledQuery.TimestreamConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "dimension_mappings": "dimensionMappings",
            "measure_name_column": "measureNameColumn",
            "mixed_measure_mappings": "mixedMeasureMappings",
            "multi_measure_mappings": "multiMeasureMappings",
            "table_name": "tableName",
            "time_column": "timeColumn",
        },
    )
    class TimestreamConfigurationProperty:
        def __init__(
            self,
            *,
            database_name: builtins.str,
            dimension_mappings: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.DimensionMappingProperty"]]],
            measure_name_column: typing.Optional[builtins.str] = None,
            mixed_measure_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MixedMeasureMappingProperty"]]]] = None,
            multi_measure_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureMappingsProperty"]] = None,
            table_name: builtins.str,
            time_column: builtins.str,
        ) -> None:
            '''
            :param database_name: ``CfnScheduledQuery.TimestreamConfigurationProperty.DatabaseName``.
            :param dimension_mappings: ``CfnScheduledQuery.TimestreamConfigurationProperty.DimensionMappings``.
            :param measure_name_column: ``CfnScheduledQuery.TimestreamConfigurationProperty.MeasureNameColumn``.
            :param mixed_measure_mappings: ``CfnScheduledQuery.TimestreamConfigurationProperty.MixedMeasureMappings``.
            :param multi_measure_mappings: ``CfnScheduledQuery.TimestreamConfigurationProperty.MultiMeasureMappings``.
            :param table_name: ``CfnScheduledQuery.TimestreamConfigurationProperty.TableName``.
            :param time_column: ``CfnScheduledQuery.TimestreamConfigurationProperty.TimeColumn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_timestream as timestream
                
                timestream_configuration_property = timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    table_name="tableName",
                    time_column="timeColumn",
                
                    # the properties below are optional
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                        measure_value_type="measureValueType",
                
                        # the properties below are optional
                        measure_name="measureName",
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                
                        # the properties below are optional
                        target_multi_measure_name="targetMultiMeasureName"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "database_name": database_name,
                "dimension_mappings": dimension_mappings,
                "table_name": table_name,
                "time_column": time_column,
            }
            if measure_name_column is not None:
                self._values["measure_name_column"] = measure_name_column
            if mixed_measure_mappings is not None:
                self._values["mixed_measure_mappings"] = mixed_measure_mappings
            if multi_measure_mappings is not None:
                self._values["multi_measure_mappings"] = multi_measure_mappings

        @builtins.property
        def database_name(self) -> builtins.str:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.DatabaseName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-databasename
            '''
            result = self._values.get("database_name")
            assert result is not None, "Required property 'database_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dimension_mappings(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.DimensionMappingProperty"]]]:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.DimensionMappings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-dimensionmappings
            '''
            result = self._values.get("dimension_mappings")
            assert result is not None, "Required property 'dimension_mappings' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.DimensionMappingProperty"]]], result)

        @builtins.property
        def measure_name_column(self) -> typing.Optional[builtins.str]:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.MeasureNameColumn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-measurenamecolumn
            '''
            result = self._values.get("measure_name_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mixed_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MixedMeasureMappingProperty"]]]]:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.MixedMeasureMappings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-mixedmeasuremappings
            '''
            result = self._values.get("mixed_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MixedMeasureMappingProperty"]]]], result)

        @builtins.property
        def multi_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureMappingsProperty"]]:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.MultiMeasureMappings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-multimeasuremappings
            '''
            result = self._values.get("multi_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScheduledQuery.MultiMeasureMappingsProperty"]], result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.TableName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_column(self) -> builtins.str:
            '''``CfnScheduledQuery.TimestreamConfigurationProperty.TimeColumn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-timecolumn
            '''
            result = self._values.get("time_column")
            assert result is not None, "Required property 'time_column' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestreamConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-timestream.CfnScheduledQueryProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_token": "clientToken",
        "error_report_configuration": "errorReportConfiguration",
        "kms_key_id": "kmsKeyId",
        "notification_configuration": "notificationConfiguration",
        "query_string": "queryString",
        "schedule_configuration": "scheduleConfiguration",
        "scheduled_query_execution_role_arn": "scheduledQueryExecutionRoleArn",
        "scheduled_query_name": "scheduledQueryName",
        "tags": "tags",
        "target_configuration": "targetConfiguration",
    },
)
class CfnScheduledQueryProps:
    def __init__(
        self,
        *,
        client_token: typing.Optional[builtins.str] = None,
        error_report_configuration: typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, aws_cdk.core.IResolvable],
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_configuration: typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.NotificationConfigurationProperty],
        query_string: builtins.str,
        schedule_configuration: typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.ScheduleConfigurationProperty],
        scheduled_query_execution_role_arn: builtins.str,
        scheduled_query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        target_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.TargetConfigurationProperty]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Timestream::ScheduledQuery``.

        :param client_token: ``AWS::Timestream::ScheduledQuery.ClientToken``.
        :param error_report_configuration: ``AWS::Timestream::ScheduledQuery.ErrorReportConfiguration``.
        :param kms_key_id: ``AWS::Timestream::ScheduledQuery.KmsKeyId``.
        :param notification_configuration: ``AWS::Timestream::ScheduledQuery.NotificationConfiguration``.
        :param query_string: ``AWS::Timestream::ScheduledQuery.QueryString``.
        :param schedule_configuration: ``AWS::Timestream::ScheduledQuery.ScheduleConfiguration``.
        :param scheduled_query_execution_role_arn: ``AWS::Timestream::ScheduledQuery.ScheduledQueryExecutionRoleArn``.
        :param scheduled_query_name: ``AWS::Timestream::ScheduledQuery.ScheduledQueryName``.
        :param tags: ``AWS::Timestream::ScheduledQuery.Tags``.
        :param target_configuration: ``AWS::Timestream::ScheduledQuery.TargetConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_timestream as timestream
            
            cfn_scheduled_query_props = timestream.CfnScheduledQueryProps(
                error_report_configuration=timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                    s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                        bucket_name="bucketName",
            
                        # the properties below are optional
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                ),
                notification_configuration=timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                    sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                ),
                query_string="queryString",
                schedule_configuration=timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                ),
                scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
            
                # the properties below are optional
                client_token="clientToken",
                kms_key_id="kmsKeyId",
                scheduled_query_name="scheduledQueryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_configuration=timestream.CfnScheduledQuery.TargetConfigurationProperty(
                    timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        table_name="tableName",
                        time_column="timeColumn",
            
                        # the properties below are optional
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                            measure_value_type="measureValueType",
            
                            # the properties below are optional
                            measure_name="measureName",
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
            
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
            
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
            
                            # the properties below are optional
                            target_multi_measure_name="targetMultiMeasureName"
                        )
                    )
                )
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "error_report_configuration": error_report_configuration,
            "notification_configuration": notification_configuration,
            "query_string": query_string,
            "schedule_configuration": schedule_configuration,
            "scheduled_query_execution_role_arn": scheduled_query_execution_role_arn,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if scheduled_query_name is not None:
            self._values["scheduled_query_name"] = scheduled_query_name
        if tags is not None:
            self._values["tags"] = tags
        if target_configuration is not None:
            self._values["target_configuration"] = target_configuration

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.ClientToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_report_configuration(
        self,
    ) -> typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, aws_cdk.core.IResolvable]:
        '''``AWS::Timestream::ScheduledQuery.ErrorReportConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-errorreportconfiguration
        '''
        result = self._values.get("error_report_configuration")
        assert result is not None, "Required property 'error_report_configuration' is missing"
        return typing.cast(typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, aws_cdk.core.IResolvable], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.NotificationConfigurationProperty]:
        '''``AWS::Timestream::ScheduledQuery.NotificationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-notificationconfiguration
        '''
        result = self._values.get("notification_configuration")
        assert result is not None, "Required property 'notification_configuration' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.NotificationConfigurationProperty], result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''``AWS::Timestream::ScheduledQuery.QueryString``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.ScheduleConfigurationProperty]:
        '''``AWS::Timestream::ScheduledQuery.ScheduleConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduleconfiguration
        '''
        result = self._values.get("schedule_configuration")
        assert result is not None, "Required property 'schedule_configuration' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.ScheduleConfigurationProperty], result)

    @builtins.property
    def scheduled_query_execution_role_arn(self) -> builtins.str:
        '''``AWS::Timestream::ScheduledQuery.ScheduledQueryExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryexecutionrolearn
        '''
        result = self._values.get("scheduled_query_execution_role_arn")
        assert result is not None, "Required property 'scheduled_query_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scheduled_query_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::ScheduledQuery.ScheduledQueryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryname
        '''
        result = self._values.get("scheduled_query_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::Timestream::ScheduledQuery.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.TargetConfigurationProperty]]:
        '''``AWS::Timestream::ScheduledQuery.TargetConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-targetconfiguration
        '''
        result = self._values.get("target_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnScheduledQuery.TargetConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTable(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-timestream.CfnTable",
):
    '''A CloudFormation ``AWS::Timestream::Table``.

    :cloudformationResource: AWS::Timestream::Table
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_timestream as timestream
        
        # retention_properties is of type object
        
        cfn_table = timestream.CfnTable(self, "MyCfnTable",
            database_name="databaseName",
        
            # the properties below are optional
            retention_properties=retention_properties,
            table_name="tableName",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        retention_properties: typing.Any = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: ``AWS::Timestream::Table.DatabaseName``.
        :param retention_properties: ``AWS::Timestream::Table.RetentionProperties``.
        :param table_name: ``AWS::Timestream::Table.TableName``.
        :param tags: ``AWS::Timestream::Table.Tags``.
        '''
        props = CfnTableProps(
            database_name=database_name,
            retention_properties=retention_properties,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''``AWS::Timestream::Table.DatabaseName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retentionProperties")
    def retention_properties(self) -> typing.Any:
        '''``AWS::Timestream::Table.RetentionProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        '''
        return typing.cast(typing.Any, jsii.get(self, "retentionProperties"))

    @retention_properties.setter
    def retention_properties(self, value: typing.Any) -> None:
        jsii.set(self, "retentionProperties", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Table.TableName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tableName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::Timestream::Table.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-timestream.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "retention_properties": "retentionProperties",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        retention_properties: typing.Any = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Timestream::Table``.

        :param database_name: ``AWS::Timestream::Table.DatabaseName``.
        :param retention_properties: ``AWS::Timestream::Table.RetentionProperties``.
        :param table_name: ``AWS::Timestream::Table.TableName``.
        :param tags: ``AWS::Timestream::Table.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_timestream as timestream
            
            # retention_properties is of type object
            
            cfn_table_props = timestream.CfnTableProps(
                database_name="databaseName",
            
                # the properties below are optional
                retention_properties=retention_properties,
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "database_name": database_name,
        }
        if retention_properties is not None:
            self._values["retention_properties"] = retention_properties
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> builtins.str:
        '''``AWS::Timestream::Table.DatabaseName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_properties(self) -> typing.Any:
        '''``AWS::Timestream::Table.RetentionProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        '''
        result = self._values.get("retention_properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Timestream::Table.TableName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::Timestream::Table.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDatabase",
    "CfnDatabaseProps",
    "CfnScheduledQuery",
    "CfnScheduledQueryProps",
    "CfnTable",
    "CfnTableProps",
]

publication.publish()
