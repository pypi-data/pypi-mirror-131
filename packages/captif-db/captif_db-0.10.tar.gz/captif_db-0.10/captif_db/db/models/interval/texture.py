"""
The texture profile models are used to describe the texture profiler instruments and
associated measurements.
"""

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from ..base import Table, Base


__all__ = [
    "TextureProfilerType",
    "TextureProfiler",
    "TextureProfilerVersion",
]


class TextureProfilerType(Table, Base):
    """
    Texture profiler type.

    :param texture_profiler_type: type of texture profiler (e.g. stationary laser
        profiler) (required)

    :relationships: - texture_profiler_obj (viewonly)

    """

    __tablename__ = "texture_profiler_type"
    __index_column__ = "texture_profiler_type"

    texture_profiler_type = Column(String(50), primary_key=True)

    # Relationships:
    texture_profiler_obj = relationship(
        "TextureProfiler",
        back_populates="texture_profiler_type_obj",
        lazy=True,
        viewonly=True,
    )

    __table_args__ = (
        {"info": {"er_tags": ["readings", "interval", "texture_profiler"]}},
    )


class TextureProfiler(Table, Base):
    """
    Texture profiler instrument details.

    :param name: texture profiler instrument name (e.g. CAPTIF SLP) (required)
    :param texture_profiler_type: type of texture profiler (required)

    :relationships: - texture_profiler_type_obj
                    - texture_profiler_version_obj (viewonly)

    """

    __tablename__ = "texture_profiler"
    __index_column__ = "name"

    name = Column(String(50), primary_key=True)
    texture_profiler_type = Column(String(50), nullable=False)

    # Relationships:
    texture_profiler_type_obj = relationship(
        "TextureProfilerType", back_populates="texture_profiler_obj", lazy=True
    )
    texture_profiler_version_obj = relationship(
        "TextureProfilerVersion",
        back_populates="texture_profiler_obj",
        lazy=True,
        viewonly=True,
    )

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["texture_profiler_type"],
            ["texture_profiler_type.texture_profiler_type"],
        ),
        {"info": {"er_tags": ["readings", "interval", "texture_profiler"]}},
    )


class TextureProfilerVersion(Table, Base):
    """
    Texture profiler instrument version details.

    Used to track changes to the instrument following identification of faults or general
    improvements.

    :param texture_profiler_name: texture profiler instrument name (required)
    :param version_no: version number (required)
    :param version_details: details of changes from the previous version (required)
    :param version_notes: additional notes

    :relationships: - texture_profiler_obj

    """

    __tablename__ = "texture_profiler_version"
    __index_column__ = ["texture_profiler_name", "version_no"]

    texture_profiler_name = Column(String(50), primary_key=True)
    version_no = Column(Integer, primary_key=True)
    version_details = Column(String(100), nullable=False)
    version_notes = Column(String(200))

    # Relationships:
    texture_profiler_obj = relationship(
        "TextureProfiler", back_populates="texture_profiler_version_obj", lazy=True
    )

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["texture_profiler_name"],
            ["texture_profiler.name"],
            onupdate="CASCADE",
        ),
        {"info": {"er_tags": ["readings", "interval", "texture_profiler"]}},
    )
