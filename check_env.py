import os
import sys


def load_env_vars(file_path):
    """Loads the variables from a .env file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    # Filter comments and empty lines, and extract the keys
    vars = [line.split("=")[0].strip() for line in lines if line.strip() and not line.startswith("#")]
    return set(vars)


def check_env_files(env_file, example_file):
    env_vars = load_env_vars(env_file)
    example_vars = load_env_vars(example_file)

    # Check for differences
    if env_vars != example_vars:
        print(f"Error: {example_file} is not up to date with the variables in {env_file}")
        print("Missing variables in .env.example:", env_vars - example_vars)
        print("Additional variables in .env.example:", example_vars - env_vars)
        return False
    else:
        print(f"{example_file} is up to date.")
        return True


def main():
    root_dir = os.getcwd()
    all_up_to_date = True

    for dirpath, _, filenames in os.walk(root_dir):
        if ".env" in filenames and ".env.example" in filenames:
            env_file = os.path.join(dirpath, ".env")
            example_file = os.path.join(dirpath, ".env.example")
            if not check_env_files(env_file, example_file):
                all_up_to_date = False

    if not all_up_to_date:
        sys.exit(1)  # Fail the commit


if __name__ == "__main__":
    main()
