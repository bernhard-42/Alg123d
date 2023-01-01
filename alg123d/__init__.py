from .direct_api import *
from .conversions import *
from .common import *
from .generic import *
from .part import *
from .sketch import *
from .line import *
from .algcompound import AlgCompound, LazyAlgCompound

from .assembly import *

try:
    if os.environ.get("JPY_PARENT_PID") is not None:
        from jupyter_cadquery import show, show_object, set_defaults, open_viewer
        print("Loaded show, show_object, set_defaults, open_viewer")
    else:
        from cq_vscode import show, show_object, set_defaults, reset_show, Animation
        print("Loaded show, show_object, set_defaults, reset_show and Animation")

except Exception as ex:
    ...
