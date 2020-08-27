"""
# Terraform CDK github Provider ~> 2.0

This repo builds and publishes the Terraform github Provider bindings for [cdktf](https://cdk.tf).

Current build targets are:

* npm
* Pypi

## Versioning

This project is explicitly not tracking the Terraform github Provider version 1:1. In fact, it always tracks `latest` of `~> 2.0` with every release. If there scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform github Provider](https://github.com/terraform-providers/terraform-provider-github)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform github Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

## projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

## cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/skorfmann/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

## provider version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).
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

import cdktf
import constructs


class ActionsSecret(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.ActionsSecret",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        plaintext_value: str,
        repository: str,
        secret_name: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param plaintext_value: 
        :param repository: 
        :param secret_name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ActionsSecretConfig(
            plaintext_value=plaintext_value,
            repository=repository,
            secret_name=secret_name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(ActionsSecret, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> str:
        return jsii.get(self, "createdAt")

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> str:
        return jsii.get(self, "updatedAt")

    @builtins.property
    @jsii.member(jsii_name="plaintextValue")
    def plaintext_value(self) -> str:
        return jsii.get(self, "plaintextValue")

    @plaintext_value.setter
    def plaintext_value(self, value: str) -> None:
        jsii.set(self, "plaintextValue", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> str:
        return jsii.get(self, "secretName")

    @secret_name.setter
    def secret_name(self, value: str) -> None:
        jsii.set(self, "secretName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.ActionsSecretConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "plaintext_value": "plaintextValue",
        "repository": "repository",
        "secret_name": "secretName",
    },
)
class ActionsSecretConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        plaintext_value: str,
        repository: str,
        secret_name: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param plaintext_value: 
        :param repository: 
        :param secret_name: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "plaintext_value": plaintext_value,
            "repository": repository,
            "secret_name": secret_name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def plaintext_value(self) -> str:
        return self._values.get("plaintext_value")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def secret_name(self) -> str:
        return self._values.get("secret_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Branch(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.Branch",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        branch: str,
        repository: str,
        source_branch: typing.Optional[str] = None,
        source_sha: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param branch: 
        :param repository: 
        :param source_branch: 
        :param source_sha: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = BranchConfig(
            branch=branch,
            repository=repository,
            source_branch=source_branch,
            source_sha=source_sha,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Branch, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        return jsii.get(self, "ref")

    @builtins.property
    @jsii.member(jsii_name="sha")
    def sha(self) -> str:
        return jsii.get(self, "sha")

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> str:
        return jsii.get(self, "branch")

    @branch.setter
    def branch(self, value: str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="sourceBranch")
    def source_branch(self) -> typing.Optional[str]:
        return jsii.get(self, "sourceBranch")

    @source_branch.setter
    def source_branch(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceBranch", value)

    @builtins.property
    @jsii.member(jsii_name="sourceSha")
    def source_sha(self) -> typing.Optional[str]:
        return jsii.get(self, "sourceSha")

    @source_sha.setter
    def source_sha(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceSha", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.BranchConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "branch": "branch",
        "repository": "repository",
        "source_branch": "sourceBranch",
        "source_sha": "sourceSha",
    },
)
class BranchConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        branch: str,
        repository: str,
        source_branch: typing.Optional[str] = None,
        source_sha: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param branch: 
        :param repository: 
        :param source_branch: 
        :param source_sha: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "branch": branch,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if source_branch is not None:
            self._values["source_branch"] = source_branch
        if source_sha is not None:
            self._values["source_sha"] = source_sha

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def branch(self) -> str:
        return self._values.get("branch")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def source_branch(self) -> typing.Optional[str]:
        return self._values.get("source_branch")

    @builtins.property
    def source_sha(self) -> typing.Optional[str]:
        return self._values.get("source_sha")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtection(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.BranchProtection",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        branch: str,
        repository: str,
        enforce_admins: typing.Optional[bool] = None,
        required_pull_request_reviews: typing.Optional[typing.List["BranchProtectionRequiredPullRequestReviews"]] = None,
        required_status_checks: typing.Optional[typing.List["BranchProtectionRequiredStatusChecks"]] = None,
        require_signed_commits: typing.Optional[bool] = None,
        restrictions: typing.Optional[typing.List["BranchProtectionRestrictions"]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param branch: 
        :param repository: 
        :param enforce_admins: 
        :param required_pull_request_reviews: required_pull_request_reviews block.
        :param required_status_checks: required_status_checks block.
        :param require_signed_commits: 
        :param restrictions: restrictions block.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = BranchProtectionConfig(
            branch=branch,
            repository=repository,
            enforce_admins=enforce_admins,
            required_pull_request_reviews=required_pull_request_reviews,
            required_status_checks=required_status_checks,
            require_signed_commits=require_signed_commits,
            restrictions=restrictions,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(BranchProtection, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> str:
        return jsii.get(self, "branch")

    @branch.setter
    def branch(self, value: str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="enforceAdmins")
    def enforce_admins(self) -> typing.Optional[bool]:
        return jsii.get(self, "enforceAdmins")

    @enforce_admins.setter
    def enforce_admins(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "enforceAdmins", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="requiredPullRequestReviews")
    def required_pull_request_reviews(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRequiredPullRequestReviews"]]:
        return jsii.get(self, "requiredPullRequestReviews")

    @required_pull_request_reviews.setter
    def required_pull_request_reviews(
        self,
        value: typing.Optional[typing.List["BranchProtectionRequiredPullRequestReviews"]],
    ) -> None:
        jsii.set(self, "requiredPullRequestReviews", value)

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecks")
    def required_status_checks(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRequiredStatusChecks"]]:
        return jsii.get(self, "requiredStatusChecks")

    @required_status_checks.setter
    def required_status_checks(
        self,
        value: typing.Optional[typing.List["BranchProtectionRequiredStatusChecks"]],
    ) -> None:
        jsii.set(self, "requiredStatusChecks", value)

    @builtins.property
    @jsii.member(jsii_name="requireSignedCommits")
    def require_signed_commits(self) -> typing.Optional[bool]:
        return jsii.get(self, "requireSignedCommits")

    @require_signed_commits.setter
    def require_signed_commits(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "requireSignedCommits", value)

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRestrictions"]]:
        return jsii.get(self, "restrictions")

    @restrictions.setter
    def restrictions(
        self, value: typing.Optional[typing.List["BranchProtectionRestrictions"]]
    ) -> None:
        jsii.set(self, "restrictions", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.BranchProtectionConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "branch": "branch",
        "repository": "repository",
        "enforce_admins": "enforceAdmins",
        "required_pull_request_reviews": "requiredPullRequestReviews",
        "required_status_checks": "requiredStatusChecks",
        "require_signed_commits": "requireSignedCommits",
        "restrictions": "restrictions",
    },
)
class BranchProtectionConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        branch: str,
        repository: str,
        enforce_admins: typing.Optional[bool] = None,
        required_pull_request_reviews: typing.Optional[typing.List["BranchProtectionRequiredPullRequestReviews"]] = None,
        required_status_checks: typing.Optional[typing.List["BranchProtectionRequiredStatusChecks"]] = None,
        require_signed_commits: typing.Optional[bool] = None,
        restrictions: typing.Optional[typing.List["BranchProtectionRestrictions"]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param branch: 
        :param repository: 
        :param enforce_admins: 
        :param required_pull_request_reviews: required_pull_request_reviews block.
        :param required_status_checks: required_status_checks block.
        :param require_signed_commits: 
        :param restrictions: restrictions block.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "branch": branch,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if enforce_admins is not None:
            self._values["enforce_admins"] = enforce_admins
        if required_pull_request_reviews is not None:
            self._values["required_pull_request_reviews"] = required_pull_request_reviews
        if required_status_checks is not None:
            self._values["required_status_checks"] = required_status_checks
        if require_signed_commits is not None:
            self._values["require_signed_commits"] = require_signed_commits
        if restrictions is not None:
            self._values["restrictions"] = restrictions

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def branch(self) -> str:
        return self._values.get("branch")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def enforce_admins(self) -> typing.Optional[bool]:
        return self._values.get("enforce_admins")

    @builtins.property
    def required_pull_request_reviews(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRequiredPullRequestReviews"]]:
        """required_pull_request_reviews block."""
        return self._values.get("required_pull_request_reviews")

    @builtins.property
    def required_status_checks(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRequiredStatusChecks"]]:
        """required_status_checks block."""
        return self._values.get("required_status_checks")

    @builtins.property
    def require_signed_commits(self) -> typing.Optional[bool]:
        return self._values.get("require_signed_commits")

    @builtins.property
    def restrictions(
        self,
    ) -> typing.Optional[typing.List["BranchProtectionRestrictions"]]:
        """restrictions block."""
        return self._values.get("restrictions")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.BranchProtectionRequiredPullRequestReviews",
    jsii_struct_bases=[],
    name_mapping={
        "dismissal_teams": "dismissalTeams",
        "dismissal_users": "dismissalUsers",
        "dismiss_stale_reviews": "dismissStaleReviews",
        "include_admins": "includeAdmins",
        "require_code_owner_reviews": "requireCodeOwnerReviews",
        "required_approving_review_count": "requiredApprovingReviewCount",
    },
)
class BranchProtectionRequiredPullRequestReviews:
    def __init__(
        self,
        *,
        dismissal_teams: typing.Optional[typing.List[str]] = None,
        dismissal_users: typing.Optional[typing.List[str]] = None,
        dismiss_stale_reviews: typing.Optional[bool] = None,
        include_admins: typing.Optional[bool] = None,
        require_code_owner_reviews: typing.Optional[bool] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param dismissal_teams: 
        :param dismissal_users: 
        :param dismiss_stale_reviews: 
        :param include_admins: 
        :param require_code_owner_reviews: 
        :param required_approving_review_count: 
        """
        self._values = {}
        if dismissal_teams is not None:
            self._values["dismissal_teams"] = dismissal_teams
        if dismissal_users is not None:
            self._values["dismissal_users"] = dismissal_users
        if dismiss_stale_reviews is not None:
            self._values["dismiss_stale_reviews"] = dismiss_stale_reviews
        if include_admins is not None:
            self._values["include_admins"] = include_admins
        if require_code_owner_reviews is not None:
            self._values["require_code_owner_reviews"] = require_code_owner_reviews
        if required_approving_review_count is not None:
            self._values["required_approving_review_count"] = required_approving_review_count

    @builtins.property
    def dismissal_teams(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("dismissal_teams")

    @builtins.property
    def dismissal_users(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("dismissal_users")

    @builtins.property
    def dismiss_stale_reviews(self) -> typing.Optional[bool]:
        return self._values.get("dismiss_stale_reviews")

    @builtins.property
    def include_admins(self) -> typing.Optional[bool]:
        return self._values.get("include_admins")

    @builtins.property
    def require_code_owner_reviews(self) -> typing.Optional[bool]:
        return self._values.get("require_code_owner_reviews")

    @builtins.property
    def required_approving_review_count(self) -> typing.Optional[jsii.Number]:
        return self._values.get("required_approving_review_count")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRequiredPullRequestReviews(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.BranchProtectionRequiredStatusChecks",
    jsii_struct_bases=[],
    name_mapping={
        "contexts": "contexts",
        "include_admins": "includeAdmins",
        "strict": "strict",
    },
)
class BranchProtectionRequiredStatusChecks:
    def __init__(
        self,
        *,
        contexts: typing.Optional[typing.List[str]] = None,
        include_admins: typing.Optional[bool] = None,
        strict: typing.Optional[bool] = None,
    ) -> None:
        """
        :param contexts: 
        :param include_admins: 
        :param strict: 
        """
        self._values = {}
        if contexts is not None:
            self._values["contexts"] = contexts
        if include_admins is not None:
            self._values["include_admins"] = include_admins
        if strict is not None:
            self._values["strict"] = strict

    @builtins.property
    def contexts(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("contexts")

    @builtins.property
    def include_admins(self) -> typing.Optional[bool]:
        return self._values.get("include_admins")

    @builtins.property
    def strict(self) -> typing.Optional[bool]:
        return self._values.get("strict")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRequiredStatusChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.BranchProtectionRestrictions",
    jsii_struct_bases=[],
    name_mapping={"apps": "apps", "teams": "teams", "users": "users"},
)
class BranchProtectionRestrictions:
    def __init__(
        self,
        *,
        apps: typing.Optional[typing.List[str]] = None,
        teams: typing.Optional[typing.List[str]] = None,
        users: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param apps: 
        :param teams: 
        :param users: 
        """
        self._values = {}
        if apps is not None:
            self._values["apps"] = apps
        if teams is not None:
            self._values["teams"] = teams
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def apps(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("apps")

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("teams")

    @builtins.property
    def users(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("users")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubActionsPublicKey(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubActionsPublicKey",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        repository: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param repository: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubActionsPublicKeyConfig(
            repository=repository,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubActionsPublicKey, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        return jsii.get(self, "keyId")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubActionsPublicKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "repository": "repository",
    },
)
class DataGithubActionsPublicKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        repository: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param repository: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubActionsPublicKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubBranch(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubBranch",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        branch: str,
        repository: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param branch: 
        :param repository: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubBranchConfig(
            branch=branch,
            repository=repository,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubBranch, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        return jsii.get(self, "ref")

    @builtins.property
    @jsii.member(jsii_name="sha")
    def sha(self) -> str:
        return jsii.get(self, "sha")

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> str:
        return jsii.get(self, "branch")

    @branch.setter
    def branch(self, value: str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubBranchConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "branch": "branch",
        "repository": "repository",
    },
)
class DataGithubBranchConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        branch: str,
        repository: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param branch: 
        :param repository: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "branch": branch,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def branch(self) -> str:
        return self._values.get("branch")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubBranchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubCollaborators(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubCollaborators",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        owner: str,
        repository: str,
        affiliation: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param owner: 
        :param repository: 
        :param affiliation: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubCollaboratorsConfig(
            owner=owner,
            repository=repository,
            affiliation=affiliation,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubCollaborators, self, [scope, id, config])

    @jsii.member(jsii_name="collaborator")
    def collaborator(self, index: str) -> "DataGithubCollaboratorsCollaborator":
        """
        :param index: -
        """
        return jsii.invoke(self, "collaborator", [index])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> str:
        return jsii.get(self, "owner")

    @owner.setter
    def owner(self, value: str) -> None:
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="affiliation")
    def affiliation(self) -> typing.Optional[str]:
        return jsii.get(self, "affiliation")

    @affiliation.setter
    def affiliation(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "affiliation", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


class DataGithubCollaboratorsCollaborator(
    cdktf.ComplexComputedList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubCollaboratorsCollaborator",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: str,
        index: str,
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -
        :param index: -

        stability
        :stability: experimental
        """
        jsii.create(DataGithubCollaboratorsCollaborator, self, [terraform_resource, terraform_attribute, index])

    @builtins.property
    @jsii.member(jsii_name="eventsUrl")
    def events_url(self) -> str:
        return jsii.get(self, "eventsUrl")

    @builtins.property
    @jsii.member(jsii_name="followersUrl")
    def followers_url(self) -> str:
        return jsii.get(self, "followersUrl")

    @builtins.property
    @jsii.member(jsii_name="followingUrl")
    def following_url(self) -> str:
        return jsii.get(self, "followingUrl")

    @builtins.property
    @jsii.member(jsii_name="gistsUrl")
    def gists_url(self) -> str:
        return jsii.get(self, "gistsUrl")

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> str:
        return jsii.get(self, "htmlUrl")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> str:
        return jsii.get(self, "login")

    @builtins.property
    @jsii.member(jsii_name="organizationsUrl")
    def organizations_url(self) -> str:
        return jsii.get(self, "organizationsUrl")

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> str:
        return jsii.get(self, "permission")

    @builtins.property
    @jsii.member(jsii_name="receivedEventsUrl")
    def received_events_url(self) -> str:
        return jsii.get(self, "receivedEventsUrl")

    @builtins.property
    @jsii.member(jsii_name="reposUrl")
    def repos_url(self) -> str:
        return jsii.get(self, "reposUrl")

    @builtins.property
    @jsii.member(jsii_name="siteAdmin")
    def site_admin(self) -> bool:
        return jsii.get(self, "siteAdmin")

    @builtins.property
    @jsii.member(jsii_name="starredUrl")
    def starred_url(self) -> str:
        return jsii.get(self, "starredUrl")

    @builtins.property
    @jsii.member(jsii_name="subscriptionsUrl")
    def subscriptions_url(self) -> str:
        return jsii.get(self, "subscriptionsUrl")

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubCollaboratorsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "owner": "owner",
        "repository": "repository",
        "affiliation": "affiliation",
    },
)
class DataGithubCollaboratorsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        owner: str,
        repository: str,
        affiliation: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param owner: 
        :param repository: 
        :param affiliation: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "owner": owner,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if affiliation is not None:
            self._values["affiliation"] = affiliation

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def owner(self) -> str:
        return self._values.get("owner")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def affiliation(self) -> typing.Optional[str]:
        return self._values.get("affiliation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubCollaboratorsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubIpRanges(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubIpRanges",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubIpRangesConfig(
            count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider
        )

        jsii.create(DataGithubIpRanges, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(self) -> typing.List[str]:
        return jsii.get(self, "git")

    @builtins.property
    @jsii.member(jsii_name="hooks")
    def hooks(self) -> typing.List[str]:
        return jsii.get(self, "hooks")

    @builtins.property
    @jsii.member(jsii_name="importer")
    def importer(self) -> typing.List[str]:
        return jsii.get(self, "importer")

    @builtins.property
    @jsii.member(jsii_name="pages")
    def pages(self) -> typing.List[str]:
        return jsii.get(self, "pages")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubIpRangesConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
    },
)
class DataGithubIpRangesConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubIpRangesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubMembership(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubMembership",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        username: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubMembershipConfig(
            username=username,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubMembership, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubMembershipConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "username": "username",
    },
)
class DataGithubMembershipConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        username: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param username: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubOrganizationTeamSyncGroups(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubOrganizationTeamSyncGroups",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubOrganizationTeamSyncGroupsConfig(
            count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider
        )

        jsii.create(DataGithubOrganizationTeamSyncGroups, self, [scope, id, config])

    @jsii.member(jsii_name="groups")
    def groups(self, index: str) -> "DataGithubOrganizationTeamSyncGroupsGroups":
        """
        :param index: -
        """
        return jsii.invoke(self, "groups", [index])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubOrganizationTeamSyncGroupsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
    },
)
class DataGithubOrganizationTeamSyncGroupsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubOrganizationTeamSyncGroupsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubOrganizationTeamSyncGroupsGroups(
    cdktf.ComplexComputedList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubOrganizationTeamSyncGroupsGroups",
):
    def __init__(
        self,
        terraform_resource: cdktf.ITerraformResource,
        terraform_attribute: str,
        index: str,
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -
        :param index: -

        stability
        :stability: experimental
        """
        jsii.create(DataGithubOrganizationTeamSyncGroupsGroups, self, [terraform_resource, terraform_attribute, index])

    @builtins.property
    @jsii.member(jsii_name="groupDescription")
    def group_description(self) -> str:
        return jsii.get(self, "groupDescription")

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> str:
        return jsii.get(self, "groupId")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        return jsii.get(self, "groupName")


class DataGithubRelease(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubRelease",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        owner: str,
        repository: str,
        retrieve_by: str,
        release_id: typing.Optional[jsii.Number] = None,
        release_tag: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param owner: 
        :param repository: 
        :param retrieve_by: 
        :param release_id: 
        :param release_tag: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubReleaseConfig(
            owner=owner,
            repository=repository,
            retrieve_by=retrieve_by,
            release_id=release_id,
            release_tag=release_tag,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubRelease, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="assertsUrl")
    def asserts_url(self) -> str:
        return jsii.get(self, "assertsUrl")

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> str:
        return jsii.get(self, "body")

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> str:
        return jsii.get(self, "createdAt")

    @builtins.property
    @jsii.member(jsii_name="draft")
    def draft(self) -> bool:
        return jsii.get(self, "draft")

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> str:
        return jsii.get(self, "htmlUrl")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="prerelease")
    def prerelease(self) -> bool:
        return jsii.get(self, "prerelease")

    @builtins.property
    @jsii.member(jsii_name="publishedAt")
    def published_at(self) -> str:
        return jsii.get(self, "publishedAt")

    @builtins.property
    @jsii.member(jsii_name="tarballUrl")
    def tarball_url(self) -> str:
        return jsii.get(self, "tarballUrl")

    @builtins.property
    @jsii.member(jsii_name="targetCommitish")
    def target_commitish(self) -> str:
        return jsii.get(self, "targetCommitish")

    @builtins.property
    @jsii.member(jsii_name="uploadUrl")
    def upload_url(self) -> str:
        return jsii.get(self, "uploadUrl")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="zipballUrl")
    def zipball_url(self) -> str:
        return jsii.get(self, "zipballUrl")

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> str:
        return jsii.get(self, "owner")

    @owner.setter
    def owner(self, value: str) -> None:
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="retrieveBy")
    def retrieve_by(self) -> str:
        return jsii.get(self, "retrieveBy")

    @retrieve_by.setter
    def retrieve_by(self, value: str) -> None:
        jsii.set(self, "retrieveBy", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="releaseId")
    def release_id(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "releaseId")

    @release_id.setter
    def release_id(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "releaseId", value)

    @builtins.property
    @jsii.member(jsii_name="releaseTag")
    def release_tag(self) -> typing.Optional[str]:
        return jsii.get(self, "releaseTag")

    @release_tag.setter
    def release_tag(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "releaseTag", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubReleaseConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "owner": "owner",
        "repository": "repository",
        "retrieve_by": "retrieveBy",
        "release_id": "releaseId",
        "release_tag": "releaseTag",
    },
)
class DataGithubReleaseConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        owner: str,
        repository: str,
        retrieve_by: str,
        release_id: typing.Optional[jsii.Number] = None,
        release_tag: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param owner: 
        :param repository: 
        :param retrieve_by: 
        :param release_id: 
        :param release_tag: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "owner": owner,
            "repository": repository,
            "retrieve_by": retrieve_by,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if release_id is not None:
            self._values["release_id"] = release_id
        if release_tag is not None:
            self._values["release_tag"] = release_tag

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def owner(self) -> str:
        return self._values.get("owner")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def retrieve_by(self) -> str:
        return self._values.get("retrieve_by")

    @builtins.property
    def release_id(self) -> typing.Optional[jsii.Number]:
        return self._values.get("release_id")

    @builtins.property
    def release_tag(self) -> typing.Optional[str]:
        return self._values.get("release_tag")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubReleaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubRepositories(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubRepositories",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        query: str,
        sort: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param query: 
        :param sort: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubRepositoriesConfig(
            query=query,
            sort=sort,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubRepositories, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="fullNames")
    def full_names(self) -> typing.List[str]:
        return jsii.get(self, "fullNames")

    @builtins.property
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[str]:
        return jsii.get(self, "names")

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> str:
        return jsii.get(self, "query")

    @query.setter
    def query(self, value: str) -> None:
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> typing.Optional[str]:
        return jsii.get(self, "sort")

    @sort.setter
    def sort(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sort", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubRepositoriesConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "query": "query",
        "sort": "sort",
    },
)
class DataGithubRepositoriesConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        query: str,
        sort: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param query: 
        :param sort: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "query": query,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if sort is not None:
            self._values["sort"] = sort

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def query(self) -> str:
        return self._values.get("query")

    @builtins.property
    def sort(self) -> typing.Optional[str]:
        return self._values.get("sort")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubRepositoriesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubRepository(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubRepository",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        full_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param full_name: 
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubRepositoryConfig(
            full_name=full_name,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubRepository, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="allowMergeCommit")
    def allow_merge_commit(self) -> bool:
        return jsii.get(self, "allowMergeCommit")

    @builtins.property
    @jsii.member(jsii_name="allowRebaseMerge")
    def allow_rebase_merge(self) -> bool:
        return jsii.get(self, "allowRebaseMerge")

    @builtins.property
    @jsii.member(jsii_name="allowSquashMerge")
    def allow_squash_merge(self) -> bool:
        return jsii.get(self, "allowSquashMerge")

    @builtins.property
    @jsii.member(jsii_name="archived")
    def archived(self) -> bool:
        return jsii.get(self, "archived")

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> str:
        return jsii.get(self, "defaultBranch")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        return jsii.get(self, "description")

    @builtins.property
    @jsii.member(jsii_name="gitCloneUrl")
    def git_clone_url(self) -> str:
        return jsii.get(self, "gitCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="hasDownloads")
    def has_downloads(self) -> bool:
        return jsii.get(self, "hasDownloads")

    @builtins.property
    @jsii.member(jsii_name="hasIssues")
    def has_issues(self) -> bool:
        return jsii.get(self, "hasIssues")

    @builtins.property
    @jsii.member(jsii_name="hasProjects")
    def has_projects(self) -> bool:
        return jsii.get(self, "hasProjects")

    @builtins.property
    @jsii.member(jsii_name="hasWiki")
    def has_wiki(self) -> bool:
        return jsii.get(self, "hasWiki")

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> str:
        return jsii.get(self, "homepageUrl")

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> str:
        return jsii.get(self, "htmlUrl")

    @builtins.property
    @jsii.member(jsii_name="httpCloneUrl")
    def http_clone_url(self) -> str:
        return jsii.get(self, "httpCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> str:
        return jsii.get(self, "nodeId")

    @builtins.property
    @jsii.member(jsii_name="private")
    def private(self) -> bool:
        return jsii.get(self, "private")

    @builtins.property
    @jsii.member(jsii_name="sshCloneUrl")
    def ssh_clone_url(self) -> str:
        return jsii.get(self, "sshCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="svnUrl")
    def svn_url(self) -> str:
        return jsii.get(self, "svnUrl")

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[str]:
        return jsii.get(self, "topics")

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> typing.Optional[str]:
        return jsii.get(self, "fullName")

    @full_name.setter
    def full_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "fullName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubRepositoryConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "full_name": "fullName",
        "name": "name",
    },
)
class DataGithubRepositoryConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        full_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param full_name: 
        :param name: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if full_name is not None:
            self._values["full_name"] = full_name
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def full_name(self) -> typing.Optional[str]:
        return self._values.get("full_name")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubTeam(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubTeam",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        slug: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param slug: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubTeamConfig(
            slug=slug,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubTeam, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        return jsii.get(self, "description")

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.List[str]:
        return jsii.get(self, "members")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> str:
        return jsii.get(self, "nodeId")

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> str:
        return jsii.get(self, "permission")

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> str:
        return jsii.get(self, "privacy")

    @builtins.property
    @jsii.member(jsii_name="slug")
    def slug(self) -> str:
        return jsii.get(self, "slug")

    @slug.setter
    def slug(self, value: str) -> None:
        jsii.set(self, "slug", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubTeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "slug": "slug",
    },
)
class DataGithubTeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        slug: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param slug: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "slug": slug,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def slug(self) -> str:
        return self._values.get("slug")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubTeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubUser(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.DataGithubUser",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        username: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataGithubUserConfig(
            username=username,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataGithubUser, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> str:
        return jsii.get(self, "avatarUrl")

    @builtins.property
    @jsii.member(jsii_name="bio")
    def bio(self) -> str:
        return jsii.get(self, "bio")

    @builtins.property
    @jsii.member(jsii_name="blog")
    def blog(self) -> str:
        return jsii.get(self, "blog")

    @builtins.property
    @jsii.member(jsii_name="company")
    def company(self) -> str:
        return jsii.get(self, "company")

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> str:
        return jsii.get(self, "createdAt")

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> str:
        return jsii.get(self, "email")

    @builtins.property
    @jsii.member(jsii_name="followers")
    def followers(self) -> jsii.Number:
        return jsii.get(self, "followers")

    @builtins.property
    @jsii.member(jsii_name="following")
    def following(self) -> jsii.Number:
        return jsii.get(self, "following")

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[str]:
        return jsii.get(self, "gpgKeys")

    @builtins.property
    @jsii.member(jsii_name="gravatarId")
    def gravatar_id(self) -> str:
        return jsii.get(self, "gravatarId")

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> str:
        return jsii.get(self, "location")

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> str:
        return jsii.get(self, "login")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> str:
        return jsii.get(self, "nodeId")

    @builtins.property
    @jsii.member(jsii_name="publicGists")
    def public_gists(self) -> jsii.Number:
        return jsii.get(self, "publicGists")

    @builtins.property
    @jsii.member(jsii_name="publicRepos")
    def public_repos(self) -> jsii.Number:
        return jsii.get(self, "publicRepos")

    @builtins.property
    @jsii.member(jsii_name="siteAdmin")
    def site_admin(self) -> bool:
        return jsii.get(self, "siteAdmin")

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[str]:
        return jsii.get(self, "sshKeys")

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> str:
        return jsii.get(self, "updatedAt")

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.DataGithubUserConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "username": "username",
    },
)
class DataGithubUserConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        username: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param username: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GithubProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.GithubProvider",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        alias: typing.Optional[str] = None,
        anonymous: typing.Optional[bool] = None,
        base_url: typing.Optional[str] = None,
        individual: typing.Optional[bool] = None,
        insecure: typing.Optional[bool] = None,
        organization: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alias: Alias name.
        :param anonymous: Authenticate without a token. When ``anonymous``is true, the provider will not be able to access resourcesthat require authentication.
        :param base_url: The GitHub Base API URL.
        :param individual: 
        :param insecure: Whether server should be accessed without verifying the TLS certificate.
        :param organization: The GitHub organization name to manage. If ``individual`` is false, ``organization`` is required.
        :param token: The OAuth token used to connect to GitHub. If ``anonymous`` is false, ``token`` is required.
        """
        config = GithubProviderConfig(
            alias=alias,
            anonymous=anonymous,
            base_url=base_url,
            individual=individual,
            insecure=insecure,
            organization=organization,
            token=token,
        )

        jsii.create(GithubProvider, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[str]:
        return jsii.get(self, "alias")

    @alias.setter
    def alias(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="anonymous")
    def anonymous(self) -> typing.Optional[bool]:
        return jsii.get(self, "anonymous")

    @anonymous.setter
    def anonymous(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "anonymous", value)

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> typing.Optional[str]:
        return jsii.get(self, "baseUrl")

    @base_url.setter
    def base_url(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "baseUrl", value)

    @builtins.property
    @jsii.member(jsii_name="individual")
    def individual(self) -> typing.Optional[bool]:
        return jsii.get(self, "individual")

    @individual.setter
    def individual(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "individual", value)

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(self) -> typing.Optional[bool]:
        return jsii.get(self, "insecure")

    @insecure.setter
    def insecure(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "insecure", value)

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> typing.Optional[str]:
        return jsii.get(self, "organization")

    @organization.setter
    def organization(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "organization", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[str]:
        return jsii.get(self, "token")

    @token.setter
    def token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "token", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.GithubProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "anonymous": "anonymous",
        "base_url": "baseUrl",
        "individual": "individual",
        "insecure": "insecure",
        "organization": "organization",
        "token": "token",
    },
)
class GithubProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[str] = None,
        anonymous: typing.Optional[bool] = None,
        base_url: typing.Optional[str] = None,
        individual: typing.Optional[bool] = None,
        insecure: typing.Optional[bool] = None,
        organization: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param alias: Alias name.
        :param anonymous: Authenticate without a token. When ``anonymous``is true, the provider will not be able to access resourcesthat require authentication.
        :param base_url: The GitHub Base API URL.
        :param individual: 
        :param insecure: Whether server should be accessed without verifying the TLS certificate.
        :param organization: The GitHub organization name to manage. If ``individual`` is false, ``organization`` is required.
        :param token: The OAuth token used to connect to GitHub. If ``anonymous`` is false, ``token`` is required.
        """
        self._values = {}
        if alias is not None:
            self._values["alias"] = alias
        if anonymous is not None:
            self._values["anonymous"] = anonymous
        if base_url is not None:
            self._values["base_url"] = base_url
        if individual is not None:
            self._values["individual"] = individual
        if insecure is not None:
            self._values["insecure"] = insecure
        if organization is not None:
            self._values["organization"] = organization
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def alias(self) -> typing.Optional[str]:
        """Alias name."""
        return self._values.get("alias")

    @builtins.property
    def anonymous(self) -> typing.Optional[bool]:
        """Authenticate without a token.

        When ``anonymous``is true, the provider will not be able to access resourcesthat require authentication.
        """
        return self._values.get("anonymous")

    @builtins.property
    def base_url(self) -> typing.Optional[str]:
        """The GitHub Base API URL."""
        return self._values.get("base_url")

    @builtins.property
    def individual(self) -> typing.Optional[bool]:
        return self._values.get("individual")

    @builtins.property
    def insecure(self) -> typing.Optional[bool]:
        """Whether server should be accessed without verifying the TLS certificate."""
        return self._values.get("insecure")

    @builtins.property
    def organization(self) -> typing.Optional[str]:
        """The GitHub organization name to manage.

        If ``individual`` is false, ``organization`` is required.
        """
        return self._values.get("organization")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """The OAuth token used to connect to GitHub.

        If ``anonymous`` is false, ``token`` is required.
        """
        return self._values.get("token")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IssueLabel(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.IssueLabel",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        color: str,
        name: str,
        repository: str,
        description: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param color: 
        :param name: 
        :param repository: 
        :param description: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = IssueLabelConfig(
            color=color,
            name=name,
            repository=repository,
            description=description,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(IssueLabel, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> str:
        return jsii.get(self, "color")

    @color.setter
    def color(self, value: str) -> None:
        jsii.set(self, "color", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.IssueLabelConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "color": "color",
        "name": "name",
        "repository": "repository",
        "description": "description",
    },
)
class IssueLabelConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        color: str,
        name: str,
        repository: str,
        description: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param color: 
        :param name: 
        :param repository: 
        :param description: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "color": color,
            "name": name,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def color(self) -> str:
        return self._values.get("color")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        return self._values.get("description")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueLabelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Membership(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.Membership",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        username: str,
        role: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: 
        :param role: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = MembershipConfig(
            username=username,
            role=role,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Membership, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[str]:
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "role", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.MembershipConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "username": "username",
        "role": "role",
    },
)
class MembershipConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        username: str,
        role: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param username: 
        :param role: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    @builtins.property
    def role(self) -> typing.Optional[str]:
        return self._values.get("role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationBlock(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.OrganizationBlock",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        username: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = OrganizationBlockConfig(
            username=username,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(OrganizationBlock, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.OrganizationBlockConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "username": "username",
    },
)
class OrganizationBlockConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        username: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param username: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationBlockConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationProject(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.OrganizationProject",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        body: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param body: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = OrganizationProjectConfig(
            name=name,
            body=body,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(OrganizationProject, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Optional[str]:
        return jsii.get(self, "body")

    @body.setter
    def body(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.OrganizationProjectConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "body": "body",
    },
)
class OrganizationProjectConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        body: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param body: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if body is not None:
            self._values["body"] = body

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def body(self) -> typing.Optional[str]:
        return self._values.get("body")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationWebhook(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.OrganizationWebhook",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        events: typing.List[str],
        active: typing.Optional[bool] = None,
        configuration: typing.Optional[typing.List["OrganizationWebhookConfiguration"]] = None,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param events: 
        :param active: 
        :param configuration: configuration block.
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = OrganizationWebhookConfig(
            events=events,
            active=active,
            configuration=configuration,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(OrganizationWebhook, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[str]:
        return jsii.get(self, "events")

    @events.setter
    def events(self, value: typing.List[str]) -> None:
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Optional[bool]:
        return jsii.get(self, "active")

    @active.setter
    def active(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.List["OrganizationWebhookConfiguration"]]:
        return jsii.get(self, "configuration")

    @configuration.setter
    def configuration(
        self, value: typing.Optional[typing.List["OrganizationWebhookConfiguration"]]
    ) -> None:
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.OrganizationWebhookConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "events": "events",
        "active": "active",
        "configuration": "configuration",
        "name": "name",
    },
)
class OrganizationWebhookConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        events: typing.List[str],
        active: typing.Optional[bool] = None,
        configuration: typing.Optional[typing.List["OrganizationWebhookConfiguration"]] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param events: 
        :param active: 
        :param configuration: configuration block.
        :param name: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "events": events,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if active is not None:
            self._values["active"] = active
        if configuration is not None:
            self._values["configuration"] = configuration
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def events(self) -> typing.List[str]:
        return self._values.get("events")

    @builtins.property
    def active(self) -> typing.Optional[bool]:
        return self._values.get("active")

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.List["OrganizationWebhookConfiguration"]]:
        """configuration block."""
        return self._values.get("configuration")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationWebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.OrganizationWebhookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "content_type": "contentType",
        "insecure_ssl": "insecureSsl",
        "secret": "secret",
    },
)
class OrganizationWebhookConfiguration:
    def __init__(
        self,
        *,
        url: str,
        content_type: typing.Optional[str] = None,
        insecure_ssl: typing.Optional[bool] = None,
        secret: typing.Optional[str] = None,
    ) -> None:
        """
        :param url: 
        :param content_type: 
        :param insecure_ssl: 
        :param secret: 
        """
        self._values = {
            "url": url,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if insecure_ssl is not None:
            self._values["insecure_ssl"] = insecure_ssl
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def url(self) -> str:
        return self._values.get("url")

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        return self._values.get("content_type")

    @builtins.property
    def insecure_ssl(self) -> typing.Optional[bool]:
        return self._values.get("insecure_ssl")

    @builtins.property
    def secret(self) -> typing.Optional[str]:
        return self._values.get("secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationWebhookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectColumn(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.ProjectColumn",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        project_id: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param project_id: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ProjectColumnConfig(
            name=name,
            project_id=project_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(ProjectColumn, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> str:
        return jsii.get(self, "projectId")

    @project_id.setter
    def project_id(self, value: str) -> None:
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.ProjectColumnConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "project_id": "projectId",
    },
)
class ProjectColumnConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        project_id: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param project_id: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
            "project_id": project_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def project_id(self) -> str:
        return self._values.get("project_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Repository(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.Repository",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        allow_merge_commit: typing.Optional[bool] = None,
        allow_rebase_merge: typing.Optional[bool] = None,
        allow_squash_merge: typing.Optional[bool] = None,
        archived: typing.Optional[bool] = None,
        auto_init: typing.Optional[bool] = None,
        default_branch: typing.Optional[str] = None,
        delete_branch_on_merge: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
        gitignore_template: typing.Optional[str] = None,
        has_downloads: typing.Optional[bool] = None,
        has_issues: typing.Optional[bool] = None,
        has_projects: typing.Optional[bool] = None,
        has_wiki: typing.Optional[bool] = None,
        homepage_url: typing.Optional[str] = None,
        is_template: typing.Optional[bool] = None,
        license_template: typing.Optional[str] = None,
        private: typing.Optional[bool] = None,
        template: typing.Optional[typing.List["RepositoryTemplate"]] = None,
        topics: typing.Optional[typing.List[str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param allow_merge_commit: 
        :param allow_rebase_merge: 
        :param allow_squash_merge: 
        :param archived: 
        :param auto_init: 
        :param default_branch: Can only be set after initial repository creation, and only if the target branch exists.
        :param delete_branch_on_merge: 
        :param description: 
        :param gitignore_template: 
        :param has_downloads: 
        :param has_issues: 
        :param has_projects: 
        :param has_wiki: 
        :param homepage_url: 
        :param is_template: 
        :param license_template: 
        :param private: 
        :param template: template block.
        :param topics: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryConfig(
            name=name,
            allow_merge_commit=allow_merge_commit,
            allow_rebase_merge=allow_rebase_merge,
            allow_squash_merge=allow_squash_merge,
            archived=archived,
            auto_init=auto_init,
            default_branch=default_branch,
            delete_branch_on_merge=delete_branch_on_merge,
            description=description,
            gitignore_template=gitignore_template,
            has_downloads=has_downloads,
            has_issues=has_issues,
            has_projects=has_projects,
            has_wiki=has_wiki,
            homepage_url=homepage_url,
            is_template=is_template,
            license_template=license_template,
            private=private,
            template=template,
            topics=topics,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Repository, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> str:
        return jsii.get(self, "fullName")

    @builtins.property
    @jsii.member(jsii_name="gitCloneUrl")
    def git_clone_url(self) -> str:
        return jsii.get(self, "gitCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> str:
        return jsii.get(self, "htmlUrl")

    @builtins.property
    @jsii.member(jsii_name="httpCloneUrl")
    def http_clone_url(self) -> str:
        return jsii.get(self, "httpCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> str:
        return jsii.get(self, "nodeId")

    @builtins.property
    @jsii.member(jsii_name="sshCloneUrl")
    def ssh_clone_url(self) -> str:
        return jsii.get(self, "sshCloneUrl")

    @builtins.property
    @jsii.member(jsii_name="svnUrl")
    def svn_url(self) -> str:
        return jsii.get(self, "svnUrl")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="allowMergeCommit")
    def allow_merge_commit(self) -> typing.Optional[bool]:
        return jsii.get(self, "allowMergeCommit")

    @allow_merge_commit.setter
    def allow_merge_commit(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "allowMergeCommit", value)

    @builtins.property
    @jsii.member(jsii_name="allowRebaseMerge")
    def allow_rebase_merge(self) -> typing.Optional[bool]:
        return jsii.get(self, "allowRebaseMerge")

    @allow_rebase_merge.setter
    def allow_rebase_merge(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "allowRebaseMerge", value)

    @builtins.property
    @jsii.member(jsii_name="allowSquashMerge")
    def allow_squash_merge(self) -> typing.Optional[bool]:
        return jsii.get(self, "allowSquashMerge")

    @allow_squash_merge.setter
    def allow_squash_merge(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "allowSquashMerge", value)

    @builtins.property
    @jsii.member(jsii_name="archived")
    def archived(self) -> typing.Optional[bool]:
        return jsii.get(self, "archived")

    @archived.setter
    def archived(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "archived", value)

    @builtins.property
    @jsii.member(jsii_name="autoInit")
    def auto_init(self) -> typing.Optional[bool]:
        return jsii.get(self, "autoInit")

    @auto_init.setter
    def auto_init(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "autoInit", value)

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> typing.Optional[str]:
        return jsii.get(self, "defaultBranch")

    @default_branch.setter
    def default_branch(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "defaultBranch", value)

    @builtins.property
    @jsii.member(jsii_name="deleteBranchOnMerge")
    def delete_branch_on_merge(self) -> typing.Optional[bool]:
        return jsii.get(self, "deleteBranchOnMerge")

    @delete_branch_on_merge.setter
    def delete_branch_on_merge(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "deleteBranchOnMerge", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="gitignoreTemplate")
    def gitignore_template(self) -> typing.Optional[str]:
        return jsii.get(self, "gitignoreTemplate")

    @gitignore_template.setter
    def gitignore_template(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "gitignoreTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="hasDownloads")
    def has_downloads(self) -> typing.Optional[bool]:
        return jsii.get(self, "hasDownloads")

    @has_downloads.setter
    def has_downloads(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "hasDownloads", value)

    @builtins.property
    @jsii.member(jsii_name="hasIssues")
    def has_issues(self) -> typing.Optional[bool]:
        return jsii.get(self, "hasIssues")

    @has_issues.setter
    def has_issues(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "hasIssues", value)

    @builtins.property
    @jsii.member(jsii_name="hasProjects")
    def has_projects(self) -> typing.Optional[bool]:
        return jsii.get(self, "hasProjects")

    @has_projects.setter
    def has_projects(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "hasProjects", value)

    @builtins.property
    @jsii.member(jsii_name="hasWiki")
    def has_wiki(self) -> typing.Optional[bool]:
        return jsii.get(self, "hasWiki")

    @has_wiki.setter
    def has_wiki(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "hasWiki", value)

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> typing.Optional[str]:
        return jsii.get(self, "homepageUrl")

    @homepage_url.setter
    def homepage_url(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "homepageUrl", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isTemplate")
    def is_template(self) -> typing.Optional[bool]:
        return jsii.get(self, "isTemplate")

    @is_template.setter
    def is_template(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "isTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="licenseTemplate")
    def license_template(self) -> typing.Optional[str]:
        return jsii.get(self, "licenseTemplate")

    @license_template.setter
    def license_template(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "licenseTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="private")
    def private(self) -> typing.Optional[bool]:
        return jsii.get(self, "private")

    @private.setter
    def private(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "private", value)

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Optional[typing.List["RepositoryTemplate"]]:
        return jsii.get(self, "template")

    @template.setter
    def template(
        self, value: typing.Optional[typing.List["RepositoryTemplate"]]
    ) -> None:
        jsii.set(self, "template", value)

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "topics")

    @topics.setter
    def topics(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "topics", value)


class RepositoryCollaborator(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.RepositoryCollaborator",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        repository: str,
        username: str,
        permission: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param repository: 
        :param username: 
        :param permission: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryCollaboratorConfig(
            repository=repository,
            username=username,
            permission=permission,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(RepositoryCollaborator, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="invitationId")
    def invitation_id(self) -> str:
        return jsii.get(self, "invitationId")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> typing.Optional[str]:
        return jsii.get(self, "permission")

    @permission.setter
    def permission(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "permission", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryCollaboratorConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "repository": "repository",
        "username": "username",
        "permission": "permission",
    },
)
class RepositoryCollaboratorConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        repository: str,
        username: str,
        permission: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param repository: 
        :param username: 
        :param permission: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "repository": repository,
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    @builtins.property
    def permission(self) -> typing.Optional[str]:
        return self._values.get("permission")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryCollaboratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "allow_merge_commit": "allowMergeCommit",
        "allow_rebase_merge": "allowRebaseMerge",
        "allow_squash_merge": "allowSquashMerge",
        "archived": "archived",
        "auto_init": "autoInit",
        "default_branch": "defaultBranch",
        "delete_branch_on_merge": "deleteBranchOnMerge",
        "description": "description",
        "gitignore_template": "gitignoreTemplate",
        "has_downloads": "hasDownloads",
        "has_issues": "hasIssues",
        "has_projects": "hasProjects",
        "has_wiki": "hasWiki",
        "homepage_url": "homepageUrl",
        "is_template": "isTemplate",
        "license_template": "licenseTemplate",
        "private": "private",
        "template": "template",
        "topics": "topics",
    },
)
class RepositoryConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        allow_merge_commit: typing.Optional[bool] = None,
        allow_rebase_merge: typing.Optional[bool] = None,
        allow_squash_merge: typing.Optional[bool] = None,
        archived: typing.Optional[bool] = None,
        auto_init: typing.Optional[bool] = None,
        default_branch: typing.Optional[str] = None,
        delete_branch_on_merge: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
        gitignore_template: typing.Optional[str] = None,
        has_downloads: typing.Optional[bool] = None,
        has_issues: typing.Optional[bool] = None,
        has_projects: typing.Optional[bool] = None,
        has_wiki: typing.Optional[bool] = None,
        homepage_url: typing.Optional[str] = None,
        is_template: typing.Optional[bool] = None,
        license_template: typing.Optional[str] = None,
        private: typing.Optional[bool] = None,
        template: typing.Optional[typing.List["RepositoryTemplate"]] = None,
        topics: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param allow_merge_commit: 
        :param allow_rebase_merge: 
        :param allow_squash_merge: 
        :param archived: 
        :param auto_init: 
        :param default_branch: Can only be set after initial repository creation, and only if the target branch exists.
        :param delete_branch_on_merge: 
        :param description: 
        :param gitignore_template: 
        :param has_downloads: 
        :param has_issues: 
        :param has_projects: 
        :param has_wiki: 
        :param homepage_url: 
        :param is_template: 
        :param license_template: 
        :param private: 
        :param template: template block.
        :param topics: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if allow_merge_commit is not None:
            self._values["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge is not None:
            self._values["allow_rebase_merge"] = allow_rebase_merge
        if allow_squash_merge is not None:
            self._values["allow_squash_merge"] = allow_squash_merge
        if archived is not None:
            self._values["archived"] = archived
        if auto_init is not None:
            self._values["auto_init"] = auto_init
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if delete_branch_on_merge is not None:
            self._values["delete_branch_on_merge"] = delete_branch_on_merge
        if description is not None:
            self._values["description"] = description
        if gitignore_template is not None:
            self._values["gitignore_template"] = gitignore_template
        if has_downloads is not None:
            self._values["has_downloads"] = has_downloads
        if has_issues is not None:
            self._values["has_issues"] = has_issues
        if has_projects is not None:
            self._values["has_projects"] = has_projects
        if has_wiki is not None:
            self._values["has_wiki"] = has_wiki
        if homepage_url is not None:
            self._values["homepage_url"] = homepage_url
        if is_template is not None:
            self._values["is_template"] = is_template
        if license_template is not None:
            self._values["license_template"] = license_template
        if private is not None:
            self._values["private"] = private
        if template is not None:
            self._values["template"] = template
        if topics is not None:
            self._values["topics"] = topics

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def allow_merge_commit(self) -> typing.Optional[bool]:
        return self._values.get("allow_merge_commit")

    @builtins.property
    def allow_rebase_merge(self) -> typing.Optional[bool]:
        return self._values.get("allow_rebase_merge")

    @builtins.property
    def allow_squash_merge(self) -> typing.Optional[bool]:
        return self._values.get("allow_squash_merge")

    @builtins.property
    def archived(self) -> typing.Optional[bool]:
        return self._values.get("archived")

    @builtins.property
    def auto_init(self) -> typing.Optional[bool]:
        return self._values.get("auto_init")

    @builtins.property
    def default_branch(self) -> typing.Optional[str]:
        """Can only be set after initial repository creation, and only if the target branch exists."""
        return self._values.get("default_branch")

    @builtins.property
    def delete_branch_on_merge(self) -> typing.Optional[bool]:
        return self._values.get("delete_branch_on_merge")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        return self._values.get("description")

    @builtins.property
    def gitignore_template(self) -> typing.Optional[str]:
        return self._values.get("gitignore_template")

    @builtins.property
    def has_downloads(self) -> typing.Optional[bool]:
        return self._values.get("has_downloads")

    @builtins.property
    def has_issues(self) -> typing.Optional[bool]:
        return self._values.get("has_issues")

    @builtins.property
    def has_projects(self) -> typing.Optional[bool]:
        return self._values.get("has_projects")

    @builtins.property
    def has_wiki(self) -> typing.Optional[bool]:
        return self._values.get("has_wiki")

    @builtins.property
    def homepage_url(self) -> typing.Optional[str]:
        return self._values.get("homepage_url")

    @builtins.property
    def is_template(self) -> typing.Optional[bool]:
        return self._values.get("is_template")

    @builtins.property
    def license_template(self) -> typing.Optional[str]:
        return self._values.get("license_template")

    @builtins.property
    def private(self) -> typing.Optional[bool]:
        return self._values.get("private")

    @builtins.property
    def template(self) -> typing.Optional[typing.List["RepositoryTemplate"]]:
        """template block."""
        return self._values.get("template")

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("topics")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryDeployKey(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.RepositoryDeployKey",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        key: str,
        repository: str,
        title: str,
        read_only: typing.Optional[bool] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param key: 
        :param repository: 
        :param title: 
        :param read_only: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryDeployKeyConfig(
            key=key,
            repository=repository,
            title=title,
            read_only=read_only,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(RepositoryDeployKey, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @key.setter
    def key(self, value: str) -> None:
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> str:
        return jsii.get(self, "title")

    @title.setter
    def title(self, value: str) -> None:
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Optional[bool]:
        return jsii.get(self, "readOnly")

    @read_only.setter
    def read_only(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "readOnly", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryDeployKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "key": "key",
        "repository": "repository",
        "title": "title",
        "read_only": "readOnly",
    },
)
class RepositoryDeployKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        key: str,
        repository: str,
        title: str,
        read_only: typing.Optional[bool] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param key: 
        :param repository: 
        :param title: 
        :param read_only: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "key": key,
            "repository": repository,
            "title": title,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def key(self) -> str:
        return self._values.get("key")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def title(self) -> str:
        return self._values.get("title")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        return self._values.get("read_only")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDeployKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryFile(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.RepositoryFile",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        content: str,
        file: str,
        repository: str,
        branch: typing.Optional[str] = None,
        commit_author: typing.Optional[str] = None,
        commit_email: typing.Optional[str] = None,
        commit_message: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param content: The file's content.
        :param file: The file path to manage.
        :param repository: The repository name.
        :param branch: The branch name, defaults to "master".
        :param commit_author: The commit author name, defaults to the authenticated user's name.
        :param commit_email: The commit author email address, defaults to the authenticated user's email address.
        :param commit_message: The commit message when creating or updating the file.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryFileConfig(
            content=content,
            file=file,
            repository=repository,
            branch=branch,
            commit_author=commit_author,
            commit_email=commit_email,
            commit_message=commit_message,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(RepositoryFile, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="sha")
    def sha(self) -> str:
        return jsii.get(self, "sha")

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> str:
        return jsii.get(self, "content")

    @content.setter
    def content(self, value: str) -> None:
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> str:
        return jsii.get(self, "file")

    @file.setter
    def file(self, value: str) -> None:
        jsii.set(self, "file", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> typing.Optional[str]:
        return jsii.get(self, "branch")

    @branch.setter
    def branch(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="commitAuthor")
    def commit_author(self) -> typing.Optional[str]:
        return jsii.get(self, "commitAuthor")

    @commit_author.setter
    def commit_author(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "commitAuthor", value)

    @builtins.property
    @jsii.member(jsii_name="commitEmail")
    def commit_email(self) -> typing.Optional[str]:
        return jsii.get(self, "commitEmail")

    @commit_email.setter
    def commit_email(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "commitEmail", value)

    @builtins.property
    @jsii.member(jsii_name="commitMessage")
    def commit_message(self) -> typing.Optional[str]:
        return jsii.get(self, "commitMessage")

    @commit_message.setter
    def commit_message(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "commitMessage", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryFileConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "content": "content",
        "file": "file",
        "repository": "repository",
        "branch": "branch",
        "commit_author": "commitAuthor",
        "commit_email": "commitEmail",
        "commit_message": "commitMessage",
    },
)
class RepositoryFileConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        content: str,
        file: str,
        repository: str,
        branch: typing.Optional[str] = None,
        commit_author: typing.Optional[str] = None,
        commit_email: typing.Optional[str] = None,
        commit_message: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param content: The file's content.
        :param file: The file path to manage.
        :param repository: The repository name.
        :param branch: The branch name, defaults to "master".
        :param commit_author: The commit author name, defaults to the authenticated user's name.
        :param commit_email: The commit author email address, defaults to the authenticated user's email address.
        :param commit_message: The commit message when creating or updating the file.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "content": content,
            "file": file,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if branch is not None:
            self._values["branch"] = branch
        if commit_author is not None:
            self._values["commit_author"] = commit_author
        if commit_email is not None:
            self._values["commit_email"] = commit_email
        if commit_message is not None:
            self._values["commit_message"] = commit_message

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def content(self) -> str:
        """The file's content."""
        return self._values.get("content")

    @builtins.property
    def file(self) -> str:
        """The file path to manage."""
        return self._values.get("file")

    @builtins.property
    def repository(self) -> str:
        """The repository name."""
        return self._values.get("repository")

    @builtins.property
    def branch(self) -> typing.Optional[str]:
        """The branch name, defaults to "master"."""
        return self._values.get("branch")

    @builtins.property
    def commit_author(self) -> typing.Optional[str]:
        """The commit author name, defaults to the authenticated user's name."""
        return self._values.get("commit_author")

    @builtins.property
    def commit_email(self) -> typing.Optional[str]:
        """The commit author email address, defaults to the authenticated user's email address."""
        return self._values.get("commit_email")

    @builtins.property
    def commit_message(self) -> typing.Optional[str]:
        """The commit message when creating or updating the file."""
        return self._values.get("commit_message")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryProject(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.RepositoryProject",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        repository: str,
        body: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param repository: 
        :param body: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryProjectConfig(
            name=name,
            repository=repository,
            body=body,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(RepositoryProject, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Optional[str]:
        return jsii.get(self, "body")

    @body.setter
    def body(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryProjectConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "repository": "repository",
        "body": "body",
    },
)
class RepositoryProjectConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        repository: str,
        body: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param repository: 
        :param body: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if body is not None:
            self._values["body"] = body

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def body(self) -> typing.Optional[str]:
        return self._values.get("body")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryTemplate",
    jsii_struct_bases=[],
    name_mapping={"owner": "owner", "repository": "repository"},
)
class RepositoryTemplate:
    def __init__(self, *, owner: str, repository: str) -> None:
        """
        :param owner: 
        :param repository: 
        """
        self._values = {
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def owner(self) -> str:
        return self._values.get("owner")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryWebhook(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.RepositoryWebhook",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        events: typing.List[str],
        repository: str,
        active: typing.Optional[bool] = None,
        configuration: typing.Optional[typing.List["RepositoryWebhookConfiguration"]] = None,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param events: 
        :param repository: 
        :param active: 
        :param configuration: configuration block.
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = RepositoryWebhookConfig(
            events=events,
            repository=repository,
            active=active,
            configuration=configuration,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(RepositoryWebhook, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[str]:
        return jsii.get(self, "events")

    @events.setter
    def events(self, value: typing.List[str]) -> None:
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Optional[bool]:
        return jsii.get(self, "active")

    @active.setter
    def active(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.List["RepositoryWebhookConfiguration"]]:
        return jsii.get(self, "configuration")

    @configuration.setter
    def configuration(
        self, value: typing.Optional[typing.List["RepositoryWebhookConfiguration"]]
    ) -> None:
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryWebhookConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "events": "events",
        "repository": "repository",
        "active": "active",
        "configuration": "configuration",
        "name": "name",
    },
)
class RepositoryWebhookConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        events: typing.List[str],
        repository: str,
        active: typing.Optional[bool] = None,
        configuration: typing.Optional[typing.List["RepositoryWebhookConfiguration"]] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param events: 
        :param repository: 
        :param active: 
        :param configuration: configuration block.
        :param name: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "events": events,
            "repository": repository,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if active is not None:
            self._values["active"] = active
        if configuration is not None:
            self._values["configuration"] = configuration
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def events(self) -> typing.List[str]:
        return self._values.get("events")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def active(self) -> typing.Optional[bool]:
        return self._values.get("active")

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.List["RepositoryWebhookConfiguration"]]:
        """configuration block."""
        return self._values.get("configuration")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryWebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.RepositoryWebhookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "content_type": "contentType",
        "insecure_ssl": "insecureSsl",
        "secret": "secret",
    },
)
class RepositoryWebhookConfiguration:
    def __init__(
        self,
        *,
        url: str,
        content_type: typing.Optional[str] = None,
        insecure_ssl: typing.Optional[bool] = None,
        secret: typing.Optional[str] = None,
    ) -> None:
        """
        :param url: 
        :param content_type: 
        :param insecure_ssl: 
        :param secret: 
        """
        self._values = {
            "url": url,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if insecure_ssl is not None:
            self._values["insecure_ssl"] = insecure_ssl
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def url(self) -> str:
        return self._values.get("url")

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        return self._values.get("content_type")

    @builtins.property
    def insecure_ssl(self) -> typing.Optional[bool]:
        return self._values.get("insecure_ssl")

    @builtins.property
    def secret(self) -> typing.Optional[str]:
        return self._values.get("secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryWebhookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Team(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.Team",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        description: typing.Optional[str] = None,
        ldap_dn: typing.Optional[str] = None,
        parent_team_id: typing.Optional[jsii.Number] = None,
        privacy: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param description: 
        :param ldap_dn: 
        :param parent_team_id: 
        :param privacy: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = TeamConfig(
            name=name,
            description=description,
            ldap_dn=ldap_dn,
            parent_team_id=parent_team_id,
            privacy=privacy,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Team, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> str:
        return jsii.get(self, "nodeId")

    @builtins.property
    @jsii.member(jsii_name="slug")
    def slug(self) -> str:
        return jsii.get(self, "slug")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ldapDn")
    def ldap_dn(self) -> typing.Optional[str]:
        return jsii.get(self, "ldapDn")

    @ldap_dn.setter
    def ldap_dn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ldapDn", value)

    @builtins.property
    @jsii.member(jsii_name="parentTeamId")
    def parent_team_id(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "parentTeamId")

    @parent_team_id.setter
    def parent_team_id(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "parentTeamId", value)

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> typing.Optional[str]:
        return jsii.get(self, "privacy")

    @privacy.setter
    def privacy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "privacy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.TeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "description": "description",
        "ldap_dn": "ldapDn",
        "parent_team_id": "parentTeamId",
        "privacy": "privacy",
    },
)
class TeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        description: typing.Optional[str] = None,
        ldap_dn: typing.Optional[str] = None,
        parent_team_id: typing.Optional[jsii.Number] = None,
        privacy: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param description: 
        :param ldap_dn: 
        :param parent_team_id: 
        :param privacy: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if ldap_dn is not None:
            self._values["ldap_dn"] = ldap_dn
        if parent_team_id is not None:
            self._values["parent_team_id"] = parent_team_id
        if privacy is not None:
            self._values["privacy"] = privacy

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        return self._values.get("description")

    @builtins.property
    def ldap_dn(self) -> typing.Optional[str]:
        return self._values.get("ldap_dn")

    @builtins.property
    def parent_team_id(self) -> typing.Optional[jsii.Number]:
        return self._values.get("parent_team_id")

    @builtins.property
    def privacy(self) -> typing.Optional[str]:
        return self._values.get("privacy")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamMembership(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.TeamMembership",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        team_id: str,
        username: str,
        role: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param team_id: 
        :param username: 
        :param role: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = TeamMembershipConfig(
            team_id=team_id,
            username=username,
            role=role,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(TeamMembership, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> str:
        return jsii.get(self, "teamId")

    @team_id.setter
    def team_id(self, value: str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str) -> None:
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[str]:
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "role", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.TeamMembershipConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "username": "username",
        "role": "role",
    },
)
class TeamMembershipConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: str,
        username: str,
        role: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: 
        :param username: 
        :param role: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "team_id": team_id,
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def team_id(self) -> str:
        return self._values.get("team_id")

    @builtins.property
    def username(self) -> str:
        return self._values.get("username")

    @builtins.property
    def role(self) -> typing.Optional[str]:
        return self._values.get("role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamRepository(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.TeamRepository",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        repository: str,
        team_id: str,
        permission: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param repository: 
        :param team_id: 
        :param permission: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = TeamRepositoryConfig(
            repository=repository,
            team_id=team_id,
            permission=permission,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(TeamRepository, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> str:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> str:
        return jsii.get(self, "teamId")

    @team_id.setter
    def team_id(self, value: str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> typing.Optional[str]:
        return jsii.get(self, "permission")

    @permission.setter
    def permission(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "permission", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.TeamRepositoryConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "repository": "repository",
        "team_id": "teamId",
        "permission": "permission",
    },
)
class TeamRepositoryConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        repository: str,
        team_id: str,
        permission: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param repository: 
        :param team_id: 
        :param permission: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "repository": repository,
            "team_id": team_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def repository(self) -> str:
        return self._values.get("repository")

    @builtins.property
    def team_id(self) -> str:
        return self._values.get("team_id")

    @builtins.property
    def permission(self) -> typing.Optional[str]:
        return self._values.get("permission")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamSyncGroupMapping(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.TeamSyncGroupMapping",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        team_slug: str,
        group: typing.Optional[typing.List["TeamSyncGroupMappingGroup"]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param team_slug: 
        :param group: group block.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = TeamSyncGroupMappingConfig(
            team_slug=team_slug,
            group=group,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(TeamSyncGroupMapping, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="teamSlug")
    def team_slug(self) -> str:
        return jsii.get(self, "teamSlug")

    @team_slug.setter
    def team_slug(self, value: str) -> None:
        jsii.set(self, "teamSlug", value)

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[typing.List["TeamSyncGroupMappingGroup"]]:
        return jsii.get(self, "group")

    @group.setter
    def group(
        self, value: typing.Optional[typing.List["TeamSyncGroupMappingGroup"]]
    ) -> None:
        jsii.set(self, "group", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.TeamSyncGroupMappingConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_slug": "teamSlug",
        "group": "group",
    },
)
class TeamSyncGroupMappingConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_slug: str,
        group: typing.Optional[typing.List["TeamSyncGroupMappingGroup"]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_slug: 
        :param group: group block.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "team_slug": team_slug,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if group is not None:
            self._values["group"] = group

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def team_slug(self) -> str:
        return self._values.get("team_slug")

    @builtins.property
    def group(self) -> typing.Optional[typing.List["TeamSyncGroupMappingGroup"]]:
        """group block."""
        return self._values.get("group")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamSyncGroupMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.TeamSyncGroupMappingGroup",
    jsii_struct_bases=[],
    name_mapping={
        "group_description": "groupDescription",
        "group_id": "groupId",
        "group_name": "groupName",
    },
)
class TeamSyncGroupMappingGroup:
    def __init__(
        self, *, group_description: str, group_id: str, group_name: str
    ) -> None:
        """
        :param group_description: 
        :param group_id: 
        :param group_name: 
        """
        self._values = {
            "group_description": group_description,
            "group_id": group_id,
            "group_name": group_name,
        }

    @builtins.property
    def group_description(self) -> str:
        return self._values.get("group_description")

    @builtins.property
    def group_id(self) -> str:
        return self._values.get("group_id")

    @builtins.property
    def group_name(self) -> str:
        return self._values.get("group_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamSyncGroupMappingGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserGpgKey(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.UserGpgKey",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        armored_public_key: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param armored_public_key: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = UserGpgKeyConfig(
            armored_public_key=armored_public_key,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(UserGpgKey, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        return jsii.get(self, "keyId")

    @builtins.property
    @jsii.member(jsii_name="armoredPublicKey")
    def armored_public_key(self) -> str:
        return jsii.get(self, "armoredPublicKey")

    @armored_public_key.setter
    def armored_public_key(self, value: str) -> None:
        jsii.set(self, "armoredPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.UserGpgKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "armored_public_key": "armoredPublicKey",
    },
)
class UserGpgKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        armored_public_key: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param armored_public_key: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "armored_public_key": armored_public_key,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def armored_public_key(self) -> str:
        return self._values.get("armored_public_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserGpgKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserInvitationAccepter(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.UserInvitationAccepter",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        invitation_id: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param invitation_id: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = UserInvitationAccepterConfig(
            invitation_id=invitation_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(UserInvitationAccepter, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="invitationId")
    def invitation_id(self) -> str:
        return jsii.get(self, "invitationId")

    @invitation_id.setter
    def invitation_id(self, value: str) -> None:
        jsii.set(self, "invitationId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.UserInvitationAccepterConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "invitation_id": "invitationId",
    },
)
class UserInvitationAccepterConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        invitation_id: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param invitation_id: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "invitation_id": invitation_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def invitation_id(self) -> str:
        return self._values.get("invitation_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserInvitationAccepterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserSshKey(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.UserSshKey",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        key: str,
        title: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param key: 
        :param title: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = UserSshKeyConfig(
            key=key,
            title=title,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(UserSshKey, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> str:
        return jsii.get(self, "etag")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @key.setter
    def key(self, value: str) -> None:
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> str:
        return jsii.get(self, "title")

    @title.setter
    def title(self, value: str) -> None:
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-github.UserSshKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "key": "key",
        "title": "title",
    },
)
class UserSshKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        key: str,
        title: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param key: 
        :param title: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "key": key,
            "title": title,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.TerraformResource]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def key(self) -> str:
        return self._values.get("key")

    @builtins.property
    def title(self) -> str:
        return self._values.get("title")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserSshKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionsSecret",
    "ActionsSecretConfig",
    "Branch",
    "BranchConfig",
    "BranchProtection",
    "BranchProtectionConfig",
    "BranchProtectionRequiredPullRequestReviews",
    "BranchProtectionRequiredStatusChecks",
    "BranchProtectionRestrictions",
    "DataGithubActionsPublicKey",
    "DataGithubActionsPublicKeyConfig",
    "DataGithubBranch",
    "DataGithubBranchConfig",
    "DataGithubCollaborators",
    "DataGithubCollaboratorsCollaborator",
    "DataGithubCollaboratorsConfig",
    "DataGithubIpRanges",
    "DataGithubIpRangesConfig",
    "DataGithubMembership",
    "DataGithubMembershipConfig",
    "DataGithubOrganizationTeamSyncGroups",
    "DataGithubOrganizationTeamSyncGroupsConfig",
    "DataGithubOrganizationTeamSyncGroupsGroups",
    "DataGithubRelease",
    "DataGithubReleaseConfig",
    "DataGithubRepositories",
    "DataGithubRepositoriesConfig",
    "DataGithubRepository",
    "DataGithubRepositoryConfig",
    "DataGithubTeam",
    "DataGithubTeamConfig",
    "DataGithubUser",
    "DataGithubUserConfig",
    "GithubProvider",
    "GithubProviderConfig",
    "IssueLabel",
    "IssueLabelConfig",
    "Membership",
    "MembershipConfig",
    "OrganizationBlock",
    "OrganizationBlockConfig",
    "OrganizationProject",
    "OrganizationProjectConfig",
    "OrganizationWebhook",
    "OrganizationWebhookConfig",
    "OrganizationWebhookConfiguration",
    "ProjectColumn",
    "ProjectColumnConfig",
    "Repository",
    "RepositoryCollaborator",
    "RepositoryCollaboratorConfig",
    "RepositoryConfig",
    "RepositoryDeployKey",
    "RepositoryDeployKeyConfig",
    "RepositoryFile",
    "RepositoryFileConfig",
    "RepositoryProject",
    "RepositoryProjectConfig",
    "RepositoryTemplate",
    "RepositoryWebhook",
    "RepositoryWebhookConfig",
    "RepositoryWebhookConfiguration",
    "Team",
    "TeamConfig",
    "TeamMembership",
    "TeamMembershipConfig",
    "TeamRepository",
    "TeamRepositoryConfig",
    "TeamSyncGroupMapping",
    "TeamSyncGroupMappingConfig",
    "TeamSyncGroupMappingGroup",
    "UserGpgKey",
    "UserGpgKeyConfig",
    "UserInvitationAccepter",
    "UserInvitationAccepterConfig",
    "UserSshKey",
    "UserSshKeyConfig",
]

publication.publish()
