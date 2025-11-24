from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select, String
from typing import Optional, List
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

    url_data: Mapped[List["UrlData"]] = relationship(
        "UrlData", back_populates="url", cascade="all, delete-orphan"
    )


class UrlData(db.Model):
    __tablename__ = "url_data"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4()
    )
    device_type: Mapped[Optional[str]]
    ip_address: Mapped[Optional[str]]

    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), db.ForeignKey("urls.id"), nullable=False
    )
    url: Mapped["Url"] = relationship("Url", back_populates="url_data")


class DatabaseAction:

    def store_url_to_db(self, original_url: str) -> str:
        """generates and stores the original and short url to db."""

        short_url = url_actions.generate_unique_url()

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

    def increment_visit_count(self, short_url: str, ip_address, device_type):
        """Increase visit count safely and return updated object."""

        url = db.session.execute(
            select(Url).where(Url.short_url == short_url)
        ).scalar_one_or_none()

        if url is None:
            return None

        # Increment visit count
        url.visit_count = (url.visit_count or 0) + 1

        # Create a new UrlData record for this visit
        new_url_data = UrlData()

        new_url_data.url_id = url.id
        new_url_data.ip_address = ip_address
        new_url_data.device_type = device_type

        db.session.add(new_url_data)

        db.session.commit()
        db.session.refresh(url)

        return url

    def get_url_data(self, short_url: str):
        """returns the data related to the url"""

        url = db.session.execute(
            select(Url).where(Url.short_url == short_url)
        ).scalar_one_or_none()

        if url is None:
            return None

        return {"url": url, "data": url.url_data}

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
