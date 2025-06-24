1. 🧾 **Header**
# 🔧📝 Text Tools - Your Swiss Army Knife for Text Processing

A powerful Python CLI tool for extracting links, dividing, and joining text files with advanced filtering capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) 
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20Mac-lightgrey)
[![Author](https://img.shields.io/badge/Author-AvroHere-green?logo=github)](https://github.com/AvroHere)

2. 🧩 **Features**
- 🔗 **Smart Link Extractor** - Categorizes URLs into userinfo, postinfo, and garbage
- 🧵 **Text Divider** - Splits large files into equal parts with smart distribution
- 🧩 **Text Jointer** - Merges multiple files with duplicate detection
- 🔍 **Keyword Filtering** - Include/exclude URLs based on keywords
- 📊 **Auto-Stats** - Shows processed counts and unique entries
- 📂 **Smart File Naming** - Output files include item counts in filenames
- 🖥️ **Clean UI** - ASCII-art menus and clear progress reporting
- ♻️ **Duplicate Handling** - Identifies and separates duplicate lines

  3. 💾 **Installation**
```bash
# Clone the repository
git clone https://github.com/AvroHere/text-tools.git
cd text-tools

# Install requirements
pip install -r requirements.txt

# Run the tool
python main.py
```

```
📥 Clone the repo

🐍 Install Python 3.8+ if needed

🔧 Install dependencies

🚀 Run the script
```

```markdown
4. 🧠 **Usage**
```bash
1. 🏠 Main Menu - Choose from 3 tools
2. 📂 Select file(s) - Pick from detected .txt files
3. ⚙️ Set options - Filters/divisions as needed
4. 💾 Get results - Saved automatically with smart names
5. 🔄 Repeat - Returns to main menu after each operation
---
🔗 Link Extractor: Extracts URLs with keyword filtering

✂️ Text Divider: Splits files into N parts

🧩 Text Jointer: Merges files with duplicate tracking
```

```markdown
5. 📁 **Folder Structure
├── LICENSE.txt # MIT License
├── README.md # This documentation
├── main.py # Main application script
├── requirements.txt # Dependency list
```


Output files will be created in working directory:
- `X_userinfo.txt` - Profile links
- `Y_postinfo.txt` - Content links 
- `Z_garbage.txt` - Unclassified links
- `N_combined_unique.txt` - Merged unique content

  
6. 🛠 **Built With**
- Standard Libraries:
  - `re` - Advanced regex pattern matching
  - `os` - File system operations
  - `pathlib` - Cross-platform path handling

- External Dependencies: None! 🎉

7. 🚧 **Roadmap**
- 🌐 Add URL validation and status checking
- 📊 Export statistics to CSV/JSON
- 🔄 Add batch processing for multiple files
- 🎨 Colorized terminal output
- 🧹 Add text cleaning/preprocessing options
- 🔍 Add more URL categorization patterns
- 🤖 Convert to GUI/web interface

  9. 📄 **License**
MIT License

Copyright (c) 2025 AvroHere

Permission is hereby granted... [standard MIT terms]

10. 👨‍💻 **Author**
**Avro**  
[GitHub Profile](https://github.com/AvroHere)

> "The best way to predict the future is to create it." - Abraham Lincoln

⭐ If you find this tool useful, please consider starring the repo!
  
