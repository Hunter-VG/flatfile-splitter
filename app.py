import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from processor import process_file


class RecordSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Splitter")
        self.root.geometry("760x620")

        self.mapping_rows = []

        self.build_interface()

    def build_interface(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Input file
        ttk.Label(
            main_frame,
            text="Input File"
        ).grid(row=0, column=0, sticky="w")

        self.input_file_var = tk.StringVar()

        ttk.Entry(
            main_frame,
            textvariable=self.input_file_var,
            width=65
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        ttk.Button(
            main_frame,
            text="Browse",
            command=self.select_input_file
        ).grid(row=1, column=1)

        # Output folder
        ttk.Label(
            main_frame,
            text="Output Folder"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(15, 0)
        )

        self.output_folder_var = tk.StringVar()

        ttk.Entry(
            main_frame,
            textvariable=self.output_folder_var,
            width=65
        ).grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        ttk.Button(
            main_frame,
            text="Browse",
            command=self.select_output_folder
        ).grid(row=3, column=1)

        # Project name
        ttk.Label(
            main_frame,
            text="Project / Buyer Name"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(15, 0)
        )

        self.project_name_var = tk.StringVar()

        ttk.Entry(
            main_frame,
            textvariable=self.project_name_var,
            width=40
        ).grid(
            row=5,
            column=0,
            sticky="w"
        )

        # Split variable
        ttk.Label(
            main_frame,
            text="Split Variable"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(15, 0)
        )

        self.split_variable_var = tk.StringVar()

        ttk.Entry(
            main_frame,
            textvariable=self.split_variable_var,
            width=40
        ).grid(
            row=7,
            column=0,
            sticky="w"
        )

        ttk.Label(
            main_frame,
            text="Example: Category, O0Category, Pipe:Category"
        ).grid(
            row=8,
            column=0,
            sticky="w"
        )

        # Mapping section
        ttk.Separator(
            main_frame,
            orient="horizontal"
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=20
        )

        ttk.Label(
            main_frame,
            text="Output Mapping"
        ).grid(
            row=10,
            column=0,
            sticky="w"
        )

        ttk.Label(
            main_frame,
            text="Value"
        ).grid(
            row=11,
            column=0,
            sticky="w"
        )

        ttk.Label(
            main_frame,
            text="Output Category Name"
        ).grid(
            row=11,
            column=0,
            sticky="w",
            padx=(120, 0)
        )

        self.mapping_frame = ttk.Frame(main_frame)

        self.mapping_frame.grid(
            row=12,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        # Start with 3 mapping rows
        for _ in range(3):
            self.add_mapping_row()

        ttk.Button(
            main_frame,
            text="+ Add Mapping",
            command=self.add_mapping_row
        ).grid(
            row=13,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

        # Process button
        ttk.Separator(
            main_frame,
            orient="horizontal"
        ).grid(
            row=14,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=20
        )

        ttk.Button(
            main_frame,
            text="Process File",
            command=self.run_processing
        ).grid(
            row=15,
            column=0,
            sticky="w"
        )

        self.status_var = tk.StringVar(
            value="Ready"
        )

        ttk.Label(
            main_frame,
            textvariable=self.status_var
        ).grid(
            row=16,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(15, 0)
        )

        main_frame.columnconfigure(
            0,
            weight=1
        )

    def select_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("Text files", "*.txt"),
                ("TSV files", "*.tsv"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.input_file_var.set(filename)

    def select_output_folder(self):
        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:
            self.output_folder_var.set(folder)

    def add_mapping_row(self):
        row_number = len(self.mapping_rows)

        value_var = tk.StringVar()
        category_var = tk.StringVar()

        value_entry = ttk.Entry(
            self.mapping_frame,
            textvariable=value_var,
            width=15
        )

        value_entry.grid(
            row=row_number,
            column=0,
            padx=(0, 10),
            pady=3
        )

        category_entry = ttk.Entry(
            self.mapping_frame,
            textvariable=category_var,
            width=35
        )

        category_entry.grid(
            row=row_number,
            column=1,
            padx=(0, 10),
            pady=3
        )

        remove_button = ttk.Button(
            self.mapping_frame,
            text="Remove",
            command=lambda: self.remove_mapping_row(
                value_entry,
                category_entry,
                remove_button,
                value_var,
                category_var
            )
        )

        remove_button.grid(
            row=row_number,
            column=2,
            pady=3
        )

        self.mapping_rows.append(
            {
                "value": value_var,
                "category": category_var,
                "widgets": [
                    value_entry,
                    category_entry,
                    remove_button
                ]
            }
        )

    def remove_mapping_row(
        self,
        value_entry,
        category_entry,
        remove_button,
        value_var,
        category_var
    ):
        for row in self.mapping_rows:
            if row["value"] == value_var:
                self.mapping_rows.remove(row)
                break

        value_entry.destroy()
        category_entry.destroy()
        remove_button.destroy()

    def run_processing(self):
        input_file = self.input_file_var.get().strip()
        output_folder = self.output_folder_var.get().strip()
        project_name = self.project_name_var.get().strip()
        split_variable = self.split_variable_var.get().strip()

        if not input_file:
            messagebox.showerror(
                "Missing Input",
                "Please select an input file."
            )
            return

        if not output_folder:
            messagebox.showerror(
                "Missing Output",
                "Please select an output folder."
            )
            return

        if not project_name:
            messagebox.showerror(
                "Missing Project",
                "Please enter a project or buyer name."
            )
            return

        if not split_variable:
            messagebox.showerror(
                "Missing Split Variable",
                "Please enter the split variable."
            )
            return

        mappings = {}

        for row in self.mapping_rows:
            value = row["value"].get().strip()
            category = row["category"].get().strip()

            if value and category:
                mappings[value] = category

        if not mappings:
            messagebox.showerror(
                "Missing Mapping",
                "Please enter at least one value mapping."
            )
            return

        try:
            self.status_var.set(
                "Processing..."
            )

            self.root.update_idletasks()

            stats = process_file(
                input_file=input_file,
                output_folder=output_folder,
                split_variable=split_variable,
                project_name=project_name,
                mappings=mappings
            )

            result = (
                f"Processing Complete\n\n"
                f"Records processed: "
                f"{stats['records_processed']:,}\n"
                f"Records written: "
                f"{stats['records_written']:,}\n"
                f"Unmapped records: "
                f"{stats['records_unmapped']:,}\n"
                f"Missing assignment: "
                f"{stats['records_missing_assignment']:,}\n"
                f"Output files created: "
                f"{len(stats['output_files'])}"
            )

            self.status_var.set(
                "Processing complete."
            )

            messagebox.showinfo(
                "Complete",
                result
            )

        except Exception as error:
            self.status_var.set(
                "Processing failed."
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = RecordSplitterApp(root)
    root.mainloop()
