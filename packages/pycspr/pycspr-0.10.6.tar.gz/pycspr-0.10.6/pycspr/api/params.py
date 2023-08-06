import typing

from pycspr import serialisation
from pycspr import types
from pycspr.types.cl_values import CL_Key


def get_account_balance_params(
    purse_uref: typing.Union[str, types.CL_URef],
    state_root_hash: types.StateRootIdentifier = None
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at a point in chain time.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(purse_uref, types.CL_URef):
        purse_uref = purse_uref.to_string()
    if isinstance(state_root_hash, bytes):
        state_root_hash = state_root_hash.hex()

    return {
        "purse_uref": purse_uref,
        "state_root_hash": state_root_hash
    }


def get_account_info_params(
    account_key: types.AccountIdentifier,
    block_id: types.BlockIdentifier = None
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param account_key: Account public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(account_key, bytes):
        account_key = account_key.hex()
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return {
            "public_key": account_key
        }
    elif isinstance(block_id, str):
        return {
            "public_key": account_key,
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "public_key": account_key,
            "block_identifier": {
                "Height": block_id
            }
        }


def get_auction_info_params(block_id: types.BlockIdentifier = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def get_block_params(block_id: types.BlockIdentifier = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, bytes):
        return {
            "block_identifier": {
                "Hash": block_id.hex()
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }
    else:
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }


def get_block_transfers_params(block_id: types.BlockIdentifier = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, bytes):
        return {
            "block_identifier": {
                "Hash": block_id.hex()
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }
    else:
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }


def get_deploy_params(deploy_id: types.DeployIdentifier) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a deploy.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(deploy_id, bytes):
        deploy_id = deploy_id.hex()

    return {
        "deploy_hash": deploy_id
    }


def get_dictionary_item_params(identifier: types.DictionaryIdentifier) -> dict:
    """Returns JSON-RPC API request parameters.

    :param identifier: Identifier of a state dictionary.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(identifier, types.DictionaryIdentifier_AccountNamedKey):
        return {
            "AccountNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }
        }

    elif isinstance(identifier, types.DictionaryIdentifier_ContractNamedKey):
        return {
            "ContractNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }
        }

    elif isinstance(identifier, types.DictionaryIdentifier_SeedURef):
        return {
            "URef": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "seed_uref": identifier.dictionary_name
            }
        }

    elif isinstance(identifier, types.DictionaryIdentifier_UniqueKey):
        return {
            "Dictionary": identifier.seed_uref.as_string()
        }

    else:
        raise ValueError("Unrecognized dictionary item type.")


def get_era_info_params(block_id: types.BlockIdentifier = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def get_query_global_state_params(
    state_id: types.GlobalStateIdentifier,
    key: CL_Key,
    path: typing.List[str]
) -> dict:
    """Returns results of a query to global state at a specified block or state root hash.

    :param state_id: Identifier of global state leaf.
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :returns: Results of a global state query.

    """
    if state_id.typeof == types.GlobalStateIdentifierType.BLOCK:
        state_id_type = "BlockHash" 
    else:
        state_id_type = "StateRootHash" 
    state_id = state_id.identifier.hex() if isinstance(state_id.identifier, bytes) else state_id.identifier

    return {
        "state_identifier": {
            state_id_type: state_id
        },
        "key": key.to_string(),
        "path": path
    }


def get_state_item_params(
    item_key: str,
    item_path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: bytes = None,
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param item_key: A global state item key.
    :param item_path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "key": item_key,
        "path": item_path if isinstance(item_path, list) else [item_path],
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }


def get_state_root_hash_params(block_id: types.BlockIdentifier = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def put_deploy_params(deploy: types.Deploy) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "deploy": serialisation.deploy_to_json(deploy)
    }
