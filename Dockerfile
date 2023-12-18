FROM public.ecr.aws/lambda/python:3.9

# Instalación de New Relic CLI
RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash \
    && export PATH=$PATH:/usr/local/bin

# Configuración de New Relic CLI
RUN NEW_RELIC_API_KEY=NRAK-H8ZQF9411O7EETFLAHI6J40BIUH NEW_RELIC_ACCOUNT_ID=4141381 \
    /usr/local/bin/newrelic install -y

# Resto de tu configuración...
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY . ${LAMBDA_TASK_ROOT}

# Definición del punto de entrada y comando por defecto
ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["main.lambda_handler"]
