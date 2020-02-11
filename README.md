# minichain

A really small and simple python implementation to teach and learn about blockchain.

- blockchain.py: Contains the Blockchain class
- web.py: Web API (Flask)
- cmd_block_new: Creates a new block
- cmd_block_get: Obtains a block by the index
- cmd_chain_get: Obtains the whole chain

## API Endpoints

|----------------------------------------------------|
| Method    Path           Function                  |
|------    -------------  ---------------------------|
| GET       /              Show status               |
| GET       /chain         Returns the whole chain   |
| POST      /block         Creates a new block       |
| GET       /block/last    Returns the last block    |
| GET       /block/<int>   Returns a block by index  |
| GET       /validate      Validates the whole chain |
|----------------------------------------------------|






