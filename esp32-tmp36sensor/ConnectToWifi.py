def connect(ssid: str, password: str):
    import network
    station = network.WLAN(network.STA_IF)
    
    if station.isconnected() == True:
        print("Device already connected to the internet")
        return
    
    station.active(True)
    station.connect(ssid, password)
    
    while station.isconnected() == False:
        pass
    
    print("Wifi connection successful!")
    print(station.ifconfig())