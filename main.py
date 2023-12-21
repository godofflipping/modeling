from window import Window


if __name__ == "__main__":
    
    map_path = 'map.txt'
    mail_path = 'mail_10000.txt'
    scale = 50
    
    window = Window(map_path, mail_path, scale)
    window.run()