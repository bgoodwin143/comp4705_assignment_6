import pytest
import sys
import os

# Again, add the project root to the path so we can find the 'monitoring' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_dashboard_imports_correctly():

    try:
        # We try to import the file we renamed to dashboard.py
        import monitoring.dashboard
    except ImportError as e:
        pytest.fail(f"Failed to import the dashboard script. Check for missing libraries in requirements.txt!: {e}")
    except Exception as e:
        pytest.fail(f"The dashboard script has an error and could not be imported: {e}")