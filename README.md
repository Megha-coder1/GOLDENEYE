# GoldenEye

GoldenEye is a Python 3 application for **SECURITY TESTING PURPOSES ONLY**!

GoldenEye is an HTTP Denial of Service (DoS) test tool.

**Attack Vector Exploited:** HTTP Keep Alive + NoCache

## Usage

To use GoldenEye, navigate to the location of `goldeneye/` and run:

`cd location_of_goldeneye/`

`./goldeneye.py <example.com> [OPTIONS]`

## Options

| Flag             | Description                                       | Default                    |
|------------------|---------------------------------------------------|----------------------------|
| `-u`, `--useragents` | File with user-agents to use                      | Randomly generated         |
| `-w`, `--workers`   | Number of concurrent workers                      | 50                         |
| `-s`, `--sockets`   | Number of concurrent sockets                      | 30                         |
| `-m`, `--method`    | HTTP Method to use ('get', 'post', or 'random')   | get                        |
| `-d`, `--debug`     | Enable Debug Mode (more verbose output)           | True                      |
| `-n`, `--nosslcheck`| Do not verify SSL Certificate                      | True                       |
| `-h`, `--help`      | Shows this help message                           |                            |

## Utilities

- **util/getuas.py**: Fetches user-agent lists from [UserAgentString](http://www.useragentstring.com/pages/useragentstring.php) subpages (e.g., `./getuas.py "http://www.useragentstring.com/pages/useragentstring.php?name=All"`). **Requires BeautifulSoup4**.
  
- **res/lists/useragents**: Text lists (one per line) of User-Agent strings (from [UserAgentString](http://www.useragentstring.com)).

## To-do

- Change from `getopt` to `argparse`
- Change from `string.format()` to `printf`-like

## License

This software is distributed under the [GNU General Public License version 3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html).

## Legal Notice

**THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY!**

If you engage in any illegal activity, the author does not take any responsibility for it. By using this software, you agree with these terms.

## Author

**K. Meghaditya**

Contact: [meggha2013@gmail.com]  
Phone: +91 79890 57980
