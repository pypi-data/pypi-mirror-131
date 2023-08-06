variables:
  DOCKER_AUTH_CONFIG: '{ "auths":{ "https://{{ params['registry'] }}": { "auth": "$REGISTRY_AUTH_HASH" } }}'

stages:
  - build
  - deploy

docker-build-master:
  image: {{ params['registry'] }}/tmaier/docker-compose:latest
  stage: build

  #services:
  #  - {{ params['registry'] }}/docker:dind

  before_script:
    - docker login -u "$REGISTRY_LOGIN" -p "$REGISTRY_PASSWORD" $REGISTRY_URL

  script:
    - echo "|---- start build ----:>"
    - docker-compose -f docker-stack.yml build --force-rm
    - echo ":>----  finish build ----=|"
    - echo "|---- start push to registry ----:>"
    - docker-compose -f docker-stack.yml push
    - echo ":>----  finish push ----=|"

  after_script:
    - docker logout $REGISTRY_URL

  only:
    - master

docker-deploy-master:
  image: {{ params['registry'] }}/tmaier/docker-compose:latest
  stage: deploy

  before_script:
    - docker login -u "$REGISTRY_LOGIN" -p "$REGISTRY_PASSWORD" $REGISTRY_URL

  #services:
  #  - {{ params['registry'] }}/docker:dind

  script:
    - echo "|---- Start deploy ----:>"
    - docker stack deploy --with-registry-auth --compose-file=docker-stack.yml {{params['project_name'] }} --prune
    - echo ":>---- Finish deploy ----=|"

  after_script:
    - docker logout $REGISTRY_URL

  only:
    - master
