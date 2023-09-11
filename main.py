import subprocess
import requests
import webbrowser

class StackOverflowSearcher:
    def __init__(self, file_path: str):
        """
        Initialize with the path of the Python file to check.
        """
        self.file_path = file_path

    def _execute_file(self) -> str:
        """
        Executes the given Python file and returns any error details.
        """
        process = subprocess.Popen(['python', self.file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        return stderr.decode('utf-8')
    
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
    
    def _search_stack_overflow(self, error: str) -> dict:
        """
        Searches Stack Overflow for the given error and returns search results.
        """
        url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&tagged=python&intitle={error}&site=stackoverflow"
        return requests.get(url).json()
    
    def _open_web_links(self, search_results: dict):
        """
        Opens the links from the Stack Overflow search results in a web browser.
        """
        answer_links = [item["link"] for item in search_results["items"] if item["is_answered"]][:3]
        for link in answer_links:
            webbrowser.open(link)
    
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

# Example Usage:
err_searcher = StackOverflowSearcher("test.py")
err_searcher.search_for_errors()