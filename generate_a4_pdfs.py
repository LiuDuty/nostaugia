import base64
import functools
import http.server
import socketserver
import threading
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
PORT = 8767


def print_pdf(driver, html_name, pdf_name, wait_selector):
    url = f"http://127.0.0.1:{PORT}/{html_name}"
    driver.get(url)
    WebDriverWait(driver, 25).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, wait_selector)) > 0)
    result = driver.execute_cdp_cmd(
        "Page.printToPDF",
        {
            "printBackground": True,
            "paperWidth": 8.2677,
            "paperHeight": 11.6929,
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0,
            "preferCSSPageSize": True,
        },
    )
    out = PUBLIC / pdf_name
    out.write_bytes(base64.b64decode(result["data"]))
    print(f"PDF={out} bytes={out.stat().st_size}")


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(PUBLIC))
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1200,1600")
    driver = webdriver.Chrome(options=opts)
    try:
        print_pdf(driver, "aruco-markers-a4.html", "aruco-markers-a4.pdf", ".marker svg")
        print_pdf(driver, "puzzle-pieces-a4.html", "puzzle-pieces-a4.pdf", ".piece-svg path")
    finally:
        driver.quit()
        httpd.shutdown()


if __name__ == "__main__":
    main()
