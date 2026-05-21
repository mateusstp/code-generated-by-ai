#!/bin/bash

# ─────────────────────────────────────────────
# GSP510 - Manage Kubernetes in Google Cloud
# ─────────────────────────────────────────────

# ── Task 1: Create GKE cluster ───────────────
gcloud config set compute/zone $ZONE

# FIX: removido --cluster-version latest (usava "latest" em vez de "default")
gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --release-channel regular \
  --num-nodes 3 \
  --min-nodes 2 \
  --max-nodes 6 \
  --enable-autoscaling \
  --no-enable-ip-alias

# ── Task 2: Enable Managed Prometheus ────────
gcloud container clusters update $CLUSTER_NAME \
  --enable-managed-prometheus \
  --zone $ZONE

kubectl create ns $NAMESPACE

gcloud storage cp gs://spls/gsp510/prometheus-app.yaml .

cat > prometheus-app.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-test
  labels:
    app: prometheus-test
spec:
  selector:
    matchLabels:
      app: prometheus-test
  replicas: 3
  template:
    metadata:
      labels:
        app: prometheus-test
    spec:
      nodeSelector:
        kubernetes.io/os: linux
        kubernetes.io/arch: amd64
      containers:
      - image: nilebox/prometheus-example-app:latest
        name: prometheus-test
        ports:
        - name: metrics
          containerPort: 1234
        command:
        - "/main"
        - "--process-metrics"
        - "--go-metrics"
EOF

kubectl -n $NAMESPACE apply -f prometheus-app.yaml

gcloud storage cp gs://spls/gsp510/pod-monitoring.yaml .

cat > pod-monitoring.yaml <<EOF
apiVersion: monitoring.googleapis.com/v1alpha1
kind: PodMonitoring
metadata:
  name: prometheus-test
  labels:
    app.kubernetes.io/name: prometheus-test
spec:
  selector:
    matchLabels:
      app: prometheus-test
  endpoints:
  - port: metrics
    interval: $INTERVAL
EOF

kubectl -n $NAMESPACE apply -f pod-monitoring.yaml

# ── Task 3: Deploy app with intentional error ─
gcloud storage cp -r gs://spls/gsp510/hello-app/ .

export PROJECT_ID=$(gcloud config get-value project)
export REGION="${ZONE%-*}"

gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

cd ~/hello-app
kubectl -n $NAMESPACE apply -f manifests/helloweb-deployment.yaml

# ── Task 4: Logs-based metric + alerting policy
# FIX: adicionada criação da logs-based metric que estava faltando
gcloud logging metrics create pod-image-errors \
  --description="Conta erros de imagem inválida em pods Kubernetes" \
  --log-filter='resource.type="k8s_pod" severity=WARNING'

cat > quicklab.json <<EOF
{
  "displayName": "Pod Error Alert",
  "userLabels": {},
  "conditions": [
    {
      "displayName": "Kubernetes Pod - logging/user/pod-image-errors",
      "conditionThreshold": {
        "filter": "resource.type = \"k8s_pod\" AND metric.type = \"logging.googleapis.com/user/pod-image-errors\"",
        "aggregations": [
          {
            "alignmentPeriod": "600s",
            "crossSeriesReducer": "REDUCE_SUM",
            "perSeriesAligner": "ALIGN_COUNT"
          }
        ],
        "comparison": "COMPARISON_GT",
        "duration": "0s",
        "trigger": {
          "count": 1
        },
        "thresholdValue": 0
      }
    }
  ],
  "alertStrategy": {
    "autoClose": "604800s"
  },
  "combiner": "OR",
  "enabled": true,
  "notificationChannels": []
}
EOF

gcloud alpha monitoring policies create --policy-from-file="quicklab.json"

# ── Task 5: Fix image and re-deploy ──────────
cd ~/hello-app/manifests/

cat > helloweb-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helloweb
  labels:
    app: hello
spec:
  selector:
    matchLabels:
      app: hello
      tier: web
  template:
    metadata:
      labels:
        app: hello
        tier: web
    spec:
      containers:
      - name: hello-app
        image: us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 200m
EOF

cd ~/hello-app

kubectl delete deployment helloweb -n $NAMESPACE
kubectl -n $NAMESPACE apply -f manifests/helloweb-deployment.yaml

# ── Task 6: Containerize v2 and push ─────────
cat > main.go <<EOF
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", hello)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

func hello(w http.ResponseWriter, r *http.Request) {
	log.Printf("Serving request: %s", r.URL.Path)
	host, _ := os.Hostname()
	fmt.Fprintf(w, "Hello, world!\n")
	fmt.Fprintf(w, "Version: 2.0.0\n")
	fmt.Fprintf(w, "Hostname: %s\n", host)
}
EOF

export PROJECT_ID=$(gcloud config get-value project)
export REGION="${ZONE%-*}"

gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/hello-app:v2 .
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/hello-app:v2

kubectl set image deployment/helloweb -n $NAMESPACE \
  hello-app=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/hello-app:v2

kubectl expose deployment helloweb -n $NAMESPACE \
  --name=$SERVICE_NAME \
  --type=LoadBalancer \
  --port=8080 \
  --target-port=8080
