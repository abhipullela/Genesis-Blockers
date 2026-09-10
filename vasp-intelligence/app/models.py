from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VASP(Base):
    __tablename__ = "vasps"

    vasp_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    supported_chains: Mapped[str] = mapped_column(Text, nullable=False)


class Source(Base):
    __tablename__ = "sources"

    source_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


class VASPAddress(Base):
    __tablename__ = "vasp_addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(42), nullable=False)
    chain: Mapped[str] = mapped_column(String(30), nullable=False)
    vasp_id: Mapped[str] = mapped_column(
        ForeignKey("vasps.vasp_id"),
        nullable=False,
    )
    address_type: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    source_id: Mapped[str] = mapped_column(
        ForeignKey("sources.source_id"),
        nullable=False,
    )
    last_verified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="confidence_range",
        ),
    )