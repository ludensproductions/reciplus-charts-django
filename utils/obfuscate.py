import random
import string


def obfuscate_name(original_name: str, result_length: int = 255):
    """
    Obfuscate the name of a file. It gets the original name, and then it concatenates an underscore and random letter and numbers.
    The total lenght of the new name is 255 characters by default.

    Parameters
    ------------
        original_name: str
            he original name of the file.
        result_length: int
            The length of the new name (Including extension and the original name part).

    Return
    -----------
        new_name: str
            The new name of the file.
    """
    # Get the extension of the file
    extension = original_name.split(".")[-1]

    # Get the original name without the extension
    original_name = original_name.replace(f".{extension}", "")

    # Get the length of the original name
    length = len(f"{original_name}_.{extension}")

    # Get the length of the new name
    new_length = result_length - length

    # Generate a random string with letters and numbers
    random_string = "".join(
        random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase,
            k=new_length,
        )
    )

    # Concatenate the original name, an underscore and the random string
    new_name = f"{original_name}_{random_string}.{extension}"

    return new_name
