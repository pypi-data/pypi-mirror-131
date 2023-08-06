"""Exception for AquamaHydro"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021


class ApiError(Exception):
    pass

class ApiHttpNot200(Exception):
    pass

class ApiResponseEmpty(Exception):
    pass

class ApiResponseNotMessage(Exception):
    pass
