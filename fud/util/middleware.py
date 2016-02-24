from django.http import HttpResponsePermanentRedirect


class LocalhostRedirectionMiddleware(object):
    def process_request(self, request):
        """
        Redirects requests to localhost to fud.localhost
        """
        path = request.get_raw_uri()
        if 'localhost' in path and 'fud' not in path:
            path = path.replace('localhost', 'fud.localhost')
            return HttpResponsePermanentRedirect(path)
        else:
            pass
