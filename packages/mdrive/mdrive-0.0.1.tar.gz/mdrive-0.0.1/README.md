# MDrive
_Data and Actions as a Service_

1. Docker and daemonize database.
`docker-compose up -d`

```
[Service]
Restart=always
User=myuser
ExecStart=/usr/bin/docker-compose -f /path/to/mdrive/docker-compose.yml up
```

( https://github.com/docker/compose/issues/4266 )
( full sample: https://gist.github.com/mosquito/b23e1c1e5723a7fd9e6568e5cf91180f )

2. Daemonize API (api.py)
(the cli.py should work as interface to API)

*Run:*

`python mdrive/api.py run`

Or add it to the systemd:

```
[Unit]
Description=MDrive
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=mindey
WorkingDirectory=/home/mindey/Projects/Development/mindey/mdrive/
ExecStartPre=/bin/bash -c "source .env/bin/activate"
ExecStart=/home/mindey/Projects/Development/mindey/mdrive/.env/bin/python3 /home/mindey/Projects/Development/mindey/mdrive/mdrive/api.py run

[Install]
WantedBy=multi-user.target
```

3. Create Sentry server, and add `.vars` as `SENTRY_DSN`:
Can do like so:
https://gist.github.com/denji/b801f19d95b7d7910982c22bb1478f96
https://gist.github.com/Cubixmeister/f037950ef5a0a8d950f474ee2998673e
