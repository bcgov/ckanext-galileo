# ckanext-galileo
Logs CKAN usage to the Galileo Analytics platform

Installation

1. Install ckanext-galileo 

  Within the CKAN virtualenv run the following:

    pip install -e 'git+https://github.com/bcgov/ckanext-galileo#egg=ckanext-galileo'

2. Update the CKAN .ini file

  ckan.plugins=<other plugins...>,galileo,<other plugins...>

  #Galileo settings
  galileo_service_token = <token here>
  galileo_environment = <environment name here>
  galileo_host = <collector host name here>
  galileo_port = <colector port here>