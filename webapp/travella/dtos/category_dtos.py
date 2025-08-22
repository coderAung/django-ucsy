from datetime import datetime

class CategoryDTO:
    def __init__(self, id: int, name: str, created_by: str, packages_count: int=0, created_at=None):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.packages_count = packages_count
        self.created_at = created_at or datetime.now() 

    @classmethod
    def from_model(cls, model_instance):
        packages_count = getattr(model_instance, 'packages_count', 0)
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            created_by=model_instance.createdBy.email,
            packages_count=packages_count,
            created_at=getattr(model_instance, 'created_at', None)
        )