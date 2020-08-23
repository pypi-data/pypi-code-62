from __future__ import annotations
import asyncio
import signal
from typing import Any, Dict, List, Optional, Union

import backoff
import httpx
import typer
import loguru

from devtools import pformat
from pydantic import BaseModel, Field, parse_obj_as

from servo import api
from servo.api import descriptor_to_adjustments
from servo.assembly import Assembly, BaseServoConfiguration
from servo.configuration import Optimizer
from servo.errors import ConnectorError
from servo.logging import ProgressHandler
from servo.servo import Events, Servo
from servo.types import Adjustment, Control, Duration, Description, Measurement
from servo.utilities import commandify, value_for_key_path


class Runner(api.Mixin):
    assembly: Assembly

    def __init__(self, assembly: Assembly) -> None:
        self.assembly = assembly
        super().__init__()

    @property
    def optimizer(self) -> Optimizer:
        return self.servo.optimizer
    
    @property
    def servo(self) -> Servo:
        return self.assembly.servo

    @property
    def config(self) -> BaseServoConfiguration:
        return self.servo.config

    @property
    def logger(self) -> loguru.Logger:
        return self.servo.logger
    
    def display_banner(self) -> None:
        banner = (
            "   _____                      _  __\n"
            "  / ___/___  ______   ______ | |/ /\n"
            "  \__ \/ _ \/ ___/ | / / __ \|   /\n"
            " ___/ /  __/ /   | |/ / /_/ /   |\n"
            "/____/\___/_/    |___/\____/_/|_|"
        )
        typer.secho(banner, fg=typer.colors.BRIGHT_BLUE, bold=True)
                
        types = Assembly.all_connector_types()
        types.remove(Servo)
        
        names = []
        for c in types:
            name = typer.style(commandify(c.__default_name__), fg=typer.colors.CYAN, bold=False)
            version = typer.style(str(c.version), fg=typer.colors.WHITE, bold=True)
            names.append(f"{name}-{version}")
        version = typer.style(f"v{Servo.version}", fg=typer.colors.WHITE, bold=True)
        codename = typer.style("woke up like this", fg=typer.colors.MAGENTA, bold=False)
        initialized = typer.style("initialized", fg=typer.colors.BRIGHT_GREEN, bold=True)        
        
        typer.secho(f"{version} \"{codename}\" {initialized}")
        typer.secho()
        typer.secho(f"connectors:  {', '.join(sorted(names))}")
        typer.secho(f"config file: {typer.style(str(self.assembly.config_file), bold=True, fg=typer.colors.YELLOW)}")
        id = typer.style(self.optimizer.id, bold=True, fg=typer.colors.WHITE)        
        typer.secho(f"optimizer:   {id}")
        if self.optimizer.base_url != "https://api.opsani.com/":
            base_url = typer.style(f"{self.optimizer.base_url}", bold=True, fg=typer.colors.RED)
            typer.secho(f"base url: {base_url}")
        typer.secho()

    async def describe(self) -> Description:
        self.logger.info("Describing...")

        aggregate_description = Description.construct()
        results: List[EventResult] = await self.servo.dispatch_event(Events.DESCRIBE)
        for result in results:
            description = result.value
            aggregate_description.components.extend(description.components)
            aggregate_description.metrics.extend(description.metrics)

        return aggregate_description

    async def measure(self, param: api.MeasureParams) -> Measurement:
        self.logger.info(f"Measuring... [metrics={', '.join(param.metrics)}]")
        self.logger.trace(pformat(param))

        aggregate_measurement = Measurement.construct()
        results: List[EventResult] = await self.servo.dispatch_event(
            Events.MEASURE, metrics=param.metrics, control=param.control
        )
        for result in results:
            measurement = result.value
            aggregate_measurement.readings.extend(measurement.readings)
            aggregate_measurement.annotations.update(measurement.annotations)

        return aggregate_measurement

    async def adjust(self, adjustments: List[Adjustment], control: Control) -> None:
        summary = f"[{', '.join(list(map(str, adjustments)))}]"
        self.logger.info(f"Adjusting... {summary}")
        self.logger.trace(pformat(adjustments))
        
        await self.servo.dispatch_event(Events.ADJUST, adjustments)
        self.logger.info(f"Adjustment completed {summary}")

    async def exec_command(self):
        cmd_response = await self._post_event(api.Event.WHATS_NEXT, None)
        self.logger.info(f"What's Next? => {cmd_response.command}")
        self.logger.trace(pformat(cmd_response))

        try:
            if cmd_response.command == api.Command.DESCRIBE:
                description = await self.describe()
                self.logger.info(
                    f"Described: {len(description.components)} components, {len(description.metrics)} metrics"
                )
                self.logger.trace(pformat(description))
                param = dict(descriptor=description.opsani_dict(), status="ok")
                await self._post_event(api.Event.DESCRIPTION, param)

            elif cmd_response.command == api.Command.MEASURE:
                measurement = await self.measure(cmd_response.param)
                self.logger.info(
                    f"Measured: {len(measurement.readings)} readings, {len(measurement.annotations)} annotations"
                )
                self.logger.trace(pformat(measurement))
                param = measurement.opsani_dict()
                await self._post_event(api.Event.MEASUREMENT, param)

            elif cmd_response.command == api.Command.ADJUST:
                adjustments = descriptor_to_adjustments(cmd_response.param["state"])
                control = Control(**cmd_response.param.get("control", {}))
                await self.adjust(adjustments, control)

                # TODO: Model a response class ("Adjusted"?) -- map errors to the response
                # If no errors, report state matching the request
                reply = { "status": "ok", "state": cmd_response.param["state"] }

                components_dict = cmd_response.param["state"]["application"]["components"]
                components_count = len(components_dict)
                settings_count = sum(
                    len(components_dict[component]["settings"])
                    for component in components_dict
                )
                self.logger.info(
                    f"Adjusted: {components_count} components, {settings_count} settings"
                )

                await self._post_event(api.Event.ADJUSTMENT, reply)

            elif cmd_response.command == api.Command.SLEEP:
                    # TODO: Model this
                    duration = Duration(cmd_response.param.get("duration", 120))
                    status = value_for_key_path(cmd_response.param, "data.status", None)
                    reason = value_for_key_path(cmd_response.param, "data.reason", "unknown reason")
                    msg = f"{status}: {reason}" if status else f"{reason}"
                    self.logger.info(f"Sleeping for {duration} ({msg}).")
                    await asyncio.sleep(duration.total_seconds())

            else:
                raise ValueError(f"Unknown command '{cmd_response.command.value}'")

        except Exception as error:            
            self.logger.exception(f"{cmd_response.command} command failed: {error}")
            param = dict(status="failed", message=str(error))
            await self.shutdown(asyncio.get_event_loop())
            await self._post_event(cmd_response.command.response_event, param)

    async def main(self) -> None:
        # Setup logging
        self.progress_handler = ProgressHandler(self.servo.report_progress, self.logger.warning)
        self.logger.add(self.progress_handler.sink, catch=True)

        self.logger.info(
            f"Servo started with {len(self.servo.connectors)} active connectors [{self.optimizer.id} @ {self.optimizer.base_url}]"
        )
        self.logger.info("Dispatching startup event...")
        await self.servo.startup()

        self.logger.info("Saying HELLO.", end=" ")
        await self._post_event(api.Event.HELLO, dict(agent=api.USER_AGENT))

        while True:
            try:
                await self.exec_command()
            except Exception:
                self.logger.exception("Exception encountered while executing command")
    
    async def shutdown(self, loop, signal=None):
        if signal:
            self.logger.info(f"Received exit signal {signal.name}...")

        try:
            reason = signal.name if signal else 'shutdown'
            await self._post_event(api.Event.GOODBYE, dict(reason=reason))
        except Exception:
            self.logger.exception(f"Exception occurred during GOODBYE request")
        
        self.logger.info("Dispatching shutdown event...")
        await self.servo.shutdown()
        
        tasks = [t for t in asyncio.all_tasks() if t is not
                asyncio.current_task()]

        [task.cancel() for task in tasks]

        self.logger.info(f"Cancelling {len(tasks)} outstanding tasks")
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.logger.info("Servo shutdown complete.")
        await self.logger.complete()
        
        loop.stop()
    
    def handle_exception(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        self.logger.error(f"asyncio exception handler triggered with context: {context}")

        # context["message"] will always be there; but context["exception"] may not
        exception = context.get("exception")
        if exception:
            # FIXME: it is not necessary to re-raise this to get the right logging it is logging None atm
            try:
                raise exception
            except:
                self.logger.exception(f"exception details: {exception}")

        self.logger.critical("Shutting down due to unhandled exception in asyncio task...")

        # try to shutdown cleanly
        try:
            asyncio.create_task(self.shutdown(loop))
        except Exception as exception:
            self.logger.exception(f"caught exception trying to schedule shutdown: {exception}")

    def run(self) -> None:
        self.display_banner()

        # Setup async event loop
        loop = asyncio.get_event_loop()
        
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT, signal.SIGUSR1)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(self.shutdown(loop, signal=s)))
        
        loop.set_exception_handler(self.handle_exception)

        try:
            loop.create_task(self.main())
            loop.run_forever()
        finally:
            loop.close()            
