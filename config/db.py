from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, String
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from core import ShortUrl
import uuid


db = SQLAlchemy()


class Url(db.Model):

    __tablename__ = "urls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4()
    )
    original_url: Mapped[Optional[str]] = mapped_column(String(1500))
    short_url: Mapped[Optional[str]] = mapped_column(unique=True)
    visit_count: Mapped[Optional[int]] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class DatabaseAction:

    def store_url_to_db(self, original_url: str) -> str:
        """generates and stores the original and short url to db."""

        # generate a short unique url
        short_url = url_actions.generate_unique_url()

        # store the information

        url = Url()
        url.original_url = original_url
        url.short_url = short_url

        db.session.add(url)
        db.session.commit()

        return short_url

    def get_redirect_url(self, short_url: str) -> Optional[str]:
        """return the redirect url for the short url"""

        query = select(Url.original_url).where(Url.short_url == short_url)

        url = db.session.execute(query).scalar_one_or_none()

        return url

    def increment_visit_count(self, short_url: str):
        """Increase visit count safely and return updated object."""

        url = db.session.execute(
            select(Url).where(Url.short_url == short_url)
        ).scalar_one_or_none()

        if url is None:
            return None

        url.visit_count = (url.visit_count or 0) + 1
        db.session.commit()
        db.session.refresh(url)

        return url

    def get_url_data(self, short_url: str):
        """returns the data related to the url"""

        query = select(Url).where(Url.short_url == short_url)

        result = db.session.execute(query).scalar_one_or_none()

        return result

    def delete_url(self, short_url: str, original_url: str) -> None:
        """deletes the entry where the original_url and short_url matches."""
        query = select(Url).where(
            Url.original_url == original_url, Url.short_url == short_url
        )

        url = db.session.execute(query).scalar_one_or_none()

        if url:
            db.session.delete(url)
            db.session.commit()

    def check_if_generated_str_exists(self, generated_str) -> bool:

        exists = db.session.execute(
            select(Url).where(Url.short_url == generated_str)
        ).scalar_one_or_none()

        if exists:
            return True

        return False


database_actions = DatabaseAction()
url_actions = ShortUrl(database_actions)
