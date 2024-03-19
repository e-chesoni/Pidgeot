import logging
import numpy as np

# Log Levels
# NOTSET    = 0
# Debug     = 10
# INFO      = 20
# WARNING   = 30
# ERROR     = 40
# CRITICAL  = 50

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler("debug.log"),
                        logging.StreamHandler()
                    ])

def print_info_table(info_dict, title="INFORMATION"):
    """
    Prints a table of information based on a dictionary input, handling None values and lists differently.

    Parameters:
    - info_dict: A dictionary where keys are property names (as strings) and values are the corresponding values.
    - title: A string for the title of the table.
    """
    if not info_dict:
        logging.info("No information to display.")
        return

    # Calculate the maximum width for the property column based on the longest key
    max_key_length = max(len(key) for key in info_dict.keys())
    property_width = max(max_key_length, len("Property")) + 5  # Add some padding
    value_width = 25  # Adjusted to potentially accommodate longer list representations

    header = f"{'Property':<{property_width}} | {'Value':<{value_width}}"
    divider = "-" * (property_width + value_width + 3)  # 3 for " | " separator and extra space

    logging.info(title)
    logging.info(divider)
    logging.info(header)
    logging.info(divider)

    for key, value in info_dict.items():
        # Check if value is None and replace it with the string "None"
        if value is None:
            display_value = "None"
        elif isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) > 3:
                display_value = f"[{value[0]}, ..., {value[-1]}]"  # Show start and end for long lists
            else:
                display_value = str(value)  # Convert short lists directly to string
        else:
            display_value = value
        logging.info(f"{key:<{property_width}} | {display_value:<{value_width}}")
    
    print("\n")