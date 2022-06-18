from django.core.exceptions import ValidationError


def validate_file(value):
    value= str(value)
    if value.endswith(".pdf") != True and value.endswith(".doc") != True and value.endswith(".docx") != True: 
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        return value
