from django.urls import path
from django.views.generic import View

urlpatterns = []

class RouteView(View):
    """
     A view able to register itself in the django urls patterns

     route:str The url pattern for the view
     name:str:optional The name of the view. Default to self.__name__
    """

    route:str = None
    name:str = None

    def __init_subclass__(cls) -> None:
        cls._init_properties(cls)
        cls._add_route_(cls)

    def _init_properties(self) -> None:
        if self.route is None:
            raise ValueError("route property cannot be None")

        if self.name is None:
            self.name = self.__name__

    def _add_route_(self):
        urlpatterns.append(path(self.route, self.as_view(), name=self.name))
