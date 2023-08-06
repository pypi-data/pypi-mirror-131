from oregano.plugins import BasePlugin, daemon_command
from .contract_finder import find_contract_for_address, find_contract_by_p2sh
from oregano.wallet import Standard_Wallet
from oregano.storage import WalletStorage
from oregano.util import NotEnoughFunds, ServerErrorResponse, Weak
from oregano.address import Address
from .mecenas_contract import MecenasContract, ContractManager, PROTEGE, UTXO
import random, os, tempfile, string

class Plugin(BasePlugin):
    def __init__(self, parent, config, name):
        BasePlugin.__init__(self, parent, config, name)
        witam=0

    def fullname(self):
        return 'Mecenas'

    def description(self):
        return "description"

    def diagnostic_name(self):
        return "mecenas"

    @daemon_command
    def hello(self, daemon, config):
        return "hello"


    @daemon_command
    def mecenas_in_address(self, daemon, config):
        network = daemon.network
        if not network:
            return "error: cannot run test server without electrumx connection"
        subargs = config.get('subargs', ())
        a = subargs[0]
        tmp_wallet, passwd = create_tmp_wallet(network)
        c = find_contract_for_address(a,network,MecenasContract)
        keypairs, public_keys = get_keypairs_whatever(tmp_wallet, passwd, c)
        manager = ContractManager(c, keypairs, public_keys, wallet=None)
        # -1 means all utxos on the address
        for tup in c:
            utxos = len(tup[UTXO])
            for i in range(utxos):
                manager.choice(tup, i, PROTEGE)
                tx = manager.pledge_tx()
                complete = manager.complete_method()
                manager.signtx(tx)
                complete(tx)
                try:
                    network.broadcast_transaction2(tx)
                except ServerErrorResponse as e:
                    bip68msg = 'the transaction was rejected by network rules.\n\nnon-BIP68-final (code 64)'
                    if bip68msg in e.server_msg['message']:
                        print("not ready")
                    else:
                        print(e.server_msg['message'])
        return

    @daemon_command
    def mecenas_in_p2sh_address(self, daemon, config):
        network = daemon.network
        if not network:
            return "error: cannot run test server without electrumx connection"
        subargs = config.get('subargs', ())
        a = subargs[0]
        tmp_wallet, passwd = create_tmp_wallet(network)
        c = find_contract_by_p2sh(a, network, MecenasContract)
        keypairs, public_keys = get_keypairs_whatever(tmp_wallet, passwd, c)
        manager = ContractManager(c, keypairs, public_keys, wallet=None)
        for tup in c:
            utxos = len(tup[UTXO])
            for i in range(utxos):
                manager.choice(tup, i, PROTEGE)
                tx = manager.pledge_tx()
                complete = manager.complete_method()
                manager.signtx(tx)
                complete(tx)
                try:
                    network.broadcast_transaction2(tx)
                except ServerErrorResponse as e:
                    bip68msg = 'the transaction was rejected by network rules.\n\nnon-BIP68-final (code 64)'
                    if bip68msg in e.server_msg['message']:
                        print("not ready")
                    else:
                        print(e.server_msg['message'])
        return

    @daemon_command
    def contract(self, daemon, config):
        network = daemon.network
        if not network:
            return "error: cannot run test server without electrumx connection"
        subargs = config.get('subargs', ())
        contract_address = subargs[0]
        c = find_contract_for_address(contract_address, network, MecenasContract)
        return

def create_tmp_wallet(network):
    file = ''
    for x in range(10):
        name = 'tmp_wo_wallet' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        file = os.path.join(tempfile.gettempdir(), name)
        if not os.path.exists(file):
            break
    else:
        raise RuntimeError('Could not find a unique temp file in tmp directory', tempfile.gettempdir())
    #tmp_pass = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    tmp_pass = None
    storage = WalletStorage(file)
    storage.set_password(tmp_pass, encrypt=True)
    from oregano import mnemonic, keystore
    seed = mnemonic.Mnemonic('en').make_seed('standard')
    keystore = keystore.from_seed(seed, tmp_pass, False)
    storage.put('keystore', keystore.dump())
    tmp_wallet = Standard_Wallet(storage)
    tmp_wallet.start_threads(network)
    Weak.finalize(tmp_wallet, delete_temp_wallet_file, file)
    print("tmp_pass", tmp_pass)
    return tmp_wallet, tmp_pass

def delete_temp_wallet_file(file):
    ''' deletes the wallet file '''
    if file and os.path.exists(file):
        try:
            os.remove(file)
        except Exception as e:
            pass

def get_keypairs_whatever(wallet, passwd, contract_tuple_list):
    keypairs = dict()
    public_keys = [dict()]*len(contract_tuple_list)
    address = wallet.get_unused_address()
    i = wallet.get_address_index(address)
    priv = wallet.keystore.get_private_key(i, None)
    public = wallet.get_public_keys(address)
    for t in contract_tuple_list:
        for m in range(3):
            public_keys[contract_tuple_list.index(t)][m]=public[0]
    keypairs[public[0]] = priv
    return keypairs, public_keys
