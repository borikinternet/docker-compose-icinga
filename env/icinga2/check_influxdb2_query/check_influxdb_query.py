#!/usr/bin/env python3
# coding=UTF-8
"""Nagios plugin to check values queried from InfluxDB 2

(c) Dmitrii Borisov, borik.internet@gmail.com, dborisov@mail.ru
Licenced under terms of MIT Licence
https://opensource.org/license/mit/

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import nagiosplugin, argparse
from influxdb_client import InfluxDBClient


class Requester:
  def __init__(self, host: str, port: int, org: str, token: str):
    self.url = 'http://' + host + ':' + str(port)
    self.token = token
    self.org = org

  def get_data(self, query: str) -> (any, any):
    client = InfluxDBClient(self.url, token=self.token, org=self.org)
    query_api = client.query_api()
    result = query_api.query(org=self.org, query=query)
    for table in result:
      for record in table:
        return 'value', record.get_value()
    return 'value', -1


class Value(nagiosplugin.Resource):
  def __init__(self, req: Requester, query: str):
    self.req = req
    self.query = query

  def probe(self):
    return nagiosplugin.Metric(*self.req.get_data(self.query), min=0, context='def')


@nagiosplugin.guarded
def main():
  argp = argparse.ArgumentParser(prog='check_influxdb_query.py',
                                 description=__doc__)
  argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                    help='return warning if value is outside RANGE')
  argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                    help='return critical if value is outside RANGE')
  argp.add_argument('-H', '--host', metavar='IP_OR_HOSTNAME', default='127.0.0.1',
                    help='address of InfluxDB2 server')
  argp.add_argument('-p', '--port', default=8086, type=int,
                    help='listen port of InfluxDB2 server')
  argp.add_argument('-o', '--organization', type=str, required=True,
                    help='organisation name')
  argp.add_argument('-q', '--query', type=str, required=True,
                    help='query to get data from DB')
  argp.add_argument('-t', '--token', type=str, required=True,
                    help='authentication token to connect database')
  args = argp.parse_args()
  check = nagiosplugin.Check(
    Value(Requester(args.host, args.port, args.organization, args.token), args.query),
    nagiosplugin.ScalarContext('def', args.warning, args.critical)
  )
  check.main()


if __name__ == "__main__":
  main()
