# tekton-pipeline
Ref: https://github.com/oladapooloyede/tekton-pipeline/blob/master/pipelines/ci-pipeline.yaml


buildah --storage-driver=vfs build --format oci --tls-verify=false --no-cache -f ./docker/Dockerfile  -t default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds

buildah --storage-driver=vfs push --format oci --tls-verify=false default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds docker://default-route-openshift-image-registry.apps.524vf.dynamic.opentlc.com/cicd/spring-web-quickstart:dsdsds


oc policy add-role-to-user system:image-puller system:serviceaccount:dev:default --namespace=cicd


kubeseal < github-pat-secret.yaml  > github-pat-secret-sealed.yaml  -o yaml -n cicd
