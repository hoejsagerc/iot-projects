def connect():
    import network
    
    SSID = "Guest_Wifi"
    PASSWORD = "P!ssword123"
    
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