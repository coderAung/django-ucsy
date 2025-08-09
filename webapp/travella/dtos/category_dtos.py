
class CategoryDTO:
    def __init__(self, id: int, name: str, created_by: str):
        self.id = id
        self.name = name
        self.created_by = created_by

    @classmethod
    def from_model(cls, model_instance):
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            created_by=model_instance.createdBy.email
        )
