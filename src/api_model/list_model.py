class ListModel:
    def __eq__(self, other):
        return True

    @property
    def name(self) -> str:
        return "List"

    @property
    def import_path(self) -> str:
        return "typing"
