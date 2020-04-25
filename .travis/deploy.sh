#!/bin/bash

git config --global push.default simple # we only want to push one branch — master
git remote add production ssh://git@$IP/$DEPLOY_DIR
git push production master


ssh git@$IP <<EOF
  cd $DEPLOY_DIR
  sudo docker run -p 8000:8000 -i -t vbs-registration-app-api_app
EOF
