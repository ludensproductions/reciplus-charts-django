import os
import sys
from pathlib import Path

# Load .env if exists (local dev). CI uses Jenkins environment variables, no .env file present.
try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # Fallback: if dotenv not installed, use system environment variables

from ci.integration.plane.client import PlaneClient
from ci.integration.plane.service import PlaneIssueService
from ci.scripts.extract_tests_results import extract_test_results


def _require_env(var_name: str) -> str:
    """Retrieve required environment variable.

    Args:
        var_name: Name of the environment variable.

    Returns:
        The environment variable value.

    Raises:
        RuntimeError: If the environment variable is not set.
    """
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required env var: {var_name}")
    return value


def load_config() -> dict:
    """Load Plane and Jenkins configuration from environment variables.

    Returns:
        Dictionary with Plane API configuration and Jenkins report URL.
    """
    return {
        "plane_api_key": _require_env("PLANE_API_KEY"),
        "plane_base_url": _require_env("PLANE_BASE_URL"),
        "plane_workspace": _require_env("PLANE_WORKSPACE"),
        "plane_project_id": _require_env("PLANE_PROJECT_ID"),
        "jenkins_report_url": os.getenv("JENKINS_REPORT_URL"),
    }


def main() -> int:
    """Load configuration, extract test results, and synchronize with Plane.

    Returns:
        Exit code (0 for success).
    """
    config = load_config()

    test_results = extract_test_results()
    if not test_results:
        print("No test results found. Skipping Plane sync.")
        return 0

    client = PlaneClient(
        api_key=config["plane_api_key"],
        base_url=config["plane_base_url"],
        workspace_slug=config["plane_workspace"],
        project_id=config["plane_project_id"],
    )

    service = PlaneIssueService(client)

    result = service.sync_test_results(
        tests=test_results,
        jenkins_report_url=config["jenkins_report_url"],
    )

    print("Plane sync result:", result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
