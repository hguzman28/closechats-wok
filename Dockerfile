FROM public.ecr.aws/lambda/python:3.9

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install --no-cache-dir newrelic
COPY . ${LAMBDA_TASK_ROOT}
#ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["main.lambda_handler"] 
