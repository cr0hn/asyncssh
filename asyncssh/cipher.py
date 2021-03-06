# Copyright (c) 2013-2014 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

"""Symmetric key encryption handlers"""

"""A shim for accessing symmetric ciphers needed by asyncssh"""

_ciphers = {}

def register_cipher(cipher_name, mode_name, cipher):
    """Register a symmetric cipher

       If multiple modules try to register the same cipher and mode, the
       first one to register it is used.

    """

    if (cipher_name, mode_name) not in _ciphers:
        cipher.cipher_name = cipher_name
        cipher.mode_name = mode_name
        _ciphers[(cipher_name, mode_name)] = cipher

def lookup_cipher(cipher_name, mode_name):
    """Look up a symmetric cipher"""

    return _ciphers.get((cipher_name, mode_name))


_enc_algs = []
_enc_params = {}
_enc_ciphers = {}

def register_encryption_alg(alg, cipher_name, mode_name, key_size,
                            initial_bytes):
    """Register an encryption algorithm"""

    cipher = lookup_cipher(cipher_name, mode_name)
    if cipher:
        _enc_algs.append(alg)
        _enc_params[alg] = (key_size, cipher.iv_size,
                            cipher.block_size, mode_name == 'gcm')
        _enc_ciphers[alg] = (cipher, initial_bytes)

def get_encryption_algs():
    """Return a list of available encryption algorithms"""

    return _enc_algs

def get_encryption_params(alg):
    """Get parameters of an encryption algorithm

       This function returns the key, iv, and block sizes of an encryption
       algorithm.

    """

    return _enc_params[alg]

def get_cipher(alg, key, iv=None):
    """Return an instance of a cipher

       This function returns a cipher object initialized with the specified
       key and iv that can be used for data encryption and decryption.

    """

    cipher, initial_bytes = _enc_ciphers[alg]
    return cipher.new(key, iv, initial_bytes)

register_encryption_alg(b'aes256-ctr',             'aes',      'ctr', 32, 0)
register_encryption_alg(b'aes192-ctr',             'aes',      'ctr', 24, 0)
register_encryption_alg(b'aes128-ctr',             'aes',      'ctr', 16, 0)
register_encryption_alg(b'aes256-gcm@openssh.com', 'aes',      'gcm', 32, 0)
register_encryption_alg(b'aes128-gcm@openssh.com', 'aes',      'gcm', 16, 0)
register_encryption_alg(b'aes256-cbc',             'aes',      'cbc', 32, 0)
register_encryption_alg(b'aes192-cbc',             'aes',      'cbc', 24, 0)
register_encryption_alg(b'aes128-cbc',             'aes',      'cbc', 16, 0)
register_encryption_alg(b'3des-cbc',               'des3',     'cbc', 24, 0)
register_encryption_alg(b'blowfish-cbc',           'blowfish', 'cbc', 16, 0)
register_encryption_alg(b'cast128-cbc',            'cast',     'cbc', 16, 0)
register_encryption_alg(b'arcfour256',             'arc4',     None,  32, 1536)
register_encryption_alg(b'arcfour128',             'arc4',     None,  16, 1536)
register_encryption_alg(b'arcfour',                'arc4',     None,  16, 0)
