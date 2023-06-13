class Command:
    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and self.arguments == __value.arguments
