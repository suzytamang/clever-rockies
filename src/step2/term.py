class Term:
    def __init__(self, _id, label, _class, _subclass):
        self._id = _id
        self.label = label
        self._class = _class
        self._subclass = _subclass

    def __repr__(self) -> str:
        return f"Label: \"{self.label}\", Class: {self._class}, Subclass: {self._subclass}"

    # def __eq__(self, value: object) -> bool:
    #     if isinstance(value, str):
    #         return self._class == value
    #     if isinstance(value, Term):
    #         return self._class == value._class
    #     return False
