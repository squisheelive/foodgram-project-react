from django.core.exceptions import ValidationError


def validate_amount(value: int):
    if value < 0:
        raise ValidationError('Количество не может быть отрицательным!')


def validate_time(value: int):
    if value < 0:
        raise ValidationError(
            'Время приготовления не может быть отрицательным!'
        )
    if value > 1440:
        raise ValidationError(
            'Время приготовления не может быть больше 24 часов!'
        )
