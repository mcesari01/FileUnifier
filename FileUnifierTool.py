import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

selected_files = []  # Nuova lista globale dei file selezionati

def add_files(listbox):
    files = filedialog.askopenfilenames(title="Select files to merge")
    for file in files:
        if file not in selected_files:
            selected_files.append(file)
            listbox.insert(tk.END, file)

def remove_selected_file(listbox):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        selected_files.pop(index)
        listbox.delete(index)

def merge_files_into_one(results, merged_file):
    unified_text = ""
    for file_path in results:
        file_name = os.path.basename(file_path)
        unified_text += f"\n\n# Start of file: {file_name}\n\n"
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_input:
            unified_text += file_input.read()
    with open(merged_file, 'w', encoding='utf-8') as file_output:
        file_output.write(unified_text)
    return unified_text

def perform_merge(text_widget, merge_button):
    merge_button.configure(state='disabled')

    if not selected_files:
        messagebox.showwarning("No files", "No files selected for merging.")
        merge_button.configure(state='normal')
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
    if not output_file:
        merge_button.configure(state='normal')
        return

    unified_text = merge_files_into_one(selected_files, output_file)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, unified_text)

    messagebox.showinfo("Success", f"Files merged into:\n{output_file}")
    merge_button.configure(state='normal')

def start_merge_thread(text_widget, merge_button):
    thread = threading.Thread(target=perform_merge, args=(text_widget, merge_button))
    thread.start()

def main():
    root = tk.Tk()
    root.title("File Unifier Tool")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # === File selection controls ===
    file_frame = tk.Frame(frame)
    file_frame.grid(row=0, column=0, columnspan=3, sticky="we")

    listbox_files = tk.Listbox(file_frame, width=80, height=8, selectmode=tk.SINGLE)
    listbox_files.pack(side=tk.LEFT, padx=(0, 5))

    buttons_file_ops = tk.Frame(file_frame)
    buttons_file_ops.pack(side=tk.RIGHT)

    btn_add = tk.Button(buttons_file_ops, text="Add files", command=lambda: add_files(listbox_files))
    btn_add.pack(pady=(0, 5))

    btn_remove = tk.Button(buttons_file_ops, text="Remove selected", command=lambda: remove_selected_file(listbox_files))
    btn_remove.pack()

    # === Text area for preview ===
    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
    text_widget.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

    # === Merge button ===
    merge_button = tk.Button(frame, text="Merge files", command=lambda: start_merge_thread(text_widget, merge_button))
    merge_button.grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
