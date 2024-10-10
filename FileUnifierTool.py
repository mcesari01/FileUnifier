import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading

def search_file_foler(folder, extensions):
    results = []
    for current_folder, _, files in os.walk(folder):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                results.append(os.path.join(current_folder, file))
    return results

def merge_files_into_one(results, merged_file):
    unified_text = ""
    for risultato in results:
        nome_file = os.path.basename(risultato)
        unified_text += f"\n\n# Start of file: {nome_file}\n\n"
        with open(risultato, 'r', encoding='utf-8', errors='ignore') as file_input:
            unified_text += file_input.read()

    with open(merged_file, 'w') as file_output:
        file_output.write(unified_text)

    return unified_text

def perform_file_merge(entry_folder, checkboxes_extensions, text_widget, merge_button):
    merge_button.configure(state='disabled')
    
    folder_input = entry_folder.get()
    extensions_selezionate = [ext for ext, var in checkboxes_extensions if var.get() == 1]

    folder_output = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TextFile", "*.txt")])
    if not folder_output:
        print("Operation cancelled.")
        merge_button.configure(state='normal')
        return

    extensions_file = extensions_selezionate
    results = search_file_foler(folder_input, extensions_file)

    if results:
        unified_text = merge_files_into_one(results, folder_output)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, unified_text)
        print(f"The files have been successfully merged into {folder_output}")
    else:
        print("No files found with the specified extensions.")

    merge_button.configure(state='normal')

def browse_folder(entry_folder):
    selected_folder = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, selected_folder)

def start_union_process(entry_folder, checkboxes_extensions, text_widget, merge_button):
    thread = threading.Thread(target=perform_file_merge, args=(entry_folder, checkboxes_extensions, text_widget, merge_button))
    thread.start()

def main():
    root = tk.Tk()
    root.title("File Merge Tool")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label_folder = tk.Label(frame, text="Folder:")
    label_folder.grid(row=0, column=0, sticky="w")

    entry_folder = tk.Entry(frame, width=50)
    entry_folder.grid(row=0, column=1, padx=5, pady=5)

    button_sfoglia = tk.Button(frame, text="Browse", command=lambda: browse_folder(entry_folder))
    button_sfoglia.grid(row=0, column=2, padx=5, pady=5)

    label_extensions = tk.Label(frame, text="     Extensions:")
    label_extensions.grid(row=1, column=0, sticky="w")

    available_extensions = [".py", ".java", ".txt", ".cpp", ".html", ".css", ".js", ".json", ".scala", ".ts", ".c", ".mat", ".h", ".cs", ".gms", ".jsx"]  # Estensioni aggiunte
    checkboxes_extensions = []
    for i, ext in enumerate(available_extensions):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(frame, text=ext, variable=var, onvalue=1, offvalue=0)
        checkbox.grid(row=i // 2 + 1, column=i % 2 + 1, sticky="w", padx=(0, 2), pady=2)  # Modificato il valore di padx
        checkboxes_extensions.append((ext, var))

    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
    text_widget.grid(row=len(available_extensions) // 2 + 2, column=0, columnspan=3, padx=5, pady=5)

    merge_button = tk.Button(frame, text="Merge files", command=lambda: start_union_process(entry_folder, checkboxes_extensions, text_widget, merge_button))
    merge_button.grid(row=len(available_extensions) // 2 + 3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
