import os

def get_env_var(name, default=None):
    return os.getenv(name, default)

def get_config_file_value(filename, file_path_env):
    home_directory = get_env_var(file_path_env)
    if home_directory is None:
        print(f"{file_path_env} environment variable not set.")
        return "File NOT FOUND"
    file_path = os.path.join(home_directory, filename)
    err = ""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError as exp:
        err = "Error: file not found"
        print(f"{err} {exp}")
        return err
    except Exception as exp:
        err = "Error: Other error while file read"
        print(f"{err} {exp}")
        return err
    return ""

if __name__ == "__main__":
    print(get_config_file_value("test.txt", "TEMP_PATH"))
