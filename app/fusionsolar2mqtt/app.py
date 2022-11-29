from fusionsolarapi import ApiClient, Station, Device
from datetime import datetime, timezone, timedelta
import time
import os
import paho.mqtt.client as mqttClient
import schedule
import json
import logging

# import dot env file
# from dotenv import load_dotenv
# load_dotenv()

def publish_station_data(mqtt_client, frequency, base_topic, station_data, station_code):
    print("Publishing station data")
    for key, value in station_data.items():
        if value is None: value = 0
        #print(f"{base_topic}/{station_code}/{frequency}/{key}/{value}")
        topic = base_topic + "/" + station_code + "/" + frequency + "/" + key
        #mqtt_client.publish(f"{base_topic}/{station_code()}/{frequency}/{key}/{value}")
        mqtt_client.publish(topic, str(value))
        time.sleep(0.1)

def publish_device_data(mqtt_client, frequency, base_topic, device_data, station_code, device_id):
    print("Publishing device data")
    for key, value in device_data.items():
        if value is None: value = 0
        #print(f"{base_topic}/{station_code}/{device_id}/{frequency}/{key}/{value}")
        topic = base_topic+"/"+station_code+"/"+device_id+"/"+frequency+"/"+key
        #mqtt_client.publish(f"{base_topic}/{station_code}/{device_id}/{frequency}/{key}/{value}")
        mqtt_client.publish(topic, str(value))
        time.sleep(0.1)

def publish_realtime_data(mqtt_client, apiclient, stations, publish_objects, base_topic):
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
                        publish_device_data(mqtt_client, "realtime", base_topic, device_data, station.get_station_code(), device.get_id())
                    except Exception as e:
                        print(f"Error while publishing device realtime data, no data, {e}")
                    

            else:
                print(f"Unknown publish object: {publish_object}") 

def publish_hour_data(mqtt_client, apiclient, stations, publish_objects, base_topic):
    print("Publishing hour data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_hour(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data(mqtt_client, "hour", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station hour data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_day_data(mqtt_client, apiclient, stations, publish_objects, base_topic):
    print("Publishing day data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_day(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data(mqtt_client, "day", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station day data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass
                # station_devices = station.get_devices()
                # for device in station_devices:
                #     device_data = apiclient.get_dev_kpi_day(device.get_id(), device.get_dev_type_id(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                #     try:
                #         device_data = device_data["data"][-1]["dataItemMap"]
                #         publish_device_data(mqtt_client, "day", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device day data, no data, {e}")

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_month_data(mqtt_client, apiclient, stations, publish_objects, base_topic):
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
                #         publish_device_data(mqtt_client, "month", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device month data, no data, {e}")

            else:
                print(f"Unknown publish object: {publish_object}")  

def publish_year_data(mqtt_client, apiclient, stations, publish_objects, base_topic):
    print("Publishing year data")
    for station in stations:
        for publish_object in publish_objects:

            if publish_object == "STATIONS":
                station_data = apiclient.get_station_kpi_year(station.get_station_code(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                try:
                    station_data = station_data["data"][-1]["dataItemMap"]
                    publish_station_data(mqtt_client, "year", base_topic, station_data, station.get_station_code())
                except Exception as e:
                    print(f"Error while publishing station year data, no data, {e}")
                

            elif publish_object == "DEVICES":
                pass
                # station_devices = station.get_devices()
                # for device in station_devices:
                #     device_data = apiclient.get_dev_kpi_year(device.get_id(), device.get_dev_type_id(), datetime.timestamp(datetime.now(timezone(timedelta(hours=2)))))
                #     try:
                #         device_data = device_data["data"][-1]["dataItemMap"]
                #         publish_device_data(mqtt_client, "year", base_topic, device_data, station.get_station_code(), device.get_id())
                #     except Exception as e:
                #         print(f"Error while publishing device year data, no data, {e}")

                    

            else:
                print(f"Unknown publish object: {publish_object}")  

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        global Connected    
        Connected = True
    else:
        print("Connection failed", rc)
 
Connected = False

if __name__ == '__main__':
    fusion_username = os.environ.get('FUSIONSOLAR_USR')
    fusion_password = os.environ.get('FUSIONSOLAR_PASS')

    publish_objects = json.loads(os.environ.get('PUBLISH_OBJECTS'))

    publish_device_type_ids = json.loads(os.environ.get('PUBLISH_DEVICE_TYPE_IDS'))
    publish_device_type_ids = [int(i) for i in publish_device_type_ids]
    publish_station_codes = json.loads(os.environ.get('PUBLISH_PLANT_IDS'))
    allowed_device_type_ids = [1, 38, 39]
    
    publish_interval = int(os.environ.get('PUBLISH_INTERVAL'))
    base_topic = os.environ.get('PUBLISH_BASE_TOPIC')

    client = mqttClient.Client(os.environ.get('MQTTCLIENT_ID'))
    client.username_pw_set(os.environ.get('MQTT_USR'), os.environ.get('MQTT_PASS'))
    client.connect_async(os.environ.get('MQTTBROKER_HOST'), port=int(os.environ.get('MQTTBROKER_PORT')))
    client.on_connect= on_connect


    client.loop_start()

    while Connected != True:
        print("Waiting for connection")
        time.sleep(0.1)
    try:
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
                                    str(device["id"]),
                                    device["invType"])
                            )
                        elif not publish_device_type_ids and device["devTypeId"] in allowed_device_type_ids:
                            station_to_add.add_device(
                                Device(
                                    device["devName"],
                                    device["devTypeId"],
                                    str(device["id"]),
                                    device["invType"])
                            )
                    stations.append(station_to_add)
            print("Stations and devices loaded")
            publish_realtime_data(client, apiclient, stations, publish_objects, base_topic)
            schedule.every(publish_interval).minutes.do(publish_realtime_data, client, apiclient, stations, publish_objects, base_topic)
            schedule.every().hour.do(publish_hour_data, client, apiclient, stations, publish_objects, base_topic)

            schedule.every().day.at("00:01").do(publish_day_data, client, apiclient, stations, publish_objects, base_topic)
            #schedule.every().day.at("00:01").do(publish_month_data(client, apiclient, stations, publish_objects, base_topic))
            #schedule.every().day.at("00:01").do(publish_year_data(client, apiclient, stations, publish_objects, base_topic))

            print("Scheduling jobs")
            while True:
                schedule.run_pending()
                time.sleep(1)
    
    except ConnectionError:
        print("Connection error")
        client.disconnect()
        client.loop_stop()
