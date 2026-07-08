from . import gap
from . import drought

HANDLERS = {
    "gap": gap.evaluate,
    "drought": drought.evaluate
}