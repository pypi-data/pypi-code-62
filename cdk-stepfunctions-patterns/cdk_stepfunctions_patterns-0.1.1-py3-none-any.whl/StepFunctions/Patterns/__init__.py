"""
# cdk-stepfunctions-patterns

![build](https://github.com/kolomied/cdk-stepfunctions-patterns/workflows/build/badge.svg)
![jsii-publish](https://github.com/kolomied/cdk-stepfunctions-patterns/workflows/jsii-publish/badge.svg)
![downloads](https://img.shields.io/npm/dt/cdk-stepfunctions-patterns)

[![npm version](https://badge.fury.io/js/cdk-stepfunctions-patterns.svg)](https://badge.fury.io/js/cdk-stepfunctions-patterns)
[![PyPI version](https://badge.fury.io/py/cdk-stepfunctions-patterns.svg)](https://badge.fury.io/py/cdk-stepfunctions-patterns)
[![NuGet version](https://badge.fury.io/nu/Talnakh.StepFunctions.Patterns.svg)](https://badge.fury.io/nu/Talnakh.StepFunctions.Patterns)

*cdk-stepfunctions-patterns* library is a set of [AWS CDK](https://aws.amazon.com/cdk/) constructs that provide
resiliency patterns implementation for AWS Step Functions.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_stepfunctions_tasks
import aws_cdk.core


@jsii.implements(aws_cdk.core.IAspect)
class ResilienceLambdaChecker(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-stepfunctions-patterns.ResilienceLambdaChecker",
):
    """
    stability
    :stability: experimental
    """

    def __init__(self, *, fail: typing.Optional[bool] = None) -> None:
        """
        :param fail: 

        stability
        :stability: experimental
        """
        props = ResilienceLambdaCheckerProps(fail=fail)

        jsii.create(ResilienceLambdaChecker, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, construct: aws_cdk.core.IConstruct) -> None:
        """All aspects can visit an IConstruct.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "visit", [construct])


@jsii.data_type(
    jsii_type="cdk-stepfunctions-patterns.ResilienceLambdaCheckerProps",
    jsii_struct_bases=[],
    name_mapping={"fail": "fail"},
)
class ResilienceLambdaCheckerProps:
    def __init__(self, *, fail: typing.Optional[bool] = None) -> None:
        """
        :param fail: 

        stability
        :stability: experimental
        """
        self._values = {}
        if fail is not None:
            self._values["fail"] = fail

    @builtins.property
    def fail(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("fail")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResilienceLambdaCheckerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResilientLambdaTask(
    aws_cdk.aws_stepfunctions_tasks.LambdaInvoke,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-stepfunctions-patterns.ResilientLambdaTask",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        client_context: typing.Optional[str] = None,
        invocation_type: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        payload_response_only: typing.Optional[bool] = None,
        qualifier: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[str] = None,
        result_path: typing.Optional[str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
        :param payload_response_only: Invoke the Lambda in a way that only returns the payload response without additional metadata. The ``payloadResponseOnly`` property cannot be used if ``integrationPattern``, ``invocationType``, ``clientContext``, or ``qualifier`` are specified. It always uses the REQUEST_RESPONSE behavior. Default: false
        :param qualifier: Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the ``lambdaFunction`` argument. Default: - Version or alias inherent to the ``lambdaFunction`` object.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_stepfunctions_tasks.LambdaInvokeProps(
            lambda_function=lambda_function,
            client_context=client_context,
            invocation_type=invocation_type,
            payload=payload,
            payload_response_only=payload_response_only,
            qualifier=qualifier,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(ResilientLambdaTask, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultRetry")
    @builtins.classmethod
    def add_default_retry(
        cls, task: aws_cdk.aws_stepfunctions_tasks.LambdaInvoke
    ) -> None:
        """
        :param task: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "addDefaultRetry", [task])

    @jsii.python.classproperty
    @jsii.member(jsii_name="TransientErrors")
    def TRANSIENT_ERRORS(cls) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TransientErrors")


@jsii.data_type(
    jsii_type="cdk-stepfunctions-patterns.RetryWithJitterProps",
    jsii_struct_bases=[],
    name_mapping={
        "retry_props": "retryProps",
        "try_process": "tryProcess",
        "comment": "comment",
        "input_path": "inputPath",
        "result_path": "resultPath",
    },
)
class RetryWithJitterProps:
    def __init__(
        self,
        *,
        retry_props: aws_cdk.aws_stepfunctions.RetryProps,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        comment: typing.Optional[str] = None,
        input_path: typing.Optional[str] = None,
        result_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param retry_props: 
        :param try_process: 
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        if isinstance(retry_props, dict):
            retry_props = aws_cdk.aws_stepfunctions.RetryProps(**retry_props)
        self._values = {
            "retry_props": retry_props,
            "try_process": try_process,
        }
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def retry_props(self) -> aws_cdk.aws_stepfunctions.RetryProps:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_props")

    @builtins.property
    def try_process(self) -> aws_cdk.aws_stepfunctions.IChainable:
        """
        stability
        :stability: experimental
        """
        return self._values.get("try_process")

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get("comment")

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get("input_path")

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get("result_path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryWithJitterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RetryWithJitterTask(
    aws_cdk.aws_stepfunctions.Parallel,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-stepfunctions-patterns.RetryWithJitterTask",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        retry_props: aws_cdk.aws_stepfunctions.RetryProps,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        comment: typing.Optional[str] = None,
        input_path: typing.Optional[str] = None,
        result_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param retry_props: 
        :param try_process: 
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = RetryWithJitterProps(
            retry_props=retry_props,
            try_process=try_process,
            comment=comment,
            input_path=input_path,
            result_path=result_path,
        )

        jsii.create(RetryWithJitterTask, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-stepfunctions-patterns.TryProps",
    jsii_struct_bases=[],
    name_mapping={
        "try_process": "tryProcess",
        "catch_error_path": "catchErrorPath",
        "catch_process": "catchProcess",
        "catch_props": "catchProps",
        "comment": "comment",
        "finally_process": "finallyProcess",
        "input_path": "inputPath",
        "result_path": "resultPath",
    },
)
class TryProps:
    def __init__(
        self,
        *,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        catch_error_path: typing.Optional[str] = None,
        catch_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        catch_props: typing.Optional[aws_cdk.aws_stepfunctions.CatchProps] = None,
        comment: typing.Optional[str] = None,
        finally_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        input_path: typing.Optional[str] = None,
        result_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param try_process: 
        :param catch_error_path: 
        :param catch_process: 
        :param catch_props: 
        :param comment: An optional description for this state. Default: No comment
        :param finally_process: 
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        if isinstance(catch_props, dict):
            catch_props = aws_cdk.aws_stepfunctions.CatchProps(**catch_props)
        self._values = {
            "try_process": try_process,
        }
        if catch_error_path is not None:
            self._values["catch_error_path"] = catch_error_path
        if catch_process is not None:
            self._values["catch_process"] = catch_process
        if catch_props is not None:
            self._values["catch_props"] = catch_props
        if comment is not None:
            self._values["comment"] = comment
        if finally_process is not None:
            self._values["finally_process"] = finally_process
        if input_path is not None:
            self._values["input_path"] = input_path
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def try_process(self) -> aws_cdk.aws_stepfunctions.IChainable:
        """
        stability
        :stability: experimental
        """
        return self._values.get("try_process")

    @builtins.property
    def catch_error_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("catch_error_path")

    @builtins.property
    def catch_process(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IChainable]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("catch_process")

    @builtins.property
    def catch_props(self) -> typing.Optional[aws_cdk.aws_stepfunctions.CatchProps]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("catch_props")

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get("comment")

    @builtins.property
    def finally_process(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IChainable]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("finally_process")

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get("input_path")

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get("result_path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TryTask(
    aws_cdk.aws_stepfunctions.Parallel,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-stepfunctions-patterns.TryTask",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        catch_error_path: typing.Optional[str] = None,
        catch_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        catch_props: typing.Optional[aws_cdk.aws_stepfunctions.CatchProps] = None,
        comment: typing.Optional[str] = None,
        finally_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        input_path: typing.Optional[str] = None,
        result_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param try_process: 
        :param catch_error_path: 
        :param catch_process: 
        :param catch_props: 
        :param comment: An optional description for this state. Default: No comment
        :param finally_process: 
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = TryProps(
            try_process=try_process,
            catch_error_path=catch_error_path,
            catch_process=catch_process,
            catch_props=catch_props,
            comment=comment,
            finally_process=finally_process,
            input_path=input_path,
            result_path=result_path,
        )

        jsii.create(TryTask, self, [scope, id, props])


__all__ = [
    "ResilienceLambdaChecker",
    "ResilienceLambdaCheckerProps",
    "ResilientLambdaTask",
    "RetryWithJitterProps",
    "RetryWithJitterTask",
    "TryProps",
    "TryTask",
]

publication.publish()
