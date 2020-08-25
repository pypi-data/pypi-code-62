# Django libraries
# 3rd Party libraries
import graphene
from graphene_django.types import DjangoObjectType
# Standard/core python libraries
# Our custom libraries

# EXAMPLE GRAPHENE ObjectType


class UserType(graphene.ObjectType):
    id_user = graphene.ID(description="A unique int value identifying User",
        required=False)
    username = graphene.String(description="A unique string value identifying User",
        required=False)
    email = graphene.String(description="A unique string value identifying User's email",
                            required=False)
    first_name = graphene.String(description="A string value identifying User's name",
        required=False)
    last_name = graphene.String(description="A string value identifying User's last name",
                                required=False)

    class Meta:
        name = "User"
        description = "Manejo de Usuarios"

# EXAMPLE GRAPHENE DjangoObjectType
# class PortType(DjangoObjectType):
#     class Meta:
#         name = "Name"
#         description = "Description name"
#         model = Model
#         fields = ["field_1",
#                   "field_2",
#                   "field_3",
#                   ]
