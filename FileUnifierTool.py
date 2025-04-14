import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading


def search_file_foler(folder, extensions):
    results = []
    for current_folder, _, files in os.walk(folder):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in extensions):
                results.append(os.path.join(current_folder, file))
    return results


def merge_files_into_one(results, merged_file, progress_var, status_label):
    total = len(results)
    unified_text = ""

    for i, risultato in enumerate(results):
        nome_file = os.path.basename(risultato)
        unified_text += f"\n\n# Start of file: {nome_file}\n\n"
        with open(risultato, 'r', encoding='utf-8', errors='ignore') as file_input:
            unified_text += file_input.read()

        progress = int((i + 1) / total * 100)
        progress_var.set(progress)
        status_label.config(text=f"Merging file {i + 1} of {total}: {nome_file}")

    with open(merged_file, 'w', encoding='utf-8') as file_output:
        file_output.write(unified_text)

    return unified_text


def perform_file_merge(entry_folder, checkboxes_extensions, text_widget, merge_button, progress_var, status_label,
                       mode_var):
    merge_button.configure(state='disabled')
    progress_var.set(0)
    status_label.config(text="Starting merge...")

    selected_input = entry_folder.get()
    extensions_selezionate = [ext for ext, var in checkboxes_extensions if var.get() == 1]

    if not selected_input:
        status_label.config(text="No input selected.")
        merge_button.configure(state='normal')
        return
    if not extensions_selezionate:
        status_label.config(text="No extensions selected.")
        merge_button.configure(state='normal')
        return

    folder_output = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
    if not folder_output:
        status_label.config(text="Operation cancelled.")
        merge_button.configure(state='normal')
        return

    results = []
    if mode_var.get() == "folder":
        results = search_file_foler(selected_input, extensions_selezionate)
    else:  # file mode
        candidate_files = selected_input.split(";")
        results = [f for f in candidate_files if any(f.lower().endswith(ext.lower()) for ext in extensions_selezionate)]

    if results:
        unified_text = merge_files_into_one(results, folder_output, progress_var, status_label)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, unified_text)
        status_label.config(text=f"Merged {len(results)} files into {os.path.basename(folder_output)}.")
    else:
        status_label.config(text="No matching files found.")

    merge_button.configure(state='normal')


def browse_input(entry_folder, mode_var):
    if mode_var.get() == "folder":
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, selected_folder)
    else:
        selected_files = filedialog.askopenfilenames(title="Select files", filetypes=[("All files", "*.*")])
        if selected_files:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, ";".join(selected_files))


def start_union_process(entry_folder, checkboxes_extensions, text_widget, merge_button, progress_var, status_label,
                        mode_var):
    thread = threading.Thread(
        target=perform_file_merge,
        args=(entry_folder, checkboxes_extensions, text_widget, merge_button, progress_var, status_label, mode_var)
    )
    thread.start()


def main():
    root = tk.Tk()
    root.title("File Merge Tool")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    mode_var = tk.StringVar(value="folder")

    tk.Label(frame, text="Input type:").grid(row=0, column=0, sticky="w")
    tk.Radiobutton(frame, text="Folder", variable=mode_var, value="folder").grid(row=0, column=1, sticky="w")
    tk.Radiobutton(frame, text="Files", variable=mode_var, value="files").grid(row=0, column=2, sticky="w")

    label_input = tk.Label(frame, text="Input:")
    label_input.grid(row=1, column=0, sticky="w")

    entry_folder = tk.Entry(frame, width=50)
    entry_folder.grid(row=1, column=1, padx=5, pady=5)

    button_browse = tk.Button(frame, text="Browse", command=lambda: browse_input(entry_folder, mode_var))
    button_browse.grid(row=1, column=2, padx=5, pady=5)

    label_extensions = tk.Label(frame, text="     Extensions:")
    label_extensions.grid(row=2, column=0, sticky="w")

    available_extensions = [".py", ".java", ".txt", ".cpp", ".html", ".css", ".js", ".json", ".scala", ".ts", ".c",
                            ".mat", ".h", ".cs", ".gms", ".jsx"]
    checkboxes_extensions = []
    for i, ext in enumerate(available_extensions):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(frame, text=ext, variable=var)
        checkbox.grid(row=i // 2 + 2, column=i % 2 + 1, sticky="w", padx=(0, 2), pady=2)
        checkboxes_extensions.append((ext, var))

    row_offset = len(available_extensions) // 2 + 3

    progress_var = tk.IntVar()
    progress_bar = tk.Scale(frame, variable=progress_var, from_=0, to=100, orient='horizontal', length=400,
                            label="Progress")
    progress_bar.grid(row=row_offset, column=0, columnspan=3, pady=(10, 5))

    status_label = tk.Label(frame, text="Select input and extensions to begin.", anchor="w")
    status_label.grid(row=row_offset + 1, column=0, columnspan=3, sticky="w", padx=5)

    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
    text_widget.grid(row=row_offset + 2, column=0, columnspan=3, padx=5, pady=5)

    merge_button = tk.Button(
        frame,
        text="Merge files",
        command=lambda: start_union_process(entry_folder, checkboxes_extensions, text_widget, merge_button,
                                            progress_var, status_label, mode_var)
    )
    merge_button.grid(row=row_offset + 3, column=0, columnspan=3, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
