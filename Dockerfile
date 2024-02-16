FROM public.ecr.aws/lambda/python:3.9


# Resto de tu configuración...
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY . ${LAMBDA_TASK_ROOT}

# Definición del punto de entrada y comando por defecto
#ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["main.lambda_handler"]
