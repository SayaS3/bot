import pyautogui as gui
import time
from links import *
from DatabaseConnector import DatabaseConnector

db = DatabaseConnector()

db.connect()
invoices = db.fetch_invoices()


def __wait_until_image_is_displayed(image_path, sec, invoice_no=None):
    for _ in range(sec):
        try:
            point = gui.locateOnScreen(image_path, confidence=0.8)
            if point:
                time.sleep(0.1)
                return point
        except gui.ImageNotFoundException:
            pass
        time.sleep(1.0)

    if invoice_no:
        log_error(invoice_no, image_path)
    return False


def partial_correct_invoice(symbol, numeriai, sku_list):
    try:
        time.sleep(5)
        gui.hotkey('altleft')  # kartoteka FSN
        gui.hotkey('altleft', '0')  # kartoteka FSN
        time.sleep(2)
        gui.hotkey('ctrl', 'f12')  # kasowanie filtra
        time.sleep(2)
        gui.press('enter')
        time.sleep(2)

        symbol_point = __wait_until_image_is_displayed(symbol_png, 16, symbol)
        if not symbol_point:
            print(f"Skipping invoice {symbol} as {symbol_png} not found")
            close_window(symbol)
            return False
        print(f"Found {symbol_png} at {symbol_point}")
        gui.click(symbol_point, duration=0.25)
        gui.write(' ' + ' ' + str(symbol).upper(), interval=0.25)
        gui.press("enter")
        time.sleep(2)
        gui.moveRel(-30, 50, duration=0.25)
        gui.click()

        time.sleep(2)
        skoryguj = __wait_until_image_is_displayed(skoryguj_png, 16, symbol)
        if not skoryguj:
            print(f"Skipping invoice {symbol} as {skoryguj_png} not found")
            close_window(symbol)
            return False
        print(f"Found {skoryguj_png} at {skoryguj}")
        gui.click(skoryguj, duration=0.25)
        time.sleep(2)
        bez_zerowania_ilosci = __wait_until_image_is_displayed(bez_zerowania_ilosci_png, 16, symbol)
        if not bez_zerowania_ilosci:
            print(f"Skipping invoice {symbol} as {bez_zerowania_ilosci_png} not found")
            close_window(symbol)
            return False
        gui.click(bez_zerowania_ilosci, duration=0.25)
        yes = __wait_until_image_is_displayed(yes_png, 16, symbol)
        if not yes:
            print(f"Skipping invoice {symbol} as {yes_png} not found")
            close_window(symbol)
            return False
        gui.press("enter")

        kfs = __wait_until_image_is_displayed(KFS_png, 16)
        if not kfs:
            print(f"Skipping invoice {symbol} as {KFS_png} not found")
            close_window(symbol)
            return False
        print(f"Found {KFS_png} at {kfs}")

        for single_sku in sku_list:
            lp_values = db.fetch_lp_for_invoice(numeriai, single_sku.strip())
            for lp in lp_values:
                pozycje_dokumentu = __wait_until_image_is_displayed(pozycje_dokumentu_png, 16)
                if not pozycje_dokumentu:
                    print(f"Skipping invoice {symbol} as {pozycje_dokumentu_png} not found")
                    close_window(symbol)
                    return False
                print(f"Found {pozycje_dokumentu_png} at {pozycje_dokumentu}")
                time.sleep(2)
                gui.doubleClick(pozycje_dokumentu, duration=0.5)
                gui.hotkey('backspace')
                gui.write(str(lp), interval=0.7)
                gui.press('enter')
                time.sleep(2)
                ilosc = __wait_until_image_is_displayed(ilosc_png, 16)
                if not ilosc:
                    print(f"Skipping invoice {symbol} as {ilosc_png} not found")
                    close_window(symbol)
                    return False
                time.sleep(2)
                gui.click(ilosc, duration=0.4)
                gui.hotkey('right')
                gui.hotkey('backspace')
                gui.write('-1', interval=0.5)

        pozostale = __wait_until_image_is_displayed(pozostale_png, 16, symbol)
        if not pozostale:
            print(f"Skipping invoice {symbol} as {pozostale_png} not found")
            close_window(symbol)
            return False
        print(f"Found {pozostale_png} at {pozostale}")
        gui.click(pozostale)

        przyczyna_korekty = __wait_until_image_is_displayed(przyczyna_korekty_png, 16, symbol)
        if not przyczyna_korekty:
            print(f"Skipping invoice {symbol} as {przyczyna_korekty_png} not found")
            close_window(symbol)
            return False
        print(f"Found {przyczyna_korekty_png} at {przyczyna_korekty}")
        gui.moveTo(przyczyna_korekty.left + 10, przyczyna_korekty.top)
        gui.click(przyczyna_korekty)
        gui.press(['1', 'enter', 'enter'], interval=3)

        fakture_odebral = __wait_until_image_is_displayed(fakture_odebral_png, 16, symbol)
        if not fakture_odebral:
            print(f"Skipping invoice {symbol} as {fakture_odebral_png} not found")
            close_window(symbol)
            return False
        print(f"Found {fakture_odebral_png} at {fakture_odebral}")
        gui.click(fakture_odebral)
        gui.write('*', interval=0.25)

        sprzedaz_wysylkowa = __wait_until_image_is_displayed(sprzedaz_wysylkowa_png, 16, symbol)
        if not sprzedaz_wysylkowa:
            print(f"Skipping invoice {symbol} as {sprzedaz_wysylkowa_png} not found")
            close_window(symbol)
            return False
        print(f"Found {sprzedaz_wysylkowa_png} at {sprzedaz_wysylkowa}")
        gui.click(sprzedaz_wysylkowa)

        pobierz_dane = __wait_until_image_is_displayed(pobierz_dane_png, 16, symbol)
        if not pobierz_dane:
            print(f"Skipping invoice {symbol} as {pobierz_dane_png} not found")
            close_window(symbol)
            return False
        print(f"Found {pobierz_dane_png} at {pobierz_dane}")
        gui.click(pobierz_dane)
        time.sleep(3)
        gui.press('f11')
        pytanie_czy_zatwierdzic = __wait_until_image_is_displayed(pytanie_czy_zatwierdzic_png, 16, symbol)
        if not pytanie_czy_zatwierdzic:
            print(f"Skipping invoice {symbol} as {pytanie_czy_zatwierdzic_png} not found")
            close_window(symbol)
            return False
        gui.press('enter')

        time.sleep(3)
        drukowanie = __wait_until_image_is_displayed(drukowanie_png, 20, symbol)
        if not drukowanie:
            print(f"Skipping invoice {symbol} as {drukowanie_png} not found")
            close_window(symbol)
            return False
        gui.click(drukowanie, duration=0.25)
        if __wait_until_image_is_displayed(zastosuj_clicked_png, 12, symbol):
            drukuj = __wait_until_image_is_displayed(drukuj_png, 12, symbol)
            if not drukuj:
                print(f"Skipping invoice {symbol} as {drukuj_png} not found")
                close_window(symbol)
                return False
            gui.click(drukuj)
            zapisywanie_wydruku = __wait_until_image_is_displayed(zapisywanie_wydruku_png, 20, symbol)
            nazwa_pliku = __wait_until_image_is_displayed(nazwa_pliku_png, 20, symbol)
            if not (nazwa_pliku or zapisywanie_wydruku):
                print(f"Skipping invoice {symbol} as {nazwa_pliku_png} or {zapisywanie_wydruku_png} not found")
                close_window(symbol)
                return False
            gui.write(str(symbol).replace('/', '_'), interval=0.25)  # wpisanie nazwy pliku
            time.sleep(5)
            gui.hotkey('altleft', 'z')  # zapisanie .pdf
            time.sleep(2)

        return True
    except Exception as e:
        print(f"Error processing invoice {symbol}: {e}")
        return False


def open_teta():
    gui.hotkey('winleft', 'd')
    time.sleep(2)
    point = __wait_until_image_is_displayed(frog_png, 10)
    if point:
        print(f"Found {frog_png} at {point}")
        gui.doubleClick(point, duration=0.5)

        if __wait_until_image_is_displayed(logowanie_png, 10):
            print(f"Found {logowanie_png} at {gui.locateOnScreen(logowanie_png, confidence=0.85)}")
            gui.press('enter')
            print("pressed enter")


def close_teta():
    gui.hotkey('altleft', 'f4')


def close_window(symbol):
    okno = __wait_until_image_is_displayed(okno_png, 20, symbol)
    if not okno:
        print(f"Skipping invoice {symbol} as {okno_png} not found")
        return False
    gui.click(okno)
    gui.press(['up', 'enter'])


def log_error(symbol, image_path):
    with open('errors.txt', 'a') as f:
        f.write(f"Faktura: {symbol} - Nie znaleziono zdjecia:  {image_path}\n")


def correct_invoice(symbol):
    try:
        time.sleep(5)
        gui.hotkey('altleft')  # kartoteka FSN
        gui.hotkey('altleft', '0')  # kartoteka FSN
        time.sleep(2)
        gui.hotkey('ctrl', 'f12')  # kasowanie filtra
        time.sleep(2)
        gui.press('enter')

        symbol_point = __wait_until_image_is_displayed(symbol_png, 16, symbol)
        if not symbol_point:
            print(f"Skipping invoice {symbol} as {symbol_png} not found")
            close_window(symbol)
            return False
        print(f"Found {symbol_png} at {symbol_point}")
        gui.click(symbol_point, duration=0.25)
        gui.write(' ' + ' ' + str(symbol).upper(), interval=0.25)
        gui.press("enter")
        time.sleep(2)
        gui.moveRel(-30, 50, duration=0.25)
        gui.click()

        time.sleep(3)
        skoryguj = __wait_until_image_is_displayed(skoryguj_png, 16, symbol)
        if not skoryguj:
            print(f"Skipping invoice {symbol} as {skoryguj_png} not found")
            close_window(symbol)
            return False
        print(f"Found {skoryguj_png} at {skoryguj}")
        gui.click(skoryguj, duration=0.25)
        time.sleep(2)
        zeruj_ilosci = __wait_until_image_is_displayed(zeruj_ilosci_png, 16, symbol)
        if not zeruj_ilosci:
            print(f"Skipping invoice {symbol} as {zeruj_ilosci_png} not found")
            close_window(symbol)
            return False
        gui.click(zeruj_ilosci, duration=0.25)
        yes = __wait_until_image_is_displayed(yes_png, 16, symbol)
        if not yes:
            print(f"Skipping invoice {symbol} as {yes_png} not found")
            close_window(symbol)
            return False
        gui.press("enter")

        kfs = __wait_until_image_is_displayed(KFS_png, 16)
        if not kfs:
            print(f"Skipping invoice {symbol} as {KFS_png} not found")
            close_window(symbol)
            return False
        print(f"Found {KFS_png} at {kfs}")

        pozostale = __wait_until_image_is_displayed(pozostale_png, 16, symbol)
        if not pozostale:
            print(f"Skipping invoice {symbol} as {pozostale_png} not found")
            close_window(symbol)
            return False
        print(f"Found {pozostale_png} at {pozostale}")
        gui.click(pozostale)

        przyczyna_korekty = __wait_until_image_is_displayed(przyczyna_korekty_png, 16, symbol)
        if not przyczyna_korekty:
            print(f"Skipping invoice {symbol} as {przyczyna_korekty_png} not found")
            close_window(symbol)
            return False
        print(f"Found {przyczyna_korekty_png} at {przyczyna_korekty}")
        gui.moveTo(przyczyna_korekty.left + 10, przyczyna_korekty.top)
        gui.click(przyczyna_korekty)
        gui.press(['1', 'enter', 'enter'], interval=3)

        fakture_odebral = __wait_until_image_is_displayed(fakture_odebral_png, 16, symbol)
        if not fakture_odebral:
            print(f"Skipping invoice {symbol} as {fakture_odebral_png} not found")
            close_window(symbol)
            return False
        print(f"Found {fakture_odebral_png} at {fakture_odebral}")
        gui.click(fakture_odebral)
        gui.write('*', interval=0.25)

        sprzedaz_wysylkowa = __wait_until_image_is_displayed(sprzedaz_wysylkowa_png, 16, symbol)
        if not sprzedaz_wysylkowa:
            print(f"Skipping invoice {symbol} as {sprzedaz_wysylkowa_png} not found")
            close_window(symbol)
            return False
        print(f"Found {sprzedaz_wysylkowa_png} at {sprzedaz_wysylkowa}")
        gui.click(sprzedaz_wysylkowa)

        pobierz_dane = __wait_until_image_is_displayed(pobierz_dane_png, 16, symbol)
        if not pobierz_dane:
            print(f"Skipping invoice {symbol} as {pobierz_dane_png} not found")
            close_window(symbol)
            return False
        print(f"Found {pobierz_dane_png} at {pobierz_dane}")
        gui.click(pobierz_dane)
        time.sleep(5)
        gui.press('f11')
        pytanie_czy_zatwierdzic = __wait_until_image_is_displayed(pytanie_czy_zatwierdzic_png, 16, symbol)
        if not pytanie_czy_zatwierdzic:
            print(f"Skipping invoice {symbol} as {pytanie_czy_zatwierdzic_png} not found")
            close_window(symbol)
            return False
        print(f"Found {pytanie_czy_zatwierdzic} at {pytanie_czy_zatwierdzic}")
        gui.press('enter')

        # Drukowanie
        time.sleep(5)
        drukowanie = __wait_until_image_is_displayed(drukowanie_png, 20, symbol)
        if not drukowanie:
            print(f"Skipping invoice {symbol} as {drukowanie_png} not found")
            close_window(symbol)
            return False
        gui.click(drukowanie, duration=0.25)
        if __wait_until_image_is_displayed(zastosuj_clicked_png, 12, symbol):
            drukuj = __wait_until_image_is_displayed(drukuj_png, 12, symbol)
            if not drukuj:
                print(f"Skipping invoice {symbol} as {drukuj_png} not found")
                close_window(symbol)
                return False
            gui.click(drukuj)
            zapisywanie_wydruku = __wait_until_image_is_displayed(zapisywanie_wydruku_png, 20, symbol)
            nazwa_pliku = __wait_until_image_is_displayed(nazwa_pliku_png, 20, symbol)
            if not (nazwa_pliku or zapisywanie_wydruku):
                print(f"Skipping invoice {symbol} as {nazwa_pliku_png} or {zapisywanie_wydruku_png} not found")
                close_window(symbol)
                return False
            gui.write(str(symbol).replace('/', '_'), interval=0.25)  # wpisanie nazwy pliku
            time.sleep(6)
            gui.hotkey('altleft', 'z')  # zapisanie .pdf
            time.sleep(2)

        return True
    except Exception as e:
        print(f"Error processing invoice {symbol}: {e}")
        return False


if not invoices:
    print("Brak faktur do skorygowania.")
else:
    open_teta()

    start_job = time.time()
    for invoice in invoices:
        start = time.time()
        symbol = invoice[5]
        sku_list = invoice[2].split(',')
        numeriai = invoice[1]
        calosc = invoice[6]
        print(f"Processing invoice: {invoice}")
        if calosc == 'tak':
            if correct_invoice(symbol.upper()):
                db.update_invoice_status(symbol)
            else:
                print(f"Failed to update status of invoice: {invoice}")
        if calosc == 'nie':
            if partial_correct_invoice(symbol, numeriai, sku_list):
                db.update_invoice_status(symbol)
            else:
                print(f"Failed to update status of invoice: {invoice}")
        print(f"end of looping item: {invoice}")
        end = time.time()
        print(f'Order {invoice} finished in: ', time.strftime("%H:%M:%S", time.gmtime(end - start)) + '\n')

    end_job = time.time()
    print('Job finished in: ', time.strftime("%H:%M:%S", time.gmtime(end_job - start_job)))
    print('\n')
    db.close()
    close_teta()
