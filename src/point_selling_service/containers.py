from dependency_injector import providers, containers, resources

__all__ = ["Container"]

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
