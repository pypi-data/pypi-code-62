from typing import Optional, List
from aws_cdk.aws_cloudformation import CustomResource, CustomResourceProvider, ICustomResourceProvider
from aws_cdk.aws_iam import Role, CompositePrincipal, ServicePrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import IFunction, Runtime, Code, Function
from aws_cdk.core import Stack, RemovalPolicy, Duration
from aws_empty_ecr_repository.package import package_root
from aws_cdk.aws_ecr import Repository, LifecycleRule


class EmptyEcrRepository(Repository):
    def __init__(
            self,
            scope: Stack,
            id: str,
            lifecycle_registry_id: Optional[str] = None,
            lifecycle_rules: Optional[List[LifecycleRule]] = None,
            removal_policy: Optional[RemovalPolicy] = None,
            repository_name: Optional[str] = None,
            **kwargs
    ) -> None:
        assert repository_name, 'Repository name must be provided!'
        removal_policy = removal_policy or RemovalPolicy.DESTROY
        
        known_args = dict(
            scope=scope,
            id=id,
            lifecycle_registry_id=lifecycle_registry_id,
            lifecycle_rules=lifecycle_rules,
            removal_policy=removal_policy,
            repository_name=repository_name
        )

        unknown_args = kwargs

        super().__init__(
            **{
                **known_args,
                **unknown_args
            }
        )

        self.__role = Role(
            scope=scope,
            id=repository_name + 'Role',
            role_name=repository_name + 'Role',
            assumed_by=CompositePrincipal(
                ServicePrincipal("lambda.amazonaws.com"),
                ServicePrincipal("cloudformation.amazonaws.com")
            ),
            inline_policies={
                repository_name + 'Policy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                'ecr:ListImages',
                                'ecr:BatchDeleteImage',
                                'ecr:DeleteRepository',
                            ],
                            effect=Effect.ALLOW,
                            resources=[self.repository_arn]
                        ),
                        PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            effect=Effect.ALLOW,
                            resources=['*']
                        ),
                    ]
                )
            },
            managed_policies=[]
        )

        self.__custom_backend = Function(
            scope=scope,
            id=repository_name + 'Backend',
            code=Code.from_asset(
                path=package_root
            ),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6,
            description=f'.',
            function_name=repository_name + 'Backend',
            memory_size=128,
            role=self.__role,
            timeout=Duration.seconds(900),
        )

        # noinspection PyTypeChecker
        provider: ICustomResourceProvider = CustomResourceProvider.from_lambda(self.__custom_backend)

        self.__custom_resource = CustomResource(
            scope=scope,
            id=repository_name + 'CustomResource',
            provider=provider,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'repositoryName': repository_name
            },
            resource_type='Custom::EmptyEcrRepository'
        )

        # Make sure that custom resource is deleted before lambda function backend.
        self.__custom_resource.node.add_dependency(self.__custom_backend)
        # Make sure that custom resource is deleted before the repository.
        self.__custom_resource.node.add_dependency(self)

    @property
    def backend(self) -> IFunction:
        return self.__custom_backend

    @property
    def custom_resource(self) -> CustomResource:
        return self.__custom_resource
