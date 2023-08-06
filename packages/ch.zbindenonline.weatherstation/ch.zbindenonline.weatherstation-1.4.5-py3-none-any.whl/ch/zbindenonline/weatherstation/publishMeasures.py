import argparse
import datetime
import logging
import sqlite3
import sys

import requests

from .config import *


class RestService:
    def __init__(self, url, username, password):
        self.url = url
        self.auth = {'username': username, 'password': password}
        self.headers = {'User-Agent': 'python'}
        self.login()

    def login(self):
        logging.debug("Try to login to " + self.url + '/login')
        try:
            response = requests.post(self.url + '/login', data=json.dumps(self.auth), headers=self.headers, timeout=20)
        except requests.exceptions.RequestException as e:
            logging.exception("RequestException occured: " + str(e))
            sys.exit(1)

        if not response.ok:
            response.raise_for_status()
        str_response = response.content.decode('utf-8')
        logging.debug(str_response)
        if str_response:
            jwtdata = json.loads(str_response)
            jwt = jwtdata['access_jwt']
            logging.info(jwt)
            self.headers['Authorization'] = 'Bearer ' + jwt

    def get_sensors(self):
        response = requests.get(self.url + '/sensors', headers=self.headers, timeout=10)
        logging.info(response)
        if response.ok:
            str_response = response.content.decode('utf-8')
            logging.debug(str_response)
            return json.loads(str_response)
        else:
            response.raise_for_status()

    def get_last_timestamp(self, sensor_id):
        response = requests.get(self.url + '/measures/last?sensor=' + sensor_id, headers=self.headers, timeout=10)
        if response.ok:
            str_response = response.content.decode('utf-8')
            logging.debug(str_response)
            if str_response:
                last = json.loads(str_response)
                return last['measured_at']
            return '1970-01-01 00:00'
        else:
            response.raise_for_status()

    def post_measures(self, sensor_id, measures):
        measures_data = []
        for measure in measures:
            data = {'sensor': sensor_id, 'measured_at': measure['measured_at'], 'temperature': measure['temperature'],
                    'humidity': measure['humidity']}
            measures_data.append(data)
        logging.debug('Headers:')
        logging.debug(self.headers)
        response = requests.post(self.url + '/measures', data=json.dumps(measures_data), headers=self.headers, timeout=120)
        logging.debug(response)
        if not response.ok:
            response.raise_for_status()


def read_configuration():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file", type=str, default='weatherstation.cfg')
    parser.add_argument("-l", "--log", help="level to log", type=str, default="INFO")
    args = parser.parse_args()
    return createConfig(args)


def configure_logging(loglevel):
    numeric_level = getattr(logging, loglevel, "INFO")
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=numeric_level)


class MeasureRepository:
    def __init__(self, database: str):
        self.database = database

    def get_measures_after(self, sensor_name: str, last):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT m.created_at, m.temperature, m.humidity from measure m join sensor s on s.id=m.sensor "
                "where s.name=? and m.created_at > datetime(?, '+1 second')",
                (sensor_name, last))
            records = cur.fetchall()
            measures_data = []
            for record in records:
                data = {'measured_at': record[0], 'temperature': str(record[1]),
                        'humidity': str(record[2])}
                measures_data.append(data)
            return measures_data


class Main:
    def __init__(self, service: RestService, repo: MeasureRepository):
        self.service = service
        self.repo = repo

    def run(self):
        start = datetime.datetime.now()
        try:
            sensors = self.service.get_sensors()
            posted_measures = 0
            for sensor in sensors:
                sensor_id = sensor['id']
                sensor_name = sensor['name']
                last = self.service.get_last_timestamp(sensor_id)
                measures_to_post = self.repo.get_measures_after(sensor_name, last)
                measures_per_sensor = len(measures_to_post)
                if len(measures_to_post) > 0:
                    logging.info('Posting ' + str(measures_per_sensor) + " for sensor '" + sensor['name'] + "'")
                    self.service.post_measures(sensor_id, measures_to_post)
                    posted_measures += measures_per_sensor
            elapsed_time = datetime.datetime.now() - start
            logging.info('Posted ' + str(posted_measures) + ' in ' + str(elapsed_time))
        except Exception as e:
            logging.error("Error occurred: " + str(e))


def main():
    config = read_configuration()
    configure_logging(config.loglevel)
    service = RestService(config.rest.url, config.rest.username, config.rest.password)
    repo = MeasureRepository(config.database)
    Main(service, repo).run()


if __name__ == '__main__':
    main()
