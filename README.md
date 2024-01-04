# tekton-pipeline
Ref: https://github.com/oladapooloyede/tekton-pipeline/blob/master/pipelines/ci-pipeline.yaml

```
buildah --storage-driver=vfs build --format oci --tls-verify=false --no-cache -f ./docker/Dockerfile  -t default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds

buildah --storage-driver=vfs push --format oci --tls-verify=false default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds docker://default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds
```


# To imagestream from another project, Need to add system:image-puller to default service account user

```
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-dev:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-sit:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-uat:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-prod:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-dr:default --namespace=cicd

```

# Create Secret Sealed

```
kubeseal < github-pat-secret.yaml  > github-pat-secret-sealed.yaml  -o yaml -n cicd
```


# Prerequire Secret for Update Manifest Task (Github PAT secret)

```
apiVersion: v1
kind: Secret
metadata:
  name: github-pat-secret
data:
  # User name and PAT token
  GIT_CREDS_USR: <username>
  GIT_CREDS_PSW: <password>
```

----
# Prerequire configmap and Secret for Arcocd Sync Task
# **** Image from https://quay.io/repository/argoproj/argocd not working sync success but alway return fail*****

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-env-configmap
data:
  ARGOCD_SERVER: <Argo CD server address>
---
apiVersion: v1
kind: Secret
metadata:
  name: argocd-env-secret
data:
  # choose one of username/password or auth token
  ARGOCD_USERNAME: <username>
  ARGOCD_PASSWORD: <password>
  ARGOCD_AUTH_TOKEN: <token>
```
----

# Webhook Secret
```
apiVersion: v1
kind: Secret
metadata:
  name: github-webhook-secret
data:
  secretToken: <token>
```


# SonarQube Task -Secret
```
apiVersion: v1
kind: Secret
metadata:
  name: sonarqube-secret
data:
  SONAR_HOST_URL: <username>
  SONAR_LOGIN_TOKEN: <password>
```

# Send Mail Task - Secret

```
kind: Secret
apiVersion: v1
metadata:
  name: gmail-secret
stringData:
  url: "smtp.gmail.com"
  port: "465"
  user: "gcp.pai0001@gmail.com"
  password: "password"
  tls: "True"
```
----

# Prepare New Environment for DEMO
# System Requirement
- OpenShift 4.12
- OpenShift GitOps Operator
- Openshift Pipeline Operator

# Pipeline Git Repo
https://github.com/paichayon321/tekton-pipeline.git

# Source Code Repo for test (MVN)


# Prepare ArgoCD:
Create Cluster-admin group and add user to these group

oc adm policy add-cluster-role-to-use cluster-admin system:serviceaccount:openshift-gitops:openshift-gitops-argocd-application-controller

Setting Repository to https://github.com/paichayon321/tekton-pipeline.git

Create Application:
- myapp-sealsecret  
  Path: platform/sealsecret
  Namespace: kube-system

- myapp-sonarqube
  Path: platform/sonarqube
  Namespace: cicd-tools

- myapp-cicd
  Path: cicd/pipeline
  Namespace: cicd

Install kubeseal and Re-create Secret:
argocd-env-secret
github-pat-secret
github-webhook-secret
gmail-secret
sonarqube-secret
