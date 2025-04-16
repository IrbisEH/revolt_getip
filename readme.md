# сделать файл исполняемым
chmod +x FILE

# скопировать
cp FILE "/usr/local/bin/ALIAS"

# создать файл с данными
touch "${HOME}/revolt_config/ip_addresses.lst"


### cборка пакет
dpkg-deb --build [PATH]         # Cборка пакет
sudo dpkg -i revolt_getip.deb   # Установка
sudo dpkg -r revolt_getip       # Удаление