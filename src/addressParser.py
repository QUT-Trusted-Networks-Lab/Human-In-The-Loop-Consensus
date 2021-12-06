#! python3
# address_parser.py
# Encapsulates logic for parsing header strings for email addresses

import re
import email.utils
emailRegex = re.compile(r"[\w\.]+@[\w\.]+\.\w+")

class AddressParser:
    '''
    A Block provides the basic data structure from which a blockchain
    is formed. It contains a JSON stringified Bundle representation,
    alongside its own hash and the hash of the previous block in the chain.
    '''
    def __init__(self, header):
        _headerParse = email.utils.getaddresses(header.split(" "))
        
        self.recipients = []
        self._parse_addresses(_headerParse)
    
    def _parse_addresses(self, recurseHeaderParse):
        for value in recurseHeaderParse:
            if type(value).__name__ == "tuple" or type(value).__name__ == "list":
                self._parse_addresses(value)
                continue
            e = emailRegex.findall(value)
            if e != []:
                self.recipients += e
            
