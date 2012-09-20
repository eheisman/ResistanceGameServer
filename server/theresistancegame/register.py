import jinja2
import os
import urllib
import webapp2

from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Register(webapp2.RequestHandler):
    def post(self):
        #Extract username
        uname = self.request.get("uname")
        #Verify recaptcha
        recaptcha_url = "http://www.google.com/recaptcha/api/verify"
        recaptcha_parameters = {
            "privatekey":   "6Lfem9YSAAAAALb9P93TL7b5gU-nQ9YH2Xb5j91l",
            "remoteip":     self.request.remote_addr,
            "challenge":    self.request.get("recaptcha_challenge_field"),
            "response":     self.request.get("recaptcha_response_field"),
        }
        recaptcha_parameters=urllib.urlencode(recaptcha_parameters)
        res = urlfetch.fetch(url=recaptcha_url, payload=recaptcha_parameters, method=urlfetch.POST,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if 
    #TODO: Implement automatic form-filling upon captcha fail 
    #TODO: Implement IP-based rate limiting
    def get(self, form_fields=None):
        """Handle GET requests.
           @param form_fields: Fills in form fields on error
           @type form_fields: dict
           C{form_fields} may have the following fields::
             uname: Username
             captcha_fail: True if the captcha caused the problem
        """
        template = jinja_environment.get_template("register.html")
        self.response.out.write(template.render({}))


app = webapp2.WSGIApplication([('/register', Register)],
                              debug=True)

