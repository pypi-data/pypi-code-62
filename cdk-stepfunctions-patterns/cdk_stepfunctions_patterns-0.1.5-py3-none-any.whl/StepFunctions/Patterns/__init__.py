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

All these patterns are *composable*, meaning that you can combine them together to create
quite complex state machines that are much easier to maintain and support than low-level
JSON definitions.

* [Try / Catch](#try--catch-pattern)
* [Try / Finally](#try--finally-pattern)
* [Try / Catch / Finally](#try--catch--finally-pattern)
* [Retry with backoff and jitter](#retry-with-backoff-and-jitter)
* [Resilience lambda errors handling](#resilience-lambda-errors-handling)
* [Validation of proper resilience lambda errors handling](#validation-of-proper-resilience-lambda-errors-handling)

## Try / Catch pattern

Step Functions support **Try / Catch** pattern natively with [Task](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html)
and [Parallel](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html) states.

`TryTask` construct adds a high level abstraction that allows you to use Try / Catch pattern with any state or sequence of states.

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
from cdk_stepfunctions_patterns import TryTask

# ...

sfn.StateMachine(self, "TryCatchStepMachine",
    definition=TryTask(self, "TryCatch",
        try_process=sfn.Pass(self, "A1").next(sfn.Pass(self, "B1")),
        catch_process=sfn.Pass(self, "catchHandler"),
        # optional configuration properties
        catch_props={
            "errors": ["Lambda.AWSLambdaException"],
            "result_path": "$.ErrorDetails"
        }
    )
)
```

### Resulting StepFunction

![](doc/tryCatch.png)

## Try / Finally pattern

It is often useful to design state machine using **Try / Finally** pattern. The idea is to have a *Final* state that has to be
executed regardless of successful or failed execution of the *Try* state. There may be some temporal resource you want
to delete or notification to send.

Step Functions do not provide a native way to implement that pattern but it can be done using
[Parallel](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html) state and *catch all* catch
specification.

`TryTask` construct abstracts these implementation details and allows to express the pattern directly.

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
from cdk_stepfunctions_patterns import TryTask

# ...

sfn.StateMachine(self, "TryFinallyStepMachine",
    definition=TryTask(self, "TryFinally",
        try_process=sfn.Pass(self, "A2").next(sfn.Pass(self, "B2")),
        finally_process=sfn.Pass(self, "finallyHandler"),
        # optional configuration properties
        finally_error_path="$.FinallyErrorDetails"
    )
)
```

### Resulting StepFunction

![](doc/tryFinally.png)

## Try / Catch / Finally pattern

This is a combination of two previous patterns. `TryTask` construct allows you to express rather complex
error handling logic in a very compact form.

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
from cdk_stepfunctions_patterns import TryTask

# ...

sfn.StateMachine(self, "TryCatchFinallyStepMachine",
    definition=TryTask(self, "TryCatchFinalli",
        try_process=sfn.Pass(self, "A3").next(sfn.Pass(self, "B3")),
        catch_process=sfn.Pass(self, "catchHandler3"),
        finally_process=sfn.Pass(self, "finallyHandler3")
    )
)
```

### Resulting StepFunction

![](doc/tryCatchFinally.png)

## Retry with backoff and jitter

Out of the box Step Functions retry implementation provides a way to configure backoff factor,
but there is no built in way to introduce jitter. As covered in
[Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
and [Wait and Retry with Jittered Back-off](https://github.com/Polly-Contrib/Polly.Contrib.WaitAndRetry#wait-and-retry-with-jittered-back-off) this retry technique can be very helpful in high-load
scenarios.

`RetryWithJitterTask` construct provides a custom implementation of retry with backoff and
jitter that you can use directly in your state machines.

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
from cdk_stepfunctions_patterns import RetryWithJitterTask

# ...

sfn.StateMachine(self, "RetryWithJitterStepMachine",
    definition=RetryWithJitterTask(self, "AWithJitter",
        try_process=sfn.Pass(self, "A4").next(sfn.Pass(self, "B4")),
        retry_props={"errors": ["States.ALL"], "max_attempts": 3}
    )
)
```

### Resulting StepFunction

![](doc/retryWithJitter.png)

## Resilience lambda errors handling

`LambdaInvoke` construct from [aws-stepfunctions-tasks](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-stepfunctions-tasks-readme.html)
module is probably one of the most used ones. Still, handling of
[AWS Lambda service exceptions](https://docs.aws.amazon.com/step-functions/latest/dg/bp-lambda-serviceexception.html)
is often overlooked.

`ResilientLambdaTask` is a drop-in replacement construct for `LambdaInvoke` that adds retry for the most common
transient errors:

* Lambda.ServiceException
* Lambda.AWSLambdaException
* Lambda.SdkClientException
* Lambda.TooManyRequestsException

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
from cdk_stepfunctions_patterns import ResilientLambdaTask

# ...

lambda_function = lambda_.Function(self, "LambdaFunction")

calculate_jitter_task = ResilientLambdaTask(self, "InvokeLambda",
    lambda_function=lambda_function
)
```

That would result in the following state definition:

```json
"InvokeLambda": {
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
        "FunctionName": "<ARN of lambda function>"
    },
    "Retry": [{
        "ErrorEquals": [
        "Lambda.ServiceException",
        "Lambda.AWSLambdaException",
        "Lambda.SdkClientException",
        "Lambda.TooManyRequestsException"
        ],
        "IntervalSeconds": 2,
        "MaxAttempts": 6,
        "BackoffRate": 2
    }]
}
```

## Validation of proper resilience lambda errors handling

It is often a challenge to enforce consistent transient error handling across all state machines of a large
application. To help with that, *cdk-stepfuctions-patterns* provides a [CDK aspect](https://docs.aws.amazon.com/cdk/latest/guide/aspects.html)
to verify that all Lambda invocations correctly handle transient errors from AWS Lambda service.

Use `ResilienceLambdaChecker` aspect as shown below.

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_stepfunctions_patterns import ResilienceLambdaChecker

app = cdk.App()
# ...

# validate compliance rules
app.node.apply_aspect(ResilienceLambdaChecker())
```

If there are some states in your application that do not retry transient errors or miss some recommended
error codes, there will be warning during CDK synthesize stage:

```
PS C:\Dev\GitHub\cdk-stepfunctions-patterns> cdk synth --strict
[Warning at /StepFunctionsPatterns/A] No retry for AWS Lambda transient errors defined - consider using ResilientLambdaTask construct.
[Warning at /StepFunctionsPatterns/B] Missing retry for transient errors: Lambda.AWSLambdaException,Lambda.SdkClientException.
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

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
    """Define an aspect that validates all Lambda Invoke tasks and warns if AWS Lambda transient errors are not handled properly.

    stability
    :stability: experimental
    """

    def __init__(self, *, fail: typing.Optional[builtins.bool] = None) -> None:
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
    def __init__(self, *, fail: typing.Optional[builtins.bool] = None) -> None:
        """Properties for defining resilience lambda checker aspect.

        :param fail: 

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if fail is not None:
            self._values["fail"] = fail

    @builtins.property
    def fail(self) -> typing.Optional[builtins.bool]:
        """
        stability
        :stability: experimental
        """
        result = self._values.get("fail")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
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
    """Define a Lambda Invoke task with transient errors handling implemented.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        client_context: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        qualifier: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
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
        cls,
        task: aws_cdk.aws_stepfunctions_tasks.LambdaInvoke,
    ) -> None:
        """Adds retry for transient Lambda errors.

        :param task: Lambda tast to modify.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "addDefaultRetry", [task])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="TransientErrors")
    def TRANSIENT_ERRORS(cls) -> typing.List[builtins.str]:
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
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a retry with backoff and jitter construct.

        :param retry_props: Retry configuration.
        :param try_process: Try chain to execute.
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        if isinstance(retry_props, dict):
            retry_props = aws_cdk.aws_stepfunctions.RetryProps(**retry_props)
        self._values: typing.Dict[str, typing.Any] = {
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
        """Retry configuration.

        stability
        :stability: experimental
        """
        result = self._values.get("retry_props")
        assert result is not None, "Required property 'retry_props' is missing"
        return result

    @builtins.property
    def try_process(self) -> aws_cdk.aws_stepfunctions.IChainable:
        """Try chain to execute.

        stability
        :stability: experimental
        """
        result = self._values.get("try_process")
        assert result is not None, "Required property 'try_process' is missing"
        return result

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        result = self._values.get("result_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
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
    """Define a construct that implements retry with backoff and jitter.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        retry_props: aws_cdk.aws_stepfunctions.RetryProps,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param retry_props: Retry configuration.
        :param try_process: Try chain to execute.
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
        "catch_process": "catchProcess",
        "catch_props": "catchProps",
        "comment": "comment",
        "finally_error_path": "finallyErrorPath",
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
        catch_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        catch_props: typing.Optional[aws_cdk.aws_stepfunctions.CatchProps] = None,
        comment: typing.Optional[builtins.str] = None,
        finally_error_path: typing.Optional[builtins.str] = None,
        finally_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        input_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a try/catch/finally construct.

        :param try_process: Try chain to execute.
        :param catch_process: Optional catch chain to execute.
        :param catch_props: Catch properties.
        :param comment: An optional description for this state. Default: No comment
        :param finally_error_path: JSONPath expression to indicate where to map caught exception details.
        :param finally_process: Optional finally chain to execute.
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        if isinstance(catch_props, dict):
            catch_props = aws_cdk.aws_stepfunctions.CatchProps(**catch_props)
        self._values: typing.Dict[str, typing.Any] = {
            "try_process": try_process,
        }
        if catch_process is not None:
            self._values["catch_process"] = catch_process
        if catch_props is not None:
            self._values["catch_props"] = catch_props
        if comment is not None:
            self._values["comment"] = comment
        if finally_error_path is not None:
            self._values["finally_error_path"] = finally_error_path
        if finally_process is not None:
            self._values["finally_process"] = finally_process
        if input_path is not None:
            self._values["input_path"] = input_path
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def try_process(self) -> aws_cdk.aws_stepfunctions.IChainable:
        """Try chain to execute.

        stability
        :stability: experimental
        """
        result = self._values.get("try_process")
        assert result is not None, "Required property 'try_process' is missing"
        return result

    @builtins.property
    def catch_process(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IChainable]:
        """Optional catch chain to execute.

        stability
        :stability: experimental
        """
        result = self._values.get("catch_process")
        return result

    @builtins.property
    def catch_props(self) -> typing.Optional[aws_cdk.aws_stepfunctions.CatchProps]:
        """Catch properties.

        stability
        :stability: experimental
        """
        result = self._values.get("catch_props")
        return result

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def finally_error_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to map caught exception details.

        stability
        :stability: experimental
        """
        result = self._values.get("finally_error_path")
        return result

    @builtins.property
    def finally_process(self) -> typing.Optional[aws_cdk.aws_stepfunctions.IChainable]:
        """Optional finally chain to execute.

        stability
        :stability: experimental
        """
        result = self._values.get("finally_process")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        result = self._values.get("result_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
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
    """Define a construct that helps with handling StepFunctions exceptions.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        try_process: aws_cdk.aws_stepfunctions.IChainable,
        catch_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        catch_props: typing.Optional[aws_cdk.aws_stepfunctions.CatchProps] = None,
        comment: typing.Optional[builtins.str] = None,
        finally_error_path: typing.Optional[builtins.str] = None,
        finally_process: typing.Optional[aws_cdk.aws_stepfunctions.IChainable] = None,
        input_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param try_process: Try chain to execute.
        :param catch_process: Optional catch chain to execute.
        :param catch_props: Catch properties.
        :param comment: An optional description for this state. Default: No comment
        :param finally_error_path: JSONPath expression to indicate where to map caught exception details.
        :param finally_process: Optional finally chain to execute.
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = TryProps(
            try_process=try_process,
            catch_process=catch_process,
            catch_props=catch_props,
            comment=comment,
            finally_error_path=finally_error_path,
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
