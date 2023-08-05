import json
from CompoTree import Radicals
from itertools import chain
from pathlib import Path
from .UtilsGeneral import PAT_CH_CHR


class CharacterTagger:

    def __init__(self, all_words, radicals=None) -> None:
        self.radicals = radicals
        if radicals is None: self.radicals = Radicals.load()
        self.rad_sem = self._load_data()
        self.chr2tag = {}
        self.tag2chr = {}
        for ch in chain.from_iterable(all_words):
            if not PAT_CH_CHR.match(ch): continue
            if ch in self.chr2tag: continue
            r = self.radicals.query(ch)[0]
            tags = self.rad_sem.get(r, ["NULL"])
            self.chr2tag[ch] = tags
            for t in tags:
                self.tag2chr.setdefault(t, set()).add(ch) 

    def tag(self, ch):
        return self.chr2tag[ch]
    
    def get_chars(self, tag):
        return self.tag2chr[tag]

    def _load_data(self):
        fp = Path(__file__).parent / "../data/radical_semantic_tag.json"
        with open(fp, encoding='utf-8') as f:
            return json.load(f)


class NgramTagger:
    pass
