# repair-suite

Software de propósito general orientado a talleres mecánicos.

## Manual de instalacion

- Python3
- Mysql

### Luego de hacer las instalaciones mencionadas anteriormente de realizar los sigientes pasos:

1.  git clone https://github.com/ediazgarcia/repair.git
2.  cd repair
3.  Instalar y Crear el entorno virtual:

- pip install virtualenv
- python3 -m venv env
- source ./env/Scripts/activate

4.  pip install -r requirements.txt

    - Adiccional, en caso de instalar otros paquetes despues de ejecutar pip install -r requirements.txt debe volver a ejecutar el requirements.txt ejecutando el comando sin eliminar nada ejecuta pip freeze > requirements.txt

5.  Para ejecutar la aplicacion con python index.py
