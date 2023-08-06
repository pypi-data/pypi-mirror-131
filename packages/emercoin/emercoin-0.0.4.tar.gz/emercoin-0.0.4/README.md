# Emercoin.py

Emercoin python 3 API

## Quick start
Start emercoin wallet and connect to it:
```python
from emercoin import Emer

emer = Emer('rpcuser', 'rpcpassword', 'host', 'port')

# Get current block count in local chain
emer.get_block_count()

# name_filter NVS records
emer.name_filter(r'^dns:[\d]+\.(emc)')  # show all dns records containing numbers in zone 'emc'
                                        # for example: 64327.emc

# name_show NVS record
# since name_filter return truncated record content we can fetch it manually
emer.name_show('dns:cofob.ru')

# if we want get all NVS records by type (name_filter(^type:)) and fetch full record body automagicaly (name_show) we use
emer.get_names_by_type('dns')

# if we simply want get all NVS records by regex and fetch full record body
emer.get_names_by_regex(r'^dns:[\d]+\.(emc)')

# we can get NVS record history too
emer.name_history('dns:cofob.ru')

# or call rpc connection directly (bitcoinrpc used)
emer.rpc_connection.method_name(argument1, argument2)
```
