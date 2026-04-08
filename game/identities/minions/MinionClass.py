from ..IdentityClass import Identity, Status

class Minion(Identity):
    def identityInit(self):
        self.type = 'minion'

    