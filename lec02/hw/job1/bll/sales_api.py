from lec02.hw.job1.dal.local_disk import save_to_disk
from lec02.hw.job1.dal.sales_api import get_sales
from lec02.hw.utils.file_utils import clean_directory, create_file_path, rename_file


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    clean_directory(raw_dir)

    page = 1
    total_pages = 0
    first_page_file_initial_name = f"sales_{date}.json"

    while True:
        sales_json = get_sales(date, page)
        if not sales_json:
            break

        total_pages += 1

        file_name = first_page_file_initial_name if total_pages == 1 else f"sales_{date}_{page}.json"

        save_to_disk(json_content=sales_json, dir_path=raw_dir, file_name=file_name)

        page += 1

    # rename first file to the required format in case of multiple pages
    if total_pages > 1:
        first_page_file_final_name = f"sales_{date}_1.json"

        first_page_file_initial_path = create_file_path(raw_dir, first_page_file_initial_name)
        first_page_file_final_path = create_file_path(raw_dir, first_page_file_final_name)

        rename_file(file_path_from=first_page_file_initial_path, file_path_to=first_page_file_final_path)

