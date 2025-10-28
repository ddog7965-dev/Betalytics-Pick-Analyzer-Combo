# CLI: python -m betalytics_scraper.utils.robots_check https://www.betalytics.com/home
import sys
import urllib.robotparser as rp

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m betalytics_scraper.utils.robots_check <url>")
        sys.exit(2)
    url = sys.argv[1]
    # derive robots.txt origin
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(url)
    robots_url = urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))
    r = rp.RobotFileParser()
    r.set_url(robots_url)
    try:
        r.read()
    except Exception as e:
        print(f"[WARN] Could not read robots.txt at {robots_url}: {e}")
        # Fail open? Choose conservatively:
        sys.exit(1)
    allowed = r.can_fetch("*", url)
    print(f"robots.txt: {robots_url}")
    print(f"Allowed for '*': {allowed}")
    sys.exit(0 if allowed else 1)

if __name__ == "__main__":
    main()
