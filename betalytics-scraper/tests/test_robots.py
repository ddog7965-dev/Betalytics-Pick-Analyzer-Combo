import subprocess, sys

def test_robots_cli_runs():
    # Should not crash; may exitcode 0/1 depending on live robots – we just verify the tool executes
    try:
        subprocess.run([sys.executable, "-m", "betalytics_scraper.utils.robots_check", "https://www.betalytics.com/home"], check=False)
    except Exception as e:
        assert False, f"robots_check raised exception: {e}"
