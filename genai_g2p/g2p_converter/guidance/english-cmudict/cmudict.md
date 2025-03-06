The CMU Pronouncing Dictionary

## [![](http://www.speech.cs.cmu.edu/images/Sphinx-plate.png)](http://www.speech.cs.cmu.edu/tools/) The CMU Pronouncing Dictionary

[query](#lookup) | [phonemes |](#phones) [about](#about) | | [Speech at CMU](http://www.speech.cs.cmu.edu/) | [Speech Tools](http://www.speech.cs.cmu.edu/tools/)

 * * *

### ![](http://www.speech.cs.cmu.edu/images/gifs/blueball.gif) Look up the pronunciation for a word or phrase in CMUdict (version 0.7b)

Did you spot an error? Please contact the maintainers! We will check it out. (See at bottom for contact information.)

* * *

### ![](http://www.speech.cs.cmu.edu/images/gifs/blueball.gif) Download the current CMU dictionary from SourceForge and GitHub

+   [http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict](http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/)
+   [https://github.com/Alexir/CMUdict/blob/master/cmudict-0.7b](https://github.com/Alexir/CMUdict/blob/master/cmudict-0.7b).
+   and try: [this tool](http://www.speech.cs.cmu.edu/tools/lextool.html)

**Note:** If you are looking for a dictionary for use with a speech recognizer, this dictionary is not the one that you are looking for.  
For that purpose, see

+   [http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/sphinxdict](http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/sphinxdict/)

 * * *

### ![](http://www.speech.cs.cmu.edu/images/gifs/yellowball.gif) About the CMU dictionary

The **[Carnegie Mellon University](http://www.cmu.edu/) Pronouncing Dictionary** is an open-source machine-readable pronunciation dictionary for North American English that contains over **134,000 words** and their pronunciations. CMUdict is being actively maintained and expanded. We are open to suggestions, corrections and other input.

Its entries are **particularly useful for speech recognition and synthesis**, as it has mappings from words to their pronunciations in the ARPAbet phoneme set, a standard for English pronunciation. The current phoneme set contains 39 phonemes, vowels carry a lexical stress marker:

0    — No stress  
1    — Primary stress  
2    — Secondary stress  

Bear in mind that this is a dictionary. **If your word is not in the dictionary** (or was misspelled) nothing will be returned. This also applies to items such as numbers; you should spell out what you need. This [tool](http://www.speech.cs.cmu.edu/tools/lextool.html) will try to come up with pronunciations for words not in the dictionary. Please feel free to send word suggestions or point to errors inpronunciation. Bear in mind the language changes over time, in particular novel words may not be in the dictionary; you can make suggestions for ones that seem to be here gor a while.

 * * *

### ![](http://www.speech.cs.cmu.edu/images/gifs/yellowball.gif) Phoneme Set

The current phoneme set has 39 phonemes, not counting varia due to lexical stress. This phoneme (or more accurately, phone) set is based on the ARPAbet symbol set developed for speech recognition uses. You can find a [description of the ARPAbet on Wikipedia](http://en.wikipedia.org/wiki/Arpabet), as well information on how it relates to the standard IPA symbol set. If you check off the stress box you will get a pronunciation in which vowels are annotated (see above). Stress is difficult to get right and people disagree about it. There are words in the language that differentiate by stress (e.g. PR'OGRESS PROGR'ESS).

```
        Phoneme Example Translation
        ------- ------- -----------
        AA	odd     AA D
        AE	at	AE T
        AH	hut	HH AH T
        AO	ought	AO T
        AW	cow	K AW
        AY	hide	HH AY D
        B 	be	B IY
        CH	cheese	CH IY Z
        D 	dee	D IY
        DH	thee	DH IY
        EH	Ed	EH D
        ER	hurt	HH ER T
        EY	ate	EY T
        F 	fee	F IY
        G 	green	G R IY N
        HH	he	HH IY
        IH	it	IH T
        IY	eat	IY T
        JH	gee	JH IY
        K 	key	K IY
        L 	lee	L IY
        M 	me	M IY
        N 	knee	N IY
        NG	ping	P IH NG
        OW	oat	OW T
        OY	toy	T OY
        P 	pee	P IY
        R 	read	R IY D
        S 	sea	S IY
        SH	she	SH IY
        T 	tea	T IY
        TH	theta	TH EY T AH
        UH	hood	HH UH D
        UW	two	T UW
        V 	vee	V IY
        W 	we	W IY
        Y 	yield	Y IY L D
        Z 	zee	Z IY
        ZH	seizure	S IY ZH ER
```

* * *

*This cgi was created by [kevin lenzo](http://www.linkedin.com/in/kevinlenzo), and the source code is freely available.  
For correspondence about this interface, including options you'd like to see, please email   air -at ´cs‘cmu→ εdυ*