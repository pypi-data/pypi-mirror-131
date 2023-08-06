import datetime
from typing import List

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather


class MeasureData:
    def __init__(self, sensor_id: str, measured_at: datetime, temperature: float, humidity: float):
        self.sensor_id = sensor_id
        self.measured_at = measured_at
        self.temperature = temperature
        self.humidity = humidity


class SensorService:
    def __init__(self, outdoor_weather_uid: str, host='localhost', port=4223):
        self.uid = outdoor_weather_uid
        self.host = host
        self.port = port

    def get_measures(self) -> List[MeasureData]:
        ip_connection = IPConnection()
        ow = BrickletOutdoorWeather(self.uid, ip_connection)

        ip_connection.connect(self.host, self.port)
        try:
            result = []
            sensor_ids = ow.get_sensor_identifiers()
            for sensor_id in sensor_ids:
                sensor_data = ow.get_sensor_data(sensor_id)
                measure = MeasureData(sensor_id, datetime.datetime.now(), sensor_data.temperature / 10, sensor_data.humidity)
                result.append(measure)
            return result
        finally:
            ip_connection.disconnect()
