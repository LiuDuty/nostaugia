from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    d = webdriver.Chrome(options=opts)
    try:
        d.get("http://127.0.0.1:8765/puzzle40-ghost2.html")
        WebDriverWait(d, 25).until(lambda x: len(x.find_elements(By.CSS_SELECTOR, ".piece")) == 40)
        result = d.execute_script(
            """
            const p2=document.querySelector('.piece[data-id="2"]');
            const sc=board.clientWidth/boardData.boardWidth;
            const p=p2.piece;
            p2.state.x=p.targetX*sc;
            p2.state.y=p.targetY*sc;
            p2.state.r=0;
            renderTransform(p2);
            p2.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:1,clientX:0,clientY:0}));
            return {count:count.textContent,cover2:getComputedStyle(document.getElementById('cover-2')).opacity};
            """
        )
        print("MANUAL=", result)
        d.execute_script(
            """
            setCameraReveal(1,true);
            updateCameraGhost(boardData.pieces[0],{x:.06,y:.1},true);
            setCameraReveal(2,true);
            updateCameraGhost(boardData.pieces[1],{x:.19,y:.1},true);
            updateCount();
            """
        )
        sleep(0.4)
        result2 = d.execute_script(
            """
            return {
              count:count.textContent,
              cover1:getComputedStyle(document.getElementById('cover-1')).opacity,
              cover2:getComputedStyle(document.getElementById('cover-2')).opacity,
              ghosts:document.querySelectorAll('.camera-ghost').length,
              ghostVisible:Array.from(document.querySelectorAll('.camera-ghost')).filter(g=>getComputedStyle(g).display!=='none').length
            };
            """
        )
        print("CAMERA=", result2)
    finally:
        d.quit()


if __name__ == "__main__":
    main()
