class EduLinkError(Exception):
    # Base class for all EduLink Exceptions
    pass

class ProvisioningError(EduLinkError):
    # Raised upon error in Provisioning
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SchoolDetailsError(EduLinkError):
    # Raised upon error in Provisioning
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)