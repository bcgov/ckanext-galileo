# -*- coding: utf-8 -*-

"""
This module contains a CKAN plugin that records all CKAN HTTP requests to the 
Galileo analytics platform (https://getgalileo.io/).  

Use of this plugin requires a Galileo service token.  The service token and other 
analytics recording parameters can be defined in CKAN's .ini file. The following 
parameters are available:

  galileo_service_token (required)
  galileo_environment (required)
  galileo_connection_timeout: timeout when communicating with 'galileo_host' in seconds. (optional, default=30)
  galileo_retry_count: number of times to retry sending analytics data to 'galileo_host' after a timeout. (optional, default=0)
  galileo_host (optional, default='collector.galileo.mashape.com')
  galileo_port (optional, default=443)

author: brock@bandersgeo.ca
"""

import ckan.plugins as p
from mashapeanalytics.middleware import WsgiMiddleware as GalileoAnalytics

log = __import__('logging').getLogger(__name__)

class GalileoPlugin(p.SingletonPlugin): 

  #interfaces
  p.implements(p.IMiddleware, inherit=True)

  #IMiddleware

  def make_middleware(self, app, config):

    """
    Attach the galileo analytics agent to the app
    """

    #load plugin config settings, or use defaults if not provided
    galileo_token = config.get('galileo_service_token')
    galileo_environment = config.get('galileo_environment')
    galileo_host = config.get('galileo_host', "collector.galileo.mashape.com")
    galileo_port = config.get('galileo_port', 443)
    galileo_connection_timeout = config.get('galileo_connection_timeout', 30)
    galileo_retry_count = config.get('galileo_retry_count', 0)

    #check that required configuration properties are set
    if not galileo_token:
      log.warn("'galileo_service_token' configuration property is required, but not specified in .ini file")
      return app

    if not galileo_environment:
      log.warn("'galileo_environment' configuration property is required, but not specified in .ini file")
      return app


    try:      
      #Attach the galileo analytics agent to CKAN
      app = GalileoAnalytics(app, galileo_token, environment=galileo_environment, host=galileo_host, port=galileo_port, connection_timeout=galileo_connection_timeout, retry_count=galileo_retry_count) 
      log.info("Galileo analytics enabled.  Sending analytics to target='%s:%s', environment='%s'", galileo_host, galileo_port, galileo_environment)
    except AttributeError as e:
      log.error("Unable to enable Galileo analytics with target='%s:%s', environment='%s'", galileo_host, galileo_port, galileo_environment)


    return app
