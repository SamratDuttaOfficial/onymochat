import io
import urllib.parse
import socks

# Tutorials for urllib to fetch a site using the proxy on the SOCKS_PORT:
# https://stem.torproject.org/tutorials/to_russia_with_love.html


class QueryHiddenService:
    # This is the class where the functions will reside in.
    # I made an object from the class where I wanted to use it.

    def __init__(self, domain, socks_port):
        # This is just like a Java class where I'd have done this.domain = domain
        self.domain = domain
        self.socks_port = int(socks_port)

    def query(self, route='/'):
        # This function fetches a site using the proxy on the socks_port using urllib.

        socks_port = self.socks_port
        domain = self.domain + route
        # An example: domain = z6m7z3bcgnok6zxg.onion/user/sam/message/hello there

        domain = "http://" + domain

        output = io.BytesIO()

        try:
            out = urllib.request.urlopen(domain).read()
            output.write(out)
            output = output.getvalue()
            output = output.decode('utf8', 'ignore')
            return str(output)

        except Exception as e:
            if "No connection could be made" in str(e):
                return "Unable to reach %s." % domain
            if "HTTP Error 404" in str(e):
                return "Unable to reach %s." % domain
            if "urlopen error Socket error" in str(e):
                return "Unable to reach %s." % domain
            else:
                return "Unable to reach " + domain + ". Query Error: " + str(e)
