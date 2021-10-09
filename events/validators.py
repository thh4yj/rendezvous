import os
from django.core.exceptions import ValidationError

# Source: https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
# General structure of the validator found in the solution was followed
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')