SECRET_KEY=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1`
ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`

docker build -t "redwood:latest" \
    --build-arg ARG_REDWOOD_SECRET_KEY=$SECRET_KEY \
    .
