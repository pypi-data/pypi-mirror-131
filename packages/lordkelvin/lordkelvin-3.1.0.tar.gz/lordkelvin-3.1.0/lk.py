#!/usr/bin/env python3
'''
High level python EVM interface

Usage:
  lk ( b | balance  )  [ -q ] [ -j | -J ]                                                  <address>
  lk ( s | save     )  [ -q ] [ -j | -J ]                            <contract> [--as=<x>] <address>
  lk ( d | deploy   )  [ -q ] [ -j | -J ] [--v=<value>] [--u=<unit>] <contract> [--as=<x>] [<args>...]
  lk ( t | transact )  [ -v ] [ -j | -J ] [--v=<value>] [--u=<unit>] <contract> <function> [<args>...]
  lk ( x | execute  )  [ -v ] [ -j | -J ] [--v=<value>] [--u=<unit>] <contract> <function> [<args>...]
  lk ( c | call     )  [ -q ] [ -j | -J ]                            <contract> <function> [<args>...]
  lk ( a | address  )  [ -q ] [ -j | -J ]                            <contract>
  lk -h | --help
  lk --version

Options:
  -h --help     Show this screen.
  -q            quiet mode
  -v            verbose mode
  -J            JSON on
  -j            JSON off
  --version     Show version.
'''
__version__ = '3.1.0'
import os, sys, json, time
w3 = None
def balance(address=None):
    address = address or w3.eth.default_account
    return w3.eth.get_balance(address)
def get_balance(address=None):
    address = address or w3.eth.default_account
    return w3.eth.get_balance(address)
def w3_connect(default_account, onion=None):
    global w3
    from web3.auto import w3 as _w3
    w3 = _w3
    if default_account is not None:
        w3.eth.default_account = w3.eth.accounts[int(default_account)]
    else:
        w3.eth.default_account = os.getenv('PUBLIC')
        private                = os.getenv('PRIVATE','')
        from web3.middleware import construct_sign_and_send_raw_middleware
        from eth_account import Account
        acct = Account.from_key(private)
        #acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
        pass
    return w3
def   load_abi(name):
    return json.load(open(f'out/{name}.abi'))
def   load_bytecode(name):
    return           open(f'out/{name}.bin').read()
def   load_address(name):
    return           open(f'out/{name}.cta').read()
def   save_address(name, address):
    if 1:            open(f'out/{name}.cta','w').write(address)
    return address
def        cta(name):
    return load_address(name)
def   save_cta(name, address):
    return save_address(name, address)
def __link_contract(old_name, new_name, ext, msg):
    ofn, nfn = f"./{old_name}.{ext}", f"out/{new_name}.{ext}"
    try:   os.unlink(nfn)
    except FileNotFoundError: pass
    return os.symlink(ofn, nfn)
def   link_contract(old_name, new_name):
    __link_contract(old_name, new_name, "abi", "ABI ERR")
    __link_contract(old_name, new_name, "bin", "BIN ERR")
    pass
def   load_contract(name, address=None):
    if address is None:
        address = load_address(name)
        pass
    return w3.eth.contract(abi=load_abi(name), address=address)
def     tx_wait(tx_hash):
    return w3.eth.wait_for_transaction_receipt(tx_hash)
def    new_contract(name):
    return w3.eth.contract(abi=load_abi(name),
                           bytecode=load_bytecode(name))
def   wrap_contract(*a, **kw):
    return WrapContract(load_contract(*a, **kw))
def   ctor_contract(name):
    return new_contract(name).constructor
def mk_exec_contract(name):
    with open(f'out/{name}', 'w') as f:
        f.write('exec lk x `basename $0` "$@"\n')
        pass
    assert(os.system(f'chmod +x out/{name}') == 0)
    return name
def deploy_contract(name, *args, **kw):
    tx_receipt = _wcall(ctor_contract(name), *args, **kw)
    mk_exec_contract(name)
    return save_address(name, tx_receipt.contractAddress)
def _rcall(func, *args, **kw):
    return func(*args).call(kw)
def _wcall(func, *args, _from=None, tries=0, **kw):
    if _from: kw['from'] = _from
    while 1:
        try:
            return tx_wait(func(*args).transact(kw))
        except ValueError as e:
            tries -= 1
            if not tries or e.args[0]['code'] != -32010:
                raise
            print("retry...")
            time.sleep(0.1)
            pass
        pass
    return
class WrapMixin:
    def get_balance(_, address=None):
        return get_balance(address or _.address)
    pass 
class WrapContract(WrapMixin):
    @property
    def address(_): return _.contract.address
    @property
    def  events(_): return _.contract.events
    def __init__(_, contract):
        _.ras, _.was, _.contract = [], [], contract
        for f in contract.functions._functions:
            b = f['stateMutability'] in ['view','pure']
            if b: _.ras.append(f['name'])
            else: _.was.append(f['name'])
            pass
        pass
    def __getattr__(_, key): return _.get(key)
    def get(_, key):
        from functools import partial
        func = _.contract.functions.__dict__[key]        
        if key in _.ras: return partial(_rcall, func)
        if key in _.was: return partial(_wcall, func)
        raise KeyError(key)
    def get2(_, key):
        from functools import partial
        func = _.contract.functions.__dict__[key]        
        if key in _.ras: return False, partial(_rcall, func)
        if key in _.was: return True,  partial(_wcall, func)
        raise KeyError(key)
    pass
class WrapAccount(WrapMixin):
    def transfer(_, **kw): # to, value
        try:
            _ = w3.eth.default_account
            w3.eth.default_account = _.address
            tx_hash = w3.eth.send_transaction(kw)
            return w3.eth.wait_for_transaction_receipt(tx_hash)
        finally:
            w3.eth.default_account = _
            pass
        pass
    def __init__(_, address):
        if type(address) == int:
            address = w3.eth.accounts[address]
            pass
        _.address = address
        pass
    def __repr__(_): return repr(_.address)
    def  __str__(_): return  str(_.address)
    pass
def _f(x):
    if x == 'true':
        return True
    if x == 'false':
        return False
    if x == 'null':
        return None
    if x.startswith('@@'):
        return _f(open(f'out/{x[2:]}.cta').read().strip())
    if x.startswith('@'):
        return _f(open(       x[1:]      ).read().strip())
    if x.startswith('~'):
        try:    return   -int(x[1:])
        except: pass
        try:    return -float(x[1:])
        except: pass
        pass
    try:    return   int(x)
    except: pass
    try:    return float(x)
    except: pass
    return x
def println(result, _json, quiet=False):
    if quiet:
        return
    elif _json:
        d = dict(result)
        for k, v in d.items():
            if k == "logsBloom":
                d[k] = 'logsBloom'
            elif k == "logs":
                d[k] = 'logs'
            elif type(v).__name__=="HexBytes":
                d[k] = v.hex()
                pass
            pass
        result = json.dumps(d)
        pass
    return print(result)
def main():
    import eth_account, docopt
    from functools import partial
    A = docopt.docopt(__doc__, version=__version__)
    v = A['-v']
    q = A['-q']
    j = bool(A['-J'])
    if      A['balance'] or A['b']:
        println(balance(A['<address>']), j)
        raise exit(0)
    nname  = A['--as']
    name   = A['<contract>']
    func   = A['<function>']
    value  = A['--v'] or 0
    unit   =   'wei'
    w3 = w3_connect(os.getenv('WALLET'))
    if not w3.isConnected():
        print('no connection')
        raise exit(1)
    if nname:
        link_contract(name, nname)
        name = nname
        pass
    def execf(f, j, q):
        return println(f(*[_f(x) for x in A['<args>']],
                         value = w3.toWei(value,unit)), j, q)
    if     A['deploy'] or A['d']:
        execf(partial(deploy_contract, name),j, q)
    elif A['transact'] or A['t']:
        q = not v
        execf(wrap_contract(name).get(func), j, q)
    elif     A['call'] or A['c']:
        execf(wrap_contract(name).get(func), j, q)
    elif  A['execute'] or A['x']:
        writable, func = wrap_contract(name).get2(func)
        if writable:
            q = not v
            pass
        execf(func, j, q)
    elif  A['address'] or A['a']:
        println(cta(name), j, q)
    elif     A['save'] or A['s']:
        save_cta(mk_exec_contract(name), A['<address>'])
    else: print('dunno what to do', A) or exit(1)
    pass
if __name__=='__main__': main()
