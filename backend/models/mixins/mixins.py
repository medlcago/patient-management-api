from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from utils.time import get_current_utc_time


# text("CAST(CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS TIMESTAMP WITHOUT TIME ZONE)")


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_utc_time,
        server_default=func.now()
    )

    @property
    def created_date(self) -> datetime:
        return self.created_at.replace(microsecond=0, tzinfo=None)


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        default=get_current_utc_time,
        server_default=func.now(),
        onupdate=get_current_utc_time,
        server_onupdate=func.now()
    )

    @property
    def updated_date(self) -> datetime:
        return self.updated_at.replace(microsecond=0, tzinfo=None)
