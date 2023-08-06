class ZeusAIException(Exception):
    pass


class PluginError(ZeusAIException):
    pass


class InvalidEndpoint(PluginError):
    pass


class InvalidParams(PluginError):
    pass


class ForbiddenInStandalone(PluginError):
    pass


class InvalidResponse(PluginError):
    pass
