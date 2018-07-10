#!env.exe bash

# для Linux #!/usr/bin/env bash

npm run build
sed.exe -i 's/index/\/static\/index/g' templates/login.html