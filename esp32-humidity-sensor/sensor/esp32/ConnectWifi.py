def connect():
    import network
    
    SSID = "SSID_NAME"
    PASSWORD = "PASSWORD"
    
    station = network.WLAN(network.STA_IF)
    
    if station.isconnected() == True:
        print("Device already connected to the internet")
        return
    
    station.active(True)
    station.connect(SSID, PASSWORD)
    
    while station.isconnected() == False:
        pass
    
    print("Wifi connection successful!")
    print(station.ifconfig())
