import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests


@dataclass
class PlaneConfig:
    """Configuration for Plane API client."""

    api_key: str
    workspace_slug: str
    project_id: str
    base_url: str


class PlaneClient:
    """Client for interacting with Plane API."""

    def __init__(self, api_key: str, workspace_slug: str, project_id: str, base_url: str):
        """Initialize Plane API client.

        Args:
            api_key: Your Plane API key
            workspace_slug: Workspace slug
            project_id: Project ID where issues will be created
            base_url: Base URL for Plane API
        """
        self.config = PlaneConfig(
            api_key=api_key, workspace_slug=workspace_slug, project_id=project_id, base_url=base_url
        )
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": self.config.api_key, "Content-Type": "application/json"})

        # Cache for project states and labels
        self._project_states = None
        self._project_labels = None

    def _get_base_url(self) -> str:
        """Get base URL for API endpoints."""
        return (
            f"{self.config.base_url}/api/v1/workspaces/{self.config.workspace_slug}/projects/{self.config.project_id}"
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Centralized request handler with consistent error handling.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path (e.g., '/issues/', '/states/')
            **kwargs: Additional arguments for requests (json, params, etc.)

        Returns:
            Response JSON as dictionary

        Raises:
            Exception: If the request fails with detailed error context
        """
        url = f"{self._get_base_url()}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code} on {method} {endpoint}: {e.response.text}"
            raise Exception(error_msg) from e
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from {method} {endpoint}") from e
        except requests.ConnectionError as e:
            raise Exception(f"Connection error on {method} {endpoint}") from e
        except requests.Timeout as e:
            raise Exception(f"Timeout on {method} {endpoint}") from e
        except requests.RequestException as e:
            raise Exception(f"{method} {endpoint} failed: {str(e)}") from e

    def create_issue(
        self,
        name: str,
        description_html: Optional[str] = None,
        labels: Optional[List[str]] = None,
        state: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Dict:
        """Create a new issue in Plane.

        Args:
            name: Issue title
            description_html: Issue description (HTML format)
            labels: List of label IDs
            state: State ID (if not provided, uses project default)
            assignees: List of user IDs to assign
            start_date: Start date (YYYY-MM-DD format)
            priority: Priority level (e.g., 'high', 'medium', 'low')

        Returns:
            Created issue data as dictionary

        Raises:
            Exception: If the API request fails
        """
        payload = {
            "name": name,
        }

        if description_html:
            payload["description_html"] = description_html
        if labels:
            payload["labels"] = labels
        if state:
            payload["state"] = state
        if assignees:
            payload["assignees"] = assignees
        if start_date:
            payload["start_date"] = start_date
        if priority:
            payload["priority"] = priority

        return self._make_request("POST", "/issues/", json=payload)

    def get_issues_by_title_and_state(self, title: str, state: Optional[str] = None) -> List[Dict]:
        """Get issues filtered by title and optionally by state.

        Args:
            title: Issue title to search for (partial match)
            state: State name to filter by (e.g., 'Backlog', 'Todo', 'In Progress', 'Done')

        Returns:
            List of matching issues

        Raises:
            Exception: If the API request fails
        """
        params = {"search": title}

        if state:
            params["state"] = state

        issues_response = self._make_request("GET", "/issues/", params=params)
        issues = issues_response.get("results", [])

        filtered_issues = []
        for issue in issues:
            name = issue.get("name", "").lower()
            if title.lower() in name:
                filtered_issues.append(issue)

        return filtered_issues

    def get_issues_by_label(self, label: str, state: Optional[str] = None) -> List[Dict]:
        """Get issues filtered by label and optionally by state.

        Args:
            label: Label name to filter by (e.g., 'CI failed')
            state: State name to filter by (e.g., 'Todo', 'Done')

        Returns:
            List of matching issues

        Raises:
            Exception: If the API request fails
        """
        params = {"labels": label}

        if state:
            params["state"] = state

        issues_response = self._make_request("GET", "/issues/", params=params)
        return issues_response.get("results", [])

    def add_comment(self, issue_id: str, comment_html: str) -> Dict:
        """Add a comment to an existing issue.

        Args:
            issue_id: ID of the issue
            comment_html: Comment text (HTML format)

        Returns:
            Created comment data

        Raises:
            Exception: If the API request fails
        """
        payload = {"comment_html": comment_html}

        return self._make_request("POST", f"/issues/{issue_id}/comments/", json=payload)

    def update_issue(self, issue_id: str, **kwargs) -> Dict:
        """Update an existing issue.

        Args:
            issue_id: ID of the issue to update
            **kwargs: Fields to update (name, description_html, priority, state, etc.)

        Returns:
            Updated issue data

        Raises:
            Exception: If the API request fails
        """
        return self._make_request("PATCH", f"/issues/{issue_id}/", json=kwargs)

    def close_issue(self, issue_id: str) -> Dict:
        """Close an issue by moving it to 'Done' state.

        Args:
            issue_id: ID of the issue to close

        Returns:
            Updated issue data

        Raises:
            Exception: If the API request fails or Done state not found
        """
        # Get project states using the centralized method
        states = self.get_project_states()

        # Find the 'Done' or 'Completed' state
        done_state = next((state for state in states if state.get("name", "").lower() in ["done", "completed"]), None)

        if not done_state:
            raise ValueError("Could not find 'Done' state in project")

        return self.update_issue(issue_id, state=done_state["id"])

    def get_issue(self, issue_id: str) -> Dict:
        """Get a single issue by ID.

        Args:
            issue_id: ID of the issue

        Returns:
            Issue data

        Raises:
            Exception: If the API request fails
        """
        return self._make_request("GET", f"/issues/{issue_id}/")

    def get_project_states(self) -> List[Dict]:
        """Get all states available in the project.

        Returns:
            List of state objects

        Raises:
            Exception: If the API request fails
        """
        if not self._project_states:
            states_response = self._make_request("GET", "/states/")
            self._project_states = states_response.get("results", [])
        return self._project_states

    def get_project_labels(self) -> List[Dict]:
        """Get all labels available in the project.

        Returns:
            List of label objects

        Raises:
            Exception: If the API request fails
        """
        if not self._project_labels:
            labels_response = self._make_request("GET", "/labels/")
            self._project_labels = labels_response.get("results", [])
        return self._project_labels
