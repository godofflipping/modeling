from window import Window


if __name__ == "__main__":
    
    map_path = 'map.txt'
    mail_path = 'mail_test_2.txt'
    scale = 30
    
    window = Window(map_path, mail_path, scale)
    window.run()