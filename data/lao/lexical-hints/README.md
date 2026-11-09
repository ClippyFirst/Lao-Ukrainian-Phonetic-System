# Lao orthographic lexical hints

`Lao-Dictionary.txt` is copied from [LaoNLP](https://github.com/wannaphong/LaoNLP/blob/master/laonlp/corpus/Lao-Dictionary.txt), upstream blob SHA-1 `ca5346a1971a7712ac3c50988140c376859174e3`.

The original BSD-style notice and attribution are retained verbatim in the file header. Its authors state that it was created for word wrapping and that compounds have mostly been reduced to their parts. It is not a gold-standard lexical word segmentation corpus, a complete dictionary, or a pronunciation/IPA resource.

The optional `lao_ukrainian.lexical_hints` diagnostic reports every multi-syllable spelling match, including overlapping alternatives. It does not select boundaries, change `segment_syllables`, feed IPA, or run in the production analysis pipeline. Treat each match as `SOFT_HINT_ONLY`. The MIT-derived list contains 34,937 NFC-normalized unique strings consisting only of Lao-block code points; entries with whitespace or mixed scripts are excluded because the current matcher concatenates syllable units without spaces.

The raw LaoNLP `lao-eng-dictionary.csv` is not included. Its schema and separate MIT notice have been inspected; a filtered derivative containing only unique Lao orthographic `LaoWord` values is retained in `LaoNLP-MIT-LaoWord.txt` with the full MIT notice embedded. The optional matcher can consume this file as `SOFT_HINT_ONLY`; it is not production data, IPA, or lexical-boundary gold.
