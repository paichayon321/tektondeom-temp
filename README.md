# tekton-pipeline
Ref: https://github.com/oladapooloyede/tekton-pipeline/blob/master/pipelines/ci-pipeline.yaml


buildah --storage-driver=vfs build --format oci --tls-verify=false --no-cache -f ./docker/Dockerfile  -t default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds

buildah --storage-driver=vfs push --format oci --tls-verify=false default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds docker://default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds

# To imagestream from another project, Need to add system:image-puller to default service account user
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-dev:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-sit:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-uat:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-prod:default --namespace=cicd
oc policy add-role-to-user system:image-puller system:serviceaccount:myapp-dr:default --namespace=cicd

kubeseal < github-pat-secret.yaml  > github-pat-secret-sealed.yaml  -o yaml -n cicd



----
# Prerequire configmap and Secret for Arcocd Sync Task

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
----
