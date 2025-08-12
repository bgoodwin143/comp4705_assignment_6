import pytest
import sys
import os

"""
A simple test to ensure the Streamlit dashboard can launch without errors.
"""

# This is required so Python can find the 'monitoring' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_dashboard_can_be_imported():
    import monitoring.dashboard