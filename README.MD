# intelligent-catalog-web
All files and structure for Intelligent Catalog Web Application product

## Accessing Stage
- Go to http://35.199.100.173
- user: bmind  |  password: aicatalog1

## Accessing in Production
- Go to http://35.198.9.66
- user: bmind  |  password: aicatalog1

## Running in Production

- Open GCP console
- Go to Compute Engine
- Click in bmind-intelligent-catalog-vm VM Instance
- Click in SSH to open more options
- Select "View gcloud command"
- In the modal, select RUN IN CLOUD SHELL  (Will open a window in the browser)

- Go to directory `bmind-intelligent-catalog-web-vm:/home/bmind/DataViz$`
- Run the follow command to up the Django Server

`sudo python3 manage.py runserver 10.158.0.2:80'`


## Getting Started

This repository is to develop our offer codename Intelligent Catalog used by Via Varejo and Dotz

Intelligent Catalog bMind service codename is used to support and help data scientists and DBAs to create an unique data repository using Artificial Intelligence techniques to group, link and deduplicate data.

### Steps
- Landing Zone: raw data, all data as they are
- Sensitive Zone: information with security and restritive access
- Working Zone: human interaction to work, link and audit results from bMind processing
- Golden Zone: The final goal, a data catalog cleaned, deduped and ready to use through our APIs

### Folder Structure

Describe here how will be our folder structure
- folder 1: Contains all templates
- folder 2: Contains all components to support operation
- folder 3: Contains all scripts and 3d party components

## Built With
Describe all external libraries used for this project
Examples:
* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Authors

bMind.ai (c)

## License

This is a commercial and private software development project

© 2017 bMind.ai ALL RIGHTS RESERVED

## Acknowledgments
