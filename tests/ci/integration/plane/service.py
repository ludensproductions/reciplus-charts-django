from datetime import datetime
from typing import Dict, List, Optional

from ci.scripts.extract_tests_results import TestResult

from .client import PlaneClient


class PlaneIssueService:
    """Service for managing Plane issues related to CI test results."""

    def __init__(self, client: PlaneClient):
        self.client = client
        self.label = "CI failure"
        self.ci_failed_label = "[CI Failed]"

    def sync_test_results(self, tests: List[TestResult], jenkins_report_url: str = None) -> dict:
        """Handle failed tests by creating or updating issues in Plane.

        Args:
            tests: List of TestResult dataclass with test details.
            jenkins_report_url: URL to the Jenkins build report.

        Returns:
            Dict with action taken and issue ID.
        """
        created_ids = []
        updated_ids = []

        todo_state = self.get_todo_project_state()
        ci_label = self.get_ci_label()

        for test in tests:
            if not test.failed or not test.test_id:
                continue

            open_failed_tests = self._get_existing_failed_test_issues(test.test_id)

            if open_failed_tests:
                # If there are existing open issues for this failed test, add a comment and update
                self._handle_comment_on_existing_issue(open_failed_tests[0], test)
                updated_ids.append(open_failed_tests[0]["id"])

            else:
                issue = self.client.create_issue(
                    name=f"{self.ci_failed_label}{test.test_name}",
                    description_html=(
                        "<h3>Detalles del fallo:</h3>"
                        "<p>"
                        "<strong>Jenkins build report:</strong><br/>"
                        f'<a href="{jenkins_report_url}" target="_blank" rel="noopener noreferrer">'
                        "Ver reporte en Jenkins"
                        "</a>"
                        "</p>"
                        "<pre><code>"
                        f"{test.test_error_description}"
                        "</code></pre>"
                    ),
                    labels=[ci_label["id"]],
                    state=todo_state["id"],
                    start_date=self.get_date_str(),
                    priority="high",
                )
                created_ids.append(issue["id"])

        # After handling all failed tests, close issues for tests that have passed
        close_result = self.close_passed_tests(tests)

        return {
            "created_issues": len(created_ids),
            "updated_issues": len(updated_ids),
            "closed_issues": len(close_result["issue_ids"]) if close_result else 0,
        }

    def _get_existing_failed_test_issues(self, test_id: str) -> List[Dict]:
        """Get existing issues for a failed test by ID.

        Args:
            test_id: ID of the failed test (e.g., MI_01, APAN_02).
        """
        existing_failed_tests = self.client.get_issues_by_title_and_state(
            title=f"{self.ci_failed_label} {test_id}", state=None
        )

        done_state = self.get_done_state()

        open_failed_tests = []
        for i in existing_failed_tests:
            if i.get("state") != done_state["id"]:
                open_failed_tests.append(i)

        return open_failed_tests

    def _handle_comment_on_existing_issue(self, issue: Dict, test: TestResult) -> None:
        """Add a comment to an existing issue for a failed test.

        Args:
            issue: Existing issue dictionary.
            test: TestResult dataclass with test details.
        """
        date = self.get_date_str()
        comment_html = (
            "<p>🔄 <strong>La prueba volvió a fallar</strong></p>"
            "<pre><code>"
            f"{test.test_error_description}"
            "</code></pre>"
            f"<p><strong>Falló en la fecha:</strong> {date}</p>"
        )
        self.client.add_comment(issue["id"], comment_html)

    def close_passed_tests(self, tests: List[TestResult]) -> Optional[Dict]:
        """Close issues for tests that are no longer failing.

        Gets all open issues with the CI failed label, checks if their corresponding tests have passed,
        and if so, moves the issues to the Done state and adds a comment.

        Args:
            tests: List of all TestResult dataclasses.

        Returns:
            Dict with action and list of closed issue IDs, or None if no issues closed.
        """
        ci_label = self.get_ci_label()
        all_ci_issues = self.client.get_issues_by_label(label=ci_label["id"])

        done_state = self.get_done_state()

        open_issues = []
        for i in all_ci_issues:
            if i.get("state") != done_state["id"]:
                open_issues.append(i)

        if not open_issues:
            return None

        # Get IDs of tests that have explicitly passed (not skipped)
        passed_tests_ids = set()
        for test in tests:
            if test.passed and test.test_id:
                passed_tests_ids.add(test.test_id)

        passed_issues = []
        for issue in open_issues:
            issue_title = issue.get("name", "")

            if issue_title.startswith(f"{self.ci_failed_label} "):
                title_after_prefix = issue_title.replace(f"{self.ci_failed_label} ", "", 1)
                test_id = TestResult.extract_test_id(title_after_prefix)

                if test_id and test_id in passed_tests_ids:
                    passed_issues.append(issue)

        if not passed_issues:
            return None

        closed_issue_ids = []
        date = self.get_date_str()

        for issue in passed_issues:
            self.client.update_issue(issue["id"], state=done_state["id"])

            comment_html = (
                f"<p>✅ <strong>La prueba fue ejecutada correctamente.</strong></p>"
                f"<p><strong>Fecha de correcta ejecución:</strong> {date}</p>"
            )

            self.client.add_comment(issue["id"], comment_html)

            closed_issue_ids.append(issue["id"])

        return {"action": "closed", "issue_ids": closed_issue_ids}

    def get_todo_project_state(self) -> Optional[Dict]:
        """Get the 'Todo' state from the project.

        Returns:
            Todo state dictionary
        """
        states = self.client.get_project_states()

        todo_state = next((state for state in states if state.get("name", "").lower() == "todo"), None)

        if not todo_state:
            raise Exception("Todo state not found in project states.")

        return todo_state

    def get_done_state(self) -> Dict:
        """Get the 'Done' state from the project.

        Returns:
            Done state dictionary

        Raises:
            Exception: If Done state not found in project states
        """
        states = self.client.get_project_states()

        done_state = next((state for state in states if state.get("name", "").lower() == "done"), None)

        if not done_state:
            raise Exception("Done state not found in project states.")

        return done_state

    def get_ci_label(self) -> Dict:
        """Get the CI failed label from the project.

        Returns:
            CI failed label dictionary
        """
        labels = self.client.get_project_labels()

        ci_label = next((label for label in labels if label.get("name", "") == self.label), None)

        if not ci_label:
            raise Exception(f"Label '{self.label}' not found in project labels.")

        return ci_label

    def get_date_str(self) -> str:
        """Get current date as string in YYYY-MM-DD format.

        Returns:
            Current date string
        """
        return datetime.now().strftime("%Y-%m-%d")
