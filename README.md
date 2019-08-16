## Агрегатор Twitter и VK (Python Flask + Vue.js)
* нужен файл `wall/config.py`
* для Linux изменить в *server.py* `#!/usr/bin/env python3`
* для Linux изменить в *package.json* `"build": "webpack --mode production"`
* для Linux изменить в *build.sh* `#!/usr/bin/env bash`
* файл сервера `server.sh`
* Сборка Back-end:
```
git clone https://github.com/Koljasha/social/
cd social/
cp ~/Downloads/config-social.py ./wall/config.py
virtualenv venv
source venv/Scripts/activate  (для Windows)
source venv/bin/activate  (для Linux)
pip install -r requirements.txt
```
* Сборка Front-end:
```
npm i
./build.sh
```
* `social.conf` для *Supervisor*
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
