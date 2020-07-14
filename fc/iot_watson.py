import wiotp.sdk.device


class IoT:
    client = None

    def __init__(self):
        # Configure
        my_config = wiotp.sdk.device.parseConfigFile("device.yaml")
        self.client = wiotp.sdk.device.DeviceClient(config=my_config, logHandlers=None)
        self.client.connect()

    def send_data(self, fps, detections):
        # Send Data
        my_data = {'Frames per second': fps, 'Positive detections': detections}
        self.client.publishEvent(eventId="status", msgFormat="json", data=my_data, qos=0, onPublish=None)

    def disconnect_client(self):
        # Disconnect
        self.client.disconnect()
