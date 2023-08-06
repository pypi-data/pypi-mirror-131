from abc import ABCMeta

mapper = dict()


def register_class(klass):
    mapper[klass.KLASS] = klass


class Registry(ABCMeta):
    def __new__(mcs, name, bases, class_dict):
        cls = super().__new__(mcs, name, bases, class_dict)
        register_class(cls)
        return cls
