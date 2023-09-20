docker build -t ecr-repository .
docker tag ecr-repository:latest $ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/ecr-repository:latest
docker push $ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/ecr-repository:latest
