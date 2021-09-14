## Агрегатор Twitter и VK (Python Flask + Vue.js)
* нужен файл `wall/config.py`

* Сборка Back-end:
```
git clone https://github.com/Koljasha/social/
cd social/
cp ~/Downloads/config-social.py ./wall/config.py
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
* Сборка Front-end:
```
npm i
./build.sh
```
#### Используем
* или *Supervisor* `/etc/supervisor/conf.d/social.conf`:
```
[program:social]
command=/path_to_app/social/venv/bin/waitress-serve --listen=127.0.0.1:9010 main:application
directory=/path_to_app/social
user=user_name
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
* или *Systemd* `/etc/systemd/system/social.service`:
```
[Unit]
Description=Social Service
After=network.target

[Service]
User=user_name
Group=group_name
WorkingDirectory=/path_to_app/social
ExecStart=/path_to_app/social/venv/bin/waitress-serve --listen=127.0.0.1:9010 --threads=2 main:application
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```
