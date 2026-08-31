from pathlib import Path
import re


def sanitize_filename(value: str) -> str:
    """
    Make text safe for use in a Windows filename.
    """
    value = value.strip()
    value = re.sub(r'[<>:"/\\|?*]', "_", value)
    return value


def remove_spaces(value: str) -> str:
    """
    Remove spaces for cleaner output filenames.
    Example: 'Hot Dogs' -> 'HotDogs'
    """
    return value.replace(" ", "")


def process_file(
    input_file,
    output_folder,
    split_variable,
    project_name,
    mappings,
):
    """
    Split a tab-delimited file based on a record-level variable.

    Parameters
    ----------
    input_file:
        Source text file.

    output_folder:
        Folder where split files will be created.

    split_variable:
        Exact variable name to search for in column 2.
        Examples:
        Category
        O0Category
        Pipe:Category

    project_name:
        Manually entered project/buyer name for this run.

    mappings:
        Dictionary entered by the user for this run.

        Example:
        {
            "1": "Hamburgers",
            "2": "Hot Dogs",
            "3": "Frozen Pizza"
        }

    File assumptions
    ----------------
    Column 1 = Record
    Column 2 = Value
    Column 3 = ValueNumber

    Rows belonging to the same record must appear together.
    """

    input_path = Path(input_file)
    output_path = Path(output_folder)

    output_path.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    if not split_variable.strip():
        raise ValueError(
            "Split variable cannot be blank."
        )

    if not project_name.strip():
        raise ValueError(
            "Project name cannot be blank."
        )

    open_files = {}

    stats = {
        "records_processed": 0,
        "records_written": 0,
        "records_unmapped": 0,
        "records_missing_assignment": 0,
        "output_files": set(),
    }

    current_record = None
    record_lines = []
    assignment_value = None

    def write_record(lines, assignment):
        if not lines:
            return

        stats["records_processed"] += 1

        if assignment is None:
            stats["records_missing_assignment"] += 1
            return

        assignment = assignment.strip()

        if assignment not in mappings:
            stats["records_unmapped"] += 1
            return

        category_name = mappings[assignment]

        safe_project = sanitize_filename(project_name)
        safe_category = sanitize_filename(category_name)

        safe_project = remove_spaces(safe_project)
        safe_category = remove_spaces(safe_category)

        filename = (
            f"{safe_project}{safe_category}.txt"
        )

        destination = output_path / filename

        if destination not in open_files:
            open_files[destination] = destination.open(
                "a",
                encoding="utf-8",
                newline=""
            )

        output_handle = open_files[destination]

        for original_line in lines:
            output_handle.write(original_line)

        stats["records_written"] += 1
        stats["output_files"].add(
            str(destination)
        )

    try:

        with input_path.open(
            "r",
            encoding="utf-8",
            newline=""
        ) as source:

            for line_number, original_line in enumerate(
                source,
                start=1
            ):

                stripped = original_line.rstrip(
                    "\r\n"
                )

                if not stripped:
                    continue

                columns = stripped.split("\t")

                if len(columns) < 3:
                    raise ValueError(
                        f"Line {line_number} does not "
                        "have at least 3 tab-delimited columns."
                    )

                record = columns[0].strip()
                value = columns[1].strip()
                value_number = columns[2].strip()

                if current_record is None:
                    current_record = record

                if record != current_record:

                    write_record(
                        record_lines,
                        assignment_value
                    )

                    current_record = record
                    record_lines = []
                    assignment_value = None

                record_lines.append(
                    original_line
                )

                if value == split_variable:
                    assignment_value = value_number

            write_record(
                record_lines,
                assignment_value
            )

    finally:

        for handle in open_files.values():
            handle.close()

    stats["output_files"] = sorted(
        stats["output_files"]
    )

    return stats
