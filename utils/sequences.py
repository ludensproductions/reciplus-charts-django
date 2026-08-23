"""Utilities for database-backed sequence generation."""

from datetime import datetime, timezone

from django.db import connection

SEQUENCES_DICT = {
    "sale_sequence": {
        "format": "SALE{date}{current_sequence}",
        "date": True,
        # zfill apply 7
        "current_sequence_length": 7,
    },
    "event_folio_sequence": {
        "format": "EVENTFOLIO{date}{current_sequence}",
        "date": True,
        "current_sequence_length": 5,
    },
}


def create_sequences(sequences):
    """Create database sequences for the given sequence names.

    Args:
        sequences: Iterable of sequence keys defined in `SEQUENCES_DICT`.
    """
    with connection.cursor() as cursor:
        for sequence in sequences:
            has_date = SEQUENCES_DICT[sequence]["date"]
            if has_date:
                date = datetime.now(timezone.utc)
                date_str = date.strftime("%YYYYMMDD")

            current_sequence = f"{sequence}_{date_str}" if has_date else f"{sequence}"
            cursor.execute(f"CREATE SEQUENCE IF NOT EXISTS {current_sequence}")


def get_sequence(sequence_name):
    """Get the next formatted sequence value.

    Args:
        sequence_name: Sequence key defined in `SEQUENCES_DICT`.

    Returns:
        str: Formatted sequence value for the provided key.
    """
    date = datetime.now(timezone.utc)
    date_str = date.strftime("%YYYYMMDD")

    with connection.cursor() as cursor:
        has_date = SEQUENCES_DICT[sequence_name]["date"]
        sequence = f"{sequence_name}_{date_str}" if has_date else f"{sequence_name}"
        cursor.execute(f"""SELECT nextval('{sequence}')""")
        current_sequence_id = cursor.fetchone()[0]
        return get_format_sequence(sequence_name, current_sequence_id)


def get_format_sequence(sequence_name, current_sequence_id):
    """Format a sequence value using the configured pattern.

    Args:
        sequence_name: Sequence key defined in `SEQUENCES_DICT`.
        current_sequence_id: Current numeric value from the sequence.

    Returns:
        str: Formatted sequence value.
    """
    date = datetime.now(timezone.utc)
    date_str = str(date.strftime("%m%d%Y"))
    format_sequence = SEQUENCES_DICT[sequence_name]["format"]
    length = SEQUENCES_DICT[sequence_name]["current_sequence_length"]
    sequence_format = str(current_sequence_id).zfill(length)
    return format_sequence.format(date=date_str, current_sequence=sequence_format)
