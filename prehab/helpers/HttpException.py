class HttpException(Exception):

    def __init__(self, code, custom_message='', details=''):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(details)
        # Exception.__init__(details)

        # Now for your custom code...
        self.http_detail = details
        self.http_custom_message = custom_message
        self.http_code = code
