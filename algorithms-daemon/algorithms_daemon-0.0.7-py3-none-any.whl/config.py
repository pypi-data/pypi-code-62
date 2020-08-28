import os
import uuid

GrpcHost = "127.0.0.1"
GrpcPort = 5601

# style like azure pipeline enviroment variables.
ArtifactStagingDirectory = "/a"
BinariesDirectory = "/b"
SourcesDirectory = "/s"

ArtifactInputDirectory = "/a/input"
ArtifactOutputDirectory = "/a/output"
ArtifactArgumentsDirectory = "/a/arguments"

WorkerIdentity = str(uuid.uuid4())

GrpcHost = os.getenv('GRPCHOST', GrpcHost)
GrpcPort = int(os.getenv('GRPCPORT', str(GrpcPort)))
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
