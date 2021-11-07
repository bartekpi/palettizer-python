DOCKER_NAME=plttzrrrrr-python
SERVICE_POKE_URL=${DOCKER_NAME}/pltzr-python
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
		--memory 256Mi \
		--cpu 1 \
		--concurrency 80 \
		--max-instances 10

gcloud_scheduler_up:
	gcloud scheduler jobs create http poke-${DOCKER_NAME} \
        --schedule "* * * * *" \
        --project ${PROJECT_ID} \
        --uri $(shell gcloud beta run services list --project ${PROJECT_ID} | egrep "\b${DOCKER_NAME}\b\s" | egrep -o "https://[A-Za-z0-9\\.\\-]+")/${SERVICE_POKE_URL} \
        --http-method GET \
        --time-zone "Europe/London"

gcloud_scheduler_dn:
	gcloud scheduler jobs delete poke-${DOCKER_NAME} --project ${PROJECT_ID}

