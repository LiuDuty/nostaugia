from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    d = webdriver.Chrome(options=opts)
    try:
        d.get("http://127.0.0.1:8765/puzzle40-ghost3.html")
        WebDriverWait(d, 25).until(lambda x: len(x.find_elements(By.CSS_SELECTOR, ".piece")) == 40)
        board = d.find_element(By.ID, "board")
        print("BOARD_SIZE=", board.size)
        d.find_element(By.ID, "placeAll").click()
        sleep(0.5)
        print("COUNT_AFTER_PLACE=", d.find_element(By.ID, "count").text)
        print("COVER1_AFTER_PLACE=", d.execute_script("return getComputedStyle(document.getElementById('cover-1')).opacity"))
        d.execute_script(
            """
            const r=board.getBoundingClientRect();
            board.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+10,clientY:r.top+10}));
            """
        )
        sleep(0.5)
        print("COUNT_AFTER_CLEAR=", d.find_element(By.ID, "count").text)
        print("COVER1_AFTER_CLEAR=", d.execute_script("return getComputedStyle(document.getElementById('cover-1')).opacity"))
        print("P1_X=", d.execute_script("return document.querySelector('.piece[data-id=\"1\"]').state.x"))
    finally:
        d.quit()


if __name__ == "__main__":
    main()
