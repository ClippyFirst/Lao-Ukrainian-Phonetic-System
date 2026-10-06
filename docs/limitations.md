# Limitations and unresolved questions

1. **Unspaced multi-syllable text.** The current public parser accepts explicit syllable/phrase chunks and ZWSP boundaries. Full automatic syllable segmentation is not yet a validated lexical parser.
2. **Initial clusters.** Lao permits restricted initial clusters and high-class consonant sequences. These require a dedicated cluster model rather than treating every second consonant as a coda.
3. **ໜ/ໝ.** Unicode defines these as sequences corresponding to [h]+[n]/[m] with special tonal implications. The repository currently preserves them structurally but does not claim a complete independent tonal grammar for every such form.
4. **Pali/Sanskrit.** Extended letters and virama are registered separately but are not part of the modern-Lao core output model.
5. **Tone contours.** The five-tone Vientiane system is well supported, but exact contour notation varies among descriptions.
6. **Ukrainian target.** The target correspondences are project decisions. They are not presented as an adopted Ukrainian national standard.
7. **Lexical exceptions and conventional names.** A regular phonological algorithm cannot by itself establish every conventional geographical or personal-name spelling.
8. **Empirical accuracy.** No gold-standard adjudicated corpus is currently available, so no accuracy percentage is claimed.
