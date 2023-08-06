# data file
SHADOWSOCKS_CONFIG_BASE64 = 'ewogICAgInNlcnZlciI6IjAuMC4wLjAiLAogICAgIm1vZGUiOiJ0Y3BfYW5kX3VkcCIsCiAgICAic2VydmVyX3BvcnQiOjg4NjgsCiAgICAibG9jYWxfcG9ydCI6MTA4MCwKICAgICJwYXNzd29yZCI6InBhc3Nwb3J0MTIzIiwKICAgICJ0aW1lb3V0Ijo2MCwKICAgICJtZXRob2QiOiJhZXMtMjU2LWdjbSIKfQ=='
SUPVISOR_CONF_TEMPLATE = '''[program:PLACEHOLDER]
directory=/tmp/
command=COMMAND
user=root
autostart=true
autorestart=true
redirect_stderr=true
stopasgroup=true
killasgroup=true'''

BASE64_URLS = {
    'gost':
    b'aHR0cHM6Ly9maWxlZG4uY29tL2xDZHRwdjNzaVZ5YlZ5blBjZ1hnblBtL2dvc3QtbGludXgtYW1kNjQK'
}
