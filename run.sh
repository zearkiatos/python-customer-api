activate () {
    if [ -d "venv" ] 
    then
        echo "Python 🐍 environment was activated"
        source venv/bin/activate
    else
        echo "The folder environment doesn't exist"
        python3 -m venv venv
        source venv/bin/activate
        echo "The environment folder was created and the python 🐍 environment was activated"
    fi
}

install () {
    pip3 install -r requirements.txt
}

run () {
    fastapi dev src/main.py
}

docker_local_up () {
    docker-compose -f docker-compose.local.yaml up -d --build
}

docker_local_down () {
    docker-compose -f docker-compose.local.yaml down
}

docker_up () {
    docker-compose up -d --build
}

docker_down () {
    docker-compose down
}

podman_local_up () {
    podman-compose -f docker-compose.local.yaml up -d --build
}

podman_local_down () {
    podman-compose -f docker-compose.local.yaml down
}

podman_up () {
    podman-compose up -d --build
}

podman_down () {
    podman-compose down
    podman-compose down
}

kube_local_up () {
    kubectl apply -f kubernetes/local/services.yaml
    kubectl apply -f kubernetes/local/deployments.yaml
}

kube_local_down () {
    kubectl delete -f kubernetes/local/services.yaml
    kubectl delete -f kubernetes/local/deployments.yaml
}