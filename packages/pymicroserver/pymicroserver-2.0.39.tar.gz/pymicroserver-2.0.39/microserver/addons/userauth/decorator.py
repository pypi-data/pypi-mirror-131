# @Time    : 2018/6/26 11:28
# @Author  : Niyoufa
import functools
from microserver.addons.userauth.error import AuthError


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_current_user():
            raise AuthError(401)
        return method(self, *args, **kwargs)
    return wrapper