import logging
import sys
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Union

import grpc
from formant.protos.agent.v1 import agent_pb2, agent_pb2_grpc
from formant.protos.model.v1 import (
    commands_pb2,
    datapoint_pb2,
    event_pb2,
    math_pb2,
    media_pb2,
    navigation_pb2,
    text_pb2,
)
from typing_extensions import Literal

from .exceptions import handle_agent_exceptions


def current_timestamp():
    return int(time.time() * 1000)


class Client:
    """
    A client for interacting with the Formant Agent. There are methods for:
    - Ingesting telemetry datapoints
    - Ingesting transform frames
    - Creating events
    - Handling commands
    - Reading application configuration

    Automatically handles connection and reconnection to the agent.
    """

    def __init__(
        self,
        agent_url="unix:///var/lib/formant/agent.sock",  # type: str
        enable_logging=True,  # type: bool
        ignore_throttled=False,  # type: bool
        ignore_unavailable=False,  # type: bool
    ):

        if enable_logging:
            self.logger = logging.getLogger("formant")  # type: Optional[logging.Logger]
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(levelname)s: %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            self.logger = None

        self.ignore_throttled = ignore_throttled
        self.ignore_unavailable = ignore_unavailable

        self._agent_url = agent_url  # type: str
        self._app_config = {}  # type: Dict[str, str]
        self._config_update_callbacks = []  # type: List[Callable[[], None]]
        self._command_request_callback_streams = (
            {}
        )  # type: Dict[Callable[..., None], grpc._channel._MultiThreadedRendezvous]

        self._setup_agent_communication()

    # Ingesting telemetry datapoints

    @handle_agent_exceptions
    def post_text(
        self,
        stream,  # type: str
        value,  # type: str
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post a text datapoint to a telemetry stream."""
        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                text=text_pb2.Text(value=value),
                tags=tags if tags else {},
                timestamp=timestamp if timestamp else current_timestamp(),
            )
        )

    @handle_agent_exceptions
    def post_json(
        self,
        stream,  # type: str
        value,  # type: str
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post a JSON datapoint to a telemetry stream."""
        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                json=text_pb2.Json(value=value),
                timestamp=timestamp if timestamp else int(time.time() * 1000),
                tags=tags if tags else {},
            )
        )

    @handle_agent_exceptions
    def post_numeric(
        self,
        stream,  # type: str
        value,  # type: Union[int, float]
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post a numeric datapoint to a telemetry stream."""
        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                numeric=math_pb2.Numeric(value=value),
                tags=tags if tags else {},
                timestamp=timestamp if timestamp else current_timestamp(),
            )
        )

    @handle_agent_exceptions
    def post_image(
        self,
        stream,  # type: str
        # raw bytes:
        value,  # type: str
        content_type="image/jpg",  # type: Literal["image/jpg", "image/png"]
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post an image datapoint to a telemetry stream."""
        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                image=media_pb2.Image(raw=value, content_type=content_type),
                tags=tags if tags else {},
                timestamp=timestamp if timestamp else current_timestamp(),
            )
        )

    @handle_agent_exceptions
    def post_bitset(
        self,
        stream,  # type: str
        bitset_dict,  # type: Dict[str, bool]
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post a bitset datapoint to a telemetry stream."""

        bitset = math_pb2.Bitset()
        for k, v in bitset_dict.items():
            bitset.bits.extend([math_pb2.Bit(key=k, value=v)])

        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                bitset=bitset,
                tags=tags if tags else {},
                timestamp=timestamp if timestamp else current_timestamp(),
            )
        )

    @handle_agent_exceptions
    def post_geolocation(
        self,
        stream,  # type: str
        latitude,  # type: float
        longitude,  # type: float
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Post a geolocation datapoint to a telemetry stream."""
        self.agent_stub.PostData(
            datapoint_pb2.Datapoint(
                stream=stream,
                location=navigation_pb2.Location(
                    latitude=latitude, longitude=longitude
                ),
                tags=tags if tags else {},
                timestamp=timestamp if timestamp else current_timestamp(),
            )
        )

    # Ingesting transform frames

    @handle_agent_exceptions
    def post_transform_frame(
        self,
        parent_frame,  # type: str
        child_frame,  # type: str
        tx,  # type: float
        ty,  # type: float
        tz,  # type: float
        rx,  # type: float
        ry,  # type: float
        rz,  # type: float
        rw,  # type: float
    ):
        # type: (...) -> None
        """Adds a transform frame, used to position datapoints in 3D space."""
        frame = math_pb2.TransformFrame()
        frame.parent_frame = parent_frame
        frame.child_frame = child_frame
        frame.transform.translation.x = tx
        frame.transform.translation.y = ty
        frame.transform.translation.z = tz
        frame.transform.rotation.x = rx
        frame.transform.rotation.y = ry
        frame.transform.rotation.z = rz
        frame.transform.rotation.w = rw
        self.agent_stub.PostTransformFrame(frame)

    # Creating events

    @handle_agent_exceptions
    def create_event(
        self,
        message,  # type: str
        notify=False,  # type: bool
        tags=None,  # type: Optional[Dict[str, str]]
        timestamp=None,  # type: Optional[int]
    ):
        """Creates and ingests an event."""
        self.agent_stub.CreateEvent(
            agent_pb2.CreateEventRequest(
                event=event_pb2.Event(
                    message=message,
                    notification_enabled=notify,
                    tags=tags if tags else {},
                    timestamp=timestamp if timestamp else current_timestamp(),
                )
            )
        )

    # Handling commands

    def get_command_request(
        self, command_filter=None  # type: Optional[List[str]]
    ):
        # type: (...) -> Optional[commands_pb2.CommandRequest]
        """
        If there is a command request in the agent's queue whose "command" value matches
        an element of the given command filter, takes and returns the command request.

        Otherwise, returns None if there are no matching command requests
        in the agent's queue.
        """
        command_request_request = agent_pb2.GetCommandRequestRequest(
            command_filter=command_filter
        )
        try:
            command_request = self.agent_stub.GetCommandRequest(
                command_request_request
            ).request
            return command_request if command_request.command else None
        except grpc.RpcError:
            return None

    def send_command_response(
        self,
        request_id,  # type: str
        success,  # type: bool
        datapoint=None,  # type: Optional[datapoint_pb2.Datapoint]
    ):
        # type: (...) -> None
        """
        Sends a command response for an identified command request to Formant.
        Returns an error if there was a problem sending the command response.
        """
        response = commands_pb2.CommandResponse(
            request_id=request_id, success=success, datapoint=datapoint,
        )
        request = agent_pb2.SendCommandResponseRequest(response=response)
        self.agent_stub.SendCommandResponse(request)

    def register_command_request_callback(
        self,
        f,  # type: Callable[[commands_pb2.CommandRequest], None]
        command_filter=None,
    ):
        # type : (...) -> None
        """
        Command requests issued to the agent whose "command" value matches an element
        of the given command filter will be streamed into the provided callback.
        """

        def target():
            # stream iterator will receive command requests until cancelled
            # via "stream.cancel()" in unregister_command_request_callback
            while True:
                try:
                    stream = self._get_command_request_stream(command_filter)
                    self._command_request_callback_streams[f] = stream
                    for _ in stream:
                        f(_.request)
                except grpc.RpcError as e:
                    if e.code() == grpc.StatusCode.CANCELLED:
                        return
                    # wait a short duration before re-registering when
                    # agent unavailable or other rpc error
                    time.sleep(0.1)

        threading.Thread(target=target, daemon=True).start()

    def unregister_command_request_callback(
        self, f,  # type: Callable[[commands_pb2.CommandRequest], None]
    ):
        # type : (...) -> None
        """
        Unregisters previously registered command request callbacks.
        """
        command_request_stream = self._command_request_callback_streams.pop(f, None)
        if command_request_stream is not None:
            # this call will raise grpc.StatusCode.CANCELLED
            command_request_stream.cancel()

    # Reading application configuration

    def get_app_config(self, key, *args):
        # type: (str, Any) -> Optional[str]
        """
        Returns the value for the given key that was set in
        Formant application configuration for this device,
        or returns the given default value.
        """
        if len(args) > 1:
            raise TypeError("function takes at most two args: (key: str, default: Any)")
        default = args[0] if len(args) == 1 else None

        if len(self._app_config.keys()) == 0:
            self._update_application_configuration()

        return self._app_config.get(key, default)

    def register_config_update_callback(self, f):
        # type: (Callable) -> None
        """
        Adds a function to the list of callbacks that are executed by the client
        when this device receives updated configuration from Formant.
        """
        self._config_update_callbacks.append(f)

    def unregister_config_update_callback(self, f):
        # type: (Callable) -> None
        """
        Removes a function from the list of callbacks that are executed by the client
        when this device receives updated configuration from Formant.
        """
        self._config_update_callbacks.remove(f)

    # Internal methods

    def _setup_agent_communication(self):
        self.channel = grpc.insecure_channel(self._agent_url)
        self.channel.subscribe(self._handle_connectivity_change, try_to_connect=True)
        self.agent_stub = agent_pb2_grpc.AgentStub(self.channel)

    def _handle_connectivity_change(self, connectivity):
        """Handle changes to gRPC channel connectivity."""
        if connectivity == grpc.ChannelConnectivity.READY:
            if self.logger:
                self.logger.info("Agent communication established.")
            self._update_application_configuration()
            self._run_update_config_callbacks()
        elif connectivity == grpc.ChannelConnectivity.SHUTDOWN:
            # In the case of shutdown, re-establish the connection from scratch
            if self.logger:
                self.logger.info("Agent communication lost. Re-establishing...")
            self._setup_agent_communication()

    @handle_agent_exceptions
    def _update_application_configuration(self):
        request = agent_pb2.GetApplicationConfigurationRequest()
        response = self.agent_stub.GetApplicationConfiguration(request)
        self._app_config = response.configuration.configuration_map

    def _run_update_config_callbacks(self):
        [f() for f in self._config_update_callbacks]

    def _get_command_request_stream(self, command_filter=None):
        return self.agent_stub.GetCommandRequestStream(
            agent_pb2.GetCommandRequestStreamRequest(command_filter=command_filter)
        )
