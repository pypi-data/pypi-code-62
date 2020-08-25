# Define a group of data structures from the Blockcypher API endpoints
from typing import Any
from bitmast_blockcypher.util import BusinessDataObject, validate


def validate_wallet(wallet: Any):
    if isinstance(wallet, BaseWallet):
        wallet = wallet.name
    elif isinstance(wallet, str):
        if not validate(wallet, 'name'):
            return False
    return wallet or False


class BaseAddress(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        private = kwargs.get('private')
        public = kwargs.get('public')
        address = kwargs.get('address')
        wif = kwargs.get('wif')

        if validate(private, 'private'):
            self.private = private
        if validate(public, 'public'):
            self.public = public
        if validate(address, 'address'):
            self.address = address
        if validate(wif, 'wif'):
            self.wif = wif

        super(BaseAddress, self).__init__(*args, **kwargs)


class Address(BaseAddress):

    def __init__(self, *args, **kwargs):
        address = kwargs.get('address')
        wallet = kwargs.get('wallet')
        hd_wallet = kwargs.get('hd_wallet')
        total_received = kwargs.get('total_received')
        total_sent = kwargs.get('total_sent')
        balance = kwargs.get('balance')
        unconfirmed_balance = kwargs.get('unconfirmed_balance')
        final_balance = kwargs.get('final_balance')
        n_tx = kwargs.get('n_tx')
        unconfirmed_n_tx = kwargs.get('unconfirmed_n_tx')
        final_n_tx = kwargs.get('final_n_tx')
        tx_url = kwargs.get('tx_url')
        txs = kwargs.get('txs')
        txrefs = kwargs.get('txrefs')
        unconfirmed_txrefs = kwargs.get('unconfirmed_txrefs')
        has_more = kwargs.get('hasMore')
        if validate(address, 'address'):
            self.address = address
        if validate(wallet, 'wallet'):
            self.wallet = wallet
        if validate(hd_wallet, 'hd_wallet'):
            self.hd_wallet = hd_wallet
        if validate(total_received, 'total_received'):
            self.total_received = total_received
        if validate(total_sent, 'total_sent'):
            self.total_sent = total_sent
        if validate(balance, 'balance'):
            self.balance = balance
        if validate(unconfirmed_balance, 'unconfirmed_balance'):
            self.unconfirmed_balance = unconfirmed_balance
        if validate(final_balance, 'final_balance'):
            self.final_balance = final_balance
        if validate(n_tx, 'n_tx'):
            self.n_tx = n_tx
        if validate(unconfirmed_n_tx, 'unconfirmed_n_tx'):
            self.unconfirmed_n_tx = unconfirmed_n_tx
        if validate(final_n_tx, 'final_n_tx'):
            self.final_n_tx = final_n_tx
        if validate(tx_url, 'tx_url'):
            self.tx_url = tx_url
        if validate(txs, 'txs'):
            self.txs = txs
        if validate(txrefs, 'txrefs'):
            self.txrefs = txrefs
        if validate(unconfirmed_txrefs, 'unconfirmed_txrefs'):
            self.unconfirmed_txrefs = unconfirmed_txrefs
        if validate(has_more, 'hasMore'):
            self.hasMore = has_more

        super(Address, self).__init__(*args, **kwargs)


class AddressKeyChain(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        address = kwargs.get('address')
        public = kwargs.get('public')
        private = kwargs.get('private')
        wif = kwargs.get('wif')
        pubkeys = kwargs.get('pubkeys')
        script_type = kwargs.get('script_type')
        original_address = kwargs.get('original_address')
        oap_address = kwargs.get('oap_address')

        if validate(address, 'address'):
            self.address = address
        if validate(public, 'public'):
            self.public = public
        if validate(private, 'private'):
            self.private = private
        if validate(wif, 'wif'):
            self.wif = wif
        if validate(pubkeys, 'pubkeys'):
            self.pubkeys = pubkeys
        if validate(script_type, 'script_type'):
            self.script_type = script_type
        if validate(original_address, 'original_address'):
            self.original_address = original_address
        if validate(oap_address, 'oap_address'):
            self.oap_address = oap_address

        super(AddressKeyChain, self).__init__(*args, **kwargs)


class BaseWallet(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        token = kwargs.get('token')
        name = kwargs.get('name')
        addresses = kwargs.get('addresses')

        if validate(token, 'token'):
            self.token = token
        if validate(name, 'name'):
            self.name = name
        if validate(addresses, 'addresses'):
            self.addresses = addresses

        super(BaseWallet, self).__init__(*args, **kwargs)


class HDChain(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        chain_addresses = kwargs.get('chain_addresses')
        index = kwargs.get('index')
        if validate(chain_addresses, 'chain_addresses'):
            self.chain_addresses = chain_addresses
        if validate(index, 'index'):
            self.index = index
        super(HDChain, self).__init__(*args, **kwargs)


class HDAddress(BusinessDataObject):

    def __init__(self, *args, **kwargs):

        address = kwargs.get('address')
        path = kwargs.get('path')
        public = kwargs.get('public')

        if validate(address, 'address'):
            self.address = address
        if validate(path, 'path'):
            self.path = path
        if validate(public, 'public'):
            self.public = public

        super(HDAddress, self).__init__(*args, **kwargs)


class HDWallet(BaseWallet):

    def __init__(self, *args, **kwargs):

        token = kwargs.get('token')
        name = kwargs.get('name')
        chains = kwargs.get('chains')
        hd = kwargs.get('hd')
        extended_public_key = kwargs.get('extended_public_key')
        subchain_indexes = kwargs.get('subchain_indexes')

        if validate(token, 'token'):
            self.token = token
        if validate(name, 'name'):
            self.name = name
        if validate(chains, 'chains'):
            self.chains = chains
        if validate(hd, 'hd'):
            self.hd = hd
        if validate(extended_public_key, 'extended_public_key'):
            self.extended_public_key = extended_public_key
        if validate(subchain_indexes, 'subchain_indexes'):
            self.subchain_indexes = subchain_indexes

        super(HDWallet, self).__init__(*args, **kwargs)


class Event(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        identifier = kwargs.get('id') or kwargs.get('identifier')
        event = kwargs.get('event')
        hash = kwargs.get('hash')
        wallet_name = kwargs.get('wallet_name')
        token = kwargs.get('token')
        address = kwargs.get('address')
        confirmations = kwargs.get('confirmations')
        confidence = kwargs.get('confidence')
        script = kwargs.get('script')
        url = kwargs.get('url')
        callback_errors = kwargs.get('callback_errors')

        if validate(identifier, 'id'):
            self.identifier = identifier
        if validate(event, 'event'):
            self.event = event
        if validate(hash, 'hash'):
            self.hash = hash
        if validate(wallet_name, 'wallet_name'):
            self.wallet_name = wallet_name
        if validate(token, 'token'):
            self.token = token
        if validate(address, 'address'):
            self.address = address
        if validate(confirmations, 'confirmations'):
            self.confirmations = confirmations
        if validate(confidence, 'confidence'):
            self.confidence = confidence
        if validate(script, 'script'):
            self.script = script
        if validate(url, 'url'):
            self.url = url
        if validate(callback_errors, 'callback_errors'):
            self.callback_errors = callback_errors

        super(Event, self).__init__(*args, **kwargs)


class PaymentForward(BusinessDataObject):

    def __init__(self, *args, **kwargs):

        identifier = kwargs.get('id') or kwargs.get('identifier')
        token = kwargs.get('token')
        destination = kwargs.get('destination')
        input_address = kwargs.get('input_address')
        process_fees_address = kwargs.get('process_fees_address')
        process_fees_satoshis = kwargs.get('process_fees_satoshis')
        process_fees_percent = kwargs.get('process_fees_percent')
        callback_url = kwargs.get('callback_url')
        enable_confirmations = kwargs.get('enable_confirmations')
        mining_fees_satoshis = kwargs.get('mining_fees_satoshis')
        txs = kwargs.get('txs')

        if validate(identifier, 'id'):
            self.identifier = identifier
        if validate(token, 'token'):
            self.token = token
        if validate(destination, 'destination'):
            self.destination = destination
        if validate(input_address, 'input_address'):
            self.input_address = input_address
        if validate(process_fees_address, 'process_fees_address'):
            self.process_fees_address = process_fees_address
        if validate(process_fees_satoshis, 'process_fees_satoshis'):
            self.process_fees_satoshis = process_fees_satoshis
        if validate(process_fees_percent, 'process_fees_percent'):
            self.process_fees_percent = process_fees_percent
        if validate(callback_url, 'callback_url'):
            self.callback_url = callback_url
        if validate(enable_confirmations, 'enable_confirmations'):
            self.enable_confirmations = enable_confirmations
        if validate(mining_fees_satoshis, 'mining_fees_satoshis'):
            self.mining_fees_satoshis = mining_fees_satoshis
        if validate(txs, 'txs'):
            self.txs = txs

        super(PaymentForward, self).__init__(*args, **kwargs)


class PaymentForwardCallback(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        value = kwargs.get('value')
        input_address = kwargs.get('input_address')
        destination = kwargs.get('destination')
        input_transaction_hash = kwargs.get('input_transaction_hash')
        transaction_hash = kwargs.get('transaction_hash')

        if validate(value, 'value'):
            self.value = value
        if validate(input_address, 'input_address'):
            self.input_address = input_address
        if validate(destination, 'destination'):
            self.destination = destination
        if validate(input_transaction_hash, 'input_transaction_hash'):
            self.input_transaction_hash = input_transaction_hash
        if validate(transaction_hash, 'transaction_hash'):
            self.transaction_hash = transaction_hash

        super(PaymentForwardCallback, self).__init__(*args, **kwargs)


class BaseTx(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        script = kwargs.get('script')
        addresses = kwargs.get('addresses')
        script_type = kwargs.get('script_type')
        age = kwargs.get('age')
        wallet_name = kwargs.get('wallet_name')
        wallet_token = kwargs.get('wallet_token')

        if validate(script, 'script'):
            self.script = script
        if validate(addresses, 'addresses'):
            self.addresses = addresses
        if validate(script_type, 'script_type'):
            self.script_type = script_type
        if validate(age, 'age'):
            self.age = age
        if validate(wallet_name, 'wallet_name'):
            self.wallet_name = wallet_name
        if validate(wallet_token, 'wallet_token'):
            self.wallet_token = wallet_token

        super(BaseTx, self).__init__(*args, **kwargs)


class TxSkeleton(BusinessDataObject):
    def __init__(self, *args, **kwargs):
        tx = kwargs.get('tx')
        tosign = kwargs.get('tosign')
        signatures = kwargs.get('signatures')
        pubkeys = kwargs.get('pubkeys')
        tosign_tx = kwargs.get('tosign_tx')
        errors = kwargs.get('errors')

        if validate(tx, 'tx'):
            self.tx = tx
        if validate(tosign, 'tosign'):
            self.tosign = tosign
        if validate(signatures, 'signatures'):
            self.signatures = signatures
        if validate(pubkeys, 'pubkeys'):
            self.pubkeys = pubkeys
        if validate(tosign_tx, 'tosign_tx'):
            self.tosign_tx = tosign_tx
        if validate(errors, 'errors'):
            self.errors = errors

        super(TxSkeleton, self).__init__(*args, **kwargs)


class Tx(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        block_height = kwargs.get('block_height')
        hash = kwargs.get('hash')
        addresses = kwargs.get('addresses')
        total = kwargs.get('total')
        fees = kwargs.get('fees')
        size = kwargs.get('size')
        preference = kwargs.get('preference')
        relayed_by = kwargs.get('relayed_by')
        received = kwargs.get('received')
        ver = kwargs.get('ver')
        lock_time = kwargs.get('lock_time')
        double_spend = kwargs.get('double_spend')
        vin_sz = kwargs.get('vin_sz')
        vout_sz = kwargs.get('vout_sz')
        confirmations = kwargs.get('confirmations')
        inputs = kwargs.get('inputs')
        outputs = kwargs.get('outputs')
        opt_in_rbf = kwargs.get('opt_in_rbf')
        confidence = kwargs.get('confidence')
        confirmed = kwargs.get('confirmed')
        receive_count = kwargs.get('receive_count')
        change_address = kwargs.get('change_address')
        block_hash = kwargs.get('block_hash')
        block_index = kwargs.get('block_index')
        double_of = kwargs.get('double_of')
        data_protocol = kwargs.get('data_protocol')
        hex = kwargs.get('hex')
        next_inputs = kwargs.get('next_inputs')
        next_outputs = kwargs.get('next_outputs')

        if validate(block_height, 'block_height'):
            self.block_height = block_height
        if validate(hash, 'hash'):
            self.hash = hash
        if validate(addresses, 'addresses'):
            self.addresses = addresses
        if validate(total, 'total'):
            self.total = total
        if validate(fees, 'fees'):
            self.fees = fees
        if validate(size, 'size'):
            self.size = size
        if validate(preference, 'preference'):
            self.preference = preference
        if validate(relayed_by, 'relayed_by'):
            self.relayed_by = relayed_by
        if validate(received, 'received'):
            self.received = received
        if validate(ver, 'ver'):
            self.ver = ver
        if validate(lock_time, 'lock_time'):
            self.lock_time = lock_time
        if validate(double_spend, 'double_spend'):
            self.double_spend = double_spend
        if validate(vin_sz, 'vin_sz'):
            self.vin_sz = vin_sz
        if validate(vout_sz, 'vout_sz'):
            self.vout_sz = vout_sz
        if validate(confirmations, 'confirmations'):
            self.confirmations = confirmations
        if validate(inputs, 'inputs'):
            self.inputs = inputs
        if validate(outputs, 'outputs'):
            self.outputs = outputs
        if validate(opt_in_rbf, 'opt_in_rbf'):
            self.opt_in_rbf = opt_in_rbf
        if validate(confidence, 'confidence'):
            self.confidence = confidence
        if validate(confirmed, 'confirmed'):
            self.confirmed = confirmed
        if validate(receive_count, 'receive_count'):
            self.receive_count = receive_count
        if validate(change_address, 'change_address'):
            self.change_address = change_address
        if validate(block_hash, 'block_hash'):
            self.block_hash = block_hash
        if validate(block_index, 'block_index'):
            self.block_index = block_index
        if validate(double_of, 'double_of'):
            self.double_of = double_of
        if validate(data_protocol, 'data_protocol'):
            self.data_protocol = data_protocol
        if validate(hex, 'hex'):
            self.hex = hex
        if validate(next_inputs, 'next_inputs'):
            self.next_inputs = next_inputs
        if validate(next_outputs, 'next_outputs'):
            self.next_outputs = next_outputs

        super(Tx, self).__init__(*args, **kwargs)


class TxInput(BaseTx):

    def __init__(self, *args, **kwargs):
        prev_hash = kwargs.get('prev_hash')
        output_index = kwargs.get('output_index')
        output_value = kwargs.get('output_value')
        script_type = kwargs.get('script_type')
        script = kwargs.get('script')
        addresses = kwargs.get('addresses')
        sequence = kwargs.get('sequence')
        age = kwargs.get('age')
        wallet_name = kwargs.get('wallet_name')
        wallet_token = kwargs.get('wallet_token')

        if validate(prev_hash, 'prev_hash'):
            self.prev_hash = prev_hash
        if validate(output_index, 'output_index'):
            self.output_index = output_index
        if validate(output_value, 'output_value'):
            self.output_value = output_value
        if validate(script_type, 'script_type'):
            self.script_type = script_type
        if validate(script, 'script'):
            self.script = script
        if validate(addresses, 'addresses'):
            self.addresses = addresses
        if validate(sequence, 'sequence'):
            self.sequence = sequence
        if validate(age, 'age'):
            self.age = age
        if validate(wallet_name, 'wallet_name'):
            self.wallet_name = wallet_name
        if validate(wallet_token, 'wallet_token'):
            self.wallet_token = wallet_token

        super(TxInput, self).__init__(*args, **kwargs)


class TxOutput(BaseTx):

    def __init__(self, *args, **kwargs):
        value = kwargs.get('value')
        script = kwargs.get('script')
        addresses = kwargs.get('addresses')
        script_type = kwargs.get('script_type')
        spent_by = kwargs.get('spent_by')
        data_hex = kwargs.get('data_hex')
        data_string = kwargs.get('data_string')
        age = kwargs.get('age')
        wallet_name = kwargs.get('wallet_name')
        wallet_token = kwargs.get('wallet_token')

        if validate(value, 'value'):
            self.value = value
        if validate(script, 'script'):
            self.script = script
        if validate(addresses, 'addresses'):
            self.addresses = addresses
        if validate(script_type, 'script_type'):
            self.script_type = script_type
        if validate(spent_by, 'spent_by'):
            self.spent_by = spent_by
        if validate(data_hex, 'data_hex'):
            self.data_hex = data_hex
        if validate(data_string, 'data_string'):
            self.data_string = data_string
        if validate(age, 'age'):
            self.age = age
        if validate(wallet_name, 'wallet_name'):
            self.wallet_name = wallet_name
        if validate(wallet_token, 'wallet_token'):
            self.wallet_token = wallet_token

        super(TxOutput, self).__init__(*args, **kwargs)


class TxConfidence(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        age_millis = kwargs.get('age_millis')
        receive_count = kwargs.get('receive_count')
        confidence = kwargs.get('confidence')
        txhash = kwargs.get('txhash')
        txurl = kwargs.get('txurl')

        if validate(age_millis, 'age_millis'):
            self.age_millis = age_millis
        if validate(receive_count, 'receive_count'):
            self.receive_count = receive_count
        if validate(confidence, 'confidence'):
            self.confidence = confidence
        if validate(txhash, 'txhash'):
            self.txhash = txhash
        if validate(txurl, 'txurl'):
            self.txurl = txurl

        super(TxConfidence, self).__init__(*args, **kwargs)


class TxRef(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        address = kwargs.get('address')
        block_height = kwargs.get('block_height')
        tx_hash = kwargs.get('tx_hash')
        tx_input_n = kwargs.get('tx_input_n')
        tx_output_n = kwargs.get('tx_output_n')
        value = kwargs.get('value')
        preference = kwargs.get('preference')
        spent = kwargs.get('spent')
        double_spend = kwargs.get('double_spend')
        confirmations = kwargs.get('confirmations')
        script = kwargs.get('script')
        ref_balance = kwargs.get('ref_balance')
        confidence = kwargs.get('confidence')
        confirmed = kwargs.get('confirmed')
        spent_by = kwargs.get('spent_by')
        received = kwargs.get('received')
        receive_count = kwargs.get('receive_count')
        double_of = kwargs.get('double_of')

        if validate(address, 'address'):
            self.address = address
        if validate(block_height, 'block_height'):
            self.block_height = block_height
        if validate(tx_hash, 'tx_hash'):
            self.tx_hash = tx_hash
        if validate(tx_input_n, 'tx_input_n'):
            self.tx_input_n = tx_input_n
        if validate(tx_output_n, 'tx_output_n'):
            self.tx_output_n = tx_output_n
        if validate(value, 'value'):
            self.value = value
        if validate(preference, 'preference'):
            self.preference = preference
        if validate(spent, 'spent'):
            self.spent = spent
        if validate(double_spend, 'double_spend'):
            self.double_spend = double_spend
        if validate(confirmations, 'confirmations'):
            self.confirmations = confirmations
        if validate(script, 'script'):
            self.script = script
        if validate(ref_balance, 'ref_balance'):
            self.ref_balance = ref_balance
        if validate(confidence, 'confidence'):
            self.confidence = confidence
        if validate(confirmed, 'confirmed'):
            self.confirmed = confirmed
        if validate(spent_by, 'spent_by'):
            self.spent_by = spent_by
        if validate(received, 'received'):
            self.received = received
        if validate(receive_count, 'receive_count'):
            self.receive_count = receive_count
        if validate(double_of, 'double_of'):
            self.double_of = double_of

        super(TxRef, self).__init__(*args, **kwargs)


class MicroTx(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        from_pubkey = kwargs.get('from_pubkey')
        from_private = kwargs.get('from_private')
        from_wif = kwargs.get('from_wif')
        to_address = kwargs.get('to_address')
        value_satoshis = kwargs.get('value_satoshis')
        token = kwargs.get('token')
        change_address = kwargs.get('change_address')
        wait_guarantee = kwargs.get('wait_guarantee')
        tosign = kwargs.get('tosign')
        signatures = kwargs.get('signatures')
        inputs = kwargs.get('inputs')
        outputs = kwargs.get('outputs')
        fees = kwargs.get('fees')
        hash = kwargs.get('hash')
        spent_by = kwargs.get('spent_by')
        received = kwargs.get('received')
        receive_count = kwargs.get('receive_count')
        double_of = kwargs.get('double_of')

        if validate(from_pubkey, 'from_pubkey'):
            self.from_pubkey = from_pubkey
        if validate(from_private, 'from_private'):
            self.from_private = from_private
        if validate(from_wif, 'from_wif'):
            self.from_wif = from_wif
        if validate(to_address, 'to_address'):
            self.to_address = to_address
        if validate(value_satoshis, 'value_satoshis'):
            self.value_satoshis = value_satoshis
        if validate(token, 'token'):
            self.token = token
        if validate(change_address, 'change_address'):
            self.change_address = change_address
        if validate(wait_guarantee, 'wait_guarantee'):
            self.wait_guarantee = wait_guarantee
        if validate(tosign, 'tosign'):
            self.tosign = tosign
        if validate(signatures, 'signatures'):
            self.signatures = signatures
        if validate(inputs, 'inputs'):
            self.inputs = inputs
        if validate(outputs, 'outputs'):
            self.outputs = outputs
        if validate(fees, 'fees'):
            self.fees = fees
        if validate(hash, 'hash'):
            self.hash = hash
        if validate(spent_by, 'spent_by'):
            self.spent_by = spent_by
        if validate(received, 'received'):
            self.received = received
        if validate(receive_count, 'receive_count'):
            self.receive_count = receive_count
        if validate(double_of, 'double_of'):
            self.double_of = double_of

        super(MicroTx, self).__init__(*args, **kwargs)


class BlockNullData(BusinessDataObject):

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        token = kwargs.get('token')
        encoding = kwargs.get('encoding')
        block_hash = kwargs.get('hash') or kwargs.get('block_hash')

        if validate(data, 'data'):
            self.data = data
        if validate(token, 'token'):
            self.token = token
        if validate(encoding, 'encoding'):
            self.encoding = encoding
        if validate(block_hash, 'hash'):
            self.hash = block_hash

        super(BlockNullData, self).__init__(*args, **kwargs)
