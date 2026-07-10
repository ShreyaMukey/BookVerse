from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
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


# Many-to-many association tables live here so mapper config has them.
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("canonical_book.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", UUID(as_uuid=True), ForeignKey("canonical_author.id", ondelete="CASCADE"), primary_key=True),
)

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("canonical_book.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", UUID(as_uuid=True), ForeignKey("book_category.id", ondelete="CASCADE"), primary_key=True),
)

book_subject = Table(
    "book_subject",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("canonical_book.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("book_category.id", ondelete="CASCADE"), primary_key=True),
)

book_theme = Table(
    "book_theme",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("canonical_book.id", ondelete="CASCADE"), primary_key=True),
    Column("theme_id", UUID(as_uuid=True), ForeignKey("book_category.id", ondelete="CASCADE"), primary_key=True),
)

book_trope = Table(
    "book_trope",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("canonical_book.id", ondelete="CASCADE"), primary_key=True),
    Column("trope_id", UUID(as_uuid=True), ForeignKey("book_category.id", ondelete="CASCADE"), primary_key=True),
)

author_identifier = Table(
    "author_identifier",
    Base.metadata,
    Column("author_id", UUID(as_uuid=True), ForeignKey("canonical_author.id", ondelete="CASCADE"), primary_key=True),
    Column("identifier_id", UUID(as_uuid=True), ForeignKey("author_identifier_value.id", ondelete="CASCADE"), primary_key=True),
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


class Book(Base):
    __tablename__ = "canonical_book"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    source: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(255), index=True)
    source_updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    confidence: Mapped[float] = mapped_column(Float, server_default=text("0.0"))
    version: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)

    # Identification
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

    # Classification
    classification_type: Mapped[str] = mapped_column(String(50), server_default="fiction", nullable=False)
    audience: Mapped[Optional[str]] = mapped_column(String(128))
    age_rating: Mapped[Optional[str]] = mapped_column(String(32))
    reading_level: Mapped[Optional[str]] = mapped_column(String(32))
    literary_movement: Mapped[Optional[str]] = mapped_column(String(128))
    historical_period: Mapped[Optional[str]] = mapped_column(String(128))
    setting: Mapped[Optional[str]] = mapped_column(String(255))
    locations: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(255)))

    # Story metadata
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

    # Popularity
    average_rating: Mapped[Optional[float]] = mapped_column(Float)
    rating_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    review_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    popularity_score: Mapped[Optional[float]] = mapped_column(Numeric(12, 3))
    awards: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    bestseller: Mapped[Optional[bool]] = mapped_column(Boolean)
    citation_count: Mapped[Optional[int]] = mapped_column(Integer)

    # Technical search fields
    embedding_text: Mapped[Optional[str]] = mapped_column(Text)
    search_tsv: Mapped[Optional[str]] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_canonical_book_source_id"),
        Index("ix_canonical_book_updated_at", "updated_at"),
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="ck_canonical_book_confidence"),
        CheckConstraint("rating_count >= 0 AND review_count >= 0", name="ck_canonical_book_counts"),
    )

    versions: Mapped[list[BookVersion]] = relationship(back_populates="book", cascade="all, delete-orphan")
    identifiers: Mapped[list[BookIdentifier]] = relationship(back_populates="book", cascade="all, delete-orphan")
    authors: Mapped[list[CanonicalAuthor]] = relationship(secondary=book_author, back_populates="books")
    people: Mapped[list[BookPerson]] = relationship(back_populates="book", cascade="all, delete-orphan")
    genres: Mapped[list[BookCategory]] = relationship(secondary=book_genre, back_populates="books")
    subjects: Mapped[list[BookCategory]] = relationship(secondary=book_subject, back_populates="books")
    themes: Mapped[list[BookCategory]] = relationship(secondary=book_theme, back_populates="books")
    tropes: Mapped[list[BookCategory]] = relationship(secondary=book_trope, back_populates="books")
    endings: Mapped[list[EndingMetadata] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    enrichments: Mapped[list[EnrichmentResult] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    embeddings: Mapped[list[Embedding] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    ratings: Mapped[list[Rating] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    reviews: Mapped[list[Review] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    reading_list_entries: Mapped[list[ReadingListItem] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    feeds: Mapped[list[FeedItem] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
    editions: Mapped[list[CanonicalEdition] | None] = relationship(back_populates="book", cascade="all, delete-orphan")
