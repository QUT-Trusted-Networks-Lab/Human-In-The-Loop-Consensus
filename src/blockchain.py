#! python3
# blockchain.py
# Provides a blockchain-like structure for the P.O.C application.
# Credit to https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/

import pickle, json, os
from hashlib import sha256

from .message import Bundle

genesisEmail = '''
# ---------- START BLOCKCHAIN BUNDLE ---------- #
# REQUEST ID: genesis
# REQUEST CONTENTS: genesis
# ACTION REQUESTED: approval
# RECIPIENTS: genesis@genesis.com
# RESPONSES: I genesis
# VERDICT: ACCEPTED
# ---------- END BLOCKCHAIN BUNDLE ---------- #
'''

class Block:
    '''
    A Block provides the basic data structure from which a blockchain
    is formed. It contains a JSON stringified Bundle representation,
    alongside its own hash and the hash of the previous block in the chain.
    '''
    def __init__(self, bundle, previous_hash):
        assert type(bundle).__name__ == "Bundle"
        
        self.requestID = bundle.request.id
        self.bundle = bundle.format_bundle_as_json()
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    '''
    A Blockchain provides a data structure to store Block instances.
    This Blockchain is specifically designed to store Blocks which
    represent Bundles for use in the blockchain consensus P.O.C.
    '''
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
 
    def create_genesis_block(self):
        fake_bundle = Bundle()
        fake_bundle.parse_from_email(genesisEmail)
        
        genesis_block = Block(fake_bundle, "0")
        self.chain.append(genesis_block)
    
    def add_block(self, block):
        previous_hash = self.get_last_block().hash
        previous_requestID = self.get_last_block().requestID
        if previous_hash != block.previous_hash: # Prevent incorrect chaining
            return False
        if block.requestID == previous_requestID: # Prevent duplicate addition
            return False
        self.chain.append(block)
        return True
        
    def get_last_block(self):
        return self.chain[-1]

class LocalBlockchain(Blockchain):
    '''
    A version of a Blockchain instance which allows the chain to be loaded
    from a local Pickle file, and to save the chain to a local Pickle file.
    '''
    def __init__(self, localChainPickle=None):
        Blockchain.__init__(self)
        
        # Load the local chain if applicable
        if localChainPickle != None and os.path.isfile(localChainPickle):
            localChain = pickle.load(open(localChainPickle, "rb"))
            self.chain = localChain
        
        # Store the location of where the pickle should be saved
        self.localChainPickle = localChainPickle
    
    def save(self):
        '''
        Saves the chain to a local Pickle file.
        Returns True if successful, otherwise False.
        '''
        try:
            pickle.dump(self.chain, open(self.localChainPickle, "wb"))
            return True
        except:
            return False
