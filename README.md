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
----

# Prepare New Environment for DEMO
```
Notes:
If use default cluster task -- image sha need to be change

```
## System Requirement
- OpenShift 4.12
- OpenShift GitOps Operator
- Openshift Pipeline Operator

## Clone Pipeline Repo and Source Code for demo repo as your own
```
# Pipeline Git Repo
git clone https://github.com/paichayon321/tekton-pipeline.git

## Source Code Repo for test (MVN)
git clone https://github.com/paichayon321/spring-web-quickstart.git
```

## Prepare ArgoCD:
Create "cluster-admins" group and add user to cluster-admins group

```
apiVersion: user.openshift.io/v1
kind: Group
metadata:
  name: cluster-admins
users:
  - ocadmin
```

## Add Role to gitops service account
```
oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:openshift-gitops:openshift-gitops-argocd-application-controller
```

## Login to argoCD portat
Default URL:
https://openshift-gitops-server-openshift-gitops.apps.<base domain>

Setting Repository:
```
> Setting > Repositories > connect repo
> Connect Method: HTTPS
> Type: git
> Proejct: default
> Repository URL: https://github.com/paichayon321/tekton-pipeline.git
```

Setting SealSecret Application:
```
Name: myapp-sealsecret
Project: default
Sync Policy: Automatic
Prune Resources: true
Auto-create namespace: true
Source: https://github.com/paichayon321/tekton-pipeline.git
Revision: main
Path: platform/sealsecret
Namespace: kube-system
```

Setting SonarQube Application:
```
Name: myapp-sonarqube
Project: default
Sync Policy: Automatic
Prune Resources: true
Auto-create namespace: true
Source: https://github.com/paichayon321/tekton-pipeline.git
Revision: main
Path: platform/sonarqube
Namespace: cicd-tools
```

Setting cicd pipeline Application:
```
Name: myapp-cicd
Project: default
Sync Policy: Automatic
Prune Resources: true
Auto-create namespace: true
Source: https://github.com/paichayon321/tekton-pipeline.git
Revision: main
Path: cicd/pipeline
Namespace: cicd
```


## Prepare Secret for Pipeline
Prepare kubeseal cli
```
# Download CLI (kubeseal)
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.21.0/kubeseal-0.21.0-linux-amd64.tar.gz
tar xzvf kubeseal-0.21.0-linux-amd64.tar.gz
sudo mv kubeseal /usr/bin
kubeseal --version

# Create Secret Sealed yaml
kubeseal < secretfile.yaml  > sealed-secretfile.yaml  -o yaml -n cicd
```

#### Image from https://quay.io/repository/argoproj/argocd not working sync success but alway return fail
ArgoCD configmap and secret:

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

Github PAT secret:

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

Github Webhook Secret:
```
apiVersion: v1
kind: Secret
metadata:
  name: github-webhook-secret
data:
  secretToken: <token>
```

SonarQube Secret:
```
apiVersion: v1
kind: Secret
metadata:
  name: sonarqube-secret
data:
  SONAR_HOST_URL: <username>
  SONAR_LOGIN_TOKEN: <password>
```

Gmail for Send mail Secret:

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


## Prepare PVC for Pipeline
```
cat << EOF | oc create -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-source
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
EOF


```



