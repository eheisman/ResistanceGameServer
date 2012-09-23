import jinja2
import os
import urllib
import User
import webapp2

from calculatehash import calculate_hash
from Cypto.hash import SHA256
from google.appengine.api import mail, urlfetch, users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Register(webapp2.RequestHandler):
    def post(self):
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
        #For use in case of failures
        fail_dict = {}
        #Captcha fail 
        if res.startswith("false\n"):
            fail_dict["captcha_fail"] = True
        #Extract username
        uname = self.request.get("uname")
        #Sanitize username
        if uname is None:
            fail_dict["uname_bad"] = "Username unspecified"
            fail_dict["uname"] = ""
        #Remove unwanted characters
        uname = re.sub(User.deniedset, "", uname)
        #If the name is too short, die
        if len(uname) < 3:
            fail_dict["uname_bad"] = "Invalid username"
            fail_dict["uname"] = uname
        #Shorten if necessary
        elif len(uname) > 16: 
            uname = ign[:16]
        #Make sure passwords are the same
        password = self.request.get("pass")
        if password != self.request.get("again"):
            fail_dict["pwmismatch"] = True
        #Make hash
        userkey = calculate_hash(uname, password)
        #Add the user to the database
        try:
            self.adduser(userkey, uname)
        except RuntimeError as e:
            #If it failed because the name was taken
            if str(e) == "Username in use":
                fail_dict["uname_bad"] = "Username in use"
        except Error as e:
            #Dunno.  Tell the user
            fail_dict["uname_bad"] = "Unknown error.  Please send a screenshot to the developers: %s"%str(e)
        #If anything is in fail_dict, it failed.  Try again
        if fail_dict:
            #Fill the uname field if we can
            fail_dict["uname"] = uname
            #Let the user try again
            return self.get(fail_dict)
        #Send an email to the user
        email = users.get_current_user().email()
        mail.send_mail(sender="The Resistance Game support",
                       to=email,
                       subject="TRG Account Created",
                       body="""The Resistance Game account details:
Username: %s
Userkey: %s

TODO: Put more useful info here"""%(uname,userkey))
        #Return a page telling the user his account's been created.
        template = jinja_environment.get_template("register.html")
        template_values = {"uname": uname,
                           "email": email)
        self.response.out.write(template.render(template_values))

    @db.transactional
    def adduser(self, userkey, uname):
        """Add a user to the datastore."""
        #Check for a user with that name
        if User.get(uname) is not None:
            raise RuntimeError("Username in use")
        if User.gql("WHERE googleacct = :1", users.get_current_user()).count() > 0:
            raise RuntimeError("Account in use")
        User.(key_name=uname, userkey=userkey, uname=uname).put()

    #TODO: Implement IP-based rate limiting
    def get(self, form_fields=None):
        """Handle GET requests.
           @param form_fields: Fills in form fields on error
           @type form_fields: dict
           C{form_fields} may have the following fields::
             uname: Username
             captcha_fail: True if the captcha caused the problem
             pwmismatch: True if passwords did not match
             uname_bad: String describing why the username was bad
        """
        if form_fields is None:
            form_fields = {"uname": "",
                           "captcha_fail": False}
        if "uname" not in form_fields:
            form_fields["uname"] = ""
        if "captcha_fail" not in form_fields:
            form_fields["captcha_fail"] = False
        if "pwmismatch" not in form_fields:
            form_fields["pwmismatch"] = False
        if "uname_bad" not in form_fields:
            form_fields["uname_bad"] = ""
        template = jinja_environment.get_template("register.html")
        self.response.out.write(template.render(form_fields))


app = webapp2.WSGIApplication([('/register', Register)],
                              debug=True)

