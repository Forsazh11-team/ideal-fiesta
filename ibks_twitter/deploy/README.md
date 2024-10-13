# Конфигурация gunicorn

`sudo mkdir -pv /var/{log,run}/gunicorn/`
`sudo chown -cR user:group /var/{log,run}/gunicorn/`
`gunicorn -c deploy/gunicorn-conf.py`

# Конфигурация nginx

Этот конфиг файл поместить по пути `/etc/nginx/conf.d/ibks_twitter.conf/`. Внутри
конфига проверить корректность доменного имени. Корректность конфига затем
можно протестировать командой `nginx -t`.

Nginx сервит статические файлы. Нужно создать необходимые директории:

`sudo mkdir -pv /var/www/ibks_twitter/static`
`sudo chown -cR user:group /var/www/ibks_twitter/`

После этого `python manage.py collectstatic` соберёт все статичные файлы из
Джанго проекта, указанные в настройках, и поместит туда. Сейчас выдаёт предупреждения
о дубликатах, но, например, `python manage.py findstatic css/edit.css` говорит,
что дубликаты на самом деле одни и те же файлы. Пока не фиксил TODO.

# HTTPS

Для настройки HTTPS можно использовать certbot. На Fedora `sudo dnf install certbot`.
Это стоит делать уже непосредственно на сервере, после получения доменного имени.

`sudo certbot certonly --nginx`

Изменить конфиг сайта, убрав комментирование со строк, начиная с listen 443 ssl.
