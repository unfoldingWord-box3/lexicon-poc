This repository contains a proof of concept.

# Prerequisites

- make sure you are running a recent version of Python
- create a virtual environment (for instance using `mkvirtualenv lexicon` if you are using virtualenv-wrapper)
- activate that virtual environment (for instance using `workon lexicon` if you are using virtualenv-wrapper)
- in that virtual environment install the dependencies (`pip install -r requirements.txt`)

# Resources

To create the actual database, we first need to get the text files that serve as the basis for the database. This proof of concept uses recent English resources. 

    cd data
    ./get_data.sh

# Relational database

To create and populate the database, as well as create links between the resources, do the following. This might take a cup of coffee.

    cd sql
    ./run.sh

This command will create a series of csv files in the data directory. It will also create an sqlite database called project_lexicon/alignment.db 

# Run the webapp

Move into the project_lexicon folder and run `python manage.py runserver` to start a local server and navigate to the url that is provided in the terminal when running that command.

# Visualise the data model

MOve into the projext_lexicon folder and run `python manage.py graph_models lexicon | dot -Tpng -o dataModel.png`. This command assumes you have dot up and running.

# License

MIT License

The data used in this repository have their own licenses so please verify and download the
unfoldingWord data such as the en_ULT and the hbo_uhb.

This project is not actively maintained, but feel free to create an issue in order to find out
more about the project.
