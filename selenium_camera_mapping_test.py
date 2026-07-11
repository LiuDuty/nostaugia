import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


URL = "http://127.0.0.1:8765/puzzle40.html"


def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(URL)
        WebDriverWait(driver, 25).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".piece")) == 40)
        driver.execute_async_script(
            """
            const done=arguments[arguments.length-1];
            const screen={detected:true,c1:{x:.2,y:.1},c2:{x:.9,y:.1},c3:{x:.9,y:.9},c4:{x:.2,y:.9}};
            const rawX=.2+.0625*(.9-.2);
            const rawY=.1+.10*(.9-.1);
            db.collection('tracking').doc('state').set({
              center:screen,
              markers:{m0:{score:100,ts:Date.now(),corners:[
                (rawX*640-8)+','+(rawY*480-8),
                (rawX*640+8)+','+(rawY*480-8),
                (rawX*640+8)+','+(rawY*480+8),
                (rawX*640-8)+','+(rawY*480+8)
              ]}},
              timestamp:firebase.firestore.FieldValue.serverTimestamp()
            }).then(()=>done(true)).catch(e=>done(String(e)));
            """
        )
        time.sleep(1.2)
        print("HIT_COUNT=", driver.find_element(By.ID, "count").text)
        print("HIT_COVER=", driver.execute_script("return getComputedStyle(document.getElementById('cover-1')).opacity"))
        print("CAMSTAT_HIT=", driver.find_element(By.ID, "camstat").text.encode("ascii", "ignore").decode())

        driver.execute_async_script(
            """
            const done=arguments[arguments.length-1];
            db.collection('tracking').doc('state').set({
              center:{detected:true,c1:{x:.2,y:.1},c2:{x:.9,y:.1},c3:{x:.9,y:.9},c4:{x:.2,y:.9}},
              markers:{m0:{score:100,ts:Date.now(),corners:['500,400','516,400','516,416','500,416']}},
              timestamp:firebase.firestore.FieldValue.serverTimestamp()
            }).then(()=>done(true)).catch(e=>done(String(e)));
            """
        )
        time.sleep(1.2)
        print("OUT_COUNT=", driver.find_element(By.ID, "count").text)
        print("OUT_COVER=", driver.execute_script("return getComputedStyle(document.getElementById('cover-1')).opacity"))
        print("CAMSTAT_OUT=", driver.find_element(By.ID, "camstat").text.encode("ascii", "ignore").decode())
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
