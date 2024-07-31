from pydantic import model_validator


class AtLeastOneFieldNotNoneMixin:
    @model_validator(mode="after")
    def check_at_least_one_field_not_none(self):
        data = self.model_dump(exclude_none=True)
        if not data:
            msg = f"({', '.join(f'{k}' for k in self.model_fields.keys())}). At least one field must be set."
            raise ValueError(msg)
        return self