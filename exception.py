import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class RequestException:
  def __init__(self, exception):
    self.exception = exception

  def bad_request(self):
    logger.error(self.exception)
    bad_request_obj = {
      "errorType" : 'BadRequestError',
      "message" : self.exception
    }
    return bad_request_obj
