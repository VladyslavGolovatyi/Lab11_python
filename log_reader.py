import zipfile
from datetime import datetime
import re


def read_zip_file(file_path: str) -> list[str]:
    if not file_path.endswith(".zip"):
        raise ValueError("Consider using zip archive in file_path")

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("resources/")

    with open(file_path.strip(".zip")) as file:
        lines = [line for line in file]

    return lines


def get_quantity_of_requests(file_path: str, start_datetime: str, end_datetime: str,
                             file_type: str, status_code_range: str) -> None:
    start = datetime.strptime(start_datetime, "%d/%b/%Y:%H:%M:%S")
    end = datetime.strptime(end_datetime, "%d/%b/%Y:%H:%M:%S")

    file_type_match = re.match("\.\w+", file_type)
    if not file_type_match:
        raise ValueError(f"File type '{file_type}' is not correct. Example: '.php' You may have missed the dot.")

    status_code_range_match = re.match("\d{3}-\d{3}", status_code_range)
    if not status_code_range_match:
        raise ValueError(f"Status code range '{status_code_range}' is not correct. "
                         f"Example: '300-399' Check your parameter and try again")

    log_lines = read_zip_file(file_path)

    status_code_range_start = int(status_code_range.split("-")[0])
    status_code_range_end = int(status_code_range.split("-")[1]) + 1

    counter = 0
    for line in log_lines:
        datetime_match = (re.search("\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2}", line).group(0))
        time_formatted = datetime.strptime(datetime_match, '%d/%b/%Y:%H:%M:%S')

        status_code_match = (re.search("\s\d{3}\s", line)).group(0).strip()

        if start <= time_formatted <= end \
                and int(status_code_match) in range(status_code_range_start, status_code_range_end) \
                and ".php" in line:
            counter += 1

    output = f"""
In period from {start_datetime} to {end_datetime} there were {counter} requests
which involved obtaining {file_type} files with status code in range {status_code_range}
    """

    print(output)
