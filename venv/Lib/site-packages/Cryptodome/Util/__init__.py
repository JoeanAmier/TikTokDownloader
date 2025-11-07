# -*- coding: utf-8 -*-
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

"""Miscellaneous modules

Contains useful modules that don't belong into any of the
other Cryptodome.* subpackages.

========================    =============================================
Module                      Description
========================    =============================================
`Cryptodome.Util.number`        Number-theoretic functions (primality testing, etc.)
`Cryptodome.Util.Counter`       Fast counter functions for CTR cipher modes.
`Cryptodome.Util.RFC1751`       Converts between 128-bit keys and human-readable
                            strings of words.
`Cryptodome.Util.asn1`          Minimal support for ASN.1 DER encoding
`Cryptodome.Util.Padding`       Set of functions for adding and removing padding.
========================    =============================================

:undocumented: _galois, _number_new, cpuid, py3compat, _raw_api
"""

__all__ = ['RFC1751', 'number', 'strxor', 'asn1', 'Counter', 'Padding']

