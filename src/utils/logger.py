class Logger:
    def __init__(self):
        self.api = None

    def bind(self, api):
        self.api = api

    def info(self, msg):
        if self.api is not None:
            self.api.addMessage(msg)

    def error(self, msg):
        if self.api is not None:
            self.api.addMessage("[ERROR] " + msg)

logger = Logger()
