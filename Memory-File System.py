#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json

class InMemoryFileSystem:
    def _init_(self):
        self.current_directory = '/'
        self.file_system = {}

    def mkdir(self, directory):
        path = self._get_absolute_path(directory)
        if path not in self.file_system:
            self.file_system[path] = {}
        else:
            print(f"Directory '{directory}' already exists.")

    def cd(self, path):
        if path == '/':
            self.current_directory = '/'
        else:
            new_path = os.path.normpath(os.path.join(self.current_directory, path))
            if new_path in self.file_system and isinstance(self.file_system[new_path], dict):
                self.current_directory = new_path
            else:
                print(f"Invalid path: '{path}'")

    def ls(self, directory=None):
        if directory is None:
            directory = self.current_directory

        if directory in self.file_system and isinstance(self.file_system[directory], dict):
            contents = list(self.file_system[directory].keys())
            print("\n".join(contents))
        else:
            print(f"Invalid directory: '{directory}'")

    def touch(self, filename):
        path = os.path.join(self.current_directory, filename)
        if path not in self.file_system:
            self.file_system[path] = ""
        else:
            print(f"File '{filename}' already exists.")

    def echo(self, filename, content):
        path = os.path.join(self.current_directory, filename)
        if path in self.file_system:
            self.file_system[path] = content
        else:
            print(f"File '{filename}' does not exist.")

    def cat(self, filename):
        path = os.path.join(self.current_directory, filename)
        if path in self.file_system:
            print(self.file_system[path])
        else:
            print(f"File '{filename}' not found.")

    def mv(self, source, destination):
        src_path = os.path.join(self.current_directory, source)
        dest_path = os.path.join(self.current_directory, destination)

        if src_path in self.file_system:
            self.file_system[dest_path] = self.file_system.pop(src_path)
        else:
            print(f"Source file '{source}' not found.")

    def cp(self, source, destination):
        src_path = os.path.join(self.current_directory, source)
        dest_path = os.path.join(self.current_directory, destination)

        if src_path in self.file_system:
            self.file_system[dest_path] = self.file_system[src_path]
        else:
            print(f"Source file '{source}' not found.")

    def rm(self, path):
        full_path = os.path.join(self.current_directory, path)

        if full_path in self.file_system:
            if isinstance(self.file_system[full_path], dict) and self.file_system[full_path]:
                print(f"Cannot remove non-empty directory '{path}'.")
            else:
                self.file_system.pop(full_path)
        else:
            print(f"File or directory '{path}' not found.")

    def _get_absolute_path(self, path):
        if path.startswith('/'):
            return path
        return os.path.normpath(os.path.join(self.current_directory, path))

    def save_state(self, save_path):
        with open(save_path, 'w') as file:
            json.dump({'current_directory': self.current_directory, 'file_system': self.file_system}, file)

    def load_state(self, load_path):
        with open(load_path, 'r') as file:
            data = json.load(file)
            self.current_directory = data['current_directory']
            self.file_system = data['file_system']


if __name__ == "__main__":
    file_system = InMemoryFileSystem()

    while True:
        command = input(f"{file_system.current_directory} $ ").split()
        
        if command:
            operation = command[0]
            
            if operation == 'exit':
                break
            elif operation == 'save_state':
                file_system.save_state(command[1])
            elif operation == 'load_state':
                file_system.load_state(command[1])
            else:
                try:
                    getattr(file_system, operation)(*command[1:])
                except AttributeError:
                    print(f"Invalid command: '{operation}'")

    print("Exiting the file system.")

