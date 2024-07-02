from collections import defaultdict, deque
from enum import Enum
from typing import List

# Side length of the board (NxN) that we can place letters on
N = 5

class State(Enum):
    # Tupe of (name, population), where name is without capitalization and whitespace
    CA = ("california", 39_538_223)
    TX = ("texas", 29_145_505)
    FL = ("florida", 21_538_187)
    NY = ("newyork", 20_201_249)
    PA = ("pennsylvania", 13_002_700)
    IL = ("illinois", 12_812_508)
    OH = ("ohio", 11_799_448)
    GA = ("georgia", 10_711_908)
    NC = ("northcarolina", 10_439_388)
    MI = ("michigan", 10_077_331)
    NJ = ("newjersey", 9_288_994)
    VI = ("virginia", 8_631_393)
    WA = ("washington", 7_705_281)
    AZ = ("arizona", 7_151_502)
    MA = ("massachusetts", 7_029_917)
    TN = ("tennessee", 6_910_840)
    IN = ("indiana", 6_785_528)
    MD = ("maryland", 6_177_224)
    MO = ("missouri", 6_154_913)
    WI = ("wisconsin", 5_893_718)
    CO = ("colorado", 5_773_714)
    MN = ("minnesota", 5_706_494)
    SC = ("southcarolina", 5_118_425)
    AL = ("alabama", 5_024_279)
    LA = ("louisiana", 4_657_757)
    KY = ("kentucky", 4_505_836)
    OR = ("oregon", 4_237_256)
    OK = ("oklahoma", 3_959_353)
    CT = ("connecticut", 3_605_944)
    UT = ("utah", 3_271_616)
    IA = ("iowa", 3_190_369)
    NV = ("nevada", 3_104_614)
    AR = ("arkansas", 3_011_524)
    MS = ("mississippi", 2_961_279)
    KS = ("kansas", 2_937_880)
    NM = ("newmexico", 2_117_522)
    NE = ("nebraska", 1_961_504)
    ID = ("idaho", 1_839_106)
    WV = ("westvirginia", 1_793_716)
    HI = ("hawaii", 1_455_271)
    NH = ("newhampshire", 1_377_529)
    ME = ("maine", 1_362_359)
    RI = ("rhodeisland", 1_097_379)
    MT = ("montana", 1_084_225)
    DE = ("delaware", 989_948)
    SD = ("southdakota", 886_667)
    ND = ("northdakota", 779_094)
    VT = ("vermont", 643_077)
    WY = ("wyoming", 576_851)

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.isWord = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node: TrieNode = self.root
        for c in word:
            node = node.children[c]
        node.isWord = True

    @staticmethod
    def buildTrie(words: List[str]):
        t = Trie()
        for w in words:
            t.insert(w)
        return t

def buildBoard(input: str) -> List[List[str]]:
    assert(len(input) == N*N)
    return [[input[N*i + j] for j in range(N)] for i in range(N)]

def generateStateNameVariations(state: State) -> List[str]:
    name = state.value[0]
    return [name[:i]+chr(c)+name[i+1:] for c in range(ord('a'), ord('z')+1) for i in range(len(name))]

def searchDfsIterative(board: List[List[str]], root: TrieNode, startRow: int, startCol: int) -> tuple[bool, int]:
    s = [(root, startRow, startCol)] # stack for DFS
    maxLen: int = 0
    while s:
        maxLen = max(maxLen, len(s))
        (node, r, c) = s.pop()
        if node.isWord:
            return (True, maxLen)
        if r < 0 or r >= len(board) or c < 0 or c >= len(board[r]):
            continue
        child = node.children.get(board[r][c])
        if not child:
            continue
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (x != 0 or y != 0):
                    s.append((child, r+x, c+y))
    return (False, maxLen)

def searchBfsIterative(board: List[List[str]], root: TrieNode, startRow: int, startCol: int) -> tuple[bool, int]:
    q = deque([(root, startRow, startCol)]) # queue for BFS
    maxLen: int = 0
    while q:
        maxLen = max(maxLen, len(q))
        (node, r, c) = q.popleft()
        if node.isWord:
            return (True, maxLen)
        if r < 0 or r >= len(board) or c < 0 or c >= len(board[r]):
            continue
        child = node.children.get(board[r][c])
        if not child:
            continue
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (x != 0 or y != 0):
                    q.append((child, r+x, c+y))
    return (False, maxLen)

def search(board: List[List[str]], state: State, root: TrieNode) -> bool:
    foundState: bool = False
    maxLen: int = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            (result, maxLenInSearch) = searchDfsIterative(board, root, i, j)
            # (result, maxLenInSearch) = searchBfsIterative(board, root, i, j)
            foundState |= result
            maxLen = max(maxLen, maxLenInSearch)
            if foundState:
                break
    # print("Max search states in memory: ", maxLen, ", state: ", state.value[0])
    return foundState

def canFormState(board: List[List[str]], state: State) -> bool:
    variations: List[str] = generateStateNameVariations(state)
    trie = Trie.buildTrie(variations)
    return search(board, state, trie.root)

def computeScore(input: str) -> int:
    board: List[List[str]] = buildBoard(input)
    return sum([state.value[1] if canFormState(board, state) else 0 for state in State])
