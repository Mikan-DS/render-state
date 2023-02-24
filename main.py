import threading
import time
from pathlib import Path
from urllib.parse import unquote

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument(r'user-data-dir=C:\Users\Mikan\PycharmProjects\render-state\Selpro\Main')
options.add_extension('adblock.crx')



download_directory = r"C:\Users\Mikan\Downloads" + "\\"


driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    options=options
)

driver.get("https://render-state.to/cat/environments/page/17/?s=sci-fi")#https://render-state.to/")

driver.implicitly_wait(3)
driver.implicitly_wait(0)

debug = False
show = True


def is_download_finished(temp_folder):
    chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    if chrome_temp_file:
        return False
    else:
        return True


def wait_until_downloaded():
    time.sleep(5)
    while not is_download_finished(download_directory):
        time.sleep(5)
        print("downloading...")


def add_links():
    driver.execute_script("""
    
    function addToFindList(el) {
        this.classList.toggle("findme", true); this.innerHTML = 'Обработка';
    }
    
    for (let e of document.getElementsByClassName("excerpt")) {
        btn = document.createElement("button");
        btn.innerHTML = 'Скачать';
        btn.classList.toggle("sedownload", true);
        btn.onclick = addToFindList//(x) => {btn.classList.toggle("findme", true); btn.innerHTML = 'Поиск ссылок'; console.log(x)};
        e.appendChild(btn);
        
    }
    
    """)


def download_MEGA(linkdriver, link):
    # return 0 #TODO

    print("[+] Enter MEGA", link)

    linkdriver.switch_to.new_window('window')
    linkdriver.get(link)

    try:
        btn = WebDriverWait(linkdriver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "js-megasync-download")))

        assert btn, '[-] Button dissapear'
        linkdriver.find_element(By.CLASS_NAME, "js-megasync-download").click()
        print('[+] Download sended to MEGASync')
        return 'Mega downloading'

    except Exception as e:
        if debug:
            raise e
        print("[-] No link found")


def download_MEDIAFIRE(linkdriver, link):
    # return 0 #TODO
    print("[+] Enter MEDIAFIRE", link)

    linkdriver.switch_to.new_window('window')
    linkdriver.get(link)

    try:

        btn = linkdriver.find_elements(By.ID, 'downloadButton')
        assert btn, '[-] Button dissapear'
        btn[0].click()
        print('[+] Download started from MEDIAFIRE')
        wait_until_downloaded()
        return "MEDIAFIRE downloading"
    except:
        if not is_download_finished(download_directory):
            wait_until_downloaded()
            return "MEDIAFIRE downloading"
        else:
            if debug:
                raise e
            print("[-] No link found")


def download_GOOGLE(linkdriver, link):

    print("[+] Enter GOOGLE", link)

    linkdriver.switch_to.new_window('window')
    # linkdriver.get(link)

    try:
        # btn = WebDriverWait(linkdriver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[4]/div/div[3]/div[2]/div[2]/div[3]')))
        # btn.click()
        # linkdriver.implicitly_wait(15)
        # linkdriver.find_element(By.ID, "uc-download-link").click()
        link = "https://drive.google.com/uc?id="+link.split('/')[-2]+"&export=download"
        linkdriver.get(link)


        btn = WebDriverWait(linkdriver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "uc-download-link"]')))
        btn.click()
        print('[+] Download started from GOOGLE')
        wait_until_downloaded()
        return "GOOGLE downloading"
    except Exception as e:
        if not is_download_finished(download_directory):
            wait_until_downloaded()
            return "GOOGLE downloading"
        else:
            if debug:
                raise e
            print("[-] No link found")


def get_redirect(link):
    for _ in range(30):
        if not "%" in link:
            break
        link = unquote(link or "")
    return "http"+link.split("http")[-1]

def get_real_link(linkdriver, nxtlink):

    initial_window = linkdriver.current_window_handle
    # http://ay.gy/8138182/_eaHR0cHM6Ly9yZW5kZXItc3RhdGUudG8vZXhpdC5waHA/cmVkaXJlY3Q9aHR0cHMlM0ElMkYlMkZtZWdhLm56JTJGZmlsZSUyRkFQUVUySlRUJTIzZlBvbUY4cnVxRlgxVy1uMEpuWmpCbnVIWW0wOUZ5MnhtTTNoaHliSDloNA==
    linkdriver.switch_to.new_window('window')

    print("[+] Entering link battle", nxtlink)

    for _ in range(20):
        nxtlink = get_redirect(nxtlink)
        print("", nxtlink, linkdriver.current_url, sep="\n-")


        if "http:" in nxtlink:
            if 'oaxyteek' in linkdriver.current_url:
                for meta in linkdriver.find_elements(By.XPATH, '//*[@id="main_html"]/head/meta'):
                    try:
                        cont = meta.get_attribute('content')
                        if 'render-state.to' in cont:
                            nxtlink = cont
                            linkdriver.get(nxtlink)
                            print("[~] META CUT", nxtlink)
                            break
                        elif 'redirect' in cont:
                            print("[~] GOING IN META", nxtlink)
                            linkdriver.set_page_load_timeout(4)
                            try:
                                linkdriver.get(nxtlink)
                            except TimeoutException as e:
                                pass
                            linkdriver.set_page_load_timeout(30)
                        # elif linkdriver.find_elements(By.CLASS_NAME, 'sm_content'):
                        #     if meta.get_attribute('property') == "og:url":

                    except:
                        pass
                else:
                    for cont in linkdriver.find_elements(By.ID, 'continue'):
                        for lnk in cont.find_elements(By.TAG_NAME, 'a'):
                            nxtlink = lnk.get_attribute('href')
                            linkdriver.get(nxtlink)
                            print("[~] CUT v1", nxtlink)
                            break
                    for lnk in linkdriver.find_elements(By.ID, 'skip_bu2tton'):
                        nxtlink = lnk.get_attribute('href')
                        linkdriver.get(nxtlink)
                        print("[~] CUT v2", nxtlink)
                        break



            else:

                print("[~] GOING IN", nxtlink)
                linkdriver.set_page_load_timeout(4)
                try:
                    linkdriver.get(nxtlink)
                except TimeoutException as e:
                    pass
                linkdriver.set_page_load_timeout(30)
        else:
            print("[+] Battle win", nxtlink)
            linkdriver.switch_to.window(initial_window)
            return nxtlink
    print("[-] Battle lose")
    raise Exception("NEW DEFENDER")

        # nxtlink = nxtlink \
    #     .replace("https://render-state.to/exit.php?redirect=https%3A%2F%2F", "https://") \
    #     .replace("http://render-state.to/exit.php?redirect=http%3A%2F%2F", "http://") \
    #     .replace("%23", "#") \
    #     .replace("%2F", "/")
    #
    # print(nxtlink)
    # for _ in range(20):
    #     print("Current page", linkdriver.current_url)
    #     print("Next page", nxtlink)
    #     if "oaxyteek.net/ad/locked" in linkdriver.current_url and 'render-state.to' in linkdriver.current_url:
    #
    #         nxtlink = linkdriver.current_url.split('https%3A%2F%2F')[-1]
    #         nxtlink = nxtlink.replace("%23", "#").replace("%2F", "/")
    #         print("CUT", nxtlink)
    #
    #
    #     # https://oaxyteek.net/rweasy/-1/8138182/https://render-state.to/exit.php?redirect=https%3A%2F%2Fwww.mediafire.com%2Ffile%2Fonh9m1ooxpahwnd%2FV3D_Nena_-_G8F_%252526_G8.1F.rar%2Ffile
    #
    #     elif 'http:' in (nxtlink or ""):
    #         # document.getElementById('skip_bu2tton').href
    #         print(1)
    #         linkdriver.switch_to.new_window('tab')
    #         linkdriver.set_page_load_timeout(1)
    #         try:
    #             linkdriver.get(nxtlink)
    #         except TimeoutException as e:
    #             pass
    #         linkdriver.set_page_load_timeout(30)
    #         print(2)
    #         # nxtlink = WebDriverWait(linkdriver, 20).until(
    #         #     EC.element_to_be_clickable((By.ID, "skip_bu2tton"))).get_attribute('href')
    #         for _ in range(10):
    #             try:
    #                 nxtlink = linkdriver.find_element(By.ID, 'skip_bu2tton').get_attribute('href')
    #                 break
    #             except:
    #                 if "oaxyteek.net/ad/locked" in linkdriver.current_url and 'render-state.to' in linkdriver.current_url:
    #                     nxtlink = unquote(linkdriver.current_url)
    #                     for _ in range(10):
    #                         nxtlink = unquote(nxtlink)
    #                         if not "%" in nxtlink:
    #                             break
    #                     nxtlink = 'https://' + nxtlink.split('https://')[-1]
    #                     print("CUT in WAIT", nxtlink)
    #                     linkdriver.switch_to.window(linkdriver.window_handles[0])
    #                     break
    #                 time.sleep(1)
    #
    #
    #     elif "oaxyteek.net/ad/locked" in (nxtlink or ""):
    #
    #         nxtlink = linkdriver.find_element(By.ID, 'continue').find_element(By.TAG_NAME, 'a').get_attribute(
    #             'href').split('https%3A%2F%2F')[-1]
    #         nxtlink = nxtlink.replace("%23", "#").replace("%2F", "/")
    #
    #     elif "oaxyteek.net/red" in (nxtlink or ""):
    #         if len(linkdriver.window_handles) < 2:
    #             linkdriver.switch_to.new_window('tab')
    #         else:
    #             linkdriver.switch_to.window(linkdriver.window_handles[-1])
    #
    #         linkdriver.get(nxtlink)
    #         nxtlink = linkdriver.find_element(By.TAG_NAME, "a").get_attribute("href") \
    #             .replace("https://render-state.to/exit.php?redirect=https%3A%2F%2F", "https://") \
    #             .replace("http://render-state.to/exit.php?redirect=http%3A%2F%2F", "http://") \
    #             .replace("%23", "#") \
    #             .replace("%2F", "/")
    #
    #     elif not nxtlink:
    #         for meta in linkdriver.find_elements(By.TAG_NAME, 'meta'):
    #             try:
    #                 cnt = meta.get_attribute("content")
    #                 if "render-state" in cnt:
    #                     nxtlink = unquote(linkdriver.current_url)
    #                     for _ in range(10):
    #                         nxtlink = unquote(nxtlink)
    #                         if not "%" in nxtlink:
    #                             break
    #                     nxtlink = 'https://' + nxtlink.split('https://')[-1]
    #                     print("TAKE FROM META", nxtlink)
    #                     linkdriver.switch_to.window(linkdriver.window_handles[0])
    #                     break
    #             except:
    #                 pass  # https://render-state.to/post/derelict-spaceship-corridors/
    #         else:  # https://render-state.to/cat/environments/page/53/
    #             input("NEW DEFEND???")
    #     else:
    #         linkdriver.switch_to.window(linkdriver.window_handles[0])
    #         break
    # else:
    #     linkdriver.switch_to.window(linkdriver.window_handles[0])


def try_to_download(ellink):
    el, link = ellink
    # options
    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(r'user-data-dir=C:\Users\Mikan\PycharmProjects\render-state\Selpro\Profile 2')
    options.add_extension('adblock.crx')

    if not show:
        options.add_argument("--headless=new")

    try:

        linkdriver = webdriver.Chrome(
            executable_path="chromedriver.exe",
            options=options
        )

        linkdriver.get(link)

        for sublink in linkdriver.find_elements(By.CLASS_NAME, 'local-link'):
            with lock:
                links.append((None, sublink.get_attribute('href')))
                print("[+] Add request resource link: ", links[-1][1])

        for host in linkdriver.find_elements(By.CLASS_NAME, 'ext-link'):
            linkdriver.switch_to.window(linkdriver.window_handles[0])
            print(host.text)

            nxtlink = get_real_link(linkdriver, host.get_attribute("href"))

            if "MEGA" in host.text:
                if download_MEGA(linkdriver, nxtlink):
                    break
            elif "MEDIAFIRE" in host.text:
                if download_MEDIAFIRE(linkdriver, nxtlink):
                    break
            elif host.text == "GOOGLE DRIVE" or "GDRIVE" in host.text:
                if download_GOOGLE(linkdriver, nxtlink):
                    break
            else:
                print("[-] UNKNOWN LINK", link, nxtlink)
                # input(" ".join(("NEEEEEEED HELP!!!!!!!!!!", nxtlink, link)))
        else:

            try:
                driver.execute_script(
                    """arguments[0].innerHTML = 'Доступных ссылок нет'; arguments[0].classList.toggle("findme", false);""",
                    el.find_elements(By.CLASS_NAME, 'sedownload')[0])
            except:
                pass

        try:
            driver.execute_script(
                """arguments[0].innerHTML = 'Ссылка найдена'; arguments[0].classList.toggle("findme", false);""",
                el.find_elements(By.CLASS_NAME, 'sedownload')[0])
        except:
            pass

        try:
            for _ in linkdriver.window_handles:
                linkdriver.quit()
        except Exception as e:
            if debug:
                raise e
            print('[-] Cannot close download window after download', repr(e))


        return True


    except Exception as e:
        if debug:
            raise e
        print('[-] Download fails: ', repr(e))

        try:
            a_link = el.find_elements(By.CLASS_NAME, 'sedownload')
            driver.execute_script(
                """arguments[0].innerHTML = 'Произошла ошибка'; arguments[0].classList.toggle("findme", false);""",
                a_link[0])
        except:
            pass
    try:
        for _ in linkdriver.window_handles:
            linkdriver.quit()
    except Exception as e:
        if debug:
            raise e
        print('[-] Cannot close download window', repr(e))


def downloader():
    while True:
        if links:
            print('CURRENT LIST:\n\n', "\n".join([str(i) for j, i in links]))
            with lock:
                link = links.pop(0)
            try:
                driver.execute_script(
                    """arguments[0].innerHTML = 'Поиск ссылок'; arguments[0].classList.toggle("findme", false);""",
                    a_link[0])
            except:
                pass
            try:
                # pass
                assert try_to_download(link)

            except Exception as e:
                if debug:
                    raise e
                print()
                print('[-] Problem with download:', repr(e))
                print('LINK:', link[1])
                print()


        time.sleep(2)

if __name__ == "__main__":
    lock = threading.Lock()
    links = []
    threading.Thread(target=downloader).start()

    while True:

        if not driver.find_elements(By.CLASS_NAME, 'sedownload'):
            add_links()
        for article in driver.find_elements(By.CLASS_NAME, 'excerpt'):
            try:
                a_link = article.find_elements(By.CLASS_NAME, 'findme')
                if a_link:
                    with lock:
                        driver.execute_script(
                            """arguments[0].innerHTML = 'В очереди'; arguments[0].classList.toggle("findme", false);""",
                            a_link[0])
                        links.append((article, article.find_element(By.TAG_NAME, 'a').get_attribute('href')))
                        print("[+] New link in query: ", links[-1][-1])
            except Exception as e:
                print('[-] Main cycle: ', repr(e))

        time.sleep(1)

# https://render-state.to/cat/environments/page/98/
# mediafire если попасть на страницу во время зачистки все ломается, прописать 4 сервис, отдельный список с сервисами