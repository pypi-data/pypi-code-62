"""
# AWS Budget Notifier

Setup AWS Budget notifications using AWS CDK.
By default notifications are sent to all subscribers via e-mail.

## Configuration options

* Budget

  * `limit`: The budget limit, e.g. 10.
  * `unit`: The unit of measurement for the limit, e.g. USD.
* Cost Filters<br/>

  | Key  | Description |
  |---	|---	|
  | `application`	|  If specified the application (name) is added as tag filter. |
  | `availabilityZones` | If specified the availability zones (e.g. `eu-central-1`) is added as tag filter. |
  | `costcenter` 	| If specified the cost center is added as tag filter. |
  | `service`  	| If specified the service (e.g. Lambda, EC2) is added as tag filter. |
* Notification

  * `recipients`: Notifications are sent to this e-mail addresses
  * `threshold`:  Notifications are triggered if `threshold` percent of the budget are exceeded.

### Example usage

```javascript
import * as cdk from "@aws-cdk/core";

import { CfnBudget } from "@aws-cdk/aws-budgets";
import { StackProps } from "@aws-cdk/core";
import { BudgetNotifier } from "./budget_notifier";

export class BudgetNotifierStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new BudgetNotifier(this, "test", {
      recipients: ["john@doe.com"],
      availabilityZones: ["eu-central-1", "eu-west-1"],
      application: "HelloWorld",
      costCenter: "myCostCenter",
      limit: 10,
      unit: "USD",
      threshold: 75,
    });
  }
}
```

## Links

* [AWS Cloud Development Kit (CDK)](https://github.com/aws/aws-cdk)
* [Cost Explorer filters](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-filtering.html)
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

import aws_cdk.core


class BudgetNotifier(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@stefanfreitag/aws-budget-notifier.BudgetNotifier",
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
        limit: jsii.Number,
        recipients: typing.List[str],
        threshold: jsii.Number,
        unit: str,
        application: typing.Optional[str] = None,
        availability_zones: typing.Optional[typing.List[str]] = None,
        cost_center: typing.Optional[str] = None,
        service: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param limit: The cost associated with the budget threshold.
        :param recipients: Budget notifications will be sent to each of the recipients (e-mail addresses).
        :param threshold: The threshold value in percent (0-100).
        :param unit: The unit of measurement that is used for the budget threshold, such as dollars or GB.
        :param application: If specified the application name will be added as tag filter.
        :param availability_zones: If specified the availability zones will be added as tag filter.
        :param cost_center: If specified the cost center will be added as tag filter.
        :param service: If specified the service will be added as tag filter.

        stability
        :stability: experimental
        """
        props = BudgetNotifierProps(
            limit=limit,
            recipients=recipients,
            threshold=threshold,
            unit=unit,
            application=application,
            availability_zones=availability_zones,
            cost_center=cost_center,
            service=service,
        )

        jsii.create(BudgetNotifier, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@stefanfreitag/aws-budget-notifier.BudgetNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "recipients": "recipients",
        "threshold": "threshold",
        "unit": "unit",
        "application": "application",
        "availability_zones": "availabilityZones",
        "cost_center": "costCenter",
        "service": "service",
    },
)
class BudgetNotifierProps:
    def __init__(
        self,
        *,
        limit: jsii.Number,
        recipients: typing.List[str],
        threshold: jsii.Number,
        unit: str,
        application: typing.Optional[str] = None,
        availability_zones: typing.Optional[typing.List[str]] = None,
        cost_center: typing.Optional[str] = None,
        service: typing.Optional[str] = None,
    ) -> None:
        """
        :param limit: The cost associated with the budget threshold.
        :param recipients: Budget notifications will be sent to each of the recipients (e-mail addresses).
        :param threshold: The threshold value in percent (0-100).
        :param unit: The unit of measurement that is used for the budget threshold, such as dollars or GB.
        :param application: If specified the application name will be added as tag filter.
        :param availability_zones: If specified the availability zones will be added as tag filter.
        :param cost_center: If specified the cost center will be added as tag filter.
        :param service: If specified the service will be added as tag filter.

        stability
        :stability: experimental
        """
        self._values = {
            "limit": limit,
            "recipients": recipients,
            "threshold": threshold,
            "unit": unit,
        }
        if application is not None:
            self._values["application"] = application
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cost_center is not None:
            self._values["cost_center"] = cost_center
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def limit(self) -> jsii.Number:
        """The cost associated with the budget threshold.

        stability
        :stability: experimental
        """
        return self._values.get("limit")

    @builtins.property
    def recipients(self) -> typing.List[str]:
        """Budget notifications will be sent to each of the recipients (e-mail addresses).

        stability
        :stability: experimental
        """
        return self._values.get("recipients")

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The threshold value in percent (0-100).

        stability
        :stability: experimental
        """
        return self._values.get("threshold")

    @builtins.property
    def unit(self) -> str:
        """The unit of measurement that is used for the budget threshold, such as dollars or GB.

        stability
        :stability: experimental
        """
        return self._values.get("unit")

    @builtins.property
    def application(self) -> typing.Optional[str]:
        """If specified the application name will be added as tag filter.

        stability
        :stability: experimental
        """
        return self._values.get("application")

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """If specified the availability zones will be added as tag filter.

        stability
        :stability: experimental
        """
        return self._values.get("availability_zones")

    @builtins.property
    def cost_center(self) -> typing.Optional[str]:
        """If specified the cost center will be added as tag filter.

        stability
        :stability: experimental
        """
        return self._values.get("cost_center")

    @builtins.property
    def service(self) -> typing.Optional[str]:
        """If specified the service will be added as tag filter.

        stability
        :stability: experimental
        """
        return self._values.get("service")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BudgetNotifier",
    "BudgetNotifierProps",
]

publication.publish()
