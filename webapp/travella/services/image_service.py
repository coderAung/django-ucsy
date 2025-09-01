import os
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile

def copy_and_save(_from:ImageFieldFile, _to:ImageFieldFile):
    with _from.open('rb') as f:
        file_content = ContentFile(f.read())
    
    _to.save(
        os.path.basename(_from.name),
        file_content,
        save=True
    )