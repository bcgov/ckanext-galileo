# ckanext-galileo
Logs CKAN usage to the Galileo Analytics platform

##Installation

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

##Known issues

This package depends on mashape-analytics which itself has some dependencies.  
Mashape-analytics requires specific versions of its dependencies.  CKAN also
has some dependencies, some of which overlap those of mashape-analytics.  In some
cases the required versions may be incompatible.  Suggested work arounds:

1. run ckanext-galileo in its own virtualenv
2. await an update to mashape analytics that fixes this issue: 
  https://github.com/Mashape/analytics-agent-python/issues/8