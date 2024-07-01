class UserAPI(object):

    def __init__(self, service=None):
        self.service = service
        if service is None:
            from server.apps.user.services.user import UserService
            self.service = UserService

    def claim(self, user):
        return self.service.claim(user)

    def get_user_available_balance(self, user):
        return self.service.get_user_available_balance(user)
