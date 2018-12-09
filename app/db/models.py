"""Connects to database and setups table."""
from peewee import (
    Model,
    CharField,
    IntegerField,
    UUIDField,
    PostgresqlDatabase
)

db = PostgresqlDatabase("penguin_db", port=5433)


class ImageClick(Model):
    """Represent a click on an image."""

    user_name = CharField()
    subject_zooniverse_id = CharField()
    lunar_phase = CharField()
    original_size_x = CharField()
    original_size_y = CharField()
    path = CharField()
    temperature_f = CharField()
    tmstamp = CharField()
    animals_present = CharField()
    all_marked = CharField()
    mark_order = CharField()
    value = CharField()
    x = CharField()
    y = CharField()

    class Meta:
        """Provides peewee config."""

        database = db
        table_name = "TBL_IMAGE_CLICK"


class RowAccuracy(Model):
    """Represent result of algorithm."""

    run_id = UUIDField()
    image = CharField()
    algorithm = CharField()
    number_of_clusters = IntegerField()
    expected_number_of_clusters = IntegerField()

    class Meta:
        """Provides peewee config."""

        database = db
        table_name = "TBL_ROW_ACCURACY"


def create_tables():
    """Create database tables."""
    db.create_tables([ImageClick, RowAccuracy])
