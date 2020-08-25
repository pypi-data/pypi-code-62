import os
import uuid

ZeromqConnection = "tcp://localhost:5555"
# ZeromqConnection = "ipc:///tmp/idontexist.socket"

# style like azure pipeline enviroment variables.
ArtifactStagingDirectory = "/a"
BinariesDirectory = "/b"
SourcesDirectory = "/s"

ArtifactInputDirectory = "/a/input"
ArtifactOutputDirectory = "/a/output"
ArtifactArgumentsDirectory = "/a/arguments"

WorkerIdentity = str(uuid.uuid4())

ZeromqConnection = os.getenv('ZEROMQCONNECTION', ZeromqConnection)
ArtifactStagingDirectory = os.getenv(
    'ArtifactStagingDirectory', ArtifactStagingDirectory)
BinariesDirectory = os.getenv(
    'BinariesDirectory', BinariesDirectory)
SourcesDirectory = os.getenv(
    'SourcesDirectory', SourcesDirectory)

ArtifactInputDirectory = os.getenv(
    'ArtifactInputDirectory', ArtifactInputDirectory
)

ArtifactOutputDirectory = os.getenv(
    'ArtifactOutputDirectory', ArtifactOutputDirectory
)

ArtifactArgumentsDirectory = os.getenv(
    'ArtifactArgumentsDirectory', ArtifactArgumentsDirectory
)

WorkerIdentity = os.getenv('JobId', WorkerIdentity)
