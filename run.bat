@echo off

:activate
if exist venv (
    echo Python environment was activated
    call venv\Scripts\activate.bat
) else (
    echo The folder environment doesn't exist
    python3 -m venv venv
    call venv\Scripts\activate.bat
    echo The environment folder was created and the python environment was activated
)
exit /b 0

:install
pip3 install -r requirements.txt
exit /b 0

:run
fastapi dev src/main.py
exit /b 0

:docker-local-up
docker-compose -f docker-compose.local.yaml up -d --build
exit /b 0

:docker-local-down
docker-compose -f docker-compose.local.yaml down
exit /b 0

:docker-up
docker-compose up -d --build
exit /b 0

:docker-down
docker-compose down
exit /b 0

:podman-local-up
podman-compose -f docker-compose.local.yaml up -d --build
exit /b 0

:podman-local-down
podman-compose -f docker-compose.local.yaml down
exit /b 0

:podman-up
podman-compose up -d --build
exit /b 0

:podman-down
podman-compose down
exit /b 0

:kube-local-up
kubectl apply -f kubernetes/local/services.yaml
kubectl apply -f kubernetes/local/deployments.yaml
exit /b 0

:kube-local-down
kubectl delete -f kubernetes/local/services.yaml
kubectl delete -f kubernetes/local/deployments.yaml
exit /b 0