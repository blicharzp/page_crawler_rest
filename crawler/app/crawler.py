from bs4 import BeautifulSoup
import requests
import threading, queue, time, json, os

STORAGE_ADDRESS = "http://{address}:{port}/{api}".format(
    address=os.getenv("STORAGE_SERVICE_NAME"),
    port=os.getenv("STORAGE_SERVICE_PORT"),
    api="api/v1/content/"
)


class Crawler:
    def __init__(self, link="https://www.gazeta.pl/0,0.html"):
        self.__link = link
        self.__queue = queue.Queue()

    def produce(self):
        print("Started produce job.")
        while True:
            page = requests.get(self.__link, verify=False)
            soup =  BeautifulSoup(page.content, features="html.parser")
            self.__crawle(soup)
            time.sleep(10 * 60)

    def __crawle(self, soup):
        for tag in soup.find_all("a", id="LinkArea:BoxOpLink"):
            name = tag.attrs.get("title", "Title missing")
            timestamp = tag.find("span", class_="o-article__timestamp is-new").string
            content = {'name': name, 'timestamp': timestamp}
            print("Producer - put: {}".format(content))
            self.__queue.put(content)

    def consume(self):
        print("Started consume job.")
        while True:
            try:
                content = self.__queue.get()
            except queue.Empty:
                print("Consumer - nothing to send")
            else:
                self.__send(content)
            finally:
                time.sleep(5)

    def __send(self, content):
        try:
            requests.post(STORAGE_ADDRESS, json=json.dumps(content))
            print("Consumer - send {}".format(content))
        except requests.exceptions.ConnectionError:
            print("Consumer - cannot establish connection")


def main():
    crawler = Crawler()
    threading.Thread(target = crawler.produce).start()
    threading.Thread(target = crawler.consume).start()



if __name__ == "__main__":
    main()
