from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy import select, String
from typing import Optional
from datetime import datetime
from uuid import uuid4
from core import url_actions


db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


class Url(Base):

    __tablename__ = "urls"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), unique=True
    )
    original_url: Mapped[Optional[str]] = mapped_column(String(500))
    short_url: Mapped[Optional[str]] = mapped_column(unique=True)
    visit_count: Mapped[Optional[int]] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class DatabaseAction:

    def store_url_to_db(self, original_url: str) -> None:
        """generates and stores the original and short url to db."""

        # generate a short unique url
        short_url = url_actions.generate_unique_url()

        # store the information

        url = Url(original_url=original_url, short_url=short_url)

        db.session.add(url)
        db.session.commit()

    def get_redirect_url(self, short_url: str) -> Optional[str]:
        """return the redirect url for the short url"""

        query = select(Url.original_url).where(Url.short_url == short_url)

        url = db.session.execute(query).scalar()

        return url

    def increment_visit_count(self, short_url: str):
        """Increase the visit count for a short URL and return the updated Url object."""

        stmt = select(Url).where(Url.short_url == short_url)
        url = db.session.execute(stmt).scalar_one_or_none()

        if not url:
            return None

        url.visit_count += 1  # type: ignore
        db.session.commit()

        return url

    def get_url_data(self, short_url: str):
        """returns the data related to the url"""

        query = select(Url).where(Url.short_url == short_url)

        result = db.session.execute(query).scalar_one()

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
