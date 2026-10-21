# Unicode and orthographic model

The Lao block U+0E80–U+0EFF contains modern Lao letters, vowel signs, tone marks, punctuation/digits and Pali/Sanskrit-related material. The project keeps these namespaces separate.

Important signs include ຳ U+0EB3 Sara Am, ່ U+0EC8 Mai Ek, ້ U+0EC9 Mai Tho, ໊ U+0ECA Mai Ti, ໋ U+0ECB Mai Catawa, ໍ U+0ECD Niggahita, ຺ U+0EBA Pali Virama, and ໜ/ໝ U+0EDC/U+0EDD.

Unicode order is preserved for auditing but is not treated as phonological constituent order.


## Input validation behavior

Both Python and browser validation accept CR, LF and tab as whitespace while rejecting other C0 control characters. The browser regression suite also confirms that U+200B ZERO WIDTH SPACE is rejected rather than silently stripped; Python's validator has the corresponding unsupported-code-point check. NFC normalization is applied, but the engines do not silently delete unsupported characters or reorder phonological material.

These checks cover representative controls only. A full Unicode conformance matrix for malformed combining-mark order, all format controls, ZWSP, mixed scripts, and Python/browser analysis parity remains open.
