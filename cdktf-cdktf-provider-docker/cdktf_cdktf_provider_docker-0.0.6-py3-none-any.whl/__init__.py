"""
# Terraform CDK docker Provider ~> 2.0

This repo builds and publishes the Terraform docker Provider bindings for [cdktf](https://cdk.tf).

Current build targets are:

* npm
* Pypi

## Versioning

This project is explicitly not tracking the Terraform docker Provider version 1:1. In fact, it always tracks `latest` of `~> 2.0` with every release. If there scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform docker Provider](https://github.com/terraform-providers/terraform-provider-docker)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform docker Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

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


class Config(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Config",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        data: str,
        name: str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param data: Base64-url-safe-encoded config data.
        :param name: User-defined name of the config.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ConfigConfig(
            data=data,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Config, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> str:
        return jsii.get(self, "data")

    @data.setter
    def data(self, value: str) -> None:
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "data": "data",
        "name": "name",
    },
)
class ConfigConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        data: str,
        name: str,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param data: Base64-url-safe-encoded config data.
        :param name: User-defined name of the config.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "data": data,
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
    def data(self) -> str:
        """Base64-url-safe-encoded config data."""
        return self._values.get("data")

    @builtins.property
    def name(self) -> str:
        """User-defined name of the config."""
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Container(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Container",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        image: str,
        name: str,
        attach: typing.Optional[bool] = None,
        capabilities: typing.Optional[typing.List["ContainerCapabilities"]] = None,
        command: typing.Optional[typing.List[str]] = None,
        cpu_set: typing.Optional[str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        destroy_grace_seconds: typing.Optional[jsii.Number] = None,
        devices: typing.Optional[typing.List["ContainerDevices"]] = None,
        dns: typing.Optional[typing.List[str]] = None,
        dns_opts: typing.Optional[typing.List[str]] = None,
        dns_search: typing.Optional[typing.List[str]] = None,
        domainname: typing.Optional[str] = None,
        entrypoint: typing.Optional[typing.List[str]] = None,
        env: typing.Optional[typing.List[str]] = None,
        group_add: typing.Optional[typing.List[str]] = None,
        healthcheck: typing.Optional[typing.List["ContainerHealthcheck"]] = None,
        host: typing.Optional[typing.List["ContainerHost"]] = None,
        hostname: typing.Optional[str] = None,
        ipc_mode: typing.Optional[str] = None,
        labels: typing.Optional[typing.List["ContainerLabels"]] = None,
        links: typing.Optional[typing.List[str]] = None,
        log_driver: typing.Optional[str] = None,
        log_opts: typing.Optional[typing.Mapping[str, str]] = None,
        logs: typing.Optional[bool] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        mounts: typing.Optional[typing.List["ContainerMounts"]] = None,
        must_run: typing.Optional[bool] = None,
        network_alias: typing.Optional[typing.List[str]] = None,
        network_mode: typing.Optional[str] = None,
        networks: typing.Optional[typing.List[str]] = None,
        networks_advanced: typing.Optional[typing.List["ContainerNetworksAdvanced"]] = None,
        pid_mode: typing.Optional[str] = None,
        ports: typing.Optional[typing.List["ContainerPorts"]] = None,
        privileged: typing.Optional[bool] = None,
        publish_all_ports: typing.Optional[bool] = None,
        read_only: typing.Optional[bool] = None,
        restart: typing.Optional[str] = None,
        rm: typing.Optional[bool] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        start: typing.Optional[bool] = None,
        sysctls: typing.Optional[typing.Mapping[str, str]] = None,
        tmpfs: typing.Optional[typing.Mapping[str, str]] = None,
        ulimit: typing.Optional[typing.List["ContainerUlimit"]] = None,
        upload: typing.Optional[typing.List["ContainerUpload"]] = None,
        user: typing.Optional[str] = None,
        userns_mode: typing.Optional[str] = None,
        volumes: typing.Optional[typing.List["ContainerVolumes"]] = None,
        working_dir: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param image: 
        :param name: 
        :param attach: 
        :param capabilities: capabilities block.
        :param command: 
        :param cpu_set: 
        :param cpu_shares: 
        :param destroy_grace_seconds: 
        :param devices: devices block.
        :param dns: 
        :param dns_opts: 
        :param dns_search: 
        :param domainname: 
        :param entrypoint: 
        :param env: 
        :param group_add: Additional groups for the container user.
        :param healthcheck: healthcheck block.
        :param host: host block.
        :param hostname: 
        :param ipc_mode: IPC sharing mode for the container.
        :param labels: labels block.
        :param links: 
        :param log_driver: 
        :param log_opts: 
        :param logs: 
        :param max_retry_count: 
        :param memory: 
        :param memory_swap: 
        :param mounts: mounts block.
        :param must_run: 
        :param network_alias: Set an alias for the container in all specified networks.
        :param network_mode: 
        :param networks: 
        :param networks_advanced: networks_advanced block.
        :param pid_mode: 
        :param ports: ports block.
        :param privileged: 
        :param publish_all_ports: 
        :param read_only: 
        :param restart: 
        :param rm: 
        :param shm_size: 
        :param start: 
        :param sysctls: 
        :param tmpfs: 
        :param ulimit: ulimit block.
        :param upload: upload block.
        :param user: 
        :param userns_mode: 
        :param volumes: volumes block.
        :param working_dir: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ContainerConfig(
            image=image,
            name=name,
            attach=attach,
            capabilities=capabilities,
            command=command,
            cpu_set=cpu_set,
            cpu_shares=cpu_shares,
            destroy_grace_seconds=destroy_grace_seconds,
            devices=devices,
            dns=dns,
            dns_opts=dns_opts,
            dns_search=dns_search,
            domainname=domainname,
            entrypoint=entrypoint,
            env=env,
            group_add=group_add,
            healthcheck=healthcheck,
            host=host,
            hostname=hostname,
            ipc_mode=ipc_mode,
            labels=labels,
            links=links,
            log_driver=log_driver,
            log_opts=log_opts,
            logs=logs,
            max_retry_count=max_retry_count,
            memory=memory,
            memory_swap=memory_swap,
            mounts=mounts,
            must_run=must_run,
            network_alias=network_alias,
            network_mode=network_mode,
            networks=networks,
            networks_advanced=networks_advanced,
            pid_mode=pid_mode,
            ports=ports,
            privileged=privileged,
            publish_all_ports=publish_all_ports,
            read_only=read_only,
            restart=restart,
            rm=rm,
            shm_size=shm_size,
            start=start,
            sysctls=sysctls,
            tmpfs=tmpfs,
            ulimit=ulimit,
            upload=upload,
            user=user,
            userns_mode=userns_mode,
            volumes=volumes,
            working_dir=working_dir,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Container, self, [scope, id, config])

    @jsii.member(jsii_name="networkData")
    def network_data(self, index: str) -> "ContainerNetworkData":
        """
        :param index: -
        """
        return jsii.invoke(self, "networkData", [index])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="bridge")
    def bridge(self) -> str:
        return jsii.get(self, "bridge")

    @builtins.property
    @jsii.member(jsii_name="containerLogs")
    def container_logs(self) -> str:
        return jsii.get(self, "containerLogs")

    @builtins.property
    @jsii.member(jsii_name="exitCode")
    def exit_code(self) -> jsii.Number:
        return jsii.get(self, "exitCode")

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> str:
        return jsii.get(self, "gateway")

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> str:
        return jsii.get(self, "ipAddress")

    @builtins.property
    @jsii.member(jsii_name="ipPrefixLength")
    def ip_prefix_length(self) -> jsii.Number:
        return jsii.get(self, "ipPrefixLength")

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> str:
        return jsii.get(self, "image")

    @image.setter
    def image(self, value: str) -> None:
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="attach")
    def attach(self) -> typing.Optional[bool]:
        return jsii.get(self, "attach")

    @attach.setter
    def attach(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "attach", value)

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List["ContainerCapabilities"]]:
        return jsii.get(self, "capabilities")

    @capabilities.setter
    def capabilities(
        self, value: typing.Optional[typing.List["ContainerCapabilities"]]
    ) -> None:
        jsii.set(self, "capabilities", value)

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "command")

    @command.setter
    def command(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "command", value)

    @builtins.property
    @jsii.member(jsii_name="cpuSet")
    def cpu_set(self) -> typing.Optional[str]:
        return jsii.get(self, "cpuSet")

    @cpu_set.setter
    def cpu_set(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cpuSet", value)

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "cpuShares")

    @cpu_shares.setter
    def cpu_shares(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "cpuShares", value)

    @builtins.property
    @jsii.member(jsii_name="destroyGraceSeconds")
    def destroy_grace_seconds(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "destroyGraceSeconds")

    @destroy_grace_seconds.setter
    def destroy_grace_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "destroyGraceSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="devices")
    def devices(self) -> typing.Optional[typing.List["ContainerDevices"]]:
        return jsii.get(self, "devices")

    @devices.setter
    def devices(self, value: typing.Optional[typing.List["ContainerDevices"]]) -> None:
        jsii.set(self, "devices", value)

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "dns")

    @dns.setter
    def dns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dns", value)

    @builtins.property
    @jsii.member(jsii_name="dnsOpts")
    def dns_opts(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "dnsOpts")

    @dns_opts.setter
    def dns_opts(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dnsOpts", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSearch")
    def dns_search(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "dnsSearch")

    @dns_search.setter
    def dns_search(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dnsSearch", value)

    @builtins.property
    @jsii.member(jsii_name="domainname")
    def domainname(self) -> typing.Optional[str]:
        return jsii.get(self, "domainname")

    @domainname.setter
    def domainname(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "domainname", value)

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "entrypoint")

    @entrypoint.setter
    def entrypoint(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "entrypoint", value)

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "env")

    @env.setter
    def env(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "env", value)

    @builtins.property
    @jsii.member(jsii_name="groupAdd")
    def group_add(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "groupAdd")

    @group_add.setter
    def group_add(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "groupAdd", value)

    @builtins.property
    @jsii.member(jsii_name="healthcheck")
    def healthcheck(self) -> typing.Optional[typing.List["ContainerHealthcheck"]]:
        return jsii.get(self, "healthcheck")

    @healthcheck.setter
    def healthcheck(
        self, value: typing.Optional[typing.List["ContainerHealthcheck"]]
    ) -> None:
        jsii.set(self, "healthcheck", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> typing.Optional[typing.List["ContainerHost"]]:
        return jsii.get(self, "host")

    @host.setter
    def host(self, value: typing.Optional[typing.List["ContainerHost"]]) -> None:
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> typing.Optional[str]:
        return jsii.get(self, "hostname")

    @hostname.setter
    def hostname(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipcMode")
    def ipc_mode(self) -> typing.Optional[str]:
        return jsii.get(self, "ipcMode")

    @ipc_mode.setter
    def ipc_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ipcMode", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[typing.List["ContainerLabels"]]:
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Optional[typing.List["ContainerLabels"]]) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "links")

    @links.setter
    def links(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "links", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[str]:
        return jsii.get(self, "logDriver")

    @log_driver.setter
    def log_driver(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "logDriver", value)

    @builtins.property
    @jsii.member(jsii_name="logOpts")
    def log_opts(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "logOpts")

    @log_opts.setter
    def log_opts(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "logOpts", value)

    @builtins.property
    @jsii.member(jsii_name="logs")
    def logs(self) -> typing.Optional[bool]:
        return jsii.get(self, "logs")

    @logs.setter
    def logs(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "logs", value)

    @builtins.property
    @jsii.member(jsii_name="maxRetryCount")
    def max_retry_count(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "maxRetryCount")

    @max_retry_count.setter
    def max_retry_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxRetryCount", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "memory")

    @memory.setter
    def memory(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="memorySwap")
    def memory_swap(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "memorySwap")

    @memory_swap.setter
    def memory_swap(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "memorySwap", value)

    @builtins.property
    @jsii.member(jsii_name="mounts")
    def mounts(self) -> typing.Optional[typing.List["ContainerMounts"]]:
        return jsii.get(self, "mounts")

    @mounts.setter
    def mounts(self, value: typing.Optional[typing.List["ContainerMounts"]]) -> None:
        jsii.set(self, "mounts", value)

    @builtins.property
    @jsii.member(jsii_name="mustRun")
    def must_run(self) -> typing.Optional[bool]:
        return jsii.get(self, "mustRun")

    @must_run.setter
    def must_run(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "mustRun", value)

    @builtins.property
    @jsii.member(jsii_name="networkAlias")
    def network_alias(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "networkAlias")

    @network_alias.setter
    def network_alias(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "networkAlias", value)

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> typing.Optional[str]:
        return jsii.get(self, "networkMode")

    @network_mode.setter
    def network_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "networkMode", value)

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "networks")

    @networks.setter
    def networks(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "networks", value)

    @builtins.property
    @jsii.member(jsii_name="networksAdvanced")
    def networks_advanced(
        self,
    ) -> typing.Optional[typing.List["ContainerNetworksAdvanced"]]:
        return jsii.get(self, "networksAdvanced")

    @networks_advanced.setter
    def networks_advanced(
        self, value: typing.Optional[typing.List["ContainerNetworksAdvanced"]]
    ) -> None:
        jsii.set(self, "networksAdvanced", value)

    @builtins.property
    @jsii.member(jsii_name="pidMode")
    def pid_mode(self) -> typing.Optional[str]:
        return jsii.get(self, "pidMode")

    @pid_mode.setter
    def pid_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "pidMode", value)

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List["ContainerPorts"]]:
        return jsii.get(self, "ports")

    @ports.setter
    def ports(self, value: typing.Optional[typing.List["ContainerPorts"]]) -> None:
        jsii.set(self, "ports", value)

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[bool]:
        return jsii.get(self, "privileged")

    @privileged.setter
    def privileged(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "privileged", value)

    @builtins.property
    @jsii.member(jsii_name="publishAllPorts")
    def publish_all_ports(self) -> typing.Optional[bool]:
        return jsii.get(self, "publishAllPorts")

    @publish_all_ports.setter
    def publish_all_ports(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "publishAllPorts", value)

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Optional[bool]:
        return jsii.get(self, "readOnly")

    @read_only.setter
    def read_only(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "readOnly", value)

    @builtins.property
    @jsii.member(jsii_name="restart")
    def restart(self) -> typing.Optional[str]:
        return jsii.get(self, "restart")

    @restart.setter
    def restart(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "restart", value)

    @builtins.property
    @jsii.member(jsii_name="rm")
    def rm(self) -> typing.Optional[bool]:
        return jsii.get(self, "rm")

    @rm.setter
    def rm(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "rm", value)

    @builtins.property
    @jsii.member(jsii_name="shmSize")
    def shm_size(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "shmSize")

    @shm_size.setter
    def shm_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "shmSize", value)

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> typing.Optional[bool]:
        return jsii.get(self, "start")

    @start.setter
    def start(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "start", value)

    @builtins.property
    @jsii.member(jsii_name="sysctls")
    def sysctls(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "sysctls")

    @sysctls.setter
    def sysctls(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "sysctls", value)

    @builtins.property
    @jsii.member(jsii_name="tmpfs")
    def tmpfs(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "tmpfs")

    @tmpfs.setter
    def tmpfs(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "tmpfs", value)

    @builtins.property
    @jsii.member(jsii_name="ulimit")
    def ulimit(self) -> typing.Optional[typing.List["ContainerUlimit"]]:
        return jsii.get(self, "ulimit")

    @ulimit.setter
    def ulimit(self, value: typing.Optional[typing.List["ContainerUlimit"]]) -> None:
        jsii.set(self, "ulimit", value)

    @builtins.property
    @jsii.member(jsii_name="upload")
    def upload(self) -> typing.Optional[typing.List["ContainerUpload"]]:
        return jsii.get(self, "upload")

    @upload.setter
    def upload(self, value: typing.Optional[typing.List["ContainerUpload"]]) -> None:
        jsii.set(self, "upload", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[str]:
        return jsii.get(self, "user")

    @user.setter
    def user(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="usernsMode")
    def userns_mode(self) -> typing.Optional[str]:
        return jsii.get(self, "usernsMode")

    @userns_mode.setter
    def userns_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "usernsMode", value)

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.List["ContainerVolumes"]]:
        return jsii.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: typing.Optional[typing.List["ContainerVolumes"]]) -> None:
        jsii.set(self, "volumes", value)

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> typing.Optional[str]:
        return jsii.get(self, "workingDir")

    @working_dir.setter
    def working_dir(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "workingDir", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerCapabilities",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "drop": "drop"},
)
class ContainerCapabilities:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.List[str]] = None,
        drop: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param add: 
        :param drop: 
        """
        self._values = {}
        if add is not None:
            self._values["add"] = add
        if drop is not None:
            self._values["drop"] = drop

    @builtins.property
    def add(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("add")

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("drop")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCapabilities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "image": "image",
        "name": "name",
        "attach": "attach",
        "capabilities": "capabilities",
        "command": "command",
        "cpu_set": "cpuSet",
        "cpu_shares": "cpuShares",
        "destroy_grace_seconds": "destroyGraceSeconds",
        "devices": "devices",
        "dns": "dns",
        "dns_opts": "dnsOpts",
        "dns_search": "dnsSearch",
        "domainname": "domainname",
        "entrypoint": "entrypoint",
        "env": "env",
        "group_add": "groupAdd",
        "healthcheck": "healthcheck",
        "host": "host",
        "hostname": "hostname",
        "ipc_mode": "ipcMode",
        "labels": "labels",
        "links": "links",
        "log_driver": "logDriver",
        "log_opts": "logOpts",
        "logs": "logs",
        "max_retry_count": "maxRetryCount",
        "memory": "memory",
        "memory_swap": "memorySwap",
        "mounts": "mounts",
        "must_run": "mustRun",
        "network_alias": "networkAlias",
        "network_mode": "networkMode",
        "networks": "networks",
        "networks_advanced": "networksAdvanced",
        "pid_mode": "pidMode",
        "ports": "ports",
        "privileged": "privileged",
        "publish_all_ports": "publishAllPorts",
        "read_only": "readOnly",
        "restart": "restart",
        "rm": "rm",
        "shm_size": "shmSize",
        "start": "start",
        "sysctls": "sysctls",
        "tmpfs": "tmpfs",
        "ulimit": "ulimit",
        "upload": "upload",
        "user": "user",
        "userns_mode": "usernsMode",
        "volumes": "volumes",
        "working_dir": "workingDir",
    },
)
class ContainerConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        image: str,
        name: str,
        attach: typing.Optional[bool] = None,
        capabilities: typing.Optional[typing.List["ContainerCapabilities"]] = None,
        command: typing.Optional[typing.List[str]] = None,
        cpu_set: typing.Optional[str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        destroy_grace_seconds: typing.Optional[jsii.Number] = None,
        devices: typing.Optional[typing.List["ContainerDevices"]] = None,
        dns: typing.Optional[typing.List[str]] = None,
        dns_opts: typing.Optional[typing.List[str]] = None,
        dns_search: typing.Optional[typing.List[str]] = None,
        domainname: typing.Optional[str] = None,
        entrypoint: typing.Optional[typing.List[str]] = None,
        env: typing.Optional[typing.List[str]] = None,
        group_add: typing.Optional[typing.List[str]] = None,
        healthcheck: typing.Optional[typing.List["ContainerHealthcheck"]] = None,
        host: typing.Optional[typing.List["ContainerHost"]] = None,
        hostname: typing.Optional[str] = None,
        ipc_mode: typing.Optional[str] = None,
        labels: typing.Optional[typing.List["ContainerLabels"]] = None,
        links: typing.Optional[typing.List[str]] = None,
        log_driver: typing.Optional[str] = None,
        log_opts: typing.Optional[typing.Mapping[str, str]] = None,
        logs: typing.Optional[bool] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        mounts: typing.Optional[typing.List["ContainerMounts"]] = None,
        must_run: typing.Optional[bool] = None,
        network_alias: typing.Optional[typing.List[str]] = None,
        network_mode: typing.Optional[str] = None,
        networks: typing.Optional[typing.List[str]] = None,
        networks_advanced: typing.Optional[typing.List["ContainerNetworksAdvanced"]] = None,
        pid_mode: typing.Optional[str] = None,
        ports: typing.Optional[typing.List["ContainerPorts"]] = None,
        privileged: typing.Optional[bool] = None,
        publish_all_ports: typing.Optional[bool] = None,
        read_only: typing.Optional[bool] = None,
        restart: typing.Optional[str] = None,
        rm: typing.Optional[bool] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        start: typing.Optional[bool] = None,
        sysctls: typing.Optional[typing.Mapping[str, str]] = None,
        tmpfs: typing.Optional[typing.Mapping[str, str]] = None,
        ulimit: typing.Optional[typing.List["ContainerUlimit"]] = None,
        upload: typing.Optional[typing.List["ContainerUpload"]] = None,
        user: typing.Optional[str] = None,
        userns_mode: typing.Optional[str] = None,
        volumes: typing.Optional[typing.List["ContainerVolumes"]] = None,
        working_dir: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param image: 
        :param name: 
        :param attach: 
        :param capabilities: capabilities block.
        :param command: 
        :param cpu_set: 
        :param cpu_shares: 
        :param destroy_grace_seconds: 
        :param devices: devices block.
        :param dns: 
        :param dns_opts: 
        :param dns_search: 
        :param domainname: 
        :param entrypoint: 
        :param env: 
        :param group_add: Additional groups for the container user.
        :param healthcheck: healthcheck block.
        :param host: host block.
        :param hostname: 
        :param ipc_mode: IPC sharing mode for the container.
        :param labels: labels block.
        :param links: 
        :param log_driver: 
        :param log_opts: 
        :param logs: 
        :param max_retry_count: 
        :param memory: 
        :param memory_swap: 
        :param mounts: mounts block.
        :param must_run: 
        :param network_alias: Set an alias for the container in all specified networks.
        :param network_mode: 
        :param networks: 
        :param networks_advanced: networks_advanced block.
        :param pid_mode: 
        :param ports: ports block.
        :param privileged: 
        :param publish_all_ports: 
        :param read_only: 
        :param restart: 
        :param rm: 
        :param shm_size: 
        :param start: 
        :param sysctls: 
        :param tmpfs: 
        :param ulimit: ulimit block.
        :param upload: upload block.
        :param user: 
        :param userns_mode: 
        :param volumes: volumes block.
        :param working_dir: 
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "image": image,
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
        if attach is not None:
            self._values["attach"] = attach
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if command is not None:
            self._values["command"] = command
        if cpu_set is not None:
            self._values["cpu_set"] = cpu_set
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if destroy_grace_seconds is not None:
            self._values["destroy_grace_seconds"] = destroy_grace_seconds
        if devices is not None:
            self._values["devices"] = devices
        if dns is not None:
            self._values["dns"] = dns
        if dns_opts is not None:
            self._values["dns_opts"] = dns_opts
        if dns_search is not None:
            self._values["dns_search"] = dns_search
        if domainname is not None:
            self._values["domainname"] = domainname
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if env is not None:
            self._values["env"] = env
        if group_add is not None:
            self._values["group_add"] = group_add
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if host is not None:
            self._values["host"] = host
        if hostname is not None:
            self._values["hostname"] = hostname
        if ipc_mode is not None:
            self._values["ipc_mode"] = ipc_mode
        if labels is not None:
            self._values["labels"] = labels
        if links is not None:
            self._values["links"] = links
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if log_opts is not None:
            self._values["log_opts"] = log_opts
        if logs is not None:
            self._values["logs"] = logs
        if max_retry_count is not None:
            self._values["max_retry_count"] = max_retry_count
        if memory is not None:
            self._values["memory"] = memory
        if memory_swap is not None:
            self._values["memory_swap"] = memory_swap
        if mounts is not None:
            self._values["mounts"] = mounts
        if must_run is not None:
            self._values["must_run"] = must_run
        if network_alias is not None:
            self._values["network_alias"] = network_alias
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if networks is not None:
            self._values["networks"] = networks
        if networks_advanced is not None:
            self._values["networks_advanced"] = networks_advanced
        if pid_mode is not None:
            self._values["pid_mode"] = pid_mode
        if ports is not None:
            self._values["ports"] = ports
        if privileged is not None:
            self._values["privileged"] = privileged
        if publish_all_ports is not None:
            self._values["publish_all_ports"] = publish_all_ports
        if read_only is not None:
            self._values["read_only"] = read_only
        if restart is not None:
            self._values["restart"] = restart
        if rm is not None:
            self._values["rm"] = rm
        if shm_size is not None:
            self._values["shm_size"] = shm_size
        if start is not None:
            self._values["start"] = start
        if sysctls is not None:
            self._values["sysctls"] = sysctls
        if tmpfs is not None:
            self._values["tmpfs"] = tmpfs
        if ulimit is not None:
            self._values["ulimit"] = ulimit
        if upload is not None:
            self._values["upload"] = upload
        if user is not None:
            self._values["user"] = user
        if userns_mode is not None:
            self._values["userns_mode"] = userns_mode
        if volumes is not None:
            self._values["volumes"] = volumes
        if working_dir is not None:
            self._values["working_dir"] = working_dir

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
    def image(self) -> str:
        return self._values.get("image")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def attach(self) -> typing.Optional[bool]:
        return self._values.get("attach")

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List["ContainerCapabilities"]]:
        """capabilities block."""
        return self._values.get("capabilities")

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("command")

    @builtins.property
    def cpu_set(self) -> typing.Optional[str]:
        return self._values.get("cpu_set")

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        return self._values.get("cpu_shares")

    @builtins.property
    def destroy_grace_seconds(self) -> typing.Optional[jsii.Number]:
        return self._values.get("destroy_grace_seconds")

    @builtins.property
    def devices(self) -> typing.Optional[typing.List["ContainerDevices"]]:
        """devices block."""
        return self._values.get("devices")

    @builtins.property
    def dns(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("dns")

    @builtins.property
    def dns_opts(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("dns_opts")

    @builtins.property
    def dns_search(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("dns_search")

    @builtins.property
    def domainname(self) -> typing.Optional[str]:
        return self._values.get("domainname")

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("entrypoint")

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("env")

    @builtins.property
    def group_add(self) -> typing.Optional[typing.List[str]]:
        """Additional groups for the container user."""
        return self._values.get("group_add")

    @builtins.property
    def healthcheck(self) -> typing.Optional[typing.List["ContainerHealthcheck"]]:
        """healthcheck block."""
        return self._values.get("healthcheck")

    @builtins.property
    def host(self) -> typing.Optional[typing.List["ContainerHost"]]:
        """host block."""
        return self._values.get("host")

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        return self._values.get("hostname")

    @builtins.property
    def ipc_mode(self) -> typing.Optional[str]:
        """IPC sharing mode for the container."""
        return self._values.get("ipc_mode")

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["ContainerLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def links(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("links")

    @builtins.property
    def log_driver(self) -> typing.Optional[str]:
        return self._values.get("log_driver")

    @builtins.property
    def log_opts(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("log_opts")

    @builtins.property
    def logs(self) -> typing.Optional[bool]:
        return self._values.get("logs")

    @builtins.property
    def max_retry_count(self) -> typing.Optional[jsii.Number]:
        return self._values.get("max_retry_count")

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        return self._values.get("memory")

    @builtins.property
    def memory_swap(self) -> typing.Optional[jsii.Number]:
        return self._values.get("memory_swap")

    @builtins.property
    def mounts(self) -> typing.Optional[typing.List["ContainerMounts"]]:
        """mounts block."""
        return self._values.get("mounts")

    @builtins.property
    def must_run(self) -> typing.Optional[bool]:
        return self._values.get("must_run")

    @builtins.property
    def network_alias(self) -> typing.Optional[typing.List[str]]:
        """Set an alias for the container in all specified networks."""
        return self._values.get("network_alias")

    @builtins.property
    def network_mode(self) -> typing.Optional[str]:
        return self._values.get("network_mode")

    @builtins.property
    def networks(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("networks")

    @builtins.property
    def networks_advanced(
        self,
    ) -> typing.Optional[typing.List["ContainerNetworksAdvanced"]]:
        """networks_advanced block."""
        return self._values.get("networks_advanced")

    @builtins.property
    def pid_mode(self) -> typing.Optional[str]:
        return self._values.get("pid_mode")

    @builtins.property
    def ports(self) -> typing.Optional[typing.List["ContainerPorts"]]:
        """ports block."""
        return self._values.get("ports")

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        return self._values.get("privileged")

    @builtins.property
    def publish_all_ports(self) -> typing.Optional[bool]:
        return self._values.get("publish_all_ports")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        return self._values.get("read_only")

    @builtins.property
    def restart(self) -> typing.Optional[str]:
        return self._values.get("restart")

    @builtins.property
    def rm(self) -> typing.Optional[bool]:
        return self._values.get("rm")

    @builtins.property
    def shm_size(self) -> typing.Optional[jsii.Number]:
        return self._values.get("shm_size")

    @builtins.property
    def start(self) -> typing.Optional[bool]:
        return self._values.get("start")

    @builtins.property
    def sysctls(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("sysctls")

    @builtins.property
    def tmpfs(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("tmpfs")

    @builtins.property
    def ulimit(self) -> typing.Optional[typing.List["ContainerUlimit"]]:
        """ulimit block."""
        return self._values.get("ulimit")

    @builtins.property
    def upload(self) -> typing.Optional[typing.List["ContainerUpload"]]:
        """upload block."""
        return self._values.get("upload")

    @builtins.property
    def user(self) -> typing.Optional[str]:
        return self._values.get("user")

    @builtins.property
    def userns_mode(self) -> typing.Optional[str]:
        return self._values.get("userns_mode")

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["ContainerVolumes"]]:
        """volumes block."""
        return self._values.get("volumes")

    @builtins.property
    def working_dir(self) -> typing.Optional[str]:
        return self._values.get("working_dir")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerDevices",
    jsii_struct_bases=[],
    name_mapping={
        "host_path": "hostPath",
        "container_path": "containerPath",
        "permissions": "permissions",
    },
)
class ContainerDevices:
    def __init__(
        self,
        *,
        host_path: str,
        container_path: typing.Optional[str] = None,
        permissions: typing.Optional[str] = None,
    ) -> None:
        """
        :param host_path: 
        :param container_path: 
        :param permissions: 
        """
        self._values = {
            "host_path": host_path,
        }
        if container_path is not None:
            self._values["container_path"] = container_path
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def host_path(self) -> str:
        return self._values.get("host_path")

    @builtins.property
    def container_path(self) -> typing.Optional[str]:
        return self._values.get("container_path")

    @builtins.property
    def permissions(self) -> typing.Optional[str]:
        return self._values.get("permissions")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerDevices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerHealthcheck",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "interval": "interval",
        "retries": "retries",
        "start_period": "startPeriod",
        "timeout": "timeout",
    },
)
class ContainerHealthcheck:
    def __init__(
        self,
        *,
        test: typing.List[str],
        interval: typing.Optional[str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[str] = None,
        timeout: typing.Optional[str] = None,
    ) -> None:
        """
        :param test: The test to perform as list.
        :param interval: Time between running the check (ms|s|m|h).
        :param retries: Consecutive failures needed to report unhealthy.
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h).
        :param timeout: Maximum time to allow one check to run (ms|s|m|h).
        """
        self._values = {
            "test": test,
        }
        if interval is not None:
            self._values["interval"] = interval
        if retries is not None:
            self._values["retries"] = retries
        if start_period is not None:
            self._values["start_period"] = start_period
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def test(self) -> typing.List[str]:
        """The test to perform as list."""
        return self._values.get("test")

    @builtins.property
    def interval(self) -> typing.Optional[str]:
        """Time between running the check (ms|s|m|h)."""
        return self._values.get("interval")

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        """Consecutive failures needed to report unhealthy."""
        return self._values.get("retries")

    @builtins.property
    def start_period(self) -> typing.Optional[str]:
        """Start period for the container to initialize before counting retries towards unstable (ms|s|m|h)."""
        return self._values.get("start_period")

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """Maximum time to allow one check to run (ms|s|m|h)."""
        return self._values.get("timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerHealthcheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerHost",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "ip": "ip"},
)
class ContainerHost:
    def __init__(self, *, host: str, ip: str) -> None:
        """
        :param host: 
        :param ip: 
        """
        self._values = {
            "host": host,
            "ip": ip,
        }

    @builtins.property
    def host(self) -> str:
        return self._values.get("host")

    @builtins.property
    def ip(self) -> str:
        return self._values.get("ip")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerHost(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ContainerLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerMounts",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "type": "type",
        "bind_options": "bindOptions",
        "read_only": "readOnly",
        "source": "source",
        "tmpfs_options": "tmpfsOptions",
        "volume_options": "volumeOptions",
    },
)
class ContainerMounts:
    def __init__(
        self,
        *,
        target: str,
        type: str,
        bind_options: typing.Optional[typing.List["ContainerMountsBindOptions"]] = None,
        read_only: typing.Optional[bool] = None,
        source: typing.Optional[str] = None,
        tmpfs_options: typing.Optional[typing.List["ContainerMountsTmpfsOptions"]] = None,
        volume_options: typing.Optional[typing.List["ContainerMountsVolumeOptions"]] = None,
    ) -> None:
        """
        :param target: Container path.
        :param type: The mount type.
        :param bind_options: bind_options block.
        :param read_only: Whether the mount should be read-only.
        :param source: Mount source (e.g. a volume name, a host path).
        :param tmpfs_options: tmpfs_options block.
        :param volume_options: volume_options block.
        """
        self._values = {
            "target": target,
            "type": type,
        }
        if bind_options is not None:
            self._values["bind_options"] = bind_options
        if read_only is not None:
            self._values["read_only"] = read_only
        if source is not None:
            self._values["source"] = source
        if tmpfs_options is not None:
            self._values["tmpfs_options"] = tmpfs_options
        if volume_options is not None:
            self._values["volume_options"] = volume_options

    @builtins.property
    def target(self) -> str:
        """Container path."""
        return self._values.get("target")

    @builtins.property
    def type(self) -> str:
        """The mount type."""
        return self._values.get("type")

    @builtins.property
    def bind_options(
        self,
    ) -> typing.Optional[typing.List["ContainerMountsBindOptions"]]:
        """bind_options block."""
        return self._values.get("bind_options")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        """Whether the mount should be read-only."""
        return self._values.get("read_only")

    @builtins.property
    def source(self) -> typing.Optional[str]:
        """Mount source (e.g. a volume name, a host path)."""
        return self._values.get("source")

    @builtins.property
    def tmpfs_options(
        self,
    ) -> typing.Optional[typing.List["ContainerMountsTmpfsOptions"]]:
        """tmpfs_options block."""
        return self._values.get("tmpfs_options")

    @builtins.property
    def volume_options(
        self,
    ) -> typing.Optional[typing.List["ContainerMountsVolumeOptions"]]:
        """volume_options block."""
        return self._values.get("volume_options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerMountsBindOptions",
    jsii_struct_bases=[],
    name_mapping={"propagation": "propagation"},
)
class ContainerMountsBindOptions:
    def __init__(self, *, propagation: typing.Optional[str] = None) -> None:
        """
        :param propagation: A propagation mode with the value.
        """
        self._values = {}
        if propagation is not None:
            self._values["propagation"] = propagation

    @builtins.property
    def propagation(self) -> typing.Optional[str]:
        """A propagation mode with the value."""
        return self._values.get("propagation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerMountsTmpfsOptions",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "size_bytes": "sizeBytes"},
)
class ContainerMountsTmpfsOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param mode: The permission mode for the tmpfs mount in an integer.
        :param size_bytes: The size for the tmpfs mount in bytes.
        """
        self._values = {}
        if mode is not None:
            self._values["mode"] = mode
        if size_bytes is not None:
            self._values["size_bytes"] = size_bytes

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        """The permission mode for the tmpfs mount in an integer."""
        return self._values.get("mode")

    @builtins.property
    def size_bytes(self) -> typing.Optional[jsii.Number]:
        """The size for the tmpfs mount in bytes."""
        return self._values.get("size_bytes")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsTmpfsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerMountsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "driver_name": "driverName",
        "driver_options": "driverOptions",
        "labels": "labels",
        "no_copy": "noCopy",
    },
)
class ContainerMountsVolumeOptions:
    def __init__(
        self,
        *,
        driver_name: typing.Optional[str] = None,
        driver_options: typing.Optional[typing.Mapping[str, str]] = None,
        labels: typing.Optional[typing.List["ContainerMountsVolumeOptionsLabels"]] = None,
        no_copy: typing.Optional[bool] = None,
    ) -> None:
        """
        :param driver_name: Name of the driver to use to create the volume.
        :param driver_options: key/value map of driver specific options.
        :param labels: labels block.
        :param no_copy: Populate volume with data from the target.
        """
        self._values = {}
        if driver_name is not None:
            self._values["driver_name"] = driver_name
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if labels is not None:
            self._values["labels"] = labels
        if no_copy is not None:
            self._values["no_copy"] = no_copy

    @builtins.property
    def driver_name(self) -> typing.Optional[str]:
        """Name of the driver to use to create the volume."""
        return self._values.get("driver_name")

    @builtins.property
    def driver_options(self) -> typing.Optional[typing.Mapping[str, str]]:
        """key/value map of driver specific options."""
        return self._values.get("driver_options")

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.List["ContainerMountsVolumeOptionsLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def no_copy(self) -> typing.Optional[bool]:
        """Populate volume with data from the target."""
        return self._values.get("no_copy")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerMountsVolumeOptionsLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ContainerMountsVolumeOptionsLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsVolumeOptionsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNetworkData(
    cdktf.ComplexComputedList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.ContainerNetworkData",
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
        jsii.create(ContainerNetworkData, self, [terraform_resource, terraform_attribute, index])

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> str:
        return jsii.get(self, "gateway")

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> str:
        return jsii.get(self, "ipAddress")

    @builtins.property
    @jsii.member(jsii_name="ipPrefixLength")
    def ip_prefix_length(self) -> jsii.Number:
        return jsii.get(self, "ipPrefixLength")

    @builtins.property
    @jsii.member(jsii_name="networkName")
    def network_name(self) -> str:
        return jsii.get(self, "networkName")


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerNetworksAdvanced",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "aliases": "aliases",
        "ipv4_address": "ipv4Address",
        "ipv6_address": "ipv6Address",
    },
)
class ContainerNetworksAdvanced:
    def __init__(
        self,
        *,
        name: str,
        aliases: typing.Optional[typing.List[str]] = None,
        ipv4_address: typing.Optional[str] = None,
        ipv6_address: typing.Optional[str] = None,
    ) -> None:
        """
        :param name: 
        :param aliases: 
        :param ipv4_address: 
        :param ipv6_address: 
        """
        self._values = {
            "name": name,
        }
        if aliases is not None:
            self._values["aliases"] = aliases
        if ipv4_address is not None:
            self._values["ipv4_address"] = ipv4_address
        if ipv6_address is not None:
            self._values["ipv6_address"] = ipv6_address

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("aliases")

    @builtins.property
    def ipv4_address(self) -> typing.Optional[str]:
        return self._values.get("ipv4_address")

    @builtins.property
    def ipv6_address(self) -> typing.Optional[str]:
        return self._values.get("ipv6_address")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNetworksAdvanced(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerPorts",
    jsii_struct_bases=[],
    name_mapping={
        "internal": "internal",
        "external": "external",
        "ip": "ip",
        "protocol": "protocol",
    },
)
class ContainerPorts:
    def __init__(
        self,
        *,
        internal: jsii.Number,
        external: typing.Optional[jsii.Number] = None,
        ip: typing.Optional[str] = None,
        protocol: typing.Optional[str] = None,
    ) -> None:
        """
        :param internal: 
        :param external: 
        :param ip: 
        :param protocol: 
        """
        self._values = {
            "internal": internal,
        }
        if external is not None:
            self._values["external"] = external
        if ip is not None:
            self._values["ip"] = ip
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def internal(self) -> jsii.Number:
        return self._values.get("internal")

    @builtins.property
    def external(self) -> typing.Optional[jsii.Number]:
        return self._values.get("external")

    @builtins.property
    def ip(self) -> typing.Optional[str]:
        return self._values.get("ip")

    @builtins.property
    def protocol(self) -> typing.Optional[str]:
        return self._values.get("protocol")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerUlimit",
    jsii_struct_bases=[],
    name_mapping={"hard": "hard", "name": "name", "soft": "soft"},
)
class ContainerUlimit:
    def __init__(self, *, hard: jsii.Number, name: str, soft: jsii.Number) -> None:
        """
        :param hard: 
        :param name: 
        :param soft: 
        """
        self._values = {
            "hard": hard,
            "name": name,
            "soft": soft,
        }

    @builtins.property
    def hard(self) -> jsii.Number:
        return self._values.get("hard")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def soft(self) -> jsii.Number:
        return self._values.get("soft")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerUlimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerUpload",
    jsii_struct_bases=[],
    name_mapping={
        "file": "file",
        "content": "content",
        "content_base64": "contentBase64",
        "executable": "executable",
        "source": "source",
        "source_hash": "sourceHash",
    },
)
class ContainerUpload:
    def __init__(
        self,
        *,
        file: str,
        content: typing.Optional[str] = None,
        content_base64: typing.Optional[str] = None,
        executable: typing.Optional[bool] = None,
        source: typing.Optional[str] = None,
        source_hash: typing.Optional[str] = None,
    ) -> None:
        """
        :param file: 
        :param content: 
        :param content_base64: 
        :param executable: 
        :param source: 
        :param source_hash: 
        """
        self._values = {
            "file": file,
        }
        if content is not None:
            self._values["content"] = content
        if content_base64 is not None:
            self._values["content_base64"] = content_base64
        if executable is not None:
            self._values["executable"] = executable
        if source is not None:
            self._values["source"] = source
        if source_hash is not None:
            self._values["source_hash"] = source_hash

    @builtins.property
    def file(self) -> str:
        return self._values.get("file")

    @builtins.property
    def content(self) -> typing.Optional[str]:
        return self._values.get("content")

    @builtins.property
    def content_base64(self) -> typing.Optional[str]:
        return self._values.get("content_base64")

    @builtins.property
    def executable(self) -> typing.Optional[bool]:
        return self._values.get("executable")

    @builtins.property
    def source(self) -> typing.Optional[str]:
        return self._values.get("source")

    @builtins.property
    def source_hash(self) -> typing.Optional[str]:
        return self._values.get("source_hash")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerUpload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ContainerVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "container_path": "containerPath",
        "from_container": "fromContainer",
        "host_path": "hostPath",
        "read_only": "readOnly",
        "volume_name": "volumeName",
    },
)
class ContainerVolumes:
    def __init__(
        self,
        *,
        container_path: typing.Optional[str] = None,
        from_container: typing.Optional[str] = None,
        host_path: typing.Optional[str] = None,
        read_only: typing.Optional[bool] = None,
        volume_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param container_path: 
        :param from_container: 
        :param host_path: 
        :param read_only: 
        :param volume_name: 
        """
        self._values = {}
        if container_path is not None:
            self._values["container_path"] = container_path
        if from_container is not None:
            self._values["from_container"] = from_container
        if host_path is not None:
            self._values["host_path"] = host_path
        if read_only is not None:
            self._values["read_only"] = read_only
        if volume_name is not None:
            self._values["volume_name"] = volume_name

    @builtins.property
    def container_path(self) -> typing.Optional[str]:
        return self._values.get("container_path")

    @builtins.property
    def from_container(self) -> typing.Optional[str]:
        return self._values.get("from_container")

    @builtins.property
    def host_path(self) -> typing.Optional[str]:
        return self._values.get("host_path")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        return self._values.get("read_only")

    @builtins.property
    def volume_name(self) -> typing.Optional[str]:
        return self._values.get("volume_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDockerNetwork(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.DataDockerNetwork",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataDockerNetworkConfig(
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataDockerNetwork, self, [scope, id, config])

    @jsii.member(jsii_name="ipamConfig")
    def ipam_config(self, index: str) -> "DataDockerNetworkIpamConfig":
        """
        :param index: -
        """
        return jsii.invoke(self, "ipamConfig", [index])

    @jsii.member(jsii_name="options")
    def options(self, key: str) -> str:
        """
        :param key: -
        """
        return jsii.invoke(self, "options", [key])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> str:
        return jsii.get(self, "driver")

    @builtins.property
    @jsii.member(jsii_name="internal")
    def internal(self) -> bool:
        return jsii.get(self, "internal")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> str:
        return jsii.get(self, "scope")

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
    jsii_type="@cdktf/provider-docker.DataDockerNetworkConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
    },
)
class DataDockerNetworkConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
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
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDockerNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDockerNetworkIpamConfig(
    cdktf.ComplexComputedList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.DataDockerNetworkIpamConfig",
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
        jsii.create(DataDockerNetworkIpamConfig, self, [terraform_resource, terraform_attribute, index])

    @builtins.property
    @jsii.member(jsii_name="auxAddress")
    def aux_address(self) -> typing.Any:
        return jsii.get(self, "auxAddress")

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> str:
        return jsii.get(self, "gateway")

    @builtins.property
    @jsii.member(jsii_name="ipRange")
    def ip_range(self) -> str:
        return jsii.get(self, "ipRange")

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> str:
        return jsii.get(self, "subnet")


class DataDockerRegistryImage(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.DataDockerRegistryImage",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = DataDockerRegistryImageConfig(
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataDockerRegistryImage, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="sha256Digest")
    def sha256_digest(self) -> str:
        return jsii.get(self, "sha256Digest")

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
    jsii_type="@cdktf/provider-docker.DataDockerRegistryImageConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
    },
)
class DataDockerRegistryImageConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
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
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDockerRegistryImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.DockerProvider",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        alias: typing.Optional[str] = None,
        ca_material: typing.Optional[str] = None,
        cert_material: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        host: typing.Optional[str] = None,
        key_material: typing.Optional[str] = None,
        registry_auth: typing.Optional[typing.List["DockerProviderRegistryAuth"]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alias: Alias name.
        :param ca_material: PEM-encoded content of Docker host CA certificate.
        :param cert_material: PEM-encoded content of Docker client certificate.
        :param cert_path: Path to directory with Docker TLS config.
        :param host: The Docker daemon address.
        :param key_material: PEM-encoded content of Docker client private key.
        :param registry_auth: registry_auth block.
        """
        config = DockerProviderConfig(
            alias=alias,
            ca_material=ca_material,
            cert_material=cert_material,
            cert_path=cert_path,
            host=host,
            key_material=key_material,
            registry_auth=registry_auth,
        )

        jsii.create(DockerProvider, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[str]:
        return jsii.get(self, "alias")

    @alias.setter
    def alias(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="caMaterial")
    def ca_material(self) -> typing.Optional[str]:
        return jsii.get(self, "caMaterial")

    @ca_material.setter
    def ca_material(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "caMaterial", value)

    @builtins.property
    @jsii.member(jsii_name="certMaterial")
    def cert_material(self) -> typing.Optional[str]:
        return jsii.get(self, "certMaterial")

    @cert_material.setter
    def cert_material(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certMaterial", value)

    @builtins.property
    @jsii.member(jsii_name="certPath")
    def cert_path(self) -> typing.Optional[str]:
        return jsii.get(self, "certPath")

    @cert_path.setter
    def cert_path(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certPath", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> typing.Optional[str]:
        return jsii.get(self, "host")

    @host.setter
    def host(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="keyMaterial")
    def key_material(self) -> typing.Optional[str]:
        return jsii.get(self, "keyMaterial")

    @key_material.setter
    def key_material(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "keyMaterial", value)

    @builtins.property
    @jsii.member(jsii_name="registryAuth")
    def registry_auth(
        self,
    ) -> typing.Optional[typing.List["DockerProviderRegistryAuth"]]:
        return jsii.get(self, "registryAuth")

    @registry_auth.setter
    def registry_auth(
        self, value: typing.Optional[typing.List["DockerProviderRegistryAuth"]]
    ) -> None:
        jsii.set(self, "registryAuth", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.DockerProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "ca_material": "caMaterial",
        "cert_material": "certMaterial",
        "cert_path": "certPath",
        "host": "host",
        "key_material": "keyMaterial",
        "registry_auth": "registryAuth",
    },
)
class DockerProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[str] = None,
        ca_material: typing.Optional[str] = None,
        cert_material: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        host: typing.Optional[str] = None,
        key_material: typing.Optional[str] = None,
        registry_auth: typing.Optional[typing.List["DockerProviderRegistryAuth"]] = None,
    ) -> None:
        """
        :param alias: Alias name.
        :param ca_material: PEM-encoded content of Docker host CA certificate.
        :param cert_material: PEM-encoded content of Docker client certificate.
        :param cert_path: Path to directory with Docker TLS config.
        :param host: The Docker daemon address.
        :param key_material: PEM-encoded content of Docker client private key.
        :param registry_auth: registry_auth block.
        """
        self._values = {}
        if alias is not None:
            self._values["alias"] = alias
        if ca_material is not None:
            self._values["ca_material"] = ca_material
        if cert_material is not None:
            self._values["cert_material"] = cert_material
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if host is not None:
            self._values["host"] = host
        if key_material is not None:
            self._values["key_material"] = key_material
        if registry_auth is not None:
            self._values["registry_auth"] = registry_auth

    @builtins.property
    def alias(self) -> typing.Optional[str]:
        """Alias name."""
        return self._values.get("alias")

    @builtins.property
    def ca_material(self) -> typing.Optional[str]:
        """PEM-encoded content of Docker host CA certificate."""
        return self._values.get("ca_material")

    @builtins.property
    def cert_material(self) -> typing.Optional[str]:
        """PEM-encoded content of Docker client certificate."""
        return self._values.get("cert_material")

    @builtins.property
    def cert_path(self) -> typing.Optional[str]:
        """Path to directory with Docker TLS config."""
        return self._values.get("cert_path")

    @builtins.property
    def host(self) -> typing.Optional[str]:
        """The Docker daemon address."""
        return self._values.get("host")

    @builtins.property
    def key_material(self) -> typing.Optional[str]:
        """PEM-encoded content of Docker client private key."""
        return self._values.get("key_material")

    @builtins.property
    def registry_auth(
        self,
    ) -> typing.Optional[typing.List["DockerProviderRegistryAuth"]]:
        """registry_auth block."""
        return self._values.get("registry_auth")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.DockerProviderRegistryAuth",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "config_file": "configFile",
        "config_file_content": "configFileContent",
        "password": "password",
        "username": "username",
    },
)
class DockerProviderRegistryAuth:
    def __init__(
        self,
        *,
        address: str,
        config_file: typing.Optional[str] = None,
        config_file_content: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param address: Address of the registry.
        :param config_file: Path to docker json file for registry auth.
        :param config_file_content: Plain content of the docker json file for registry auth.
        :param password: Password for the registry.
        :param username: Username for the registry.
        """
        self._values = {
            "address": address,
        }
        if config_file is not None:
            self._values["config_file"] = config_file
        if config_file_content is not None:
            self._values["config_file_content"] = config_file_content
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def address(self) -> str:
        """Address of the registry."""
        return self._values.get("address")

    @builtins.property
    def config_file(self) -> typing.Optional[str]:
        """Path to docker json file for registry auth."""
        return self._values.get("config_file")

    @builtins.property
    def config_file_content(self) -> typing.Optional[str]:
        """Plain content of the docker json file for registry auth."""
        return self._values.get("config_file_content")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """Password for the registry."""
        return self._values.get("password")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """Username for the registry."""
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerProviderRegistryAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Image(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Image",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        keep_locally: typing.Optional[bool] = None,
        pull_trigger: typing.Optional[str] = None,
        pull_triggers: typing.Optional[typing.List[str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param keep_locally: 
        :param pull_trigger: 
        :param pull_triggers: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ImageConfig(
            name=name,
            keep_locally=keep_locally,
            pull_trigger=pull_trigger,
            pull_triggers=pull_triggers,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Image, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="latest")
    def latest(self) -> str:
        return jsii.get(self, "latest")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="keepLocally")
    def keep_locally(self) -> typing.Optional[bool]:
        return jsii.get(self, "keepLocally")

    @keep_locally.setter
    def keep_locally(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "keepLocally", value)

    @builtins.property
    @jsii.member(jsii_name="pullTrigger")
    def pull_trigger(self) -> typing.Optional[str]:
        return jsii.get(self, "pullTrigger")

    @pull_trigger.setter
    def pull_trigger(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "pullTrigger", value)

    @builtins.property
    @jsii.member(jsii_name="pullTriggers")
    def pull_triggers(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "pullTriggers")

    @pull_triggers.setter
    def pull_triggers(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "pullTriggers", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ImageConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "keep_locally": "keepLocally",
        "pull_trigger": "pullTrigger",
        "pull_triggers": "pullTriggers",
    },
)
class ImageConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        keep_locally: typing.Optional[bool] = None,
        pull_trigger: typing.Optional[str] = None,
        pull_triggers: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param keep_locally: 
        :param pull_trigger: 
        :param pull_triggers: 
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
        if keep_locally is not None:
            self._values["keep_locally"] = keep_locally
        if pull_trigger is not None:
            self._values["pull_trigger"] = pull_trigger
        if pull_triggers is not None:
            self._values["pull_triggers"] = pull_triggers

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
    def keep_locally(self) -> typing.Optional[bool]:
        return self._values.get("keep_locally")

    @builtins.property
    def pull_trigger(self) -> typing.Optional[str]:
        return self._values.get("pull_trigger")

    @builtins.property
    def pull_triggers(self) -> typing.Optional[typing.List[str]]:
        return self._values.get("pull_triggers")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Network(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Network",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        attachable: typing.Optional[bool] = None,
        check_duplicate: typing.Optional[bool] = None,
        driver: typing.Optional[str] = None,
        ingress: typing.Optional[bool] = None,
        internal: typing.Optional[bool] = None,
        ipam_config: typing.Optional[typing.List["NetworkIpamConfig"]] = None,
        ipam_driver: typing.Optional[str] = None,
        ipv6: typing.Optional[bool] = None,
        labels: typing.Optional[typing.List["NetworkLabels"]] = None,
        options: typing.Optional[typing.Mapping[str, str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: 
        :param attachable: 
        :param check_duplicate: 
        :param driver: 
        :param ingress: 
        :param internal: 
        :param ipam_config: ipam_config block.
        :param ipam_driver: 
        :param ipv6: 
        :param labels: labels block.
        :param options: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = NetworkConfig(
            name=name,
            attachable=attachable,
            check_duplicate=check_duplicate,
            driver=driver,
            ingress=ingress,
            internal=internal,
            ipam_config=ipam_config,
            ipam_driver=ipam_driver,
            ipv6=ipv6,
            labels=labels,
            options=options,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Network, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> str:
        return jsii.get(self, "scope")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="attachable")
    def attachable(self) -> typing.Optional[bool]:
        return jsii.get(self, "attachable")

    @attachable.setter
    def attachable(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "attachable", value)

    @builtins.property
    @jsii.member(jsii_name="checkDuplicate")
    def check_duplicate(self) -> typing.Optional[bool]:
        return jsii.get(self, "checkDuplicate")

    @check_duplicate.setter
    def check_duplicate(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "checkDuplicate", value)

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> typing.Optional[str]:
        return jsii.get(self, "driver")

    @driver.setter
    def driver(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "driver", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> typing.Optional[bool]:
        return jsii.get(self, "ingress")

    @ingress.setter
    def ingress(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "ingress", value)

    @builtins.property
    @jsii.member(jsii_name="internal")
    def internal(self) -> typing.Optional[bool]:
        return jsii.get(self, "internal")

    @internal.setter
    def internal(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "internal", value)

    @builtins.property
    @jsii.member(jsii_name="ipamConfig")
    def ipam_config(self) -> typing.Optional[typing.List["NetworkIpamConfig"]]:
        return jsii.get(self, "ipamConfig")

    @ipam_config.setter
    def ipam_config(
        self, value: typing.Optional[typing.List["NetworkIpamConfig"]]
    ) -> None:
        jsii.set(self, "ipamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="ipamDriver")
    def ipam_driver(self) -> typing.Optional[str]:
        return jsii.get(self, "ipamDriver")

    @ipam_driver.setter
    def ipam_driver(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ipamDriver", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> typing.Optional[bool]:
        return jsii.get(self, "ipv6")

    @ipv6.setter
    def ipv6(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "ipv6", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[typing.List["NetworkLabels"]]:
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Optional[typing.List["NetworkLabels"]]) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "options")

    @options.setter
    def options(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "options", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.NetworkConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "attachable": "attachable",
        "check_duplicate": "checkDuplicate",
        "driver": "driver",
        "ingress": "ingress",
        "internal": "internal",
        "ipam_config": "ipamConfig",
        "ipam_driver": "ipamDriver",
        "ipv6": "ipv6",
        "labels": "labels",
        "options": "options",
    },
)
class NetworkConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        attachable: typing.Optional[bool] = None,
        check_duplicate: typing.Optional[bool] = None,
        driver: typing.Optional[str] = None,
        ingress: typing.Optional[bool] = None,
        internal: typing.Optional[bool] = None,
        ipam_config: typing.Optional[typing.List["NetworkIpamConfig"]] = None,
        ipam_driver: typing.Optional[str] = None,
        ipv6: typing.Optional[bool] = None,
        labels: typing.Optional[typing.List["NetworkLabels"]] = None,
        options: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: 
        :param attachable: 
        :param check_duplicate: 
        :param driver: 
        :param ingress: 
        :param internal: 
        :param ipam_config: ipam_config block.
        :param ipam_driver: 
        :param ipv6: 
        :param labels: labels block.
        :param options: 
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
        if attachable is not None:
            self._values["attachable"] = attachable
        if check_duplicate is not None:
            self._values["check_duplicate"] = check_duplicate
        if driver is not None:
            self._values["driver"] = driver
        if ingress is not None:
            self._values["ingress"] = ingress
        if internal is not None:
            self._values["internal"] = internal
        if ipam_config is not None:
            self._values["ipam_config"] = ipam_config
        if ipam_driver is not None:
            self._values["ipam_driver"] = ipam_driver
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if labels is not None:
            self._values["labels"] = labels
        if options is not None:
            self._values["options"] = options

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
    def attachable(self) -> typing.Optional[bool]:
        return self._values.get("attachable")

    @builtins.property
    def check_duplicate(self) -> typing.Optional[bool]:
        return self._values.get("check_duplicate")

    @builtins.property
    def driver(self) -> typing.Optional[str]:
        return self._values.get("driver")

    @builtins.property
    def ingress(self) -> typing.Optional[bool]:
        return self._values.get("ingress")

    @builtins.property
    def internal(self) -> typing.Optional[bool]:
        return self._values.get("internal")

    @builtins.property
    def ipam_config(self) -> typing.Optional[typing.List["NetworkIpamConfig"]]:
        """ipam_config block."""
        return self._values.get("ipam_config")

    @builtins.property
    def ipam_driver(self) -> typing.Optional[str]:
        return self._values.get("ipam_driver")

    @builtins.property
    def ipv6(self) -> typing.Optional[bool]:
        return self._values.get("ipv6")

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["NetworkLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.NetworkIpamConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aux_address": "auxAddress",
        "gateway": "gateway",
        "ip_range": "ipRange",
        "subnet": "subnet",
    },
)
class NetworkIpamConfig:
    def __init__(
        self,
        *,
        aux_address: typing.Optional[typing.Mapping[str, str]] = None,
        gateway: typing.Optional[str] = None,
        ip_range: typing.Optional[str] = None,
        subnet: typing.Optional[str] = None,
    ) -> None:
        """
        :param aux_address: 
        :param gateway: 
        :param ip_range: 
        :param subnet: 
        """
        self._values = {}
        if aux_address is not None:
            self._values["aux_address"] = aux_address
        if gateway is not None:
            self._values["gateway"] = gateway
        if ip_range is not None:
            self._values["ip_range"] = ip_range
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def aux_address(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("aux_address")

    @builtins.property
    def gateway(self) -> typing.Optional[str]:
        return self._values.get("gateway")

    @builtins.property
    def ip_range(self) -> typing.Optional[str]:
        return self._values.get("ip_range")

    @builtins.property
    def subnet(self) -> typing.Optional[str]:
        return self._values.get("subnet")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIpamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.NetworkLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class NetworkLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Secret(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Secret",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        data: str,
        name: str,
        labels: typing.Optional[typing.List["SecretLabels"]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param data: Base64-url-safe-encoded secret data.
        :param name: User-defined name of the secret.
        :param labels: labels block.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = SecretConfig(
            data=data,
            name=name,
            labels=labels,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Secret, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> str:
        return jsii.get(self, "data")

    @data.setter
    def data(self, value: str) -> None:
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[typing.List["SecretLabels"]]:
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Optional[typing.List["SecretLabels"]]) -> None:
        jsii.set(self, "labels", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.SecretConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "data": "data",
        "name": "name",
        "labels": "labels",
    },
)
class SecretConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        data: str,
        name: str,
        labels: typing.Optional[typing.List["SecretLabels"]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param data: Base64-url-safe-encoded secret data.
        :param name: User-defined name of the secret.
        :param labels: labels block.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "data": data,
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
        if labels is not None:
            self._values["labels"] = labels

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
    def data(self) -> str:
        """Base64-url-safe-encoded secret data."""
        return self._values.get("data")

    @builtins.property
    def name(self) -> str:
        """User-defined name of the secret."""
        return self._values.get("name")

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["SecretLabels"]]:
        """labels block."""
        return self._values.get("labels")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.SecretLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class SecretLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Service(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Service",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        name: str,
        task_spec: typing.List["ServiceTaskSpec"],
        auth: typing.Optional[typing.Mapping[str, str]] = None,
        converge_config: typing.Optional[typing.List["ServiceConvergeConfig"]] = None,
        endpoint_spec: typing.Optional[typing.List["ServiceEndpointSpec"]] = None,
        labels: typing.Optional[typing.List["ServiceLabels"]] = None,
        mode: typing.Optional[typing.List["ServiceMode"]] = None,
        rollback_config: typing.Optional[typing.List["ServiceRollbackConfig"]] = None,
        update_config: typing.Optional[typing.List["ServiceUpdateConfig"]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: Name of the service.
        :param task_spec: task_spec block.
        :param auth: 
        :param converge_config: converge_config block.
        :param endpoint_spec: endpoint_spec block.
        :param labels: labels block.
        :param mode: mode block.
        :param rollback_config: rollback_config block.
        :param update_config: update_config block.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = ServiceConfig(
            name=name,
            task_spec=task_spec,
            auth=auth,
            converge_config=converge_config,
            endpoint_spec=endpoint_spec,
            labels=labels,
            mode=mode,
            rollback_config=rollback_config,
            update_config=update_config,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Service, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="taskSpec")
    def task_spec(self) -> typing.List["ServiceTaskSpec"]:
        return jsii.get(self, "taskSpec")

    @task_spec.setter
    def task_spec(self, value: typing.List["ServiceTaskSpec"]) -> None:
        jsii.set(self, "taskSpec", value)

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "auth")

    @auth.setter
    def auth(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="convergeConfig")
    def converge_config(self) -> typing.Optional[typing.List["ServiceConvergeConfig"]]:
        return jsii.get(self, "convergeConfig")

    @converge_config.setter
    def converge_config(
        self, value: typing.Optional[typing.List["ServiceConvergeConfig"]]
    ) -> None:
        jsii.set(self, "convergeConfig", value)

    @builtins.property
    @jsii.member(jsii_name="endpointSpec")
    def endpoint_spec(self) -> typing.Optional[typing.List["ServiceEndpointSpec"]]:
        return jsii.get(self, "endpointSpec")

    @endpoint_spec.setter
    def endpoint_spec(
        self, value: typing.Optional[typing.List["ServiceEndpointSpec"]]
    ) -> None:
        jsii.set(self, "endpointSpec", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[typing.List["ServiceLabels"]]:
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Optional[typing.List["ServiceLabels"]]) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> typing.Optional[typing.List["ServiceMode"]]:
        return jsii.get(self, "mode")

    @mode.setter
    def mode(self, value: typing.Optional[typing.List["ServiceMode"]]) -> None:
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="rollbackConfig")
    def rollback_config(self) -> typing.Optional[typing.List["ServiceRollbackConfig"]]:
        return jsii.get(self, "rollbackConfig")

    @rollback_config.setter
    def rollback_config(
        self, value: typing.Optional[typing.List["ServiceRollbackConfig"]]
    ) -> None:
        jsii.set(self, "rollbackConfig", value)

    @builtins.property
    @jsii.member(jsii_name="updateConfig")
    def update_config(self) -> typing.Optional[typing.List["ServiceUpdateConfig"]]:
        return jsii.get(self, "updateConfig")

    @update_config.setter
    def update_config(
        self, value: typing.Optional[typing.List["ServiceUpdateConfig"]]
    ) -> None:
        jsii.set(self, "updateConfig", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "task_spec": "taskSpec",
        "auth": "auth",
        "converge_config": "convergeConfig",
        "endpoint_spec": "endpointSpec",
        "labels": "labels",
        "mode": "mode",
        "rollback_config": "rollbackConfig",
        "update_config": "updateConfig",
    },
)
class ServiceConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: str,
        task_spec: typing.List["ServiceTaskSpec"],
        auth: typing.Optional[typing.Mapping[str, str]] = None,
        converge_config: typing.Optional[typing.List["ServiceConvergeConfig"]] = None,
        endpoint_spec: typing.Optional[typing.List["ServiceEndpointSpec"]] = None,
        labels: typing.Optional[typing.List["ServiceLabels"]] = None,
        mode: typing.Optional[typing.List["ServiceMode"]] = None,
        rollback_config: typing.Optional[typing.List["ServiceRollbackConfig"]] = None,
        update_config: typing.Optional[typing.List["ServiceUpdateConfig"]] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Name of the service.
        :param task_spec: task_spec block.
        :param auth: 
        :param converge_config: converge_config block.
        :param endpoint_spec: endpoint_spec block.
        :param labels: labels block.
        :param mode: mode block.
        :param rollback_config: rollback_config block.
        :param update_config: update_config block.
        """
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values = {
            "name": name,
            "task_spec": task_spec,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if auth is not None:
            self._values["auth"] = auth
        if converge_config is not None:
            self._values["converge_config"] = converge_config
        if endpoint_spec is not None:
            self._values["endpoint_spec"] = endpoint_spec
        if labels is not None:
            self._values["labels"] = labels
        if mode is not None:
            self._values["mode"] = mode
        if rollback_config is not None:
            self._values["rollback_config"] = rollback_config
        if update_config is not None:
            self._values["update_config"] = update_config

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
        """Name of the service."""
        return self._values.get("name")

    @builtins.property
    def task_spec(self) -> typing.List["ServiceTaskSpec"]:
        """task_spec block."""
        return self._values.get("task_spec")

    @builtins.property
    def auth(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("auth")

    @builtins.property
    def converge_config(self) -> typing.Optional[typing.List["ServiceConvergeConfig"]]:
        """converge_config block."""
        return self._values.get("converge_config")

    @builtins.property
    def endpoint_spec(self) -> typing.Optional[typing.List["ServiceEndpointSpec"]]:
        """endpoint_spec block."""
        return self._values.get("endpoint_spec")

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["ServiceLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def mode(self) -> typing.Optional[typing.List["ServiceMode"]]:
        """mode block."""
        return self._values.get("mode")

    @builtins.property
    def rollback_config(self) -> typing.Optional[typing.List["ServiceRollbackConfig"]]:
        """rollback_config block."""
        return self._values.get("rollback_config")

    @builtins.property
    def update_config(self) -> typing.Optional[typing.List["ServiceUpdateConfig"]]:
        """update_config block."""
        return self._values.get("update_config")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceConvergeConfig",
    jsii_struct_bases=[],
    name_mapping={"delay": "delay", "timeout": "timeout"},
)
class ServiceConvergeConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[str] = None,
        timeout: typing.Optional[str] = None,
    ) -> None:
        """
        :param delay: The interval to check if the desired state is reached (ms|s). Default: 7s
        :param timeout: The timeout of the service to reach the desired state (s|m). Default: 3m
        """
        self._values = {}
        if delay is not None:
            self._values["delay"] = delay
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def delay(self) -> typing.Optional[str]:
        """The interval to check if the desired state is reached (ms|s).

        Default: 7s
        """
        return self._values.get("delay")

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """The timeout of the service to reach the desired state (s|m).

        Default: 3m
        """
        return self._values.get("timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConvergeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceEndpointSpec",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "ports": "ports"},
)
class ServiceEndpointSpec:
    def __init__(
        self,
        *,
        mode: typing.Optional[str] = None,
        ports: typing.Optional[typing.List["ServiceEndpointSpecPorts"]] = None,
    ) -> None:
        """
        :param mode: The mode of resolution to use for internal load balancing between tasks.
        :param ports: ports block.
        """
        self._values = {}
        if mode is not None:
            self._values["mode"] = mode
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def mode(self) -> typing.Optional[str]:
        """The mode of resolution to use for internal load balancing between tasks."""
        return self._values.get("mode")

    @builtins.property
    def ports(self) -> typing.Optional[typing.List["ServiceEndpointSpecPorts"]]:
        """ports block."""
        return self._values.get("ports")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceEndpointSpecPorts",
    jsii_struct_bases=[],
    name_mapping={
        "target_port": "targetPort",
        "name": "name",
        "protocol": "protocol",
        "published_port": "publishedPort",
        "publish_mode": "publishMode",
    },
)
class ServiceEndpointSpecPorts:
    def __init__(
        self,
        *,
        target_port: jsii.Number,
        name: typing.Optional[str] = None,
        protocol: typing.Optional[str] = None,
        published_port: typing.Optional[jsii.Number] = None,
        publish_mode: typing.Optional[str] = None,
    ) -> None:
        """
        :param target_port: The port inside the container.
        :param name: A random name for the port.
        :param protocol: Rrepresents the protocol of a port: 'tcp', 'udp' or 'sctp'.
        :param published_port: The port on the swarm hosts.
        :param publish_mode: Represents the mode in which the port is to be published: 'ingress' or 'host'.
        """
        self._values = {
            "target_port": target_port,
        }
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if published_port is not None:
            self._values["published_port"] = published_port
        if publish_mode is not None:
            self._values["publish_mode"] = publish_mode

    @builtins.property
    def target_port(self) -> jsii.Number:
        """The port inside the container."""
        return self._values.get("target_port")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """A random name for the port."""
        return self._values.get("name")

    @builtins.property
    def protocol(self) -> typing.Optional[str]:
        """Rrepresents the protocol of a port: 'tcp', 'udp' or 'sctp'."""
        return self._values.get("protocol")

    @builtins.property
    def published_port(self) -> typing.Optional[jsii.Number]:
        """The port on the swarm hosts."""
        return self._values.get("published_port")

    @builtins.property
    def publish_mode(self) -> typing.Optional[str]:
        """Represents the mode in which the port is to be published: 'ingress' or 'host'."""
        return self._values.get("publish_mode")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpecPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceMode",
    jsii_struct_bases=[],
    name_mapping={"global_": "global", "replicated": "replicated"},
)
class ServiceMode:
    def __init__(
        self,
        *,
        global_: typing.Optional[bool] = None,
        replicated: typing.Optional[typing.List["ServiceModeReplicated"]] = None,
    ) -> None:
        """
        :param global_: The global service mode.
        :param replicated: replicated block.
        """
        self._values = {}
        if global_ is not None:
            self._values["global_"] = global_
        if replicated is not None:
            self._values["replicated"] = replicated

    @builtins.property
    def global_(self) -> typing.Optional[bool]:
        """The global service mode."""
        return self._values.get("global_")

    @builtins.property
    def replicated(self) -> typing.Optional[typing.List["ServiceModeReplicated"]]:
        """replicated block."""
        return self._values.get("replicated")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceModeReplicated",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas"},
)
class ServiceModeReplicated:
    def __init__(self, *, replicas: typing.Optional[jsii.Number] = None) -> None:
        """
        :param replicas: The amount of replicas of the service.
        """
        self._values = {}
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        """The amount of replicas of the service."""
        return self._values.get("replicas")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceModeReplicated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceRollbackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceRollbackConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[str] = None,
        failure_action: typing.Optional[str] = None,
        max_failure_ratio: typing.Optional[str] = None,
        monitor: typing.Optional[str] = None,
        order: typing.Optional[str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param delay: Delay between task rollbacks (ns|us|ms|s|m|h).
        :param failure_action: Action on rollback failure: pause | continue.
        :param max_failure_ratio: Failure rate to tolerate during a rollback.
        :param monitor: Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h).
        :param order: Rollback order: either 'stop-first' or 'start-first'.
        :param parallelism: Maximum number of tasks to be rollbacked in one iteration.
        """
        self._values = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[str]:
        """Delay between task rollbacks (ns|us|ms|s|m|h)."""
        return self._values.get("delay")

    @builtins.property
    def failure_action(self) -> typing.Optional[str]:
        """Action on rollback failure: pause | continue."""
        return self._values.get("failure_action")

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[str]:
        """Failure rate to tolerate during a rollback."""
        return self._values.get("max_failure_ratio")

    @builtins.property
    def monitor(self) -> typing.Optional[str]:
        """Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h)."""
        return self._values.get("monitor")

    @builtins.property
    def order(self) -> typing.Optional[str]:
        """Rollback order: either 'stop-first' or 'start-first'."""
        return self._values.get("order")

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        """Maximum number of tasks to be rollbacked in one iteration."""
        return self._values.get("parallelism")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceRollbackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpec",
    jsii_struct_bases=[],
    name_mapping={
        "container_spec": "containerSpec",
        "force_update": "forceUpdate",
        "log_driver": "logDriver",
        "networks": "networks",
        "placement": "placement",
        "resources": "resources",
        "restart_policy": "restartPolicy",
        "runtime": "runtime",
    },
)
class ServiceTaskSpec:
    def __init__(
        self,
        *,
        container_spec: typing.List["ServiceTaskSpecContainerSpec"],
        force_update: typing.Optional[jsii.Number] = None,
        log_driver: typing.Optional[typing.List["ServiceTaskSpecLogDriver"]] = None,
        networks: typing.Optional[typing.List[str]] = None,
        placement: typing.Optional[typing.List["ServiceTaskSpecPlacement"]] = None,
        resources: typing.Optional[typing.List["ServiceTaskSpecResources"]] = None,
        restart_policy: typing.Optional[typing.Mapping[str, str]] = None,
        runtime: typing.Optional[str] = None,
    ) -> None:
        """
        :param container_spec: container_spec block.
        :param force_update: A counter that triggers an update even if no relevant parameters have been changed. See https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126
        :param log_driver: log_driver block.
        :param networks: Ids of the networks in which the container will be put in.
        :param placement: placement block.
        :param resources: resources block.
        :param restart_policy: Specification for the restart policy which applies to containers created as part of this service.
        :param runtime: Runtime is the type of runtime specified for the task executor. See https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go
        """
        self._values = {
            "container_spec": container_spec,
        }
        if force_update is not None:
            self._values["force_update"] = force_update
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if networks is not None:
            self._values["networks"] = networks
        if placement is not None:
            self._values["placement"] = placement
        if resources is not None:
            self._values["resources"] = resources
        if restart_policy is not None:
            self._values["restart_policy"] = restart_policy
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def container_spec(self) -> typing.List["ServiceTaskSpecContainerSpec"]:
        """container_spec block."""
        return self._values.get("container_spec")

    @builtins.property
    def force_update(self) -> typing.Optional[jsii.Number]:
        """A counter that triggers an update even if no relevant parameters have been changed.

        See https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126
        """
        return self._values.get("force_update")

    @builtins.property
    def log_driver(self) -> typing.Optional[typing.List["ServiceTaskSpecLogDriver"]]:
        """log_driver block."""
        return self._values.get("log_driver")

    @builtins.property
    def networks(self) -> typing.Optional[typing.List[str]]:
        """Ids of the networks in which the  container will be put in."""
        return self._values.get("networks")

    @builtins.property
    def placement(self) -> typing.Optional[typing.List["ServiceTaskSpecPlacement"]]:
        """placement block."""
        return self._values.get("placement")

    @builtins.property
    def resources(self) -> typing.Optional[typing.List["ServiceTaskSpecResources"]]:
        """resources block."""
        return self._values.get("resources")

    @builtins.property
    def restart_policy(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Specification for the restart policy which applies to containers created as part of this service."""
        return self._values.get("restart_policy")

    @builtins.property
    def runtime(self) -> typing.Optional[str]:
        """Runtime is the type of runtime specified for the task executor.

        See https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go
        """
        return self._values.get("runtime")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "configs": "configs",
        "dir": "dir",
        "dns_config": "dnsConfig",
        "env": "env",
        "groups": "groups",
        "healthcheck": "healthcheck",
        "hostname": "hostname",
        "hosts": "hosts",
        "isolation": "isolation",
        "labels": "labels",
        "mounts": "mounts",
        "privileges": "privileges",
        "read_only": "readOnly",
        "secrets": "secrets",
        "stop_grace_period": "stopGracePeriod",
        "stop_signal": "stopSignal",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpec:
    def __init__(
        self,
        *,
        image: str,
        args: typing.Optional[typing.List[str]] = None,
        command: typing.Optional[typing.List[str]] = None,
        configs: typing.Optional[typing.List["ServiceTaskSpecContainerSpecConfigs"]] = None,
        dir: typing.Optional[str] = None,
        dns_config: typing.Optional[typing.List["ServiceTaskSpecContainerSpecDnsConfig"]] = None,
        env: typing.Optional[typing.Mapping[str, str]] = None,
        groups: typing.Optional[typing.List[str]] = None,
        healthcheck: typing.Optional[typing.List["ServiceTaskSpecContainerSpecHealthcheck"]] = None,
        hostname: typing.Optional[str] = None,
        hosts: typing.Optional[typing.List["ServiceTaskSpecContainerSpecHosts"]] = None,
        isolation: typing.Optional[str] = None,
        labels: typing.Optional[typing.List["ServiceTaskSpecContainerSpecLabels"]] = None,
        mounts: typing.Optional[typing.List["ServiceTaskSpecContainerSpecMounts"]] = None,
        privileges: typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivileges"]] = None,
        read_only: typing.Optional[bool] = None,
        secrets: typing.Optional[typing.List["ServiceTaskSpecContainerSpecSecrets"]] = None,
        stop_grace_period: typing.Optional[str] = None,
        stop_signal: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param image: The image name to use for the containers of the service.
        :param args: Arguments to the command.
        :param command: The command to be run in the image.
        :param configs: configs block.
        :param dir: The working directory for commands to run in.
        :param dns_config: dns_config block.
        :param env: A list of environment variables in the form VAR="value".
        :param groups: A list of additional groups that the container process will run as.
        :param healthcheck: healthcheck block.
        :param hostname: The hostname to use for the container, as a valid RFC 1123 hostname.
        :param hosts: hosts block.
        :param isolation: Isolation technology of the containers running the service. (Windows only)
        :param labels: labels block.
        :param mounts: mounts block.
        :param privileges: privileges block.
        :param read_only: Mount the container's root filesystem as read only.
        :param secrets: secrets block.
        :param stop_grace_period: Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h).
        :param stop_signal: Signal to stop the container.
        :param user: The user inside the container.
        """
        self._values = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if configs is not None:
            self._values["configs"] = configs
        if dir is not None:
            self._values["dir"] = dir
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if env is not None:
            self._values["env"] = env
        if groups is not None:
            self._values["groups"] = groups
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if hostname is not None:
            self._values["hostname"] = hostname
        if hosts is not None:
            self._values["hosts"] = hosts
        if isolation is not None:
            self._values["isolation"] = isolation
        if labels is not None:
            self._values["labels"] = labels
        if mounts is not None:
            self._values["mounts"] = mounts
        if privileges is not None:
            self._values["privileges"] = privileges
        if read_only is not None:
            self._values["read_only"] = read_only
        if secrets is not None:
            self._values["secrets"] = secrets
        if stop_grace_period is not None:
            self._values["stop_grace_period"] = stop_grace_period
        if stop_signal is not None:
            self._values["stop_signal"] = stop_signal
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def image(self) -> str:
        """The image name to use for the containers of the service."""
        return self._values.get("image")

    @builtins.property
    def args(self) -> typing.Optional[typing.List[str]]:
        """Arguments to the command."""
        return self._values.get("args")

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command to be run in the image."""
        return self._values.get("command")

    @builtins.property
    def configs(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecConfigs"]]:
        """configs block."""
        return self._values.get("configs")

    @builtins.property
    def dir(self) -> typing.Optional[str]:
        """The working directory for commands to run in."""
        return self._values.get("dir")

    @builtins.property
    def dns_config(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecDnsConfig"]]:
        """dns_config block."""
        return self._values.get("dns_config")

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of environment variables in the form VAR="value"."""
        return self._values.get("env")

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[str]]:
        """A list of additional groups that the container process will run as."""
        return self._values.get("groups")

    @builtins.property
    def healthcheck(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecHealthcheck"]]:
        """healthcheck block."""
        return self._values.get("healthcheck")

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for the container, as a valid RFC 1123 hostname."""
        return self._values.get("hostname")

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecHosts"]]:
        """hosts block."""
        return self._values.get("hosts")

    @builtins.property
    def isolation(self) -> typing.Optional[str]:
        """Isolation technology of the containers running the service.

        (Windows only)
        """
        return self._values.get("isolation")

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def mounts(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecMounts"]]:
        """mounts block."""
        return self._values.get("mounts")

    @builtins.property
    def privileges(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivileges"]]:
        """privileges block."""
        return self._values.get("privileges")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        """Mount the container's root filesystem as read only."""
        return self._values.get("read_only")

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecSecrets"]]:
        """secrets block."""
        return self._values.get("secrets")

    @builtins.property
    def stop_grace_period(self) -> typing.Optional[str]:
        """Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h)."""
        return self._values.get("stop_grace_period")

    @builtins.property
    def stop_signal(self) -> typing.Optional[str]:
        """Signal to stop the container."""
        return self._values.get("stop_signal")

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user inside the container."""
        return self._values.get("user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "config_id": "configId",
        "file_name": "fileName",
        "config_name": "configName",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
    },
)
class ServiceTaskSpecContainerSpecConfigs:
    def __init__(
        self,
        *,
        config_id: str,
        file_name: str,
        config_name: typing.Optional[str] = None,
        file_gid: typing.Optional[str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[str] = None,
    ) -> None:
        """
        :param config_id: ID of the specific config that we're referencing.
        :param file_name: Represents the final filename in the filesystem.
        :param config_name: Name of the config that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID
        :param file_gid: Represents the file GID.
        :param file_mode: Represents represents the FileMode of the file.
        :param file_uid: Represents the file UID.
        """
        self._values = {
            "config_id": config_id,
            "file_name": file_name,
        }
        if config_name is not None:
            self._values["config_name"] = config_name
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid

    @builtins.property
    def config_id(self) -> str:
        """ID of the specific config that we're referencing."""
        return self._values.get("config_id")

    @builtins.property
    def file_name(self) -> str:
        """Represents the final filename in the filesystem."""
        return self._values.get("file_name")

    @builtins.property
    def config_name(self) -> typing.Optional[str]:
        """Name of the config that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID
        """
        return self._values.get("config_name")

    @builtins.property
    def file_gid(self) -> typing.Optional[str]:
        """Represents the file GID."""
        return self._values.get("file_gid")

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        """Represents represents the FileMode of the file."""
        return self._values.get("file_mode")

    @builtins.property
    def file_uid(self) -> typing.Optional[str]:
        """Represents the file UID."""
        return self._values.get("file_uid")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecDnsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "nameservers": "nameservers",
        "options": "options",
        "search": "search",
    },
)
class ServiceTaskSpecContainerSpecDnsConfig:
    def __init__(
        self,
        *,
        nameservers: typing.List[str],
        options: typing.Optional[typing.List[str]] = None,
        search: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param nameservers: The IP addresses of the name servers.
        :param options: A list of internal resolver variables to be modified (e.g., debug, ndots:3, etc.).
        :param search: A search list for host-name lookup.
        """
        self._values = {
            "nameservers": nameservers,
        }
        if options is not None:
            self._values["options"] = options
        if search is not None:
            self._values["search"] = search

    @builtins.property
    def nameservers(self) -> typing.List[str]:
        """The IP addresses of the name servers."""
        return self._values.get("nameservers")

    @builtins.property
    def options(self) -> typing.Optional[typing.List[str]]:
        """A list of internal resolver variables to be modified (e.g., debug, ndots:3, etc.)."""
        return self._values.get("options")

    @builtins.property
    def search(self) -> typing.Optional[typing.List[str]]:
        """A search list for host-name lookup."""
        return self._values.get("search")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecDnsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecHealthcheck",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "interval": "interval",
        "retries": "retries",
        "start_period": "startPeriod",
        "timeout": "timeout",
    },
)
class ServiceTaskSpecContainerSpecHealthcheck:
    def __init__(
        self,
        *,
        test: typing.List[str],
        interval: typing.Optional[str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[str] = None,
        timeout: typing.Optional[str] = None,
    ) -> None:
        """
        :param test: The test to perform as list.
        :param interval: Time between running the check (ms|s|m|h).
        :param retries: Consecutive failures needed to report unhealthy.
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h).
        :param timeout: Maximum time to allow one check to run (ms|s|m|h).
        """
        self._values = {
            "test": test,
        }
        if interval is not None:
            self._values["interval"] = interval
        if retries is not None:
            self._values["retries"] = retries
        if start_period is not None:
            self._values["start_period"] = start_period
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def test(self) -> typing.List[str]:
        """The test to perform as list."""
        return self._values.get("test")

    @builtins.property
    def interval(self) -> typing.Optional[str]:
        """Time between running the check (ms|s|m|h)."""
        return self._values.get("interval")

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        """Consecutive failures needed to report unhealthy."""
        return self._values.get("retries")

    @builtins.property
    def start_period(self) -> typing.Optional[str]:
        """Start period for the container to initialize before counting retries towards unstable (ms|s|m|h)."""
        return self._values.get("start_period")

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """Maximum time to allow one check to run (ms|s|m|h)."""
        return self._values.get("timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHealthcheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecHosts",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "ip": "ip"},
)
class ServiceTaskSpecContainerSpecHosts:
    def __init__(self, *, host: str, ip: str) -> None:
        """
        :param host: 
        :param ip: 
        """
        self._values = {
            "host": host,
            "ip": ip,
        }

    @builtins.property
    def host(self) -> str:
        return self._values.get("host")

    @builtins.property
    def ip(self) -> str:
        return self._values.get("ip")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecMounts",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "type": "type",
        "bind_options": "bindOptions",
        "read_only": "readOnly",
        "source": "source",
        "tmpfs_options": "tmpfsOptions",
        "volume_options": "volumeOptions",
    },
)
class ServiceTaskSpecContainerSpecMounts:
    def __init__(
        self,
        *,
        target: str,
        type: str,
        bind_options: typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsBindOptions"]] = None,
        read_only: typing.Optional[bool] = None,
        source: typing.Optional[str] = None,
        tmpfs_options: typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]] = None,
        volume_options: typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptions"]] = None,
    ) -> None:
        """
        :param target: Container path.
        :param type: The mount type.
        :param bind_options: bind_options block.
        :param read_only: Whether the mount should be read-only.
        :param source: Mount source (e.g. a volume name, a host path).
        :param tmpfs_options: tmpfs_options block.
        :param volume_options: volume_options block.
        """
        self._values = {
            "target": target,
            "type": type,
        }
        if bind_options is not None:
            self._values["bind_options"] = bind_options
        if read_only is not None:
            self._values["read_only"] = read_only
        if source is not None:
            self._values["source"] = source
        if tmpfs_options is not None:
            self._values["tmpfs_options"] = tmpfs_options
        if volume_options is not None:
            self._values["volume_options"] = volume_options

    @builtins.property
    def target(self) -> str:
        """Container path."""
        return self._values.get("target")

    @builtins.property
    def type(self) -> str:
        """The mount type."""
        return self._values.get("type")

    @builtins.property
    def bind_options(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsBindOptions"]]:
        """bind_options block."""
        return self._values.get("bind_options")

    @builtins.property
    def read_only(self) -> typing.Optional[bool]:
        """Whether the mount should be read-only."""
        return self._values.get("read_only")

    @builtins.property
    def source(self) -> typing.Optional[str]:
        """Mount source (e.g. a volume name, a host path)."""
        return self._values.get("source")

    @builtins.property
    def tmpfs_options(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]]:
        """tmpfs_options block."""
        return self._values.get("tmpfs_options")

    @builtins.property
    def volume_options(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptions"]]:
        """volume_options block."""
        return self._values.get("volume_options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecMountsBindOptions",
    jsii_struct_bases=[],
    name_mapping={"propagation": "propagation"},
)
class ServiceTaskSpecContainerSpecMountsBindOptions:
    def __init__(self, *, propagation: typing.Optional[str] = None) -> None:
        """
        :param propagation: A propagation mode with the value.
        """
        self._values = {}
        if propagation is not None:
            self._values["propagation"] = propagation

    @builtins.property
    def propagation(self) -> typing.Optional[str]:
        """A propagation mode with the value."""
        return self._values.get("propagation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "size_bytes": "sizeBytes"},
)
class ServiceTaskSpecContainerSpecMountsTmpfsOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param mode: The permission mode for the tmpfs mount in an integer.
        :param size_bytes: The size for the tmpfs mount in bytes.
        """
        self._values = {}
        if mode is not None:
            self._values["mode"] = mode
        if size_bytes is not None:
            self._values["size_bytes"] = size_bytes

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        """The permission mode for the tmpfs mount in an integer."""
        return self._values.get("mode")

    @builtins.property
    def size_bytes(self) -> typing.Optional[jsii.Number]:
        """The size for the tmpfs mount in bytes."""
        return self._values.get("size_bytes")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsTmpfsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecMountsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "driver_name": "driverName",
        "driver_options": "driverOptions",
        "labels": "labels",
        "no_copy": "noCopy",
    },
)
class ServiceTaskSpecContainerSpecMountsVolumeOptions:
    def __init__(
        self,
        *,
        driver_name: typing.Optional[str] = None,
        driver_options: typing.Optional[typing.Mapping[str, str]] = None,
        labels: typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]] = None,
        no_copy: typing.Optional[bool] = None,
    ) -> None:
        """
        :param driver_name: Name of the driver to use to create the volume.
        :param driver_options: key/value map of driver specific options.
        :param labels: labels block.
        :param no_copy: Populate volume with data from the target.
        """
        self._values = {}
        if driver_name is not None:
            self._values["driver_name"] = driver_name
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if labels is not None:
            self._values["labels"] = labels
        if no_copy is not None:
            self._values["no_copy"] = no_copy

    @builtins.property
    def driver_name(self) -> typing.Optional[str]:
        """Name of the driver to use to create the volume."""
        return self._values.get("driver_name")

    @builtins.property
    def driver_options(self) -> typing.Optional[typing.Mapping[str, str]]:
        """key/value map of driver specific options."""
        return self._values.get("driver_options")

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def no_copy(self) -> typing.Optional[bool]:
        """Populate volume with data from the target."""
        return self._values.get("no_copy")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecPrivileges",
    jsii_struct_bases=[],
    name_mapping={
        "credential_spec": "credentialSpec",
        "se_linux_context": "seLinuxContext",
    },
)
class ServiceTaskSpecContainerSpecPrivileges:
    def __init__(
        self,
        *,
        credential_spec: typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"]] = None,
        se_linux_context: typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]] = None,
    ) -> None:
        """
        :param credential_spec: credential_spec block.
        :param se_linux_context: se_linux_context block.
        """
        self._values = {}
        if credential_spec is not None:
            self._values["credential_spec"] = credential_spec
        if se_linux_context is not None:
            self._values["se_linux_context"] = se_linux_context

    @builtins.property
    def credential_spec(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"]]:
        """credential_spec block."""
        return self._values.get("credential_spec")

    @builtins.property
    def se_linux_context(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]]:
        """se_linux_context block."""
        return self._values.get("se_linux_context")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivileges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "registry": "registry"},
)
class ServiceTaskSpecContainerSpecPrivilegesCredentialSpec:
    def __init__(
        self,
        *,
        file: typing.Optional[str] = None,
        registry: typing.Optional[str] = None,
    ) -> None:
        """
        :param file: Load credential spec from this file.
        :param registry: Load credential spec from this value in the Windows registry.
        """
        self._values = {}
        if file is not None:
            self._values["file"] = file
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def file(self) -> typing.Optional[str]:
        """Load credential spec from this file."""
        return self._values.get("file")

    @builtins.property
    def registry(self) -> typing.Optional[str]:
        """Load credential spec from this value in the Windows registry."""
        return self._values.get("registry")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    jsii_struct_bases=[],
    name_mapping={
        "disable": "disable",
        "level": "level",
        "role": "role",
        "type": "type",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext:
    def __init__(
        self,
        *,
        disable: typing.Optional[bool] = None,
        level: typing.Optional[str] = None,
        role: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param disable: Disable SELinux.
        :param level: SELinux level label.
        :param role: SELinux role label.
        :param type: SELinux type label.
        :param user: SELinux user label.
        """
        self._values = {}
        if disable is not None:
            self._values["disable"] = disable
        if level is not None:
            self._values["level"] = level
        if role is not None:
            self._values["role"] = role
        if type is not None:
            self._values["type"] = type
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def disable(self) -> typing.Optional[bool]:
        """Disable SELinux."""
        return self._values.get("disable")

    @builtins.property
    def level(self) -> typing.Optional[str]:
        """SELinux level label."""
        return self._values.get("level")

    @builtins.property
    def role(self) -> typing.Optional[str]:
        """SELinux role label."""
        return self._values.get("role")

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """SELinux type label."""
        return self._values.get("type")

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """SELinux user label."""
        return self._values.get("user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecContainerSpecSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "secret_id": "secretId",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
        "secret_name": "secretName",
    },
)
class ServiceTaskSpecContainerSpecSecrets:
    def __init__(
        self,
        *,
        file_name: str,
        secret_id: str,
        file_gid: typing.Optional[str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[str] = None,
        secret_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param file_name: Represents the final filename in the filesystem.
        :param secret_id: ID of the specific secret that we're referencing.
        :param file_gid: Represents the file GID.
        :param file_mode: Represents represents the FileMode of the file.
        :param file_uid: Represents the file UID.
        :param secret_name: Name of the secret that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID
        """
        self._values = {
            "file_name": file_name,
            "secret_id": secret_id,
        }
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def file_name(self) -> str:
        """Represents the final filename in the filesystem."""
        return self._values.get("file_name")

    @builtins.property
    def secret_id(self) -> str:
        """ID of the specific secret that we're referencing."""
        return self._values.get("secret_id")

    @builtins.property
    def file_gid(self) -> typing.Optional[str]:
        """Represents the file GID."""
        return self._values.get("file_gid")

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        """Represents represents the FileMode of the file."""
        return self._values.get("file_mode")

    @builtins.property
    def file_uid(self) -> typing.Optional[str]:
        """Represents the file UID."""
        return self._values.get("file_uid")

    @builtins.property
    def secret_name(self) -> typing.Optional[str]:
        """Name of the secret that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID
        """
        return self._values.get("secret_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecLogDriver",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "options": "options"},
)
class ServiceTaskSpecLogDriver:
    def __init__(
        self, *, name: str, options: typing.Optional[typing.Mapping[str, str]] = None
    ) -> None:
        """
        :param name: The logging driver to use.
        :param options: The options for the logging driver.
        """
        self._values = {
            "name": name,
        }
        if options is not None:
            self._values["options"] = options

    @builtins.property
    def name(self) -> str:
        """The logging driver to use."""
        return self._values.get("name")

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The options for the logging driver."""
        return self._values.get("options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecLogDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecPlacement",
    jsii_struct_bases=[],
    name_mapping={
        "constraints": "constraints",
        "platforms": "platforms",
        "prefs": "prefs",
    },
)
class ServiceTaskSpecPlacement:
    def __init__(
        self,
        *,
        constraints: typing.Optional[typing.List[str]] = None,
        platforms: typing.Optional[typing.List["ServiceTaskSpecPlacementPlatforms"]] = None,
        prefs: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param constraints: An array of constraints. e.g.: node.role==manager
        :param platforms: platforms block.
        :param prefs: Preferences provide a way to make the scheduler aware of factors such as topology. They are provided in order from highest to lowest precedence, e.g.: spread=node.role.manager
        """
        self._values = {}
        if constraints is not None:
            self._values["constraints"] = constraints
        if platforms is not None:
            self._values["platforms"] = platforms
        if prefs is not None:
            self._values["prefs"] = prefs

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[str]]:
        """An array of constraints.

        e.g.: node.role==manager
        """
        return self._values.get("constraints")

    @builtins.property
    def platforms(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecPlacementPlatforms"]]:
        """platforms block."""
        return self._values.get("platforms")

    @builtins.property
    def prefs(self) -> typing.Optional[typing.List[str]]:
        """Preferences provide a way to make the scheduler aware of factors such as topology.

        They are provided in order from highest to lowest precedence, e.g.: spread=node.role.manager
        """
        return self._values.get("prefs")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecPlacementPlatforms",
    jsii_struct_bases=[],
    name_mapping={"architecture": "architecture", "os": "os"},
)
class ServiceTaskSpecPlacementPlatforms:
    def __init__(self, *, architecture: str, os: str) -> None:
        """
        :param architecture: The architecture, e.g. amd64.
        :param os: The operation system, e.g. linux.
        """
        self._values = {
            "architecture": architecture,
            "os": os,
        }

    @builtins.property
    def architecture(self) -> str:
        """The architecture, e.g. amd64."""
        return self._values.get("architecture")

    @builtins.property
    def os(self) -> str:
        """The operation system, e.g. linux."""
        return self._values.get("os")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacementPlatforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "reservation": "reservation"},
)
class ServiceTaskSpecResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.List["ServiceTaskSpecResourcesLimits"]] = None,
        reservation: typing.Optional[typing.List["ServiceTaskSpecResourcesReservation"]] = None,
    ) -> None:
        """
        :param limits: limits block.
        :param reservation: reservation block.
        """
        self._values = {}
        if limits is not None:
            self._values["limits"] = limits
        if reservation is not None:
            self._values["reservation"] = reservation

    @builtins.property
    def limits(self) -> typing.Optional[typing.List["ServiceTaskSpecResourcesLimits"]]:
        """limits block."""
        return self._values.get("limits")

    @builtins.property
    def reservation(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecResourcesReservation"]]:
        """reservation block."""
        return self._values.get("reservation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={
        "generic_resources": "genericResources",
        "memory_bytes": "memoryBytes",
        "nano_cpus": "nanoCpus",
    },
)
class ServiceTaskSpecResourcesLimits:
    def __init__(
        self,
        *,
        generic_resources: typing.Optional[typing.List["ServiceTaskSpecResourcesLimitsGenericResources"]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param generic_resources: generic_resources block.
        :param memory_bytes: The amounf of memory in bytes the container allocates.
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least 1000000
        """
        self._values = {}
        if generic_resources is not None:
            self._values["generic_resources"] = generic_resources
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def generic_resources(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecResourcesLimitsGenericResources"]]:
        """generic_resources block."""
        return self._values.get("generic_resources")

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        """The amounf of memory in bytes the container allocates."""
        return self._values.get("memory_bytes")

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        """CPU shares in units of 1/1e9 (or 10^-9) of the CPU.

        Should be at least 1000000
        """
        return self._values.get("nano_cpus")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecResourcesLimitsGenericResources",
    jsii_struct_bases=[],
    name_mapping={
        "discrete_resources_spec": "discreteResourcesSpec",
        "named_resources_spec": "namedResourcesSpec",
    },
)
class ServiceTaskSpecResourcesLimitsGenericResources:
    def __init__(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.List[str]] = None,
        named_resources_spec: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param discrete_resources_spec: The Integer resources.
        :param named_resources_spec: The String resources.
        """
        self._values = {}
        if discrete_resources_spec is not None:
            self._values["discrete_resources_spec"] = discrete_resources_spec
        if named_resources_spec is not None:
            self._values["named_resources_spec"] = named_resources_spec

    @builtins.property
    def discrete_resources_spec(self) -> typing.Optional[typing.List[str]]:
        """The Integer resources."""
        return self._values.get("discrete_resources_spec")

    @builtins.property
    def named_resources_spec(self) -> typing.Optional[typing.List[str]]:
        """The String resources."""
        return self._values.get("named_resources_spec")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesLimitsGenericResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecResourcesReservation",
    jsii_struct_bases=[],
    name_mapping={
        "generic_resources": "genericResources",
        "memory_bytes": "memoryBytes",
        "nano_cpus": "nanoCpus",
    },
)
class ServiceTaskSpecResourcesReservation:
    def __init__(
        self,
        *,
        generic_resources: typing.Optional[typing.List["ServiceTaskSpecResourcesReservationGenericResources"]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param generic_resources: generic_resources block.
        :param memory_bytes: The amounf of memory in bytes the container allocates.
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least 1000000
        """
        self._values = {}
        if generic_resources is not None:
            self._values["generic_resources"] = generic_resources
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def generic_resources(
        self,
    ) -> typing.Optional[typing.List["ServiceTaskSpecResourcesReservationGenericResources"]]:
        """generic_resources block."""
        return self._values.get("generic_resources")

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        """The amounf of memory in bytes the container allocates."""
        return self._values.get("memory_bytes")

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        """CPU shares in units of 1/1e9 (or 10^-9) of the CPU.

        Should be at least 1000000
        """
        return self._values.get("nano_cpus")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceTaskSpecResourcesReservationGenericResources",
    jsii_struct_bases=[],
    name_mapping={
        "discrete_resources_spec": "discreteResourcesSpec",
        "named_resources_spec": "namedResourcesSpec",
    },
)
class ServiceTaskSpecResourcesReservationGenericResources:
    def __init__(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.List[str]] = None,
        named_resources_spec: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """
        :param discrete_resources_spec: The Integer resources.
        :param named_resources_spec: The String resources.
        """
        self._values = {}
        if discrete_resources_spec is not None:
            self._values["discrete_resources_spec"] = discrete_resources_spec
        if named_resources_spec is not None:
            self._values["named_resources_spec"] = named_resources_spec

    @builtins.property
    def discrete_resources_spec(self) -> typing.Optional[typing.List[str]]:
        """The Integer resources."""
        return self._values.get("discrete_resources_spec")

    @builtins.property
    def named_resources_spec(self) -> typing.Optional[typing.List[str]]:
        """The String resources."""
        return self._values.get("named_resources_spec")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservationGenericResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.ServiceUpdateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceUpdateConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[str] = None,
        failure_action: typing.Optional[str] = None,
        max_failure_ratio: typing.Optional[str] = None,
        monitor: typing.Optional[str] = None,
        order: typing.Optional[str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param delay: Delay between task updates (ns|us|ms|s|m|h).
        :param failure_action: Action on update failure: pause | continue | rollback.
        :param max_failure_ratio: Failure rate to tolerate during an update.
        :param monitor: Duration after each task update to monitor for failure (ns|us|ms|s|m|h).
        :param order: Update order: either 'stop-first' or 'start-first'.
        :param parallelism: Maximum number of tasks to be updated in one iteration.
        """
        self._values = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[str]:
        """Delay between task updates (ns|us|ms|s|m|h)."""
        return self._values.get("delay")

    @builtins.property
    def failure_action(self) -> typing.Optional[str]:
        """Action on update failure: pause | continue | rollback."""
        return self._values.get("failure_action")

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[str]:
        """Failure rate to tolerate during an update."""
        return self._values.get("max_failure_ratio")

    @builtins.property
    def monitor(self) -> typing.Optional[str]:
        """Duration after each task update to monitor for failure (ns|us|ms|s|m|h)."""
        return self._values.get("monitor")

    @builtins.property
    def order(self) -> typing.Optional[str]:
        """Update order: either 'stop-first' or 'start-first'."""
        return self._values.get("order")

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        """Maximum number of tasks to be updated in one iteration."""
        return self._values.get("parallelism")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUpdateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Volume(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.Volume",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        driver: typing.Optional[str] = None,
        driver_opts: typing.Optional[typing.Mapping[str, str]] = None,
        labels: typing.Optional[typing.List["VolumeLabels"]] = None,
        name: typing.Optional[str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param driver: 
        :param driver_opts: 
        :param labels: labels block.
        :param name: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        """
        config = VolumeConfig(
            driver=driver,
            driver_opts=driver_opts,
            labels=labels,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(Volume, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        return jsii.invoke(self, "synthesizeAttributes", [])

    @builtins.property
    @jsii.member(jsii_name="mountpoint")
    def mountpoint(self) -> str:
        return jsii.get(self, "mountpoint")

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> typing.Optional[str]:
        return jsii.get(self, "driver")

    @driver.setter
    def driver(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "driver", value)

    @builtins.property
    @jsii.member(jsii_name="driverOpts")
    def driver_opts(self) -> typing.Optional[typing.Mapping[str, str]]:
        return jsii.get(self, "driverOpts")

    @driver_opts.setter
    def driver_opts(self, value: typing.Optional[typing.Mapping[str, str]]) -> None:
        jsii.set(self, "driverOpts", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[str]:
        return jsii.get(self, "id")

    @id.setter
    def id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[typing.List["VolumeLabels"]]:
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Optional[typing.List["VolumeLabels"]]) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.VolumeConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "driver": "driver",
        "driver_opts": "driverOpts",
        "labels": "labels",
        "name": "name",
    },
)
class VolumeConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.TerraformResource]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        driver: typing.Optional[str] = None,
        driver_opts: typing.Optional[typing.Mapping[str, str]] = None,
        labels: typing.Optional[typing.List["VolumeLabels"]] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param driver: 
        :param driver_opts: 
        :param labels: labels block.
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
        if driver is not None:
            self._values["driver"] = driver
        if driver_opts is not None:
            self._values["driver_opts"] = driver_opts
        if labels is not None:
            self._values["labels"] = labels
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
    def driver(self) -> typing.Optional[str]:
        return self._values.get("driver")

    @builtins.property
    def driver_opts(self) -> typing.Optional[typing.Mapping[str, str]]:
        return self._values.get("driver_opts")

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["VolumeLabels"]]:
        """labels block."""
        return self._values.get("labels")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        return self._values.get("name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.VolumeLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class VolumeLabels:
    def __init__(self, *, label: str, value: str) -> None:
        """
        :param label: Name of the label.
        :param value: Value of the label.
        """
        self._values = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> str:
        """Name of the label."""
        return self._values.get("label")

    @builtins.property
    def value(self) -> str:
        """Value of the label."""
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VolumeLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Config",
    "ConfigConfig",
    "Container",
    "ContainerCapabilities",
    "ContainerConfig",
    "ContainerDevices",
    "ContainerHealthcheck",
    "ContainerHost",
    "ContainerLabels",
    "ContainerMounts",
    "ContainerMountsBindOptions",
    "ContainerMountsTmpfsOptions",
    "ContainerMountsVolumeOptions",
    "ContainerMountsVolumeOptionsLabels",
    "ContainerNetworkData",
    "ContainerNetworksAdvanced",
    "ContainerPorts",
    "ContainerUlimit",
    "ContainerUpload",
    "ContainerVolumes",
    "DataDockerNetwork",
    "DataDockerNetworkConfig",
    "DataDockerNetworkIpamConfig",
    "DataDockerRegistryImage",
    "DataDockerRegistryImageConfig",
    "DockerProvider",
    "DockerProviderConfig",
    "DockerProviderRegistryAuth",
    "Image",
    "ImageConfig",
    "Network",
    "NetworkConfig",
    "NetworkIpamConfig",
    "NetworkLabels",
    "Secret",
    "SecretConfig",
    "SecretLabels",
    "Service",
    "ServiceConfig",
    "ServiceConvergeConfig",
    "ServiceEndpointSpec",
    "ServiceEndpointSpecPorts",
    "ServiceLabels",
    "ServiceMode",
    "ServiceModeReplicated",
    "ServiceRollbackConfig",
    "ServiceTaskSpec",
    "ServiceTaskSpecContainerSpec",
    "ServiceTaskSpecContainerSpecConfigs",
    "ServiceTaskSpecContainerSpecDnsConfig",
    "ServiceTaskSpecContainerSpecHealthcheck",
    "ServiceTaskSpecContainerSpecHosts",
    "ServiceTaskSpecContainerSpecLabels",
    "ServiceTaskSpecContainerSpecMounts",
    "ServiceTaskSpecContainerSpecMountsBindOptions",
    "ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    "ServiceTaskSpecContainerSpecMountsVolumeOptions",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    "ServiceTaskSpecContainerSpecPrivileges",
    "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    "ServiceTaskSpecContainerSpecSecrets",
    "ServiceTaskSpecLogDriver",
    "ServiceTaskSpecPlacement",
    "ServiceTaskSpecPlacementPlatforms",
    "ServiceTaskSpecResources",
    "ServiceTaskSpecResourcesLimits",
    "ServiceTaskSpecResourcesLimitsGenericResources",
    "ServiceTaskSpecResourcesReservation",
    "ServiceTaskSpecResourcesReservationGenericResources",
    "ServiceUpdateConfig",
    "Volume",
    "VolumeConfig",
    "VolumeLabels",
]

publication.publish()
