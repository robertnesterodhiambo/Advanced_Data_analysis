import json
import os
import math

def split_notebook_chain(input_file, parts=8):
    # Load notebook JSON
    with open(input_file, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    cells = notebook["cells"]
    total_cells = len(cells)
    chunk_size = math.ceil(total_cells / parts)

    base_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    for i in range(parts):
        start = i * chunk_size
        end = min((i+1) * chunk_size, total_cells)

        nb_copy = dict(notebook)
        nb_copy["cells"] = []

        # Add chain header cell
        header_cell = {
            "cell_type": "code",
            "metadata": {},
            "source": []
        }

        # Include %run for all previous parts
        for j in range(i):
            prev_name = f"{base_name}_part{j+1}.ipynb"
            header_cell["source"].append(f"%run {prev_name}\n")

        if header_cell["source"]:  # only add if there are dependencies
            nb_copy["cells"].append(header_cell)

        # Add chunk cells
        nb_copy["cells"].extend(cells[start:end])

        # Save mini notebook
        part_filename = os.path.join(base_dir, f"{base_name}_part{i+1}.ipynb")
        with open(part_filename, "w", encoding="utf-8") as f:
            json.dump(nb_copy, f, indent=2)

    print(f"✅ Created {parts} chained mini notebooks for {input_file}")

# Example usage
split_notebook_chain("2025Analysis.ipynb", parts=8)
