from string import Template

invalid_wallet = 'Invalid wallet identifier provided'

invalid_address = 'Invalid address or identifier provided'

invalid_coin = 'Invalid coin or cryptocurrency provided'

invalid_wallet_balance = 'Wallet balance has reached its limit or is invalid'

invalid_identifier = Template('Invalid identifier provided for given parameter: $param')

invalid_parameter = 'Invalid parameter provided'

invalid_enterprise = Template('Invalid enterprise provided. Expected enterprise but got $enterprise')

invalid_amount = Template('Invalid amount provided. Amount should be numeric or integer in the base unit of currency, '
                          'example satoshi for Bitcoin. Expected integer but got $amount')
operation_not_supported = 'The selected operation is currently not supported.'

required_parameter = 'A required parameter is not provided or invalid value is provided'

cipher_error = 'Given key could not decrypt message'

