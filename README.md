# Documentación para desplegar en dev y prd, y pruebas locales

## Prerequisito
- Python 3.8 o 3.9
- Cliente Oracle, descargar [aquí](https://drive.google.com/file/d/1musU0zbSWz6AB9YBGr7eUgt8NVrsNbEc/view?usp=sharing)

## Instalar dependencias
En el archivo de requerimientos.txt están todas las dependencias, usa el siguiente comando para instalarlas.

``` basch
pip install -r ./requirements.txt
```

TIP: Antes de instalar las dependencias, no olvidar crear un ambiente virtual.

## Correr localmente
- Descargar el cliente Oracle y ubicarlo en el lugar de su preferencia.
En el archivo sdk.py, ubicar la linea *cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_9")*, descomentar y actualizar la ruta del cliente Oracle.

Para correr el proyecto localmente, usar los siguientes comandos:

``` python
uvicorn main:app --reload 
```

Podrías probarlo 
```
curl http://localhost:8000/hello/{company}
```

## Deploy a Dev

### Para hacer Deploy a Dev Manual

![image](https://user-images.githubusercontent.com/80862575/168092345-64b448c6-e271-4dc6-9844-afff0bc040c7.png)

### Para hacer Deploy a Dev Automatico

El despliegue a Dev es automatico, este se ejecuta una vez se abra un Pull Request,
Requesitos:
- pull request, atraves de un issues, 
[Link](https://docs.github.com/es/issues/tracking-your-work-with-issues/creating-a-branch-for-an-issue)
- Etiquetar team Leader para el review y aprobación del mismo, y pueda hacer el merge.
- En la conversación del PR, validar si tiene recomendaciones de calidad de codígo, sesion *sonarcloud*, es requesito para prd.




### Para conocer la url del endpoind y nombre de la función:
- En el repositorio, ir a Actions
- En la el apartado Workflows, ir a Deploy Lambda, según el ambiente (Dev, Prd, o Dev Manual)
- Click en el el workflow en curso (Amarillo) o el más reciente finalizado (Verde), el nombre es el mismo del PR creado previamente
![image](https://user-images.githubusercontent.com/80862575/168094025-7b798a17-406e-4cb1-980e-9591662ba5e9.png)

- En el apartado de Jobs, click en Runner.
- Buscar entre los pasos, el paso llamado *Serverless Deploy*, y darle click

![image](https://user-images.githubusercontent.com/80862575/168094723-335ee0ab-fd63-4817-8c10-8d2caab952e6.png)

- Al fina de este, estará la URL del Endpoins y nombre de la función 
![image](https://user-images.githubusercontent.com/80862575/168095264-be062e78-f8ed-45ea-a11d-292346f34ee8.png)


## Deploy a Prd
El despliegue a Prd es automatico, este se ejecuta automaticamente una vez que el team leader apruebe el review, merge y cierre el pull request.

### Para conocer la url del endpoind y nombre de la función:
- En el repositorio, ir a Actions
- En la el apartado Workflows, ir a Deploy Lambda, según el ambiente (Dev, Prd, o Dev Manual)
- Click en el el workflow en curso (Amarillo) o el más reciente finalizado (Verde), el nombre es el mismo del PR creado previamente
![image](https://user-images.githubusercontent.com/80862575/168094025-7b798a17-406e-4cb1-980e-9591662ba5e9.png)

- En el apartado de Jobs, click en Runner.
- Buscar entre los pasos, el paso llamado *Serverless Deploy*, y darle click

![image](https://user-images.githubusercontent.com/80862575/168094723-335ee0ab-fd63-4817-8c10-8d2caab952e6.png)

- Al fina de este, estará la URL del Endpoins y nombre de la función 
![image](https://user-images.githubusercontent.com/80862575/168095264-be062e78-f8ed-45ea-a11d-292346f34ee8.png)






