# Ejemplo de pipeline de pruebas de github actions

En este proyecto se encuentra el código de ejemplo para ejecutar un pipeline de github que valida que el código esté cubierto en un mínimo de 80% en pruebas.

Este proyecto hace uso de pipenv para gestión de dependencias y pytest para el framework de pruebas.

# Estructura
````
├── .github/workflows
|   ├── ci_offer_pipeline.yml # Configuración del pipeline de pruebas para offer-management
|   ├── ci_post_pipeline.yml # Configuración del pipeline de pruebas para post-management
|   ├── ci_route_pipeline.yml # Configuración del pipeline de pruebas para route-management
|   ├── ci_user_pipeline.yml # Configuración del pipeline de pruebas para user-management
|   └── ci_pipeline.yml # Configuración del pipeline
├── archive-email # Archivos de la aplicación archive-email
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   ├── requirements.txt # Dependencias de la aplicación
|   └── gcloudprojectg14...json# Keys
├── offer-management # Archivos de la aplicacion offer-management
|   ├── modelos # Archivos de modelos de la base de datos
|   ├── tests # Paquete de pruebas
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   ├── requirements.txt # Dependencias de la aplicación
|   └── pytest.ini # Configuración de pruebas
├── post-management # Archivos de la aplicacion post-management
|   ├── modelos # Archivos de modelos de la base de datos
|   ├── tests # Paquete de pruebas
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   ├── requirements.txt # Dependencias de la aplicación
|   └── pytest.ini # Configuración de pruebas
├── route-management # Archivos de la aplicacion route-management
|   ├── modelos # Archivos de modelos de la base de datos
|   ├── tests # Paquete de pruebas
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   ├── requirements.txt # Dependencias de la aplicación
|   └── pytest.ini # Configuración de pruebas
├── send-email # Archivos de la aplicación send-email
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   └── requirements.txt # Dependencias de la aplicación
├── sidecar-api # Archivos de la aplicación sidecar-api
|   ├── test # Archivos de los test de la aplicación
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   └── requirements.txt # Dependencias de la aplicación
├── user-management # Archivos de la aplicacion user-management
|   ├── modelos # Archivos de modelos de la base de datos
|   ├── tests # Paquete de pruebas
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   ├── requirements.txt # Dependencias de la aplicación
|   └── pytest.ini # Configuración de pruebas
├── utility-management # Archivos de la aplicación utility-management
|   ├── modelos # Archivos de modelos de la base de datos
|   ├── test # Archivos de los test de la aplicación
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   └── requirements.txt # Dependencias de la aplicación
├── verify-express # Archivos de la aplicación verify-express
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   └── requirements.txt # Dependencias de la aplicación
├── verify-webhook # Archivos de la aplicación verify-webhook
|   ├── vistas # Archivos de las vistas de la aplicación
|   ├── app.py # Archivo principal de la aplicación
|   ├── Dockerfile # Archivo de configuración de docker
|   └── requirements.txt # Dependencias de la aplicación
├── .gitignore # Archivo de configuración de git
├── config.yml # Archivo de configuración para evaluador
├── docker-compose.yml # Archivo de configuración de docker-compose
├── k8s-componentes-entrega-3.yaml # Archivo de configuración de componentes entrega 3
├── k8s-ingress-deployment.yaml # Archivo de configuración de ingress
├── k8s-true-native-deployment.yaml # Archivo de configuración de true-native
├── secrets.yaml # Archivo de configuración de secrets
├── entrega3_G14.postman_collection.json # Archivo de postman para la entrega 3
└── README.md # Archivo de documentación
````

En archivo ````ci_pipeline.yml```` contiene el pipeline que ejecuta las pruebas. Se recomienda revisar como está configurado y las notas en el.

## Como ejecutar localmente las pruebas

1. Install pipenv
2. Ejecutar pruebas
```
cd component1
pipenv shell
pipenv install --dev
pipenv run pytest --cov=src -v -s --cov-fail-under=80
deactivate
```

## Correr componentes localmente

- Tener en cuenta, si se va a correr local en un mac m1 se debe poner el siguiente comando por problemas de la libreria: 
```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```
Comandos para correr localmente (Windows):
```
# Crear entorno virtual
python -m venv venv
# Activar entorno virtual
venv\Scripts\activate
# En caso de que se quiera desactivar el entorno virtual
deactivate
# Dirigirse a la carpeta del componente
cd s202311-proyecto-entrega1-grupo14/user-management
-- Instalar dependencias
pip install -r requirements.txt
```

Comandos para correr localmente (Linux):
```
# Crear entorno virtual
python3 -m venv venv
# Activar entorno virtual
source venv/bin/activate
# En caso de que se quiera desactivar el entorno virtual
deactivate
# Dirigirse a la carpeta del componente
cd s202311-proyecto-entrega1-grupo14/user-management
-- Instalar dependencias
pip3 install -r requirements.txt
-- En caso de que se quiera correr el componente de Flask individualmente local
-- user-management
flask run -p 3000
-- post-management
flask run -p 3001
-- route-management
flask run -p 3002
-- offer-management
flask run -p 3003
-- utility-management
flask run -p 3004
-- sidecar-api
flask run -p 3005
-- verify-webhook
flask run -p 3006
-- verify-express
flask run -p 3007
-- send-email
flask run -p 3008
-- archive-email
flask run -p 3009

-- Pruebas Unitarias en caso de que se quiera correr local para un componente
# user-management --94%
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_usermgr.py
coverage run --source=. -m unittest tests/test_usermgr.py
# post-management --72%
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_postmgr.py
coverage run --source=. -m unittest tests/test_postmgr.py
# route-management --74%
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_routemgr.py
coverage run --source=. -m unittest tests/test_routemgr.py
# offer-management 
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_offermgr.py 
coverage run --source=. -m unittest tests/test_offermgr.py 
# utility-management -- 84%
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_utilitymgr.py
coverage run --source=. -m unittest tests/test_utilitymgr.py
# sidecarapi -- 
coverage run --source=. --omit=*/__init__.py,*/tests/* -m unittest tests/test_apimgr.py
coverage run --source=. -m unittest tests/test_apimgr.py
-- Verificar que el coverage sea mayor o igual a 80%
coverage report --fail-under=80
-- Correr DockerCompose
docker-compose up --build -d
-- Bajar Contenedores con DockerCompose
docker compose down --volumes
```



# Entrega 2 - Pasos para desplegar en Google Cloud

Inicializar GCloud 
```
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Habilitar las siguientes APIs
```
compute.googleapis.com
servicenetworking.googleapis.com
artifactregistry.googleapis.com
kubernetes.googleapis.com
```

1. Crear Red Virtual
```
gcloud compute networks create vpn-e2g14-misw --project=gcloudprojectg14e2 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional
```
2. Crear subred
```
gcloud compute networks subnets create red-dbs-e2g14 --range=192.168.32.0/19 --network=vpn-e2g14-misw --region=us-central1 --project=gcloudprojectg14e2
```
3. Otorgar acceso a los servicios de GCP
```
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=red-dbs-e2g14 --network=vpn-e2g14-misw --project=gcloudprojectg14e2
```
4. Crear Regla de Firewall
```
gcloud compute firewall-rules create allow-db-ingress-e2g14 --direction=INGRESS --priority=1000 --network=vpn-e2g14-misw --action=ALLOW --rules=tcp:5432 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=gcloudprojectg14e2
```
5. Creación de la BD
```
Nombre: misw-db-e2g14
Contraseña: DreamTeam123*
Version: PostgreSQL 14
Region: us-central1
Disponibilidad zonal: Única
Tipo de máquina: De núcleo compartido, 1 core y 1.7 GB de RAM
Almacenamiento 10 GB de HDD
No habilitar los aumentos automáticos de almacenamiento.
Asignación de IP de la instancia: privada
Red: vpn-e2g14
Rango de IP asignado: red-dbs-e2g14
Etiqueta: basededatos
```


6. Subir las imagenes de docker a el Artifact Registry de Google Cloud
```
# Mac M1
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/users:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/users:1.0
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/offers:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/offers:1.0
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/posts:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/posts:1.0
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/routes:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/routes:1.0
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/utility:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/utility:1.0
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/sidecarapi:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/sidecarapi:1.0
# Windows
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/users:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/users:1.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/offers:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/offers:1.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/posts:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/posts:1.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/routes:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/routes:1.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/utility:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/utility:1.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/sidecarapi:1.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega2-g14/sidecarapi:1.0
```

7. Crear cluster de kubernetes en gcp ---> Autopilot
```
    Nombre: miso-cluster-g14e2 
    Region: us-central1
    Red: vpn-e2g14-misw
    Subred del nodo: red-dbs-e2g14
    Rango de direcciones del pod: 192.168.64.0/21
    Rango de direcciones del servicio: 192.168.72.0/21
```

8. Instalar gke-gcloud-auth-plugin y kubectl
```
gcloud components install gke-gcloud-auth-plugin
gcloud components install kubectl
```

9. Conexion a Cluster
```
gcloud container clusters get-credentials miso-cluster-g14e2 --region us-central1 --project gcloudprojectg14e2
```

10. Aplicar cambios
```
kubectl apply -f secrets.yaml
kubectl apply -f k8s-base-layer-deployment.yaml
kubectl apply -f k8s-new-services-deployment.yaml
kubectl apply -f k8s-ingress-deployment.yaml
kubectl get pods
kubectl get services
kubectl get ingress
kubectl logs <nombre del pod> --all-containers=true
kubectl logs -f <nombre del pod> 
```

## Entrega 3


1. Preparar Ambiente
```
kubectl delete all --all -n default
kubectl delete ingress gateway-ingress
```

2. Ejecutar componente de TrueNative
```
docker run -p 4000:4000 -e EXPRESS_RATE=<EXPRESS_RATE> -e SECRET_TOKEN=<TOKEN> -e BASIC_DELAY=30 ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0
```
- EXPRESS_RATE -> Valor que determina la frecuencia de verificacion de los usuarios por el metodo express, si no se especifica se tomara el valor por defecto de all
- SECRET_TOKEN -> Token que se utilizara para la autenticacion de los usuarios
- BASIC_DELAY -> Tiempo de espera para la verificacion de los usuarios por el metodo basico (un numero mayor o igual a 30)
```
# Sin EXPRESS_RATE o con all: -> Todos seran verificados por el metodo express
docker run -p 4000:4000 -e SECRET_TOKEN=gcloudprojectg14 -e BASIC_DELAY=30 ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0
# EXPRESS_RATE:0 -> Todos seran verificados por el metodo basico
docker run -p 4000:4000 -e EXPRESS_RATE=0 -e SECRET_TOKEN=gcloudprojectg14 -e BASIC_DELAY=30 ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0
# EXPRESS_RATE: n Valor -> cada n + 1 seran verificados por el metodo express, el resto por el basico 
#(n -> 2 entonces 1/3 seran verificados por el metodo express y 2/3 por el basico)
docker run -p 4000:4000 -e EXPRESS_RATE=2 -e SECRET_TOKEN=gcloudprojectg14 -e BASIC_DELAY=30 ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0
```


# Entrega 3

Construccion de las imagenes de docker
```
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/users:6.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/users:6.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/offers:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/offers:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/posts:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/posts:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/routes:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/routes:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/utility:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/utility:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/sidecarapi:6.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/sidecarapi:6.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/verifywebhook:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/verifywebhook:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/verifyexpress:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/verifyexpress:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/sendemail:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/sendemail:5.0
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/archiveemail:5.0 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14e2/entrega3-g14/archiveemail:5.0
-----------------------------------
docker build -t ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0 .
docker push ghcr.io/misw-4301-desarrollo-apps-en-la-nube/true-native:1.0.0
```

Aplicar cambios en gcp
```
kubectl apply -f secrets.yaml
kubectl apply -f k8s-componentes-entrega-3.yaml
kubectl apply -f k8s-true-native-deployment.yaml
kubectl apply -f k8s-ingress-deployment.yaml
kubectl get pods
kubectl get services
kubectl get ingress
kubectl logs <nombre del pod> --all-containers=true
kubectl logs -f <nombre del pod> 
```