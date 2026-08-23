from datetime import datetime


class BaseInputAttributes:
    """Clase base para atributos de entrada de campos.

    Copia los atributos relevantes de un field_instance para uso en estrategias.
    """

    # Atributos que se copian automáticamente de field_instance
    _ATTRIBUTES_TO_COPY = [
        "page",
        "name",
        "format_list",
        "custom_value",
        "original_value",
        "generate_valid_data",
        "original_field_selector",
        "input_type",
        "filter_type",
        "field_selector",
        "field_value",
        "is_required",
        "max_length",
        "min_length",
        "min_value",
        "max_value",
        "allowed_values",
        "decimal_places",
        "num_dependencies",
        "select2_search_selector",
        "detail_format_date",
        "index_format_date",
        "date_separator",
        "detail_range_of_dates_separator",
        "index_range_of_dates_separator",
        "datetime_separator",
        "time_separator",
        "regex_pattern",
        "regex_flags",
        "field_format_date",
    ]

    def __init__(self, field_instance):
        for attr in self._ATTRIBUTES_TO_COPY:
            setattr(self, attr, getattr(field_instance, attr, None))

        self.field_instance = field_instance
        self.date_now = datetime.now()
