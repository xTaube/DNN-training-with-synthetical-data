class BlenderException(Exception):
    pass


class ObjectReferenceNotExist(BlenderException):
    pass


class ObjectAlreadyAddedToScene(BlenderException):
    pass


class ObjectNotInScene(BlenderException):
    pass


class LayerNotSupported(BlenderException):
    pass