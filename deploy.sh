#!/bin/bash
set -e

./manage.py collectstatic --noinput
# Cheating, making sure that migrate is working
export LAMBDA_TASK_ROOT=/home
./manage.py migrate
# Create an admin when deploying for the first time
echo "from core.models import User; import os; User.objects.create_superuser('tsatsujnr@gmail.com', os.environ.get('DJANGO_ADMIN_PASSWORD','MyPassword')) if len(User.objects.filter(email='tsatsujnr@gmail.com')) == 0 else print('Admin exists')"|./manage.py shell
sls deploy -s dev
