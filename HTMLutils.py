from bs4 import BeautifulSoup
from FaiText import Tokenizer, defaults
from types import SimpleNamespace

TK_QUOB,TK_QUOE,TK_HLB,TK_HLE = 'xxquob','xxquoe','xxhlb','xxhle'
TK_DEL,TK_BLD,TK_ITL, TK_RED,TK_BLU,TK_GRN = 'xxdel','xxbld','xxitl', 'xxred','xxblu','xxgrn'
CSPEC_CASE = [TK_QUOB,TK_QUOE,TK_HLB,TK_HLE, TK_DEL,TK_BLD,TK_ITL, TK_RED,TK_BLU,TK_GRN]

def to_soup(htext):
    return htext if isinstance(htext, BeautifulSoup) else BeautifulSoup(htext,'html.parser')

def tokwrap(sent, insertion):
    insertion = ' '+insertion.strip()+' ' # normalize spacing around tokens
    return insertion + sent.replace(' ', insertion)+' '

def _insert_outer(ele, head_tok, tail_tok):
    """Prepend `head_tok` and append `tail_tok` to a soup element in place"""
    ele.insert(0,f' {head_tok} ')
    ele.extend(f' {tail_tok} ')
    ele.unwrap()

def findall_replace(text, token_map=None, **kwargs):
    """Insert custom tokens before each word in a tag span

    Args:
        token_map: dict, mapping of {TOK:'tag'} or {TOK:['tag1','tag2',..]}
            (default: {TK_DEL: 'del', TK_BLD: ['b', 'strong'], TK_ITL: ['i', 'em']} )
    """
    token_map = token_map if token_map is not None else {TK_DEL: 'del', TK_BLD: ['b', 'strong'], TK_ITL: ['i', 'em']}
    soup = to_soup(text)
    for tok,tags in token_map.items():
        for t in soup.find_all(tags):
            t.replace_with(tokwrap(t.get_text(), tok))
    return soup

def process_spantags(text, max_tok_ins=5, **kwargs):
    """Replace span tags with corresponding color/highlight tokens

    Args:
        max_tok_ins: int, maximum number of specific color tokens
                     before defaulting to generic highlight token
    """
    soup = to_soup(text)
    for t in soup.find_all('span'):
        if len(t.get_text().split()) > max_tok_ins or not t.has_attr('class'):
            _insert_outer(t,TK_HLB,TK_HLE)
        else:
            colattr = t['class'][0]
            if colattr == 'r':   t.replace_with(tokwrap(t.get_text(), TK_RED))
            elif colattr == 'b': t.replace_with(tokwrap(t.get_text(), TK_BLU))
            elif colattr == 'g': t.replace_with(tokwrap(t.get_text(), TK_GRN))
    return soup

def destroy_tags(text, rm_tags=None, **kwargs):
    """Completely remove elements from DOM, including tags and inner items
    
    Args:
        rmtags: list(str), tag elements to remove (default: ['ul','a','img','li'])
    
    """
    rm_tags = rm_tags if rm_tags is not None else ['ul','a','img','li']
    soup = to_soup(text)
    for t in soup.find_all(rm_tags):
        t.decompose() # destroy these elements
    return soup

def wrap_quotes(text, **kwargs):
    # add quoted text tags
    soup = to_soup(text)
    for t in soup.find_all('div',{'class':'q'}):
        _insert_outer(t,TK_QUOB,TK_QUOE)
    return soup

def br2newline(text, **kwargs):
    """Replace `<br/>` with `\n` """
    soup = to_soup(text)
    for t in soup.find_all('br'):
        t.replace_with('\n')
    return soup

def unwrap_tags(text, untag=None, **kwargs):
    """Remove elements' tags, but preserve inner items
    
    Args:
        untag: list(str), element tags to unwrap (default: ['h2'])
    """
    untag = untag if untag is not None else ['h2']
    soup = to_soup(text)
    for ut in untag:
        for t in soup.select(ut):
            t.unwrap()  # extract text from h2
    return soup


_funcdict = {'findall_replace': findall_replace,
             'process_spantags': process_spantags,
             'destroy_tags': destroy_tags,
             'wrap_quotes': wrap_quotes,
             'br2newline': br2newline,
             'unwrap_tags': unwrap_tags
             }
available_functions = list(_funcdict.keys())


class HTMLTokenizer(Tokenizer):
    """**kwargs are passed to Tokenizer"""

    def __init__(self, markup='', parser='html.parser', **kwargs):
        self.soup = BeautifulSoup(markup, parser)
        super().__init__(**kwargs)
    
    def partial_process(self, *args, **kwargs):
        for func in args:
            func = _funcdict[func] if isinstance(func, str) else func
            func(self.soup, **kwargs)
        return self.soup
        
    def full_process_html(self):
        unwrap_tags(self.soup, untag=['h2'])
        br2newline(self.soup)
        destroy_tags(self.soup, rm_tags=['ul', 'a', 'img', 'li'])
        findall_replace(self.soup, token_map={TK_DEL: 'del', TK_BLD: ['b', 'strong'], TK_ITL: ['i', 'em']})
        process_spantags(self.soup, max_tok_ins=5)
        wrap_quotes(self.soup)
        # remove the misc content and starting div
        unwrap_tags(self.soup, untag=['div.cb', 'div.pTx'])

        return str(self.soup)

    @classmethod
    def tokenize(cls, x):
        return cls(x).full_process_html()

# ht.partial_process(br2newline, destroy_tags, findall_replace, unwrap_tags, token_map={TK_DEL: 'del'}, untag=['h2','div.cb','div.pTx'])