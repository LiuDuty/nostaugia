from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://infinitepuzze.web.app/puzzle40.html"


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
        board = driver.find_element(By.ID, "board")
        first = pieces[0]

        before = first.value_of_css_property("transform")
        driver.execute_script(
            """
            const el = arguments[0];
            const r = el.getBoundingClientRect();
            const x = r.left + r.width / 2;
            const y = r.top + r.height / 2;
            el.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, pointerId:1, clientX:x, clientY:y}));
            el.dispatchEvent(new PointerEvent('pointermove', {bubbles:true, pointerId:1, clientX:x+120, clientY:y+70}));
            el.dispatchEvent(new PointerEvent('pointerup', {bubbles:true, pointerId:1, clientX:x+120, clientY:y+70}));
            """,
            first,
        )
        after_drag = first.value_of_css_property("transform")
        driver.execute_script(
            "arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles:true, cancelable:true}))",
            first,
        )
        after_rotate = first.value_of_css_property("transform")

        print("SELENIUM_OK")
        print("URL=", URL)
        print("TITLE=", driver.title)
        print("PIECES=", len(pieces))
        print("COUNT=", driver.find_element(By.ID, "count").text)
        print("BOARD_SIZE=", board.size)
        print("FIRST_SIZE=", first.size)
        print("DRAG_CHANGED=", before != after_drag)
        print("ROTATE_CHANGED=", after_drag != after_rotate)
        print("BEFORE=", before)
        print("AFTER_DRAG=", after_drag)
        print("AFTER_ROTATE=", after_rotate)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
