#! /bin/zsh

docker buildx build --platform linux/amd64 --push -t registry.heroku.com/cufinditt/web .
heroku container:release web --app cufinditt
docker tag registry.heroku.com/cufinditt/web 
docker push https://cufinditt.herokuapp.com/

