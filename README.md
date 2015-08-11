##check public ip

when Public IP changed send a mail to you

###how to use

```bash
git clone https://github.com/Firxiao/check_public_ip.git
cd check_public_ip
cp conf.ini.example conf.ini
```

make config.ini correct


###run

```bash
chmod +x check_public_ip.py
./check_public_ip.py
```


###cron
you can add it to crontab like this

```
*/5 * * * * /opt/check_public_ip/check_public_ip.py >/dev/null 2>&1
```

