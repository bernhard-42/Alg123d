from build123d.direct_api import *
from build123d.build_enums import *

from .direct_api import *
from .common import *
from .generic import *
from .part import *
from .sketch import *
from .line import *

MM = 1
CM = 10 * MM
M = 1000 * MM
IN = 25.4 * MM
FT = 12 * IN

try:
    from cq_vscode import show, show_object, set_defaults, reset_show

    print("Loaded show, show_object, set_defaults, reset_show")
except:
    ...
