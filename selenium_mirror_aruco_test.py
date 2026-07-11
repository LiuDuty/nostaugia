from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


opts = Options()
opts.add_argument("--headless=new")
d = webdriver.Chrome(options=opts)
try:
    d.get("http://127.0.0.1:8765/puzzle40-ghost5.html")
    WebDriverWait(d, 25).until(lambda x: x.execute_script("return !!window.AR && !!arucoDict"))
    result = d.execute_async_script(
        r"""
        const done = arguments[0];
        const markerEl = document.querySelector('.aruco-marker svg');
        const svg = markerEl.outerHTML.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ');
        const img = new Image();
        const markup = '<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240">'
          + '<rect width="240" height="240" fill="white"/>'
          + '<g transform="translate(40 40) scale(4)">' + svg + '</g></svg>';
        img.onload = () => {
          const det = new AR.Detector({dictionaryName:'ARUCO'});
          const c = document.createElement('canvas');
          c.width = 240;
          c.height = 240;
          const x = c.getContext('2d', {willReadFrequently:true});
          x.drawImage(img, 0, 0);
          const normal = det.detect(x.getImageData(0, 0, 240, 240)).map(m => m.id);
          x.clearRect(0, 0, 240, 240);
          x.save();
          x.translate(240, 0);
          x.scale(-1, 1);
          x.drawImage(img, 0, 0);
          x.restore();
          const mirrored = det.detect(x.getImageData(0, 0, 240, 240)).map(m => m.id);
          done(JSON.stringify({normal, mirrored}));
        };
        img.onerror = () => done('IMG_ERROR');
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(markup);
        """
    )
    print(result)
finally:
    d.quit()
