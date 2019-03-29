sudo yum install -y \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-dev \
    python3-pip

if [ -d /tmp/codedeploy-deployment-staging-area ]; then
  sudo rm -R /tmp/codedeploy-deployment-staging-area
  mkdir /tmp/codedeploy-deployment-staging-area