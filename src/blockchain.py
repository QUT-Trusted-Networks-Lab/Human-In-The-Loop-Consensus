#! python3
# blockchain.py
# Provides a blockchain-like structure for the P.O.C application.
# Credit to https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/

import pickle, json, os
from hashlib import sha256

from .message import Request

class Block:
    '''
    A Block provides the basic data structure from which a blockchain
    is formed. It contains a JSON stringified Bundle representation,
    alongside its own hash and the hash of the previous block in the chain.
    '''
    def __init__(self, previous_hash):
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class BundleBlock(Block):
    '''
    A BundleBlock contains a JSON stringified Bundle representation,
    alongside its own hash and the hash of the previous block in the chain.
    '''
    def __init__(self, bundle, previous_hash):
        assert type(bundle).__name__ == "Bundle"
        super().__init__(previous_hash)
        
        self.requestID = bundle.request.id
        self.bundle = bundle.format_bundle_as_json()
        
        self.hash = self.compute_hash()

class RequestBlock(Block):
    '''
    A RequestBlock contains a JSON stringified Request representation,
    alongside its own hash and the hash of the previous block in the chain.
    
    This block is special since its hash is pre-computed before being made
    into a block; as such, the requestID and hash fields are redundant.
    '''
    def __init__(self, request, previous_hash):
        assert type(request).__name__ == "Request"
        super().__init__(previous_hash)
        
        self.requestID = request.id
        self.message = request.message
        self.action = request.action
        self.date = request.date
        
        self.hash = request.id

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
        genesisRequest = Request()
        genesisRequest.create_new("Genesis", "approval")
        
        genesis_block = RequestBlock(genesisRequest, "0")
        self.chain.append(genesis_block)
    
    def add_block(self, block):
        # Prevent incorrect chaining
        previousHash = self.get_last_block().hash
        if previousHash != block.previous_hash: 
            return False
        
        # Prevent duplication (simple)
        thisHash = block.hash
        if self.find_block_by_hash(thisHash) != False:
            return False
        
        # Prevent duplication (complex)
        '''
        This check is necessary since every time the controller creates
        a Bundle it will technically have a new hash. We want to prevent
        repeat Bundles being added to the blockchain, so we need to handle
        this especially.
        '''
        if type(block).__name__ == "BundleBlock":
            thisRequestID = block.requestID
            if self.find_bundleblock_by_requestID(thisRequestID) != False:
                return False
        
        # Write to blockchain if all checks pass
        self.chain.append(block)
        return True
        
    def get_last_block(self):
        return self.chain[-1]
    
    def find_block_by_hash(self, hash):
        '''
        Slowly crawls through the blockchain like a linked list to find
        a block with the provided hash.
        '''
        for b in self.chain:
            if b.hash == hash:
                return b
        return False
    
    def find_bundleblock_by_requestID(self, requestID):
        '''
        Slowly crawls through the blockchain like a linked list to find
        a BundleBlock with the provided requestID.
        '''
        
        for b in self.chain:
            if b.requestID == requestID and type(b).__name__ == "BundleBlock":
                return b
        return False

class LocalBlockchain(Blockchain):
    '''
    A version of a Blockchain instance which allows the chain to be loaded
    from a local Pickle file, and to save the chain to a local Pickle file.
    '''
    def __init__(self, localChainPickle=None):
        Blockchain.__init__(self)
        
        # Find our where to load the local chain from (if applicable)
        if localChainPickle == None: # if != None, we already know where to load it from
            localChainPickle = os.path.join(os.getcwd(), "local_chain.pkl")
        
        # Load the local chain if it actually exists
        if os.path.isfile(localChainPickle):
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
