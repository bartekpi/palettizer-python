DOCKER_NAME=plttzrrrrr-python
PROJECT_ID=my-portfolio-project-e0899
PROJECT_REGION=europe-west1
DOCKER_REPO=eu.gcr.io/${PROJECT_ID}
PORT=8080

docker_build:
	docker build \
		-t ${DOCKER_NAME} -t ${DOCKER_NAME}:latest \
		-t ${DOCKER_REPO}/${DOCKER_NAME}:latest .

docker_run:
	docker run -p ${PORT}:8080 -ti ${DOCKER_NAME}:latest

docker_push:
	docker push ${DOCKER_REPO}/${DOCKER_NAME}

gcloud_deploy:
	gcloud beta run deploy ${DOCKER_NAME} \
		--image eu.gcr.io/${PROJECT_ID}/${DOCKER_NAME} \
		--platform managed \
		--region ${PROJECT_REGION} \
		--allow-unauthenticated \
		--memory 256Mi
