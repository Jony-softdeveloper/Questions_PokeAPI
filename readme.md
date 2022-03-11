# Questions PokeAPI ¿ 🦁 🦎 ?

<hr/>

### Version 1.0

Note: This file is in spanish, but the documentation and code inside the files was written in english, so you can review the mini-project.

<br/>

Es un mini-projecto creado usando:

* [Python] v3(.10) como lenguaje de programación.
* [Pandas] v1.4 como librería para el manejo de datos.
* [Request] v2.27 como paquete para realizar peticiones.

Además, de usar [Mypy] como la herramienta para verificar las sugerencias de tipo.

Fue creado a manera de reto, en el proceso para un puesto de backend, para una empresa.

El archivo _requirements.txt_ contiene el listado de estos paquetes, junto a las dependencias necesarias para que el proyecto funcione. Simplemente se deben hacen las importaciones necesarias.

En _functions.py_:

* from pandas import DataFrame
* from requests.exceptions import JSONDecodeError

Y en _request.py_:

* import requests
* from requests.exceptions import JSONDecodeError

Mientras que los datos de los pokémons son obtenidos de la [PokeAPI].

<br/>

## Descripción: Description

Busca resolver tres preguntas en particular.

1. Número de pokémons con 'at' y doble 'a' en su nombre.
2. La cantidad de especies de pokémon son capaces de procrear/cruzarce con 'Raichu'.
3. El peso máximo y mínimo de los pokémon tipo 'lucha' de la 'primera' generación.

Se uso siguieron las normas de PEP8 en cuánto el formateo del código (aunque se usa 120 como límite de caracteres por línea).

Las docstings siguen lo indicado por el PEP257 con un formato NumPy. **Los cuatro archivos de código contienen docstrings.**

Se trato de seguir de la mejor manera posible, los PEP483, PEP484, PEP526..., en cuánto a las sugerencias de tipo en variables y métodos/funciones.

<br/>

## Instalación: Instalation

Para su uso, hay que clonar el reposiotio en una carpeta. Si no desea moficar los paquetes de python instalados en el operativo, puede crear un ambiente virtual mediante 'venv' de python.

Para instalar y crear un ambiente virtual, escribir en un intérprete de comandos:

    > cd ruta_donde_clono_repositorio/
    > python -m pip install venv
    > python -m venv nombre_ambiente_virtual

Ahora hay que activar el ambiente virtual (linux).

    > . nombre_ambiente_virtual/bin/activate

Enseguida proceder a actualizar el pip en el ambiente virtual. Ya que muchas veces, la maquina virtual se crea con una versión antigua de pip.

    > pip install --upgrade pip

Finalmente se procede a instalar los paquetes necesarios usando el archivo _requirements.txt_.

    > pip install -r requirements.txt

<br/>

## Uso: Running the program (in powershell)** 💻

Se ejecuta como culquier script de python. El script principal es _main.py_ y se encontrará en la carpeta src.

    > python src/main.py

Se despliega un menú con estas tres opciones, junto a una cuarta para salir del programa.

![menu](https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/images/Menu.png)

Simplemente hay que elegir la opción desea y se desplegará la respuesta.

### Pregunta 1. El número de pokémons que tienen 'at' y doble 'a' en su nombre es: _140_

![Respuesta 1](https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/images/Question_1.png)

### Pregunta 2. La cantidad de especies de pokémons que son capaces de procrear/cruzarce con 'Raichu': _294_

![Respuesta 2](https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/images/Question_2.png)

### Pregunta 3. El peso máximo y mínimo de los pokémons de tipo 'lucha' de la 'primera' generación son: _Máximo es 130 kg y mínimo es 19.5 kg_

![Respuesta 3](https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/images/Question_3.png)

<br/>

## Mejoras : Improvements

> Hacer que las funciones se guarden en caché, así no se tendría que llamar a la API en cada ejecución.

> Falta desarrollar pruebas para las funciones, los métodos de las clases _RequestApi_ y _PokeApi_. Se recomienda usar el paquete [Pytest] para realizar estas.

> _Como se mencionó parráfos atras, las funciones fueron creadas de manera general, por lo que se podría obtener el peso mayor y menor de otros tipos solamente, o su cruce con otras generaciones. Por ejemplo, tipo 'insecto' de la 'octava' generación._
_También sería posible obtener pokémons que contengan en su nombre otro patrónes distintos de 'at' y doble 'a'; y/o saber con cuántas especies puede procrear cualquier otro pókemon. Simplemente podría agregarse opciones para que los usuario ingresen el ID del pokémon, el tipo, el patrón a buscar, etc._

<br/>

### Créditos: Credits

<hr/>

Autor (Author): Jonathan Garcia S. @Jony-softdeveloper

### Licencia: License

<hr/>

El projecto está [licenciado] bajo los téminos de **GPL-3.0-o-superior** .

This project is [licensed] under the terms of the **GPL-3.0-or-later**.

[Python]: https://www.python.org/downloads/ "Python"
[Pandas]: https://pandas.pydata.org/ "Pandas"
[Request]: https://docs.python-requests.org/en/latest/ "Request"
[Mypy]: https://mypy.readthedocs.io/en/stable/ "Mypy"
[PokeAPI]: https://pokeapi.co/docs/v2 "PokeAPI"
[Pytest]: https://pytest-cov.readthedocs.io/en/latest/ "Pytest"
[licenciado]: https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/copying.txt "licenciado"
[licensed]: https://github.com/Jony-softdeveloper/Questions_PokeAPI/blob/main/copying.txt "licensed"
