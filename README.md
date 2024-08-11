GoldenEye
GoldenEye is a Python 3 app for SECURITY TESTING PURPOSES ONLY!
GoldenEye is an HTTP DoS Test Tool.
Attack Vector exploited: HTTP Keep Alive + NoCache
Usage
 USAGE:cd location of goldeneye/

 ./goldeneye.py <example.com> [OPTIONS]

 OPTIONS:
    Flag           Description                     Default
    -u, --useragents   File with user-agents to use                     (default: randomly generated)
    -w, --workers      Number of concurrent workers                     (default: 50)
    -s, --sockets      Number of concurrent sockets                     (default: 30)
    -m, --method       HTTP Method to use 'get' or 'post'  or 'random'  (default: get)
    -d, --debug        Enable Debug Mode [more verbose output]          (default: False)
    -n, --nosslcheck   Do not verify SSL Certificate                    (default: True)
    -h, --help         Shows this help
Utilities
•	util/getuas.py - Fetches user-agent lists from http://www.useragentstring.com/pages/useragentstring.php subpages (ex: ./getuas.py "http://www.useragentstring.com/pages/useragentstring.php?name=All") REQUIRES BEAUTIFULSOUP4
•	res/lists/useragents - Text lists (one per line) of User-Agent strings (from http://www.useragentstring.com)
To-do
•	Change from getopt to argparse
•	Change from string.format() to printf-like
License
This software is distributed under the GNU General Public License version 3 (GPLv3)
LEGAL NOTICE
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY! IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY THE AUTHOR DOES NOT TAKE ANY RESPONSIBILITY FOR IT. BY USING THIS SOFTWARE YOU AGREE WITH THESE TERMS.
 
AUTHOR
K. Meghaditya
Contact – meggha2013@gmail.com
                      +91 79890 57980
