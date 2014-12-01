# vim:shiftwidth=2:tabstop=2:expandtab:textwidth=80:softtabstop=2:ai:

from libpius.constants import *
import json

class SignState(object):

  kSIGNED = 'SIGNED'
  kWILL_NOT_SIGN = 'WILL_NOT_SIGN'
  kNOT_SIGNED = 'NOT_SIGNED'
  kPIUS_SIGNED_KEYS = os.path.join(PIUS_HOME, 'signed_keys')

  def __init__(self):
    self.state = {}
    self._load()
    self.modified = False

  def _load(self):
    self.state = SignState.load_signed_keys()

  def _validate_value(self, val):
    assert(val in [
      SignState.kSIGNED, SignState.kWILL_NOT_SIGN, SignState.kNOT_SIGNED
    ])

  def __iter__(self):
    return self.state.__iter__()

  def signed(self, key):
    return key in self.state and self.state[key] == SignState.kSIGNED

  def will_not_sign(self, key):
    return key in self.state and self.state[key] == SignState.kWILL_NOT_SIGN

  def update(self, key, val):
    # we don't store NOT_SIGNED, it's meaningless.
    if val == SignState.kNOT_SIGNED:
      return
    self._validate_value(val)
    self.state[key] = val
    self.modified = True

  def save(self):
    SignState.store_signed_keys(self.state)

  @classmethod
  def load_signed_keys(self):
    fp = open(SignState.kPIUS_SIGNED_KEYS, 'r')
    data = fp.read()
    try:
      signstate = json.loads(data)
    except:
      signstate = dict((key, 'SIGNED') for key in data.strip().split("\n"))
    fp.close()
    return signstate

  @classmethod
  def store_signed_keys(self, signstate):
    # re-read in the list and merge it...
    prev_signstate = SignState.load_signed_keys()
    # merge the two with the one we're passed in winning
    result = dict(prev_signstate.items() + signstate.items())
    fp = open(SignState.kPIUS_SIGNED_KEYS, 'w')
    fp.write(json.dumps(result))
    fp.close()
