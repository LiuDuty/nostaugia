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
        d.get("http://127.0.0.1:8765/puzzle40.html")
        WebDriverWait(d, 25).until(lambda x: len(x.find_elements(By.CSS_SELECTOR, ".piece")) == 40)
        result = d.execute_script(
            """
            const p1=document.querySelector('.piece[data-id="1"]');
            const p2=document.querySelector('.piece[data-id="2"]');
            const sc=board.clientWidth/boardData.boardWidth;
            function placeWithoutSnap(el){
              const p=el.piece;
              el.state.x=p.targetX*sc;
              el.state.y=p.targetY*sc;
              el.state.r=0;
              renderTransform(el);
              el.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:1,clientX:0,clientY:0}));
            }
            placeWithoutSnap(p1);
            const p1Manual={count:count.textContent,cover:getComputedStyle(document.getElementById('cover-1')).opacity};
            const p=p2.piece;
            p2.state.x=p.targetX*sc;
            p2.state.y=p.targetY*sc;
            p2.state.r=0;
            renderTransform(p2);
            trySnap(p2,true);
            const p2Manual={count:count.textContent,cover:getComputedStyle(document.getElementById('cover-2')).opacity};
            setCameraReveal(1,true);
            updateCount();
            const p1Camera={count:count.textContent,cover:getComputedStyle(document.getElementById('cover-1')).opacity};
            return {p1Manual,p2Manual,p1Camera};
            """
        )
        print(result)
    finally:
        d.quit()


if __name__ == "__main__":
    main()
