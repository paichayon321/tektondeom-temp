###### Build sendgmail Image by python script
cat << EOF > Dockerfile
FROM python:3.9-slim
ADD sendgmail.py ./
EOF

podman build -t docker.io/paichayon1/sendgmail-py:0.1  .
podman push docker.io/paichayon1/sendgmail-py:0.1
