import sys
import os


# This is required so Python can find the 'monitoring' directory
# Get the directory of the current test file
current_file_dir = os.path.dirname(__file__)

# Get the path to the project's root directory (one level up)
project_root_dir = os.path.abspath(os.path.join(current_file_dir, ".."))

# Add the project root to the Python path
sys.path.insert(0, project_root_dir)


def test_dashboard_can_be_imported():
    import monitoring.dashboard  # noqa: F401
