class AidkitCLIError(Exception):
    pass


class ResourceWithIdNotFoundError(Exception):
    pass


class ResourceWithNameNotFoundError(Exception):
    pass


class AidkitClientNotConfiguredError(AidkitCLIError):
    ...


class RunTimeoutError(AidkitCLIError):
    ...
