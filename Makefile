.PHONY: tests all unit functional run docker-image docker-push docker migrate db deploy deploy-with-helm port-forward wheels docker-base-image redeploy check docker-pull clean purge-sessions

GIT_ROOT		:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_ROOT		:= $(GIT_ROOT)/.venv
export VENV		?= $(VENV_ROOT)
export FLASK_DEBUG	:= 1
export HTTPS_API	?= $(shell ps aux | grep ngrok | grep -v grep)

export OAUTH2_ACCESS_TOKEN_URL	:= https://id.t.newstore.net/auth/realms/gabriel-NA-43928/protocol/openid-connect/token
export OAUTH2_AUTHORIZE_URL	:= https://id.t.newstore.net/auth/realms/gabriel-NA-43928/protocol/openid-connect/auth
export OAUTH2_BASE_URL		:= https://id.t.newstore.net/auth/realms/gabriel-NA-43928/protocol/openid-connect/
export OAUTH2_CALLBACK_URL	:= https://keycloak.fulltest.co/callback/oauth2
export OAUTH2_CLIENT_ID		:= fake-newstore-api-v1
export OAUTH2_CLIENT_SCOPE	:= openid profile email
export OAUTH2_CLIENT_SECRET	:= da341d0c-eaa4-460b-af6b-dac5de6443b5
export OAUTH2_DOMAIN		:= id.t.newstore.net
export OAUTH2_CLIENT_AUDIENCE	:= https://keycloak.fulltest.co/
export SECRET_KEY		:= $(shell 2>/dev/null dd bs=128 count=1 if=/dev/urandom | base64 | head -1)

DEPLOY_TIMEOUT		:= 300
# NOTE: the sha must be the long version to match the ${{ github.sha
# }} variable in the github actions. Using %h (short sha) will cause
# deploys to fails with ImagePullBackOff
BASE_TAG		:= latest
PROD_TAG		:= $(shell git log --pretty="format:%H" -n1 . | tail -1)
DOCKER_AUTHOR		:= gabrielfalcao
BASE_IMAGE		:= cahoots-in-base
PROD_IMAGE		:= k8s-cahoots-in
HELM_SET_VARS		:= --set image.tag=$(PROD_TAG) --set image.repository=$(DOCKER_AUTHOR)/$(PROD_IMAGE) --set oauth2.client_id=$(OAUTH2_CLIENT_ID) --set oauth2.client_secret=$(OAUTH2_CLIENT_SECRET) --set flask.secret_key=$(SECRET_KEY)-$(PROD_TAG)
NAMESPACE		:= in-cahoots
HELM_RELEASE		:= $(NAMESPACE)-v0
FIGLET			:= $(shell which figlet)

all: dependencies tests

$(VENV):  # creates $(VENV) folder if does not exist
	python3 -mvenv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

$(VENV)/bin/cahoots-in $(VENV)/bin/nosetests $(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	test -e $(VENV)/bin/pip || $(MAKE) $(VENV)
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/pip install -e .

# Runs the unit and functional tests
tests: | $(VENV)/bin/nosetests  # runs all tests
	$(VENV)/bin/nosetests tests

# Install dependencies
dependencies: | $(VENV)/bin/nosetests
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/pip install -e .

check:
	$(VENV)/bin/cahoots-in check

migrate:
	$(VENV)/bin/cahoots-in migrate-db

# runs unit tests

unit: | $(VENV)/bin/nosetests  # runs only unit tests
	$(VENV)/bin/nosetests --cover-erase tests/unit

functional:| $(VENV)/bin/nosetests  # runs functional tests
	$(VENV)/bin/nosetests tests/functional

# runs the server, exposing the routes to http://localhost:5000
run: purge-sessions | $(VENV)/bin/python
	$(VENV)/bin/cahoots-in web --port=5000


docker-base-image:
	@$(FIGLET) base image
	docker images | grep "$(BASE_IMAGE):$(BASE_TAG)" || docker build -f Dockerfile.base -t "$(DOCKER_AUTHOR)/$(BASE_IMAGE):$(BASE_TAG)" .

docker-image: docker-base-image
	$(FIGLET) production image
	docker tag "$(DOCKER_AUTHOR)/$(BASE_IMAGE):$(BASE_TAG)" "$(DOCKER_AUTHOR)/$(BASE_IMAGE)"
	docker build -f Dockerfile -t $(DOCKER_AUTHOR)/$(PROD_IMAGE):$(PROD_TAG) .
	docker tag $(DOCKER_AUTHOR)/$(PROD_IMAGE):$(PROD_TAG) $(DOCKER_AUTHOR)/$(PROD_IMAGE):latest

docker-push:
	@2>/dev/null docker login -p $$(echo  "a2ltazI1MDIK" | base64 -d) -u gabrielfalcao
	docker push $(DOCKER_AUTHOR)/$(PROD_IMAGE):$(PROD_TAG)

docker-push-all: docker-push
	docker push $(DOCKER_AUTHOR)/$(BASE_IMAGE):$(BASE_TAG)
	docker push $(DOCKER_AUTHOR)/$(BASE_IMAGE)
	docker push $(DOCKER_AUTHOR)/$(PROD_IMAGE)

wheels:
	mkdir -p wheels
	docker run --rm -w /python -v $$(pwd):/python -v $$(pwd)/wheels:/wheels python:3.7-alpine sh -c 'pip wheel -r development.txt'

docker: docker-image docker-push

docker-pull:
	docker pull $(DOCKER_AUTHOR)/$(BASE_IMAGE):$(BASE_TAG)
	docker pull $(DOCKER_AUTHOR)/$(PROD_IMAGE):$(PROD_TAG)
	docker pull $(DOCKER_AUTHOR)/$(PROD_IMAGE)

port-forward:
	kubepfm --target "$(NAMESPACE):.*web:5000:5000" --target "ingress-nginx:*nginx-ingress-controller*:80:80"
	# kubepfm --target "$(NAMESPACE):.*kibana.*:5601:5601" --target "$(NAMESPACE):.*web:5000:5000" --target "$(NAMESPACE):.*elastic.*:9200:9200" --target "$(NAMESPACE):.*elastic.*:9300:9300" --target "$(NAMESPACE):.*queue:4242:4242" --target "$(NAMESPACE):.*queue:6969:6969" --target "$(NAMESPACE):.*forwarder:5353:5353" --target "$(NAMESPACE):.*forwarder:5858:5858"

forward-queue-port:
	kubepfm --target "$(NAMESPACE):.*queue:4242:4242"

db: purge-sessions | $(VENV)/bin/cahoots-in
	-@2>/dev/null dropdb cahoots_in || echo ''
	-@2>/dev/null dropuser cahoots_in || echo 'no db user'
	-@2>/dev/null createuser cahoots_in --createrole --createdb
	-@2>/dev/null createdb cahoots_in
	-@psql postgres << "CREATE ROLE cahoots_in WITH LOGIN PASSWORD 'Wh15K3y'"
	-@psql postgres << "GRANT ALL PRIVILEGES ON DATABASE cahoots_in TO cahoots_in;"
	$(VENV)/bin/cahoots-in migrate-db

purge-sessions:
	$(VENV)/bin/cahoots-in purge-sessions


template:
	helm dependency update --skip-refresh operations/helm/
	helm template $(HELM_SET_VARS) operations/helm

deploy: tests k8s-namespace
	iterm2 color orange
	helm template $(HELM_SET_VARS) operations/helm > /dev/null
	git push
	helm dependency update --skip-refresh operations/helm/
	iterm2 color red
	$(MAKE) helm-install || $(MAKE) helm-upgrade
	iterm2 color green

helm-install:
	helm install --namespace $(NAMESPACE) $(HELM_SET_VARS) -n $(HELM_RELEASE) operations/helm

helm-upgrade:
	helm upgrade --namespace $(NAMESPACE) $(HELM_SET_VARS) $(HELM_RELEASE) operations/helm

k8s-namespace:
	iterm2 color blue
	kubectl get namespaces | grep $(NAMESPACE) | awk '{print $$1}' || kubectl create namespace $(NAMESPACE)
	iterm2 color yellow

rollback:
	iterm2 color cyan
	-helm delete --purge $(HELM_RELEASE)
	-kubectl get pv,pvc -n $(NAMESPACE) -o yaml  | kubectl delete -f -
	iterm2 color purple

undeploy: rollback
	kubectl delete ns $(NAMESPACE)

k9s:
	iterm2 color k
	k9s -n $(NAMESPACE)

redeploy:
	$(MAKE) undeploy deploy

enqueue:
	$(VENV)/bin/cahoots-in enqueue -x $(X) -n 10 --address='tcp://127.0.0.1:4242' "$${USER}@$$(hostname):[SENT=$$(date +'%s')]"

close:
	$(VENV)/bin/cahoots-in close --address='tcp://127.0.0.1:4242'

worker:
	$(VENV)/bin/cahoots-in worker --address='tcp://127.0.0.1:6969'

setup-helm:
	helm repo add elastic https://helm.elastic.co


tunnel:
	ngrok http --subdomain=keycloak-fulltestco 5000

tunnel-react:
	ngrok http --subdomain=reactkeycloak 3000

clean:
	rm -rf .venv

frontend/build/index.html:
	cd frontend && npm run build

react-app: frontend/build/index.html
	cp -f frontend/build/index.html cahoots/web/templates/index.html
	rm -rf cahoots/web/static/{js,css}
	rsync -putaoz frontend/build/static/ cahoots/web/static/
	rsync -putaoz frontend/build/ cahoots/web/static/
	rm -rf cahoots/web/static/static
	rm -f frontend/build/index.html

# https://cert-manager.io/docs/tutorials/backup/
cert-manager-backup.yaml:
	kubectl get -o yaml --all-namespaces issuer,clusterissuer,certificates,certificaterequests > cert-manager-backup.yaml
