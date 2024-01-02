docker run --rm -ti -v /Users/ptanvann/tekton-pipeline/custom-image/approval:/apps -p 5000:5000 python:3.9-slim bash

random_number=$(shuf -i 1000000000000000-9999999999999999 -n 1)
echo "Random 16-digit number: $random_number"



pip install flask
python apps/approval.py <approvecode>

#approval.py will return user approve status in file result.txt 


# Task reture result (approve or reject)
      approve_result=$(cat result.txt)
      echo $approve_result
      printf "%s" "${approve_result}" > "$(results.approve_result.path)"


$(tasks.wait-for-approve.results.approve_result)


###### Build approve Image by python script
cat << EOF > Dockerfile
FROM python:3.9-slim
RUN pip install flask
RUN apt update
RUN apt-get -y install procps
RUN apt-get -y install curl
ADD . ./
EXPOSE 5000
EOF

podman build -t docker.io/paichayon1/tekton-approve:0.5  .
podman push docker.io/paichayon1/tekton-approve:0.5 