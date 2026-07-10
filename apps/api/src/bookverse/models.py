from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text


class Base(DeclarativeBase):
    pass


book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), primary_key=True),
    Column("author_id", UUID(as_uuid=True), primary_key=True),
)

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), primary_key=True),
    Column("genre_id", UUID(as_uuid=True), primary_key=True),
)

book_subject = Table(
    "book_subject",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), primary_key=True),
)

book_theme = Table(
    "book_theme",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), primary_key=True),
    Column("theme_id", UUID(as_uuid=True), primary_key=True),
)

book_trope = Table(
    "book_trope",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), primary_key=True),
    Column("trope_id", UUID(as_uuid=True), primary_key=True),
)


class SourceType(str, enum.Enum):
    openlibrary = "openlibrary"
    google_books = "google_books"
    internet_archive = "internet_archive"
    gutenberg = "gutenberg"
    hathitrust = "hathitrust"
    standard_ebooks = "standard_ebooks"
    loc = "loc"
    worldcat = "worldcat"
    isbndb = "isbndb"
    isfdb = "isfdb"
    wikipedia = "wikipedia"
    wikidata = "wikidata"
    internal = "internal"


class MergeOutcomeEnum(str, enum.Enum):
    created = "created"
    merged = "merged"
    replaced = "replaced"


class CanonicalBook(Base):
    __tablename__ = "canonical_book"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    source: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(255), index=True)
    source_updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    confidence: Mapped[float] = mapped_column(Float, server_default=text("0.0"))
    version: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)

    title: Mapped[str] = mapped_column(String(512), index=True)
    subtitle: Mapped[Optional[str]] = mapped_column(String(512))
    original_title: Mapped[Optional[str]] = mapped_column(String(512))
    edition: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    edition_number: Mapped[Optional[int]] = mapped_column(Integer)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer)
    original_publication_year: Mapped[Optional[int]] = mapped_column(Integer)
    language: Mapped[Optional[str]] = mapped_column(String(16), index=True)
    publisher: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(128))
    series: Mapped[Optional[str]] = mapped_column(String(255))
    series_number: Mapped[Optional[float]] = mapped_column(Float)
    volume: Mapped[Optional[str]] = mapped_column(String(50))
    classification_type: Mapped[str] = mapped_column(String(50), server_default="fiction", nullable=False)
    audience: Mapped[Optional[str]] = mapped_column(String(128))
    age_rating: Mapped[Optional[str]] = mapped_column(String(32))
    reading_level: Mapped[Optional[str]] = mapped_column(String(32))
    literary_movement: Mapped[Optional[str]] = mapped_column(String(128))
    historical_period: Mapped[Optional[str]] = mapped_column(String(128))
    setting: Mapped[Optional[str]] = mapped_column(String(255))
    locations: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(255)))

    short_summary: Mapped[Optional[str]] = mapped_column(Text)
    long_synopsis: Mapped[Optional[str]] = mapped_column(Text)
    narrative_pov: Mapped[Optional[str]] = mapped_column(String(128))
    writing_style: Mapped[Optional[str]] = mapped_column(String(128))
    tone: Mapped[Optional[str]] = mapped_column(String(128))
    mood: Mapped[Optional[str]] = mapped_column(String(128))
    pace: Mapped[Optional[str]] = mapped_column(String(128))
    complexity: Mapped[Optional[str]] = mapped_column(String(128))
    emotional_intensity: Mapped[Optional[str]] = mapped_column(String(128))
    main_characters: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    character_archetypes: Mapped[Optional[list[str]]] = mapped_column(JSONB)

    average_rating: Mapped[Optional[float]] = mapped_column(Float)
    rating_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    review_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    popularity_score: Mapped[Optional[float]] = mapped_column(Float)
    awards: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    bestseller: Mapped[Optional[bool]] = mapped_column(Boolean)
    citation_count: Mapped[Optional[int]] = mapped_column(Integer)

    embedding_text: Mapped[Optional[str]] = mapped_column(Text)
    search_tsv: Mapped[Optional[str]] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_canonical_book_source_id"),
        Index("ix_canonical_book_updated_at", "updated_at"),
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="ck_canonical_book_confidence"),
        CheckConstraint("rating_count >= 0 AND review_count >= 0", name="ck_canonical_book_counts"),
    )

    authors: Mapped[list["CanonicalAuthor"]] = relationship(secondary=book_author, back_populates="books")
    genres: Mapped[list["BookCategory"]] = relationship(secondary=book_genre, back_populates="books")
    subjects: Mapped[list["BookCategory"]] = relationship(secondary=book_subject, back_populates="books")
    themes: Mapped[list["BookCategory"]] = relationship(secondary=book_theme, back_populates="themes")
    tropes: Mapped[list["BookCategory"]] = relationship(secondary=book_trope, back_populates="tropes")
    endings: Mapped[list["EndingMetadata"] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    enrichments: Mapped[list["EnrichmentResult"] | None] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
    embeddings: Mapped[list["Embedding"] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    ratings: Mapped[list["Rating"] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    reading_list_entries: Mapped[list["ReadingListItem"] | None] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
    feeds: Mapped[list["FeedItem"] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    editions: Mapped[list["CanonicalEdition"] | None] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )


class CanonicalAuthor(Base):
    __tablename__ = "canonical_author"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    source: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(255), index=True)
    source_updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    confidence: Mapped[float] = mapped_column(Float, server_default=text("0.0"))
    version: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)

    name: Mapped[str] = mapped_column(String(255))
    sort_name: Mapped[Optional[str]] = mapped_column(String(255))
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    birth_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    death_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    nationality: Mapped[Optional[str]] = mapped_column(String(128))
    language: Mapped[Optional[str]] = mapped_column(String(16))

    identifiers: Mapped[list["AuthorIdentifier"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    books: Mapped[list["CanonicalBook"]] = relationship(secondary=book_author, back_populates="authors")


class AuthorIdentifier(Base):
    __tablename__ = "author_identifier_value"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    author_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    identifier: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[str] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(1024))

    author: Mapped[Optional[CanonicalAuthor]] = relationship(back_populates="identifiers")


class BookCategory(Base):
    __tablename__ = "book_category"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    taxonomy_type: Mapped[str] = mapped_column(String(32))


class CanonicalEdition(Base):
    __tablename__ = "canonical_edition"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    source: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(255), index=True)
    format: Mapped[Optional[str]] = mapped_column(String(64))
    pages: Mapped[Optional[int]] = mapped_column(Integer)
    isbn10: Mapped[Optional[str]] = mapped_column(String(32))
    isbn13: Mapped[Optional[str]] = mapped_column(String(32))
    identifiers: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class BookIdentifier(Base):
    __tablename__ = "book_identifier"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    identifier_type: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[str] = mapped_column(String(255), index=True)
    url: Mapped[Optional[str]] = mapped_column(String(1024))
    source: Mapped[Optional[str]] = mapped_column(String(64), index=True)
    is_canonical: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("TRUE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("identifier_type", "value", name="uq_book_identifier_type_value"),
        Index("ix_book_identifier_book_id", "book_id"),
    )


class Rating(Base):
    __tablename__ = "rating"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    rating: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("book_id", "user_id", name="uq_rating_book_user"),
        CheckConstraint("rating >= 1.0 AND rating <= 5.0", name="ck_rating_range"),
    )


class Review(Base):
    __tablename__ = "review"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    rating_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    body: Mapped[Optional[str]] = mapped_column(Text)
    spoiler: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    source: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("book_id", "user_id", name="uq_review_book_user"),
        CheckConstraint("char_length(body) <= 20000", name="ck_review_length"),
    )


class ReadingListItem(Base):
    __tablename__ = "reading_list_item"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    status: Mapped[str] = mapped_column(String(32), server_default="to_read")
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("book_id", "user_id", name="uq_reading_list_book_user"),
        CheckConstraint("status IN ('to_read','reading','finished')", name="ck_reading_status"),
    )


class EnrichmentResult(Base):
    __tablename__ = "enrichment_result"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    job_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True))
    model: Mapped[Optional[str]] = mapped_column(String(128))
    fields_enriched: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    result_metadata: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Embedding(Base):
    __tablename__ = "embedding"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    provider: Mapped[str] = mapped_column(String(64), server_default="local")
    model: Mapped[str] = mapped_column(String(128), server_default="sentence-transformers")
    vector: Mapped[Optional[list[float]]] = mapped_column(JSONB)
    dim: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("book_id", "provider", "model", name="uq_embedding_book_provider_model"),)


class EndingMetadata(Base):
    __tablename__ = "ending_metadata"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    ending_type: Mapped[str] = mapped_column(String(64), server_default="other")
    bittersweet: Mapped[Optional[bool]] = mapped_column(Boolean)
    tragic: Mapped[Optional[bool]] = mapped_column(Boolean)
    hopeful: Mapped[Optional[bool]] = mapped_column(Boolean)
    open_ended: Mapped[Optional[bool]] = mapped_column(Boolean)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class UserProfile(Base):
    __tablename__ = "user_profile"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255))
    display_name: Mapped[Optional[str]] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"))
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), unique=True, index=True)
    preferences: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class FeedItem(Base):
    __tablename__ = "feed_item"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    book_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), index=True)
    feed_type: Mapped[str] = mapped_column(String(64), index=True)
    rank_score: Mapped[Optional[float]] = mapped_column(Float)
    reason: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (UniqueConstraint("book_id", "feed_type", name="uq_feed_book_type"),)


class ConnectorRun(Base):
    __tablename__ = "connector_run"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    records_created: Mapped[Optional[int]] = mapped_column(Integer)
    records_updated: Mapped[Optional[int]] = mapped_column(Integer)
    records_skipped: Mapped[Optional[int]] = mapped_column(Integer)
    records_failed: Mapped[Optional[int]] = mapped_column(Integer)
    result_metadata: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
