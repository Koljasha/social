#!env.exe bash

# для Linux #!/usr/bin/env bash

waitress-serve --listen=127.0.0.1:9010 main:application
