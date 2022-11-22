from fusionsolarapi import ApiClient, Station, Device
import time
import os
from datetime import datetime, timezone, timedelta



# import dot env file
# from dotenv import load_dotenv
# load_dotenv("app/.env")

def publish_station_data(frequency, base_topic, station_data, station_code):
    print("Publishing station data")
    with open("info/stations_mqtt_topics.txt", "a+") as f:
        for key, value in station_data.items():
            if value is None: value = 0
            f.write(f"\n{base_topic}/{station_code}/{frequency}/{key}/{value}")
            time.sleep(0.1)
        f.write("\n")

def publish_device_data(frequency, base_topic, device_data, station_code, device_id):
    print("Publishing device data")
    with open("info/devices_mqtt_topics.txt", "a+") as f:
        for key, value in device_data.items():
            if value is None: value = 0
            f.write(f"\n{base_topic}/{station_code}/{device_id}/{frequency}/{key}/{value}")
            time.sleep(0.1)
        f.write("\n")

def publish_realtime_data(apiclient, stations, publish_objects, base_topic):
    print("Publishing realtime data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                pass

            elif publish_object == "DEVICES":
                station_devices = station.get_devices()
                for device in station_devices:
                    device_data = apiclient.get_dev_kpi_real(device.get_id(), device.get_dev_type_id())
                    try:
                        device_data = device_data["data"][-1]["dataItemMap"]
                        publish_device_data("realtime", base_topic, device_data, station.get_station_code(), device.get_id())
                    except Exception as e:
                        print(f"Error while publishing device realtime data, no data, {e}")
                    

            else:
                print(f"Unknown publish object: {publish_object}") 

def publish_hour_data(apiclient, stations, publish_objects, base_topic):
    print("Publishing hour data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_hour(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data("hour", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station hour data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_day_data(apiclient, stations, publish_objects, base_topic):
    print("Publishing day data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_day(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data("day", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station day data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass
                # station_devices = station.get_devices()
                # for device in station_devices:
                #     device_data = apiclient.get_dev_kpi_day(device.get_id(), device.get_dev_type_id(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                #     try:
                #         device_data = device_data["data"][-1]["dataItemMap"]
                #         publish_device_data("day", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device day data, no data, {e}")

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_month_data(apiclient, stations, publish_objects, base_topic):
    print("Publishing month data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_month(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data("month", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station month data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass
                # station_devices = station.get_devices()
                # for device in station_devices:
                #     device_data = apiclient.get_dev_kpi_month(device.get_id(), device.get_dev_type_id(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                #     try:
                #         device_data = device_data["data"][-1]["dataItemMap"]
                #         publish_device_data("month", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device month data, no data, {e}")

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_year_data(apiclient, stations, publish_objects, base_topic):
    print("Publishing year data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_year(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data("year", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station year data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass
                # station_devices = station.get_devices()
                # for device in station_devices:
                #     device_data = apiclient.get_dev_kpi_year(device.get_id(), device.get_dev_type_id(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                #     try:
                #         device_data = device_data["data"][-1]["dataItemMap"]
                #         publish_device_data("year", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device year data, no data, {e}")

                    

            else:
                print(f"Unknown publish object: {publish_object}")  


if __name__ == '__main__':
    fusion_username = os.environ.get('FUSIONSOLAR_USR')
    fusion_password = os.environ.get('FUSIONSOLAR_PASS')

    publish_objects = ["DEVICES", "STATIONS"]

    publish_device_type_ids = []
    publish_station_codes = []

    allowed_device_type_ids = [1, 38, 39]
    base_topic = os.environ.get('PUBLISH_BASE_TOPIC')

    with ApiClient(user_name=fusion_username, system_code=fusion_password) as apiclient:
        print("Connected to FusionSolar API")
        stations = list()
        for station in apiclient.get_stations_list()["data"]:
            station_to_add = None
            if publish_station_codes and station["stationCode"] in publish_station_codes:
                station_to_add = Station(
                    station["stationCode"],
                    station["stationName"],
                )
            elif not publish_station_codes:
                station_to_add = Station(
                    station["stationCode"],
                    station["stationName"],
                )
            if station_to_add is not None:
                for device in apiclient.get_devices_list(station_to_add.get_station_code())["data"]:
                    if publish_device_type_ids and device["devTypeId"] in publish_device_type_ids and device["devTypeId"] in allowed_device_type_ids:
                        station_to_add.add_device(
                            Device(
                                device["devName"],
                                device["devTypeId"],
                                device["id"],
                                device["invType"])
                        )
                    elif not publish_device_type_ids and device["devTypeId"] in allowed_device_type_ids:
                        station_to_add.add_device(
                            Device(
                                device["devName"],
                                device["devTypeId"],
                                device["id"],
                                device["invType"])
                        )
                stations.append(station_to_add)
        print("Stations and devices loaded")

        with open("info/api_info.txt", "w+") as f:
            print("Writing stations to file")
            for station in stations:
                f.write(f"Station: \n\tname: {station.get_station_name()}  \n\tcode: {station.get_station_code()}")
                f.write("\n\tDevices:")
                for device in station.get_devices():
                    f.write(f"\n\t\tdevice_name: {device.get_dev_name()} \n\t\tdevice_id: {device.get_id()} \
                     \n\t\tdevice_type_id: {device.get_dev_type_id()} \n\t\tdevice_inv_type: {device.get_inv_type()}")
                    f.write("\n")
                f.write("\n")

        publish_realtime_data(apiclient, stations, publish_objects, base_topic)
        time.sleep(10)
        publish_hour_data(apiclient, stations, publish_objects, base_topic)
        time.sleep(10)
        publish_day_data(apiclient, stations, publish_objects, base_topic)
    
