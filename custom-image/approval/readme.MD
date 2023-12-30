docker run --rm -ti -v /Users/ptanvann/tekton-pipeline/custom-image/approval:/apps -p 5000:5000 python:3.9-slim bash
pip install flask
python apps/approval.py
