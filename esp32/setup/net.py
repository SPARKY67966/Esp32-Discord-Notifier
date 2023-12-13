import network

class NetworkManager:
  
    def __init__(self, ssid: str = None, password: str = None) -> None:
        """
        Initializes the NetworkManager with optional SSID and password for connection.

        Args:
            ssid (str): SSID of the Wi-Fi network.
            password (str): Password of the Wi-Fi network.
        """
        self.ssid = ssid
        self.station = network.WLAN(network.STA_IF)

        # Check if not connected and no credentials provided
        if not self.station.isconnected() and not (ssid and password):
            raise ValueError('Connection unsuccessful\nCredentials are not provided')

        # If not connected, activate station mode and connect
        elif not self.station.isconnected():
            self.station.active(True)
            self.station.connect(ssid, password)
            
            # Wait until connection is established
            while not self.station.isconnected():
                pass
    
    def get_device_ip(self) -> str:
        """
        Gets the local IP address of the device.

        Returns:
            str: Local IP address.
        """
        return self.station.ifconfig()[0] 
  
    def get_connection_name(self) -> str:
        """
        Gets the SSID of the connected network.

        Returns:
            str: SSID of the connected network.
        """
        return self.ssid
  
    def get_router_ip(self) -> str:
        """
        Gets the IP address of the router.

        Returns:
            str: Router IP address.
        """
        return self.station.ifconfig()[-1]
