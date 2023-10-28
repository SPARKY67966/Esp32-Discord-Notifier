import network

class net():
  
  def __init__(self, ssid : str = None, password : str = None) -> None:
    
    self.ssid = ssid
    self.station = network.WLAN(network.STA_IF)

    if not self.station.isconnected() and (ssid or password) is None:
       raise ValueError('Connection unsuccesfull \n credentials are not provided')

    elif not self.station.isconnected():
        self.station.active(True)
        self.station.connect(ssid,password)
        while self.station.isconnected() == False:
             pass
    
  def deviceip(self) -> str:
    return self.station.ifconfig()[0] 
  
  def connection_name(self) -> str:
     return self.ssid
  
  def routerip(self) -> str:
     return self.station.ifconfig()[-1]

