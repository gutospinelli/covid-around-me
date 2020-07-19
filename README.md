# Covid-Around-Me - Rio de Janeiro


####En-Us
Covid Around Me is a project that accesses data from open platforms like
www.data.rio and www.brasil.io to show how many cases of Covid have been found around you, from
anonymous and individualized data released by the municipal health office.

For now, we only offer data from the city of Rio de Janeiro. Feel free to contribute to this project.

---
####Pt-Br
O projeto covid ao meu redor é um projeto que acessa dados de plataformas abertas como
www.data.rio e www.brasil.io para mostrar quantos casos de Covid foram encontrados ao redor de você, a partir
de dados anônimos e indivudializados divulgados pelas secretarias municipais de saúde.

Por hora, só dados do Rio de Janeiro estão disponíveis. Se desejar, contribua com o projeto.

---

### Tech Stack
Backend:
- Python
- Flask
- Pandas

FrontEnd:
- HTML
- JavaScript
- Bootstrap

---

### Usage

This project is published in Heroku at http://covid-around-me.herokuapp.com/

An so, it has some Heroku required files like:
- Procfile : required to run 
- runtime.txt : required to set python runtime to 3.7.6
- requirements.txt : required by heroku to prepare the virtual running environment (you can also use PIPFILE 
if you prefer)

To use this project in your own Environment (DEV purposes), it couldn't be easier:

Just:

```
FLASK_APP=covid_around_me.py flask run
```

---

### Acknowledgements

First of all thanks to all open data platforms as www.brasil.io and www.data.rio . Without open and 
reliable data projects like this would never be developed and open to public

Second, I would also like to thank Jessica Temporal 
for her great python tutorials and contribution to the 
open source community. You can find her at https://jtemporal.com/

Third, but not last, a great thanks to www.cepaberto.com
who provides a great Brazilian CEP API (CEP is short for Brazilian Postal Code).   