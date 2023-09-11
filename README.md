# StackOverflowSearcher

`StackOverflowSearcher` is a Python tool that helps in automatically detecting errors from a Python script and searching them on Stack Overflow for relevant solutions.

## Code Overview

### Imports

```python
import subprocess
import requests
import webbrowser
```

- `subprocess`: Used to run the provided Python file and capture any execution errors.
- `requests`: Helps in making HTTP requests to the Stack Overflow API.
- `webbrowser`: Enables the opening of Stack Overflow answer links in the default web browser.

### Class: StackOverflowSearcher

#### `__init__(self, file_path: str)`

Initializes the searcher with the path of the Python file you want to check.

#### `_execute_file(self) -> str`

```python
def _execute_file(self) -> str:
        """
        Executes the given Python file and returns any error details.
        """
        process = subprocess.Popen(['python', self.file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        return stderr.decode('utf-8')

```

Executes the given Python file and returns any error details.

#### `_parse_error_message(self, error_details: str) -> tuple`

```python
def _parse_error_message(self, error_details: str) -> tuple:
        """
        Parses the error details and returns the error type and message.
        """
        for error_line in error_details.split('\n'):
            if "Error" in error_line:
                error_type = error_line.split(":")[0]
                error_message = error_line[len(error_type)+1:]
                return error_line, error_type, error_message
        return None, None, None
```

Parses the returned error details and breaks it down into:

- The complete error line
- The error type
- The specific error message

#### `_search_stack_overflow(self, error: str) -> dict`

```python
def _search_stack_overflow(self, error: str) -> dict:
        """
        Searches Stack Overflow for the given error and returns search results.
        """
        url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&tagged=python&intitle={error}&site=stackoverflow"
        return requests.get(url).json()
```

Searches Stack Overflow using their API for the given error and fetches the search results.

#### `_open_web_links(self, search_results: dict)`

```python
def _open_web_links(self, search_results: dict):
        """
        Opens the links from the Stack Overflow search results in a web browser.
        """
        answer_links = [item["link"] for item in search_results["items"] if item["is_answered"]][:3]
        for link in answer_links:
            webbrowser.open(link)
```

Takes the search results from the Stack Overflow API and opens the top 3 answered links in the default web browser.

#### `search_for_errors(self)`

```python
def search_for_errors(self):
        """
        Search Stack Overflow for errors in the given Python file.
        """
        error_details = self._execute_file()
        error_line, error_type, error_message = self._parse_error_message(error_details)

        if error_line:
            for error in (error_line, error_type, error_message):
                search_results = self._search_stack_overflow(error)
                self._open_web_links(search_results)
        else:
            return "No Error Found"
```

The main function that ties everything together:

1. Executes the provided Python file and fetches error details (if any).
2. Parses the error to get its specifics.
3. Searches each specific part of the error on Stack Overflow.
4. Opens relevant solutions in the web browser.

### Example Usage

To utilize the `StackOverflowSearcher`, here's a quick guide:

```python
err_searcher = StackOverflowSearcher("test.py")
err_searcher.search_for_errors()
```

In the example above, it will check the `test.py` file for errors and open relevant solutions on Stack Overflow if any errors are found.

## Conclusion

The `StackOverflowSearcher` class is a handy tool for any Python developer, helping them to quickly identify and find solutions to script errors directly from Stack Overflow.
