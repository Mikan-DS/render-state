import threading
from pathlib import Path
from urllib.parse import unquote

from selenium import webdriver
import time

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
options.add_extension('adblock.crx')

download_directory = r"C:\Users\Mikan\Downloads"+"\\"


# options.add_argument('--profile-directory=Profile 1')


# headless mode
# options.add_argument("--headless")
# options.headless = True




driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    options=options
)


driver.get("https://render-state.to/")#"https://render-state.to/cat/environments/page/320/")#"https://render-state.to/")


driver.implicitly_wait(3)
driver.implicitly_wait(0)


def is_download_finished(temp_folder):
    # firefox_temp_file = sorted(Path(temp_folder).glob('*.part'))
    chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    if chrome_temp_file:
        return False
    else:
        return True
    # if (len(firefox_temp_file) == 0) and \
    #    (len(chrome_temp_file) == 0):
    #     return True
    # else:
    #     return False

def wait_until_downloaded():
    time.sleep(5)
    while not is_download_finished(download_directory):
        time.sleep(5)
        print("downloading///")

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

    linkdriver.switch_to.new_window('window')
    linkdriver.get(link)


    try:
        btn = WebDriverWait(linkdriver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "js-megasync-download")))

        # element.click();

        # btn = linkdriver.find_elements(By.CLASS_NAME, 'js-megasync-download')
        if btn:
            # input(btn[0].tag_name)
            btn.click()

            return 'Mega downloading'
    except:
        print(link)
        print("NO LINK")


def download_MEDIAFIRE(linkdriver, link):

    # return 0 #TODO


    linkdriver.switch_to.new_window('window')
    linkdriver.get(link)


    try:
        # btn = WebDriverWait(linkdriver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="download_link"]/a[3]')))
        btn =  linkdriver.find_elements(By.ID, 'downloadButton')
        if btn:
            btn[0].click()
        wait_until_downloaded()
        return "MEDIAFIRE downloading"
    except:
        print(link)
        print("NO LINK")


def download_GOOGLE(linkdriver, link):
    linkdriver.switch_to.new_window('window')
    linkdriver.get(link)

    # /html/body/div[3]/div[4]/div/div[3]/div[2]/div[2]/div[3]
    # /html/body/div[3]/div[4]/div/div[3]/div[2]/div[2]/div[3]
    # ndfHFb-c4YZDc-to915-LgbsSe ndfHFb-c4YZDc-C7uZwb-LgbsSe VIpgJd-TzA9Ye-eEGnhe ndfHFb-c4YZDc-LgbsSe ndfHFb-c4YZDc-C7uZwb-LgbsSe-SfQLQb-Bz112c
    #
    try:
        btn = WebDriverWait(linkdriver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[4]/div/div[3]/div[2]/div[2]/div[3]')))
        btn.click()
        linkdriver.implicitly_wait(15)
        linkdriver.find_element(By.ID, "uc-download-link").click()

        wait_until_downloaded()
        # input("DELETE NE 1")
        return "GOOGLE downloading"
    except Exception as e:
        # input("DELETE NE 2")

        print(link)
        print("NO LINK")


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
    try:
    # if 1:
        # link = el.find_element(By.TAG_NAME, 'a').get_attribute('href')

        linkdriver = webdriver.Chrome(
            executable_path="chromedriver.exe",
            options=options
        )

        # time.sleep(1)

        linkdriver.get(link)
        #
        # time.sleep(1)

        # with lock:
        #     for li in linkdriver.find_elements(By.CLASS_NAME, 'local-link'):
        #
        #         sublink = li.get_attribute('href')
        #         links.append((li, sublink))

        for host in linkdriver.find_elements(By.CLASS_NAME, 'ext-link'):
            linkdriver.switch_to.window(linkdriver.window_handles[0])
            print(host.text)

            nxtlink = host.get_attribute("href") \
                .replace("https://render-state.to/exit.php?redirect=https%3A%2F%2F", "https://") \
                .replace("http://render-state.to/exit.php?redirect=http%3A%2F%2F", "http://") \
                .replace("%23", "#") \
                .replace("%2F", "/")

            print(nxtlink)
            for _ in range(20):
                print("Current page", linkdriver.current_url)
                print("Next page", nxtlink)
                if "oaxyteek.net/ad/locked" in linkdriver.current_url and 'render-state.to' in linkdriver.current_url:

                    nxtlink = linkdriver.current_url.split('https%3A%2F%2F')[-1]
                    nxtlink = nxtlink.replace("%23", "#").replace("%2F", "/")
                    print("CUT", nxtlink)


                # https://oaxyteek.net/rweasy/-1/8138182/https://render-state.to/exit.php?redirect=https%3A%2F%2Fwww.mediafire.com%2Ffile%2Fonh9m1ooxpahwnd%2FV3D_Nena_-_G8F_%252526_G8.1F.rar%2Ffile

                elif 'http:' in (nxtlink or ""):
                    # document.getElementById('skip_bu2tton').href
                    print(1)
                    linkdriver.switch_to.new_window('tab')
                    linkdriver.set_page_load_timeout(1)
                    try:
                        linkdriver.get(nxtlink)
                    except TimeoutException as e:
                        pass
                    linkdriver.set_page_load_timeout(30)
                    print(2)
                    # nxtlink = WebDriverWait(linkdriver, 20).until(
                    #     EC.element_to_be_clickable((By.ID, "skip_bu2tton"))).get_attribute('href')
                    for _ in range(10):
                        try:
                            nxtlink = linkdriver.find_element(By.ID, 'skip_bu2tton').get_attribute('href')
                            break
                        except:
                            if "oaxyteek.net/ad/locked" in linkdriver.current_url and 'render-state.to' in linkdriver.current_url:
                                nxtlink = unquote(linkdriver.current_url)
                                for _ in range(10):
                                    nxtlink = unquote(nxtlink)
                                    if not "%" in nxtlink:
                                        break
                                nxtlink = 'https://'+nxtlink.split('https://')[-1]
                                print("CUT in WAIT", nxtlink)
                                linkdriver.switch_to.window(linkdriver.window_handles[0])
                                break
                            time.sleep(1)


                elif "oaxyteek.net/ad/locked" in (nxtlink or ""):

                    nxtlink = linkdriver.find_element(By.ID, 'continue').find_element(By.TAG_NAME, 'a').get_attribute('href').split('https%3A%2F%2F')[-1]
                    nxtlink = nxtlink.replace("%23", "#").replace("%2F", "/")

                elif "oaxyteek.net/red" in (nxtlink or ""):
                    if len(linkdriver.window_handles) < 2:
                        linkdriver.switch_to.new_window('tab')
                    else:
                        linkdriver.switch_to.window(linkdriver.window_handles[-1])

                    linkdriver.get(nxtlink)
                    nxtlink = linkdriver.find_element(By.TAG_NAME, "a").get_attribute("href") \
                        .replace("https://render-state.to/exit.php?redirect=https%3A%2F%2F", "https://") \
                        .replace("http://render-state.to/exit.php?redirect=http%3A%2F%2F", "http://") \
                        .replace("%23", "#") \
                        .replace("%2F", "/")

                elif not nxtlink:
                    for meta in linkdriver.find_elements(By.TAG_NAME, 'meta'):
                        try:
                            cnt = meta.get_attribute("content")
                            if "render-state" in cnt:
                                nxtlink = unquote(linkdriver.current_url)
                                for _ in range(10):
                                    nxtlink = unquote(nxtlink)
                                    if not "%" in nxtlink:
                                        break
                                nxtlink = 'https://' + nxtlink.split('https://')[-1]
                                print("TAKE FROM META", nxtlink)
                                linkdriver.switch_to.window(linkdriver.window_handles[0])
                                break
                        except:
                            pass #https://render-state.to/post/derelict-spaceship-corridors/
                    else: #https://render-state.to/cat/environments/page/53/
                        input("NEW DEFEND???")
                else:
                    linkdriver.switch_to.window(linkdriver.window_handles[0])
                    break
            else:
                linkdriver.switch_to.window(linkdriver.window_handles[0])

            if host.text == "MEGA":


                print(nxtlink)
                if download_MEGA(linkdriver, nxtlink):
                    break
            elif host.text == "MEDIAFIRE":
                if download_MEDIAFIRE(linkdriver, nxtlink):
                    break
            elif host.text == "GOOGLE DRIVE":
                if download_GOOGLE(linkdriver, nxtlink):
                    break
            else:
                input(" ".join(("NEEEEEEED HELP!!!!!!!!!!", nxtlink, link)))
        else:

            try:
                driver.execute_script(
                    """arguments[0].innerHTML = 'Доступных ссылок нет'; arguments[0].classList.toggle("findme", false);""",
                    el.find_elements(By.CLASS_NAME, 'sedownload')[0])
            except:
                pass

        try:
            driver.execute_script(
                """arguments[0].innerHTML = 'Ссылка найдена'; arguments[0].classList.toggle("findme", false);""", el.find_elements(By.CLASS_NAME, 'sedownload')[0])
        except:
            pass


    except Exception as e:
        raise e
        print(repr(e))


        try:
            a_link = el.find_elements(By.CLASS_NAME, 'sedownload')
            driver.execute_script(
                """arguments[0].innerHTML = 'Произошла ошибка'; arguments[0].classList.toggle("findme", false);""", a_link[0])
        except:
            pass
    try:
        linkdriver.close()
        print("SUCES")
        print(linkdriver.window_handles)
    except Exception as e:
        print('[-] on close', repr(e))



lock = threading.Lock()
links = []

def downloader():

    while 1:
        if links:
            print('CURRENT LIST\n', "\n".join([str(i) for j, i in links]))
            with lock:
                link = links.pop(0)
            try:
                driver.execute_script(
                    """arguments[0].innerHTML = 'Поиск ссылок'; arguments[0].classList.toggle("findme", false);""",
                    a_link[0])
            except:
                pass
            try:

                try_to_download(link)
            except Exception as e:
                print('[-] try_to_download(link)', repr(e))
                print('DOWNLOAD', link)
            print("EXIT")

        time.sleep(2)


threading.Thread(target=downloader).start()


while True:

    if not driver.find_elements(By.CLASS_NAME, 'sedownload'):
        add_links()
    for article in driver.find_elements(By.CLASS_NAME, 'excerpt'):
        try:
            a_link = article.find_elements(By.CLASS_NAME, 'findme')
            if a_link:


                with lock:
                    # try_to_download(article)
                    driver.execute_script(
                        """arguments[0].innerHTML = 'В очереди'; arguments[0].classList.toggle("findme", false);""",
                        a_link[0])
                    links.append((article, article.find_element(By.TAG_NAME, 'a').get_attribute('href')))#.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print('[+] ', "Добавлена ссылка", links[-1][-1])
        except Exception as e:
            print('[-]', repr(e))
    time.sleep(1)


# try_to_download("https://render-state.to/post/v3d-nena-g8f-g8-1f/")
# https://render-state.to/cat/environments/page/98/
# https://render-state.to/?s=Eclipse+The+White+Room