import re
import os
import sys
from pathlib import Path

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu."""
    clear_screen()
    print("""
╔══════════════════════════╗
║       TEXT TOOLS         ║
╠══════════════════════════╣
║ 1️⃣ Link Extractor        ║
║ 2️⃣ Text Divider          ║
║ 3️⃣ Text Jointer          ║
║ 4️⃣ Exit                  ║
╚══════════════════════════╝
""")

def get_user_choice():
    """Get and validate user choice from menu."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def list_txt_files():
    """List all .txt files in current directory with serial numbers."""
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    if not txt_files:
        print("No .txt files found in current directory.")
        return None
    
    print("\nAvailable text files:")
    for i, filename in enumerate(txt_files, 1):
        print(f"{i}. {filename}")
    return txt_files

def select_file(txt_files):
    """Let user select a file from the list."""
    while True:
        try:
            choice = int(input("\nEnter file number to process: "))
            if 1 <= choice <= len(txt_files):
                return txt_files[choice - 1]
            print(f"Please enter a number between 1 and {len(txt_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_keyword_filters():
    """Get include and exclude keyword filters from user."""
    include = input("Enter keywords to include (comma separated, leave empty for none): ").strip()
    exclude = input("Enter keywords to exclude (comma separated, leave empty for none): ").strip()
    
    include_keywords = [kw.strip().lower() for kw in include.split(',')] if include else []
    exclude_keywords = [kw.strip().lower() for kw in exclude.split(',')] if exclude else []
    
    return include_keywords, exclude_keywords

def matches_filters(url, include, exclude):
    """Check if URL matches include/exclude filters."""
    url_lower = url.lower()
    
    # All include keywords must be present
    if include and not all(kw in url_lower for kw in include):
        return False
    
    # No exclude keywords should be present
    if exclude and any(kw in url_lower for kw in exclude):
        return False
    
    return True

def extract_links():
    """Link Extractor functionality."""
    clear_screen()
    print("""
╔══════════════════════════╗
║      LINK EXTRACTOR      ║
╚══════════════════════════╝
""")
    
    txt_files = list_txt_files()
    if not txt_files:
        input("\nPress Enter to return to menu...")
        return
    
    filename = select_file(txt_files)
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"\nError reading file: {e}")
        input("\nPress Enter to return to menu...")
        return
    
    include, exclude = get_keyword_filters()
    
    # Regex pattern to match URLs
    url_pattern = re.compile(
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\-\.~!*\'();:@&=+$,%#?]*'
    )
    
    urls = url_pattern.findall(content)
    if not urls:
        print("\nNo URLs found in the file.")
        input("\nPress Enter to return to menu...")
        return
    
    # Categorize URLs
    userinfo = []
    postinfo = []
    garbage = []
    
    # Patterns for categorization
    userinfo_pattern = re.compile(r'https?://[^/]+/[a-zA-Z0-9_\-]+/?$')
    postinfo_pattern = re.compile(r'https?://[^/]+/[a-zA-Z0-9_\-]+/(?:\d+|[a-zA-Z0-9_\-]+)/?$')
    
    for url in urls:
        if not matches_filters(url, include, exclude):
            garbage.append(url)
            continue
            
        if userinfo_pattern.fullmatch(url):
            userinfo.append(url)
        elif postinfo_pattern.fullmatch(url):
            postinfo.append(url)
        else:
            garbage.append(url)
    
    # Sort all lists alphabetically
    userinfo.sort()
    postinfo.sort()
    garbage.sort()
    
    # Save results
    def save_links(links, category):
        if links:
            output_filename = f"{len(links)}_{category}.txt"
            with open(output_filename, 'w', encoding='utf-8') as out_file:
                out_file.write('\n'.join(links))
            return output_filename
        return None
    
    userinfo_file = save_links(userinfo, 'userinfo')
    postinfo_file = save_links(postinfo, 'postinfo')
    garbage_file = save_links(garbage, 'garbage')
    
    # Display results
    print("\nResults:")
    if userinfo_file:
        print(f"🔹 Userinfo links saved to: {userinfo_file}")
    if postinfo_file:
        print(f"🔹 Postinfo links saved to: {postinfo_file}")
    if garbage_file:
        print(f"🗑️ Garbage links saved to: {garbage_file}")
    
    total_processed = len(userinfo) + len(postinfo) + len(garbage)
    print(f"\nTotal URLs processed: {total_processed}")
    print(f"Unique URLs found: {len(set(urls))}")
    
    input("\nPress Enter to return to menu...")

def divide_text():
    """Text Divider functionality."""
    clear_screen()
    print("""
╔══════════════════════════╗
║       TEXT DIVIDER       ║
╚══════════════════════════╝
""")
    
    txt_files = list_txt_files()
    if not txt_files:
        input("\nPress Enter to return to menu...")
        return
    
    filename = select_file(txt_files)
    
    # Get number of parts
    while True:
        try:
            num_parts = int(input("\nEnter number of parts to divide into: "))
            if num_parts < 1:
                print("Number must be at least 1.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"\nError reading file: {e}")
        input("\nPress Enter to return to menu...")
        return
    
    total_lines = len(lines)
    if total_lines == 0:
        print("\nFile is empty.")
        input("\nPress Enter to return to menu...")
        return
    
    if num_parts > total_lines:
        print(f"\nWarning: File has only {total_lines} lines, which is fewer than requested {num_parts} parts.")
        num_parts = total_lines
    
    # Calculate lines per part
    base_size = total_lines // num_parts
    remainder = total_lines % num_parts
    
    # Prepare output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Split and save parts
    file_base = Path(filename).stem
    start = 0
    for i in range(1, num_parts + 1):
        end = start + base_size + (1 if i <= remainder else 0)
        part_lines = lines[start:end]
        
        part_filename = f"{output_dir}/{file_base}_part{i}.txt"
        with open(part_filename, 'w', encoding='utf-8') as part_file:
            part_file.writelines(part_lines)
        
        print(f"Saved part {i} with {len(part_lines)} lines to {part_filename}")
        start = end
    
    print(f"\nSuccessfully divided {filename} into {num_parts} parts.")
    input("\nPress Enter to return to menu...")

def join_text():
    """Text Jointer functionality - joins multiple files with duplicate tracking."""
    clear_screen()
    print("""
╔══════════════════════════╗
║       TEXT JOINTER       ║
╚══════════════════════════╝
""")
    
    txt_files = list_txt_files()
    if not txt_files:
        input("\nPress Enter to return to menu...")
        return
    
    print("\nEnter file numbers to join (comma separated, e.g. 1,2,3):")
    while True:
        try:
            choices = input("> ").strip().split(',')
            selected_indices = [int(choice.strip()) for choice in choices if choice.strip()]
            
            # Validate all choices
            if not selected_indices:
                print("Please enter at least one file number.")
                continue
                
            if any(i < 1 or i > len(txt_files) for i in selected_indices):
                print(f"Please enter numbers between 1 and {len(txt_files)}.")
                continue
                
            break
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    
    selected_files = [txt_files[i-1] for i in selected_indices]
    
    # Track all lines and duplicates
    all_lines = []
    seen_lines = set()
    duplicate_lines = set()
    
    try:
        for filename in selected_files:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:  # Skip empty lines
                        if line in seen_lines:
                            duplicate_lines.add(line)
                        else:
                            seen_lines.add(line)
                        all_lines.append(line)
    except Exception as e:
        print(f"\nError reading files: {e}")
        input("\nPress Enter to return to menu...")
        return
    
    if not all_lines:
        print("\nAll files are empty. No output created.")
        input("\nPress Enter to return to menu...")
        return
    
    # Prepare unique and duplicate lines
    unique_lines = sorted(seen_lines)
    duplicate_lines = sorted(duplicate_lines)
    
    # Save combined unique file
    combined_filename = f"{len(unique_lines)}_combined_unique.txt"
    with open(combined_filename, 'w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(unique_lines))
    
    # Save duplicates file if any
    duplicates_filename = None
    if duplicate_lines:
        duplicates_filename = f"{len(duplicate_lines)}_duplicates.txt"
        with open(duplicates_filename, 'w', encoding='utf-8') as dup_file:
            dup_file.write('\n'.join(duplicate_lines))
    
    # Display results
    print(f"\nProcessed {len(selected_files)} files with {len(all_lines)} total lines.")
    print(f"🔹 Unique lines saved to: {combined_filename} ({len(unique_lines)} lines)")
    if duplicates_filename:
        print(f"🔹 Duplicates saved to: {duplicates_filename} ({len(duplicate_lines)} lines)")
    else:
        print("🔹 No duplicates found.")
    
    input("\nPress Enter to return to menu...")

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 1:
            extract_links()
        elif choice == 2:
            divide_text()
        elif choice == 3:
            join_text()
        elif choice == 4:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)