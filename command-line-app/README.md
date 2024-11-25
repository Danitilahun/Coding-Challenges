# ToDo List Command-Line App

A simple command-line tool to manage your to-do tasks using Python. The app allows you to add, list, and remove tasks directly from the terminal.

## Features
- Add tasks to your to-do list.
- View all your tasks.
- Remove tasks by index.
- Works globally from any directory.

---

## Installation

### 1. Clone or Download the Repository
Download the `todo.py` script and place it in a folder, e.g., `C:\myScripts`.

### 2. Set Up the Batch File Wrapper
1. Create a `td.bat` file in the same directory as `todo.py`.
2. Add the following content to `td.bat`:
   ```bat
   @echo off
   python "C:\myScripts\todo.py" %*
   ```
   Replace `C:\myScripts\todo.py` with the actual path to your `todo.py`.

3. Add the folder (`C:\myScripts`) to your system `PATH`:
   - Open **Environment Variables**.
   - Add `C:\myScripts` to the `PATH`.

---

## Usage

### Add a Task
To add a task, use:
```bash
td -a "Your task here"
```
Example:
```bash
td -a "Buy groceries"
```

### List All Tasks
To view your tasks, use:
```bash
td -l
```

### Remove a Task
To remove a task by its index, use:
```bash
td -r <index>
```
Example:
```bash
td -r 1
```

---

## Example Workflow

1. Add some tasks:
   ```bash
   td -a "Finish coding challenge"
   td -a "Read a book"
   td -a "Buy groceries"
   ```

2. List tasks:
   ```bash
   td -l
   ```
   Output:
   ```
   1. Finish coding challenge
   2. Read a book
   3. Buy groceries
   ```

3. Remove a task:
   ```bash
   td -r 2
   ```

4. List tasks again:
   ```bash
   td -l
   ```
   Output:
   ```
   1. Finish coding challenge
   2. Buy groceries
   ```

---

## Requirements

- **Python**: Ensure Python 3 is installed and added to the `PATH`.
- **Windows**: A batch file wrapper is required for global access.

---

## Notes

- The tasks are stored in a file located at `C:\Users\<your-username>\tasks.txt`.
- Ensure the `todo.py` script has proper permissions to read/write to this file.