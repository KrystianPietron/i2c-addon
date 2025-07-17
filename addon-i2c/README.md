Obsługa wyświetlaczyc OLED 126x64 i2c

Przygotowanie urządzenia raspberry pi z systemem Home Assistant OS
   
    1. Po instalacji system Home Assistan OS i pierwszej konfiguracji, musimy
       włączyć obsługę systemową magistrali i2c. W tym celu należy:
        a. Wyjąć kartę SD i za pomocą adaptera podłączyć go do PC z systemem 
           Windowes lub macOS
        b. Po podłączeniu montujemy partycję hassos-boot poleceniami:
            MAC:
                - sudo mkdir /Volumes/hassos-boot      
                - sudo mount -t msdos /dev/disk4s1 /Volumes/hassos-boot
            Windows:
                Nie trzeba tworzyć katalogu montowania – system automatycznie przypisuje literę dysku po włożeniu karty SD/USB.
        c. edytujemy plik config.txt
            szukamy linii "#dtparam=i2c_arm=on" jeżeli jest zakomentowana to ją odkomentowujemy. 
            W przypadku gdy jej nie ma trzeba ją dodać. Zaraz pod tym wpisem dodajemy "dtparam=i2c_vc=on"
        d. nastepnie tworzymy katalog CONFIG
        e. w katalogu CONFIG tworzymy folder modules
        f. w folderze modules tworzymy plik rpi-i2c.conf z zawartością i2c-dev
        g. wkładamy kartę SD do raspberry pi lub podłączamy dysk SSD
        h. po uruchomieniu systemy wchodzimy w terminal na HAOS
        i. wykonujemy kolejno komendy
            - mkdir /tmp/mnt
            - mkdir -p /tmp/mnt/modules
            - echo -ne i2c-dev>/tmp/mnt/modules/rpi-i2c.conf
            - echo dtparam=i2c_vc=on >> /tmp/mnt/config.txt
            - echo dtparam=i2c_arm=on >> /tmp/mnt/config.txt
            - sync
            - reboot
        j. po ponownym uruchomieniu systemu wchodzimy ponoewnie w terminal i wykonujemy komendę
            - lsmod | grep i2c
            efekt tego powinno być mniej więcej coś takiego
                /dev/i2c-1,
                /dev/i2c-13
        k. w tym momencie nasze wyświetlacze będą widoczne

    Dodatek obsługuje w sumie 4 wyświetlacze z adresami 0x3C i 0x3D na każdej szynie po 2


