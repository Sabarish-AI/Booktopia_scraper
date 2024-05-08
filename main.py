import time,os,requests,socket,random,pychrome,html,re,csv
from datetime import datetime
def getRandomPort():
    while True:
        port = random.randint(1000, 35000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            continue
        else:
            return port
        sock.close()
def extract_book_info(html_content):
    title_pattern = r'<h1\s+class="[^"]*MuiTypography-root[^"]*">(.*?)</h1>'
    author_pattern = r'<span class="MuiTypography-root MuiTypography-body1 mui-style-1plnxgp">(.*?)</span>'
    book_type_pattern_ebook_paperback = r'<p class="MuiTypography-root MuiTypography-body1 mui-style-tgrox">(eBook|Paperback)\s*\|.*?</p>'
    original_price_pattern = r'<span class="strike">\$(\d+\.\d+)</span>'
    discounted_price_pattern = r'<p class="MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox">\$([\d.]+)</p>'
    isbn_10_pattern = r'<span class="MuiTypography-root MuiTypography-body1 detail-label mui-style-tgrox">ISBN-10<!-- -->: </span>(.*?)</p>'
    published_date_pattern = r'<span class="MuiTypography-root MuiTypography-body1 detail-label mui-style-tgrox">Published<!-- -->: </span>(.*?)</p>'
    publisher_pattern = r'<span class="MuiTypography-root MuiTypography-body1 detail-label mui-style-tgrox">Publisher<!-- -->: </span>(.*?)</p>'
    num_pages_pattern = r'<span class="MuiTypography-root MuiTypography-body1 detail-label mui-style-tgrox">Number of Pages<!-- -->: </span>(.*?)</p>'

    title_match = re.search(title_pattern, html_content, re.DOTALL)
    author_match = re.search(author_pattern, html_content, re.DOTALL)
    book_type_match_ebook_paperback = re.search(book_type_pattern_ebook_paperback, html_content, re.DOTALL)
    original_price_match = re.search(original_price_pattern, html_content, re.DOTALL)
    discounted_price_match = re.search(discounted_price_pattern, html_content, re.DOTALL)
    isbn_10_match = re.search(isbn_10_pattern, html_content, re.DOTALL)
    published_date_match = re.search(published_date_pattern, html_content, re.DOTALL)
    publisher_match = re.search(publisher_pattern, html_content, re.DOTALL)
    num_pages_match = re.search(num_pages_pattern, html_content, re.DOTALL)

    title = html.unescape(title_match.group(1).strip()) if title_match else 'None'
    author = author_match.group(1).strip() if author_match else 'None'
    book_type = book_type_match_ebook_paperback.group(1).strip() if book_type_match_ebook_paperback else 'None'
    original_price = original_price_match.group(1).strip() if original_price_match else 'None'
    discounted_price = discounted_price_match.group(1).strip() if discounted_price_match else 'None'
    isbn_10 = isbn_10_match.group(1).strip() if isbn_10_match else 'None'
    published_date = published_date_match.group(1).strip() if published_date_match else 'None'
    publisher = html.unescape(publisher_match.group(1).strip()) if publisher_match else 'None'
    num_pages = num_pages_match.group(1).strip() if num_pages_match else 'None'
    if original_price == 'None':
        original_price = discounted_price
        discounted_price = 'None'
    if published_date:
        published_date = re.sub(r'\b(\d+)(st|nd|rd|th)\b', r'\1', published_date)
        published_date = datetime.strptime(published_date, "%d %B %Y").strftime("%Y-%m-%d")
    return title, author, book_type, original_price, discounted_price, isbn_10, published_date, publisher, num_pages
class Task_1:
    def __init__(self):
        self.ses = requests.Session()
        self.ses.timeout = 40
        self.tab = ''
        self.Pychrome_wp()

    def Pychrome_wp(self):
        try:
            profilename = 'black'
            os_username = os.popen("whoami").read().strip()
            if '\\' in os_username:
                os_username = os_username.split('\\')[-1]
            if os.name == 'nt':
                browser_name = "start chrome"
                self.dir_path = f"""C:\\Users\\{os_username}\\AppData\\Local\\Google\\Chrome\\User Data\\"""
            else:
                browser_name = "google-chrome"
                self.dir_path = f"/home/{os_username}/.config/google-chrome/"
            random_key = getRandomPort()
            os.system(
                f'''{browser_name}  --remote-allow-origins=* --no-first-run --user-data-dir={self.dir_path} --profile-directory={profilename} --remote-debugging-port={random_key}&''')
            time.sleep(random.uniform(3, 6))
            self.browser = pychrome.Browser(url=f"http://localhost:{random_key}")
            tabs = self.browser.list_tab()
            isbn_list = []
            book_info_list = []
            with open('input_list.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    isbn_list.append(row['ISBN13'])
                for isbn in isbn_list:
                    url = f"https://www.booktopia.com.au/book/{isbn}.html"
                    self.load_url1 = url
                    self.tab = tabs[0]
                    self.tab.start()
                    self.tab.Network.enable()
                    self.tab.Page.navigate(url=self.load_url1)
                    wait_time = random.uniform(2.1, 3.6)
                    time.sleep(wait_time)
                    time.sleep(6)
                    page_source = self.tab.Runtime.evaluate(expression="""window.document.body.innerHTML""")
                    with open('offline.html', "w") as file:
                        file.write(str(page_source['result']['value']))
                    with open('offline.html', "r") as file:
                        html_content = file.read()
                        if "The page you are trying to access no longer exists or has been moved" in html_content:
                                    book_info_list.append(["Book not found"])
                        else:
                            book_info = extract_book_info(html_content)
                            book_info_list.append(book_info)
                    if "/ebook/" in html_content:
                        if '<p class="MuiTypography-root MuiTypography-body1 mui-style-pt1gy5">eBook</p>' in html_content:
                            self.tab.Runtime.evaluate(
                                expression="document.querySelector('p.MuiTypography-root.MuiTypography-body1.mui-style-pt1gy5').click()")
                            time.sleep(5) 
                            page_source = self.tab.Runtime.evaluate(expression="document.body.innerHTML")
                            html_content = page_source['result']['value']
                            if "The page you are trying to access no longer exists or has been moved" in html_content:
                                    book_info_list.append(["Book not found"])
                            else:
                                book_info = extract_book_info(html_content)
                                book_info_list.append(book_info)
                        else:
                            continue
                        if '/audiobook/' or '/book/' in html_content:
                            self.tab.Page.navigate(url=self.load_url1)
                            time.sleep(wait_time)
                            time.sleep(6)
                            page_source = self.tab.Runtime.evaluate(expression="""window.document.body.innerHTML""")
                            with open('offline.html', "w") as file:
                                file.write(str(page_source['result']['value']))
                            with open('offline.html', "r") as file:
                                html_content = file.read()
                            if '/ebook/' in html_content:
                                if '<p class="MuiTypography-root MuiTypography-body1 mui-style-pt1gy5">Audiobook</p>' in html_content:
                                    self.tab.Runtime.evaluate(
                                        expression="document.querySelector('a[href*=\"/audiobook/\"] > p.MuiTypography-root.MuiTypography-body1.mui-style-pt1gy5').click()")
                                    time.sleep(5)
                                    page_source_new = self.tab.Runtime.evaluate(expression="document.body.innerHTML")
                                    html_content = page_source_new['result']['value']
                                    if "The page you are trying to access no longer exists or has been moved" in html_content:
                                        book_info_list.append(["Book not found"])
                                    else:
                                        book_info = extract_book_info(html_content)
                                        book_info = (*book_info[:2], 'Digital Audiobook', *book_info[3:])
                                        book_info_list.append(book_info)
                                else: 
                                    continue
            output_file = 'results.csv'
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Title', 'Author', 'Book Type', 'Original Price', 'Discounted Price', 'ISBN-10', 'Published Date', 'Publisher', 'Number of Pages'])
                for book_info in book_info_list:
                    writer.writerow(book_info)
            print(f"Book information saved to {output_file}")
            self.tab.stop()
            self.browser.close_tab(self.tab)
        except Exception as e:
            print(e)
            return
    def __del__(self):
        self.ses.close()
        if os.name == 'nt':
            os.system('taskkill /im chrome.exe /f')
        else:
            os.system('killall -9 chrome')
        print("closed")
if __name__ == '__main__':
    Task_1()
