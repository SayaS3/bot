import pyautogui as gui
import time
from links import *


def __wait_until_image_is_displayed(image_path, sec, invoice_no=None):
    for _ in range(sec):
        try:
            point = gui.locateOnScreen(image_path, confidence=0.80)
            if point:
                time.sleep(0.1)
                return point
        except gui.ImageNotFoundException:
            pass
        time.sleep(1.0)

    if invoice_no:
        log_error(invoice_no, image_path)
    return False

def log_error(symbol, image_path):
    with open('errors.txt', 'a') as f:
        f.write(f"Faktura: {symbol} - Nie znaleziono zdjecia:  {image_path}\n")

pozycje_dokumentu = __wait_until_image_is_displayed(pozycje_dokumentu_png, 16)
if not pozycje_dokumentu:
    print(f"Skipping invoice {pozycje_dokumentu} as {pozycje_dokumentu_png} not found")
gui.click(pozycje_dokumentu_png, duration=0.5)




