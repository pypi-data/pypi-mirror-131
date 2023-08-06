
from oregano.address import Address, ScriptOutput
from oregano.transaction import Transaction
from itertools import permutations, combinations
from oregano.storage import WalletStorage
from oregano.wallet import ImportedAddressWallet
import random, os, tempfile, string


## Contract tuple list
# [(utxos, Contract, role), ... ]

def find_contract_in_wallet(wallet, contract_cls):
    contract_tuple_list=[]
    for hash, t in wallet.transactions.items():
        contract = scan_transaction(t, contract_cls)
        if contract is None:
            continue
        response = wallet.network.synchronous_get(
            ("blockchain.scripthash.listunspent", [contract.address.to_scripthash_hex()]))
        if unfunded_contract(response):  # skip unfunded and ended contracts
            continue
        a=contract.addresses
        contract_tuple_list.append((response, contract, find_my_role(a, wallet)))
    remove_duplicates(contract_tuple_list)
    return contract_tuple_list

def find_contract_for_address(address, network, contract_cls):
    contract_tuple_list=[]
    for x in range(10):
        name = 'tmp_wo_wallet' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        file = os.path.join(tempfile.gettempdir(), name)
        if not os.path.exists(file):
            break
    else:
        raise RuntimeError('Could not find a unique temp file in tmp directory', tempfile.gettempdir())
    tmp_pass = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    storage = WalletStorage(file)
    storage.set_password(tmp_pass, encrypt=True)
    wallet = ImportedAddressWallet(storage)
    a = Address.from_string(address)
    wallet.import_address(a)
    wallet.start_threads(network)
    wallet.wait_until_synchronized()
    for hash, t in wallet.transactions.items():
        contract = scan_transaction(t, contract_cls)
        if contract is None:
            continue
        response = network.synchronous_get(
            ("blockchain.scripthash.listunspent", [contract.address.to_scripthash_hex()]))
        if unfunded_contract(response):  # skip unfunded and ended contracts
            continue
        a=contract.addresses
        contract_tuple_list.append((response, contract, [0])) #executing just for Protege
    contract_tuple_list = remove_duplicates(contract_tuple_list)
    return contract_tuple_list

def find_contract_by_p2sh(p2sh_address, network, contract_cls):
    contract_tuple_list=[]
    addy = Address.from_string(p2sh_address)
    utxos = network.synchronous_get(
            ("blockchain.scripthash.listunspent", [addy.to_scripthash_hex()]))
    history = network.synchronous_get(
            ("blockchain.scripthash.get_history", [addy.to_scripthash_hex()]))
    for t in history:
        raw = network.synchronous_get(
            ("blockchain.transaction.get", [t["tx_hash"]]))
        tx = Transaction(raw)
        contract = scan_transaction(tx, contract_cls)
        if contract is None:
            continue
        else:
            role = 0
            contract_tuple_list.append((utxos, contract, [role]))
            break
    return contract_tuple_list

def remove_duplicates(contracts):
    c = contracts
    for c1, c2 in combinations(contracts,2):
        if c1[1].address == c2[1].address:
            c.remove(c1)
    return c


def unfunded_contract(r):
    """Checks if the contract is funded"""
    s = False
    if len(r) == 0:
        s = True
    for t in r:
        if t.get('value') == 0: # when contract was drained it's still in utxo
            s = True
    return s


def scan_transaction(tx, contract_cls):
    out = tx.outputs()
    address, v, data  = parse_p2sh_notification(out)
    if address is None or v is None or data is None:
        return
    no_participants = contract_cls.participants(v)
    if no_participants > (len(out)+1):
        return None
    candidates = get_candidates(out[1:], no_participants)
    for c in candidates:
        mec = contract_cls(c,tx.as_dict(),v=v, data=data)
        if mec.address.to_ui_string() == address:
            return mec


def parse_p2sh_notification(outputs):
    opreturn = outputs[0]
    try:
        assert isinstance(opreturn[1], ScriptOutput)
        assert opreturn[1].to_ui_string().split(",")[1] == " (4) '>sh\\x00'"
        a = opreturn[1].to_ui_string().split("'")[3][:42]
        version = float(opreturn[1].to_ui_string().split("'")[3][42:])
        data = [int(e) for e in opreturn[1].to_ui_string().split("'")[5].split(' ')]
        return Address.from_string(a).to_ui_string(), version, data
    except:
        return None, None, None


def get_candidates(outputs, participants):
    """Creates all permutations of addresses that are not p2sh type"""
    candidates = []
    for o in permutations(outputs, participants):
        kinds = [i[1].kind for i in o]
        #if 1 in kinds:
            #continue
        addresses = [i[1] for i in o]
        candidates.append(addresses)
    return candidates


def find_my_role(candidates, wallet):
    """Returns my role in this contract. 0 is protege, 1 is mecenas"""
    roles=[]
    for counter, a in enumerate(candidates, start=0):
        if wallet.is_mine(a):
            roles.append(counter)
    if len(roles):
        return roles

