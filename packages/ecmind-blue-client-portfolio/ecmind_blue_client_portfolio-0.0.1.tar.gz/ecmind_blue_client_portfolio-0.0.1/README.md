# ECMind blue client: Portfolio

Helper modules for the ecmind_blue_client to ease the work with the portfolio API functions.

## Installation

`pip install ecmind_blue_client_portfolio`


## Usage

```python

from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_portfolio import portfolio

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')

all_portfolios_of_user_root = portfolio.search(client, creator='ROOT')
print(all_portfolios_of_user_root)
```