# docker login -u AWS -p $AWS_ECR_PASSWORD 053467565326.dkr.ecr.us-east-1.amazonaws.com/columni
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 053467565326.dkr.ecr.us-east-1.amazonaws.com
docker kill columni_users 2> /dev/null || true
docker system prune -a -f
docker run --name columni_users -d -p 8011:8011 053467565326.dkr.ecr.us-east-1.amazonaws.com/columni:latest
