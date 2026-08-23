import json
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class TestResult:
    """Dataclass representing a test result from Allure."""

    test_name: str
    test_id: str = ""
    timestamp: str = ""
    status: str = ""
    test_error_description: Optional[str] = None

    @property
    def passed(self) -> bool:
        """Determine if the test passed based on status."""
        return self.status == "passed"

    @property
    def failed(self) -> bool:
        """Determine if the test failed based on status."""
        return self.status == "failed"

    @staticmethod
    def from_allure_result(result: Dict) -> "TestResult":
        """Create TestResult from Allure result dictionary.

        Args:
            result: Allure result dictionary

        Returns:
            TestResult instance
        """
        test_status = result.get("status", "")

        test_error_description = None
        if test_status in ["failed", "broken"]:
            status_details = result.get("statusDetails", {})
            test_error_description = status_details.get("message", "No test error message available")

        start_ms = result.get("start", 0)
        timestamp = datetime.fromtimestamp(start_ms / 1000).isoformat() if start_ms else ""

        test_name = result.get("name", "")

        return TestResult(
            test_name=test_name,
            test_id=TestResult.extract_test_id(test_name),
            timestamp=timestamp,
            status=test_status,
            test_error_description=test_error_description,
        )

    @staticmethod
    def extract_test_id(test_name: str) -> str:
        """Extract test ID from test name.

        Test names start with ID like: MI_01, MI_123, APAN_02, etc.
        Extracts everything before the first space or underscore following pattern.

        Args:
            test_name: Full test name starting with test ID

        Returns:
            Test ID string or empty string if no ID found

        Examples:
            'MI_01_SOLO_REQUIRED_INCIDENCIAS' -> 'MI_01'
            'APAN_02 => Update status' -> 'APAN_02'
            'MI_393_405_T1_CAMBIO_DE_ESTADO' -> 'MI_393_405'
        """
        if not test_name:
            return ""

        # Split by common delimiters
        parts = test_name.replace(" => ", " ").replace("_", " ").split()

        if not parts:
            return ""

        first_part = parts[0]

        test_id_parts = [first_part]

        for i in range(1, min(3, len(parts))):
            if parts[i].isdigit():
                test_id_parts.append(parts[i])
            else:
                break

        return "_".join(test_id_parts)


def read_allure_results() -> List[Dict]:
    """Read Allure results from the specified directory.

    Returns:
        List of Allure result dictionaries.
    """
    results_path = Path(os.path.join(os.getcwd(), "allure-results"))

    if not results_path.exists():
        raise FileNotFoundError(f"Directory not found: {results_path}")

    results = []

    result_files = list(results_path.glob("*-result.json"))

    for file_path in result_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                result = json.load(f)
                results.append(result)
        except Exception as e:
            raise Exception(f"Error reading file {file_path.name}: {e}")

    return results


def extract_screenshots(result: Dict) -> List[str]:
    """Extract screenshot filenames from test result.

    Unused function because plane API does not support attachments yet.

    Args:
        result: Allure result dictionary

    Returns:
        List of screenshot filenames
    """
    screenshots = []

    for step in result.get("steps", []):
        for attachment in step.get("attachments", []):
            if attachment.get("type") == "image/png":
                screenshots.append(attachment.get("source"))

    return screenshots


def _group_results_by_test_id(results: List[Dict]) -> Dict[str, List[Dict]]:
    """Group Allure results by testCaseId to handle retries.

    Args:
        results: List of Allure result dictionaries

    Returns:
        Dictionary mapping testCaseId to list of attempts
    """
    tests_by_id: Dict[str, List[Dict]] = defaultdict(list)

    for result in results:
        test_case_id = result.get("testCaseId") or result.get("fullName") or str(result.get("uuid", ""))
        tests_by_id[test_case_id].append(result)

    return tests_by_id


def _get_last_attempt(attempts: List[Dict]) -> Dict:
    """Get the most recent attempt from a list of test attempts.

    Args:
        attempts: List of test attempts (retries)

    Returns:
        The attempt with the latest timestamp
    """
    return max(attempts, key=lambda x: x.get("start", 0))


def extract_test_results() -> List[TestResult]:
    """Extract all test results from Allure results.

    Handles retries by grouping tests with the same testCaseId and
    keeping only the last attempt (based on timestamp).

    Returns:
        List of TestResult dataclasses with only the final attempt of each test.
    """
    results = read_allure_results()

    if not results:
        raise Exception("No Allure results found.")

    # Group results by testCaseId (handles retries)
    tests_by_id = _group_results_by_test_id(results)

    # Extract only the last attempt of each test
    tests_results = []
    for attempts in tests_by_id.values():
        last_attempt = _get_last_attempt(attempts)
        tests_results.append(TestResult.from_allure_result(last_attempt))

    return tests_results


def main() -> None:
    """Extract and print test results from Allure report."""
    test_results = extract_test_results()
    for result in test_results:
        print(result)


if __name__ == "__main__":
    main()
