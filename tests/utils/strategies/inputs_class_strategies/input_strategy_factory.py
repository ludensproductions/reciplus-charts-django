from tests.pages.core.constants import HtmlTagEnum, InputType

from .input_fill_strategies import (
    ButtonStrategy,
    CheckboxStrategy,
    FileStrategy,
    InputStrategy,
    MultipleFilesStrategy,
    RadioStrategy,
    Select2Strategy,
    SelectStrategy,
    TextInputStrategy,
    WYSIWYGStrategy,
)


class StrategyFactory:
    """Factory that returns the correct input filling strategy based on DOM characteristics.

    Resolution order:
        1. Direct strategy match by input_type
        2. SELECT tag (native select, not Select2)
        3. DIV tag -> Select2, WYSIWYG, or MULTIPLE_FILES
        4. INPUT/TEXTAREA tags -> text or multiple files
        5. SPAN tag -> Select2
    """

    def __init__(self) -> None:
        self._strategies = {
            "file": FileStrategy(),
            "multiple_files": MultipleFilesStrategy(),
            "radio": RadioStrategy(),
            "checkbox": CheckboxStrategy(),
            "button": ButtonStrategy(),
            "select": SelectStrategy(),
            "text": TextInputStrategy(),
            "select2": Select2Strategy(),
            "wysiwyg": WYSIWYGStrategy(),
        }

    def get_strategy(
        self,
        input_type: str,
        tag_name: str,
        idselect2: bool = False,
        has_contenteditable: bool = False,
        has_multiple_attr: bool = False,
    ) -> InputStrategy:
        """Return the best matching strategy for the given DOM characteristics.

        Args:
            input_type: The type attribute of the input element (from el.type).
            tag_name: The HTML tag name (INPUT, SELECT, DIV, etc.).
            idselect2: Whether the element has data-select2-id attribute.
            has_contenteditable: Whether the element contains a contenteditable div (WYSIWYG).
            has_multiple_attr: Whether the file input has multiple attribute.

        Returns:
            InputStrategy: The appropriate strategy for filling the input.

        Raises:
            ValueError: If no matching strategy is found.
        """
        if input_type in self._strategies:
            return self._strategies[input_type]

        if tag_name == HtmlTagEnum.SELECT.value and not idselect2:
            return self._strategies["select"]

        if tag_name == HtmlTagEnum.DIV.value:
            return self._resolve_div_strategy(input_type, idselect2, has_contenteditable)

        if tag_name in (HtmlTagEnum.INPUT.value, HtmlTagEnum.TEXTAREA.value):
            if has_multiple_attr and input_type == "file":
                return self._strategies["multiple_files"]
            if input_type in ("datetime-local", "date", "time"):
                return self._strategies["text"]
            return self._strategies["text"]

        if tag_name == HtmlTagEnum.SPAN.value:
            return self._strategies["select2"]

        raise ValueError(f"No strategy found for input type: {input_type} and tag name: {tag_name}")

    def _resolve_div_strategy(
        self,
        input_type: str,
        idselect2: bool,
        has_contenteditable: bool,
        has_multiple_attr: bool = False,
    ) -> InputStrategy:
        """Resolve strategy for DIV elements.

        DIV elements can be:
        - Select2 dropdowns (data-select2-id attribute)
        - WYSIWYG editors (contains contenteditable div)
        - Multiple file inputs (wrapper div containing input[multiple][type=file])

        Priority: WYSIWYG > multiple_files > Select2
        """
        if has_contenteditable:
            return self._strategies["wysiwyg"]

        if has_multiple_attr:
            return self._strategies["multiple_files"]

        if self._is_select2(input_type, idselect2):
            return self._strategies["select2"]

        return self._strategies["text"]

    def _is_select2(self, input_type: str, idselect2: bool) -> bool:
        """Check if the element is a Select2 component."""
        return input_type in (InputType.SELECT2.value, InputType.SELECT2_MULTIPLE.value) or idselect2
