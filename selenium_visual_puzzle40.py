from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://infinitepuzze.web.app/puzzle40.html"
OUT = Path(r"C:\Users\leand\AppData\Local\Temp\opencode\puzzle40_selenium")


def screenshot(driver, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    driver.save_screenshot(str(path))
    print(f"SCREENSHOT={path}")


def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(URL)
        WebDriverWait(driver, 20).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".piece")) == 40)
        pieces = driver.find_elements(By.CSS_SELECTOR, ".piece")
        first = pieces[0]
        print("OPENED=", URL)
        print("TITLE=", driver.title)
        print("PIECES=", len(pieces))
        print("COUNT_INITIAL=", driver.find_element(By.ID, "count").text)
        screenshot(driver, "01_loaded.png")

        driver.execute_script(
            """
            const el = arguments[0];
            const r = el.getBoundingClientRect();
            const x = r.left + r.width / 2;
            const y = r.top + r.height / 2;
            el.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, pointerId:1, clientX:x, clientY:y}));
            el.dispatchEvent(new PointerEvent('pointermove', {bubbles:true, pointerId:1, clientX:x+180, clientY:y+90}));
            el.dispatchEvent(new PointerEvent('pointerup', {bubbles:true, pointerId:1, clientX:x+180, clientY:y+90}));
            """,
            first,
        )
        sleep(0.2)
        print("AFTER_DRAG_TRANSFORM=", first.value_of_css_property("transform"))
        screenshot(driver, "02_after_drag.png")

        driver.execute_script(
            "arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles:true, cancelable:true}))",
            first,
        )
        sleep(0.2)
        print("AFTER_ROTATE_TRANSFORM=", first.value_of_css_property("transform"))
        screenshot(driver, "03_after_rotate.png")

        driver.execute_script(
            """
            const el = arguments[0];
            const p = el.piece;
            const scale = board.clientWidth / boardData.boardWidth;
            el.state.locked = false;
            el.state.x = p.targetX * scale;
            el.state.y = p.targetY * scale;
            el.state.r = 0;
            renderTransform(el);
            trySnap(el);
            """,
            first,
        )
        sleep(0.5)
        print("COUNT_AFTER_SNAP=", driver.find_element(By.ID, "count").text)
        print("LOCKED_AFTER_SNAP=", driver.execute_script("return arguments[0].state.locked", first))
        print("COVER_AFTER_SNAP=", driver.execute_script("return getComputedStyle(document.getElementById('cover-'+arguments[0].piece.id)).opacity", first))
        screenshot(driver, "04_after_snap.png")

        driver.execute_script(
            """
            const el = arguments[0];
            const r = el.getBoundingClientRect();
            el.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, pointerId:1, clientX:r.left+20, clientY:r.top+20}));
            """,
            first,
        )
        sleep(0.5)
        print("COUNT_AFTER_REMOVE=", driver.find_element(By.ID, "count").text)
        print("COVER_AFTER_REMOVE=", driver.execute_script("return getComputedStyle(document.getElementById('cover-'+arguments[0].piece.id)).opacity", first))
        screenshot(driver, "05_after_remove.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
