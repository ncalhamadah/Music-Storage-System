from .abstract_factory import AbstractFactory
from controllers.login_controller import LoginController


class ControllerFactory(AbstractFactory):
    "The Factory Class for controller"

    def create_object(self, some_property):
        "A static method to get a concrete product"
        if some_property == 'login_controller':
            return LoginController()
        return None