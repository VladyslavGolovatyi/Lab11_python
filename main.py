from log_reader import get_quantity_of_requests


def main():
    get_quantity_of_requests(
        file_path="resources/access.log.zip",
        start_datetime="23/Mar/2009:02:00:03",
        end_datetime="23/Mar/2009:05:55:02",
        file_type=".php",
        status_code_range="300-399"
    )


if __name__ == '__main__':
    main()
