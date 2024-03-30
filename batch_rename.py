import os
import argparse

def rename_files(folder_path, file_extension, padding_length, start_index, silent_mode):
    if not os.path.exists(folder_path):
        print("Error: The specified folder does not exist.")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
    if not files:
        print("No files with the specified extension found.")
        return

    files.sort()
    total_files = len(files)
    print(f"Total files to be renamed: {total_files}")

    if not silent_mode:
        confirmation = input("Do you want to proceed with renaming? (yes/no): ")
        if confirmation.lower() != "yes":
            print("Operation canceled.")
            return

    for index, old_filename in enumerate(files):
        new_index = start_index + index
        new_filename = f"{new_index:0{padding_length}}{file_extension}"
        old_filepath = os.path.join(folder_path, old_filename)
        new_filepath = os.path.join(folder_path, new_filename)
        os.rename(old_filepath, new_filepath)
        if not silent_mode:
            print(f"Renamed: {old_filename} -> {new_filename} ({index + 1}/{total_files})")

def main():
    parser = argparse.ArgumentParser(description="Rename files in a folder to a numbered and padded format.")
    parser.add_argument("folder_path", help="Path to the folder containing the files.")
    parser.add_argument("file_extension", help="File extension to filter files.")
    parser.add_argument("--padding_length", type=int, default=2, help="Length of padding with zeros (default: 2)")
    parser.add_argument("--start_index", type=int, default=1, help="Starting index for renaming (default: 1)")
    parser.add_argument("--silent", action="store_true", help="Run in silent mode without confirmation and progress.")
    args = parser.parse_args()

    rename_files(args.folder_path, args.file_extension, args.padding_length, args.start_index, args.silent)

if __name__ == "__main__":
    main()

