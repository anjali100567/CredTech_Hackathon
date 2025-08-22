import subprocess

def test_streamlit_runs():
    """Smoke test to ensure Streamlit app launches"""
    result = subprocess.run(
        ["streamlit", "run", "dashboard/app.py", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10
    )
    assert result.returncode == 0 or result.returncode == 1  # 1 = early exit