import logging
from functools import wraps
from time import sleep
from typing import Dict
import requests
from datetime import datetime, timezone, timedelta

class HTTPError(Exception):
    pass

class HTTPError407(HTTPError):
    pass

class HTTPError305(HTTPError):
    pass

class HTTPError306(HTTPError):
    pass

class HTTPError307(HTTPError):
    pass

class HTTPError401(HTTPError):
    pass

def authenticated(func):
    """
    Decorator to check if token has expired.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.token_expiration_time <= datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))):
            self.login()
        return func(*args, **kwargs)

    return wrapper


def throttle_retry(func):
    """
    Decorator to retry when throttleError is received.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except HTTPError407 as e:
            for i in range(1, self.max_retry + 1):
                delay = i * 3
                logging.debug(f'Sleeping {delay} seconds')
                sleep(delay)
                try:
                    return func(*args, **kwargs)
                except HTTPError407:
                    pass
            else:
                raise e
        except (HTTPError305, HTTPError306, HTTPError307) as e:
            # Token as expired or we aren't logged in.. Refresh it.
            logging.debug("Got login error. Logging back in and retrying")
            self.login()
            return func(*args, **kwargs)

    return wrapper

 
class ApiClient:
    def __init__(
            self,
            user_name: str,
            system_code: str,
            max_retry: int = 10,
            base_url: str = "https://intl.fusionsolar.huawei.com/thirdData"
    ):
        self.user_name = user_name
        self.system_code = system_code
        self.max_retry = max_retry
        self.base_url = base_url
        self._station_list = None

        self.session = requests.session()
        self.session.headers.update(
            {'Connection': 'keep-alive', 'Content-Type': 'application/json'})

        self.token_expiration_time = 0

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        pass

    def login(self):
        url = f'{self.base_url}/login'
        body = {
            'userName': self.user_name,
            'systemCode': self.system_code
        }
        self.session.cookies.clear()
        r = self.session.post(url=url, json=body)
        self._validate_response(response=r)
        self.session.headers.update(
            {'XSRF-TOKEN': r.cookies.get(name='XSRF-TOKEN')})
        # expiration timer 25min from now
        self.token_expiration_time = datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))) + (25*60)
        print("logged in fusionsolar api")


    def logout(self):
        """
        needs to be implemented
        """
        pass

    @staticmethod
    def _validate_response(response: requests.Response) -> bool:
        response.raise_for_status()
        body = response.json()
        success = body.get('success', False)
        if not success:
            if body.get('failCode') == 407:
                logging.debug('Error 407')
                raise HTTPError407(body.get('message'))
            elif body.get('failCode') == 305:
                logging.debug('Error 305')
                raise HTTPError305(body.get('message'))
            elif body.get('failCode') == 306:
                logging.debug('Error 306')
                raise HTTPError306(body.get('message'))
            elif body.get('failCode') == 307:
                logging.debug('Error 307')
                raise HTTPError307(body.get('message'))
            elif body.get('failCode') == 401:
                logging.debug('Error 401')
                raise HTTPError401(body.get('message'))
            else:
                raise HTTPError(body.get('message'))
        else:
            return True

    @throttle_retry
    @authenticated
    def _request(self, function: str, data=None) -> Dict:
        """
            carry out request to fusion solar api
        """
        if data is None:
            data = {}
        url = f'{self.base_url}/{function}'
        r = self.session.post(url=url, json=data)
        self._validate_response(r)
        return r.json()

# --------------------------------------------
    def get_stations_list(self) -> Dict:
        if self._station_list is None:
            self._station_list = self._request('getStationList')
        return self._station_list

    def get_devices_list(self, station_code) -> Dict:
        return self._request("getDevList", {'stationCodes': station_code})

# --------------------------------------------
    def get_station_kpi_real(self, station_code: str) -> Dict:
        return self._request("getStationRealKpi",
                             {'stationCodes': station_code})

    def get_dev_kpi_real(self, dev_id: str, dev_type_id: int) -> Dict:
        return self._request("getDevRealKpi",
                             {'devIds': dev_id, 'devTypeId': dev_type_id})

# --------------------------------------------
    def get_station_kpi_hour(self, station_code: str,
                             date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getKpiStationHour", {'stationCodes': station_code,
                                                   'collectTime': time})
# does not exist anymore
    # def get_dev_kpi_hour(self, dev_id: str, dev_type_id: int,
    #                     date: pd.Timestamp) -> Dict:
    #     time = int(date) * 1000
    #     return self._request("getDevKpiHour",
    #                             {'devIds': dev_id, 'devTypeId': dev_type_id,
    #                             'collectTime': time})

# --------------------------------------------
    def get_station_kpi_day(self, station_code: str,
                            date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getKpiStationDay", {'stationCodes': station_code,
                                                  'collectTime': time})

    def get_dev_kpi_day(self, dev_id: str, dev_type_id: int,
                    date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getDevKpiDay",
                                {'devIds': dev_id, 'devTypeId': dev_type_id,
                                'collectTime': time})

# --------------------------------------------
    def get_station_kpi_month(self, station_code: str,
                              date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getKpiStationMonth",
                             {'stationCodes': station_code,
                              'collectTime': time})

    def get_dev_kpi_month(self, dev_id: str, dev_type_id: int,
                        date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getDevKpiMonth",
                                {'devIds': dev_id, 'devTypeId': dev_type_id,
                                'collectTime': time})

# --------------------------------------------
    def get_station_kpi_year(self, station_code: str,
                             date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getKpiStationYear", {'stationCodes': station_code,
                                                   'collectTime': time})



    def get_dev_kpi_year(self, dev_id: str, dev_type_id: int,
                         date: datetime) -> Dict:
        time = int(date) * 1000
        return self._request("getDevKpiYear",
                             {'devIds': dev_id, 'devTypeId': dev_type_id,
                              'collectTime': time})

    # def dev_on_off(self, dev_id: str, dev_type_id: int,
    #                control_type: int) -> Dict:
    #     # control_type
    #     # 1: power-on
    #     # 2: power-off
    #     return self._request("devOnOff",
    #                          {'devIds': dev_id, 'devTypeId': dev_type_id,
    #                           'controlType': control_type})

    # def dev_upgrade(self, dev_id: str, dev_type_id: int) -> Dict:
    #     return self._request("devUpgrade",
    #                          {'devIds': dev_id, 'devTypeId': dev_type_id})

    # def get_dev_upgradeinfo(self, dev_id: str, dev_type_id: int) -> Dict:
    #     return self._request("getDevUpgradeInfo",
    #                          {'devIds': dev_id, 'devTypeId': dev_type_id})


class Device():
    def __init__(
        self, 
        dev_name: str, 
        dev_type_id: str, 
        id: int, 
        inv_type: str
    ):
        self.dev_name = dev_name
        self.dev_type_id = dev_type_id
        self.id = id
        self.inv_type = inv_type
    
    # get device id
    def get_id(self) -> str:
        return self.id

    # get device name
    def get_dev_name(self) -> str:
        return self.dev_name

    # get device type id
    def get_dev_type_id(self) -> int:
        return self.dev_type_id
    
    # get device type
    def get_inv_type(self) -> str:
        return self.inv_type



class Station():
    def __init__(
            self,
            station_code: str,
            station_name: str,
    ):
        self.station_code = station_code
        self.station_name = station_name
        self.devices = []
    
    # get station code
    def get_station_code(self) -> str:
        return self.station_code
    
    # get station name
    def get_station_name(self) -> str:
        return self.station_name
    
    def get_devices(self) -> list:
        return self.devices

    # add device to station
    def add_device(self, device: Device) -> None:
        self.devices.append(device)

