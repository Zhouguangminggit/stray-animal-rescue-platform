from django.core.exceptions import ValidationError


def validate_image_size(value) -> None:
    if value and value.size > 5 * 1024 * 1024:
        raise ValidationError("图片文件不能超过 5MB。")


def validate_document_size(value) -> None:
    if value and value.size > 10 * 1024 * 1024:
        raise ValidationError("材料文件不能超过 10MB。")
