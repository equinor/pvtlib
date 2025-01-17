"""MIT License

Copyright (c) 2025 Christian Hågenvik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Note:
This script is used to add the license text to all Python files in the project
"""

import os
import pathspec

# Define the path to the LICENSE file
license_file_path = 'LICENSE'

# Read the LICENSE text with UTF-8 encoding
with open(license_file_path, 'r', encoding='utf-8') as file:
    license_text = file.read()

# Define the directory to search for Python files
directory = '.'

# Read the .gitignore file
with open('.gitignore', 'r') as file:
    gitignore = file.read()

# Create a pathspec from the .gitignore file
spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore.splitlines())

# Iterate over all files in the directory
for root, _, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        
        # Skip files and directories listed in .gitignore
        if spec.match_file(file_path):
            continue
        
        if file.endswith('.py'):
            # Read the original content of the file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as original_file:
                print(file_path)
                original_content = original_file.read()
            
            # Check if the LICENSE text is already present
            if license_text not in original_content:
                # Prepend the LICENSE text to the original content
                new_content = f'"""{license_text}"""\n\n{original_content}'
                
                # Write the new content back to the file with UTF-8 encoding
                with open(file_path, 'w', encoding='utf-8') as modified_file:
                    modified_file.write(new_content)

print("LICENSE text added to all Python files where it was not already present.")