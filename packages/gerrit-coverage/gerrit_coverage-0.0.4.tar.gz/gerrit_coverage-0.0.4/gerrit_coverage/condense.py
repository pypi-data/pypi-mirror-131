from collections import defaultdict
import itertools

def _group(l):
    return [(t[0][1], t[-1][1]) for t in (tuple(g[1]) for g in itertools.groupby(enumerate(l), lambda item: item[0] - item[1]))]

def condense(lines):
    """
    Given: List of lines: [('filename', 1), ('filename', 2), ...]
    Result: List of line-ranges, if they have no gap, for example 
            [('filename', [1,2])]
    """
    res = []

    # 1. Group by file
    files = defaultdict(list)
    for filename, line in lines:
        files[filename].append(line)

    for filename, file_lines in sorted(files.items(), key=lambda elem: elem[0]):
        file_lines.sort()
        grouped = _group(file_lines)
        for group in grouped:
            res.append((filename, group))
    
    return res