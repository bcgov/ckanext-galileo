import mimetypes

import ckan.plugins as p

log = __import__('logging').getLogger(__name__)

class AnalyticsPostThread(threading.Thread):
    """
    This thread continually checks its queue of data_dict. 
    If the queue is not empty, the thread posts its values to Galileo
    """

    def __init__(self, queue):
      """
      :param queue: a queue of data_dict to be posted to Galileo.  It may be shared by
      multiple threads.
      """
      threading.Thread.__init__(self)
      self.queue = queue


    def run(self):
      while True:
        # grabs host from queue
        data_dict = self.queue.get()

        #TODO: post the data_dict to Galileo

        # signals to queue job is done
        self.queue.task_done()

class GalileoPlugin(p.SingletonPlugin): 

  #interfaces
  p.implements(p.IRoutes, inherit=True)
  p.implements(p.IConfigurable, inherit=True)

  #a queue of data_dict that should be posted to Galileo
  ananytics_queue = Queue.Queue()

  #from IConfigurable

  def configure(self, config):
    #spawn some daemon threads to post queued analytics to Galileo
    for i in range(5):
      t = AnalyticsPostThread(self.analytics_queue)
      t.setDaemon(True)
      t.start()

  #from IRoutes

  def after_map(self, map):
      """
      After setting up routes, inject the analytics reporting capability into the 
      active controller
      """
      self._inject_analytics_reporting(map)
      return map

  #private

  def _inject_analytics_reporting(self, map):

        """
        Injects analytics tracking capabilities into the active controller.        
        This is done by decorating the controller's resource_download function 
        with another function that logs the analytics.
        """

        if '_routenames' in map.__dict__:
            if 'resource_download' in map.__dict__['_routenames']:
                route_data = map.__dict__['_routenames']['resource_download'].__dict__
                route_controller = route_data['defaults']['controller'].split(
                    ':')
                module = importlib.import_module(route_controller[0])
                controller_class = getattr(module, route_controller[1])
                controller_class.resource_download = self._queue_analytics_decorator(
                    controller_class.resource_download)
            else:
                # If no custom uploader applied, use the default one
                PackageController.resource_download = self._queue_analytics_decorator(
                    PackageController.resource_download)

  def _queue_analytics(
      user, event_type, request_obj_type, request_function, request_id):

    """
    Add the analytics for the current request to the plugin's queue.
    """

    if config.get('MASHAPE_ANALYTICS_SERVICE_TOKEN'):
      data_dict = {
          "v": 1,
          "tid": config.get('MASHAPE_ANALYTICS_SERVICE_TOKEN'),
          "cid": hashlib.md5(c.user).hexdigest(),
          # customer id should be obfuscated
          "t": "event",
          "dh": c.environ['HTTP_HOST'],
          "dp": c.environ['PATH_INFO'],
          "dr": c.environ.get('HTTP_REFERER', ''),
          "ec": event_type,
          "ea": request_obj_type + request_function,
          "el": request_id,
      }
      GalileoPlugin.analytics_queue.put(data_dict)

  def _queue_analytics_decorator(func):

    """
    Decorate the given function with a call to _queue_analytics.  Return the new
    decorator function.

    :param func: a resource_download function that takes these arguments: cls, id, resource_id, filename
    """

      def decorator_func(cls, id, resource_id, filename):
          _queue_analytics(
              c.user,
              "CKAN Resource Download Request",
              "Resource",
              "Download",
              resource_id
          )

          return func(cls, id, resource_id, filename)

      return decorator_func