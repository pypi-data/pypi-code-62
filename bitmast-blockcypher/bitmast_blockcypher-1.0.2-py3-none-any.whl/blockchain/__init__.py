from typing import Any, Mapping
from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.keys import Key, HDKey
from blockcypher import get_transaction_details, generate_new_address

from bitmast_blockcypher.util import extract_data


class BlockKey(Key):

    def __init__(self,  import_key=None, network=None, compressed=True, passphrase='', is_private=None):

        if network in ('bitcoin-test', 'test-bitcoint', 'bitcoin_test', 'test_bitcoin', 'btc-testnet'):
            network = 'testnet'
            super(BlockKey, self).__init__(import_key=import_key, network=network, compressed=compressed,
                                           passphrase=passphrase, is_private=is_private)
        elif network == 'bcy':
            from bitmast_blockcypher.config import user_config
            api_key = user_config.get_by_value('token', 'block_cypher')
            key = generate_new_address(network, api_key=api_key)
            self.private_hex = key.get('private')
            self.public_hex = key.get('public')
            self._address_obj = key.get('address')
            self._wif = key.get('wif')

        super(BlockKey, self).__init__(import_key=import_key, network=network, compressed=compressed,
                                       passphrase=passphrase, is_private=is_private)

    def __len__(self):
        if self.is_private:
            return len(str(self.private_hex))
        else:
            return len(str(self.public_hex))

    def __getitem__(self, item):
        key = None
        if self.is_private:
            key = str(self.private_hex)
        else:
            key = str(self.public_hex)
        return key.__getitem__(item)


class BlockHDKey(HDKey):

    def __len__(self):
        if self.is_private:
            return len(str(self.private_hex))
        else:
            return len(str(self.public_hex))

    def __getitem__(self, item):
        key = None
        if self.is_private:
            key = str(self.private_hex)
        else:
            key = str(self.public_hex)
        return key.__getitem__(item)


class BlockTransaction(Transaction):
    """Provide a wrapper for transactions that can be initiated from data from Blockcypher"""

    @classmethod
    def input_transaction(cls, tx_raw: str = None, tx_hash: str = None, tx: Mapping = None, network: str = None,
                          coin_symbol: str = None, api_key: str = None):

        def _prepare_tranx(tranx: Mapping):
            input_list = None
            output_list = []
            # create transaction with fields: inputs, outputs, locktime, version, network,
            inputs = extract_data('inputs', tranx)
            outputs = extract_data('outputs', tranx)

            for inp in inputs:
                input_list = TxInput.import_input(inp)
            for out in outputs:
                output_list = TxOutput.import_output(out)

            return cls(inputs=input_list, outputs=output_list)

        transaction = None
        if tx_raw:
            transaction = cls.import_raw(tx_raw, network)
        elif tx_hash:
            # look up transaction by id
            tranx = get_transaction_details(tx_hash, coin_symbol=coin_symbol, api_key=api_key)
            transaction = _prepare_tranx(tranx)
        elif isinstance(tx, Mapping):
            transaction = _prepare_tranx(tx)
        return transaction


class TxInput(Input):
    """Provide an input object that can be initiated from data from Blockcypher"""

    @classmethod
    def import_input(cls, tx_input: Any = None, network: str = None):
        # get Transaction input attributes
        input_list = []
        prev_hash = extract_data('prev_has', tx_input)
        output_n = extract_data('output_index', tx_input)
        sequence = extract_data('sequence', tx_input)
        addresses = extract_data('addresses', tx_input)
        for address in addresses:
            input_list.append(cls(prev_hash=prev_hash, output_n=output_n, sequence=sequence,
                                  address=address, network=network))
        return input_list


class TxOutput(Output):
    """Provide an output object that can be initiated from data from Blockcypher"""

    @classmethod
    def import_output(cls, tx_output: Any = None, network: str = None):
        output_list = []
        value = extract_data('value', tx_output)
        addresses = extract_data('addresses', tx_output)
        script = extract_data('script', tx_output)
        for address in addresses:
            output_list.append(cls(value=value, address=address, network=network, lock_script=script))
        return output_list
