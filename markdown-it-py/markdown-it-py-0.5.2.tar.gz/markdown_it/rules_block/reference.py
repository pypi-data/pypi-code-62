import logging

from ..common.utils import isSpace, normalizeReference, charCodeAt
from ..common.normalize_url import normalizeLink, validateLink
from ..utils import AttrDict
from .state_block import StateBlock


LOGGER = logging.getLogger(__name__)


def reference(state: StateBlock, startLine, _endLine, silent):

    LOGGER.debug(
        "entering reference: %s, %s, %s, %s", state, startLine, _endLine, silent
    )

    lines = 0
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]
    nextLine = startLine + 1

    # if it's indented more than 3 spaces, it should be a code block
    if state.sCount[startLine] - state.blkIndent >= 4:
        return False

    if state.srcCharCode[pos] != 0x5B:  # /* [ */
        return False

    # Simple check to quickly interrupt scan on [link](url) at the start of line.
    # Can be useful on practice: https:#github.com/markdown-it/markdown-it/issues/54
    while pos < maximum:
        # /* ] */  /* \ */  /* : */
        if state.srcCharCode[pos] == 0x5D and state.srcCharCode[pos - 1] != 0x5C:
            if pos + 1 == maximum:
                return False
            if state.srcCharCode[pos + 1] != 0x3A:
                return False
            break
        pos += 1

    endLine = state.lineMax

    # jump line-by-line until empty one or EOF
    terminatorRules = state.md.block.ruler.getRules("reference")

    oldParentType = state.parentType
    state.parentType = "reference"

    while nextLine < endLine and not state.isEmpty(nextLine):
        # this would be a code block normally, but after paragraph
        # it's considered a lazy continuation regardless of what's there
        if state.sCount[nextLine] - state.blkIndent > 3:
            nextLine += 1
            continue

        # quirk for blockquotes, this line should already be checked by that rule
        if state.sCount[nextLine] < 0:
            nextLine += 1
            continue

        # Some tags can terminate paragraph without empty line.
        terminate = False
        for terminatorRule in terminatorRules:
            if terminatorRule(state, nextLine, endLine, True):
                terminate = True
                break

        if terminate:
            break

        nextLine += 1

    string = state.getLines(startLine, nextLine, state.blkIndent, False).strip()
    maximum = len(string)

    pos = 1
    while pos < maximum:
        ch = charCodeAt(string, pos)
        if ch == 0x5B:  # /* [ */
            return False
        elif ch == 0x5D:  # /* ] */
            labelEnd = pos
            break
        elif ch == 0x0A:  # /* \n */
            lines += 1
        elif ch == 0x5C:  # /* \ */
            pos += 1
            if pos < maximum and charCodeAt(string, pos) == 0x0A:
                lines += 1
        pos += 1

    if labelEnd < 0 or charCodeAt(string, labelEnd + 1) != 0x3A:  # /* : */
        return False

    # [label]:   destination   'title'
    #         ^^^ skip optional whitespace here
    pos = labelEnd + 2
    while pos < maximum:
        ch = charCodeAt(string, pos)
        if ch == 0x0A:
            lines += 1
        elif isSpace(ch):
            pass
        else:
            break
        pos += 1

    # [label]:   destination   'title'
    #            ^^^^^^^^^^^ parse this
    res = state.md.helpers.parseLinkDestination(string, pos, maximum)
    if not res.ok:
        return False

    href = normalizeLink(res.str)
    if not validateLink(href):
        return False

    pos = res.pos
    lines += res.lines

    # save cursor state, we could require to rollback later
    destEndPos = pos
    destEndLineNo = lines

    # [label]:   destination   'title'
    #                       ^^^ skipping those spaces
    start = pos
    while pos < maximum:
        ch = charCodeAt(string, pos)
        if ch == 0x0A:
            lines += 1
        elif isSpace(ch):
            pass
        else:
            break
        pos += 1

    # [label]:   destination   'title'
    #                          ^^^^^^^ parse this
    res = state.md.helpers.parseLinkTitle(string, pos, maximum)
    if pos < maximum and start != pos and res.ok:
        title = res.str
        pos = res.pos
        lines += res.lines
    else:
        title = ""
        pos = destEndPos
        lines = destEndLineNo

    # skip trailing spaces until the rest of the line
    while pos < maximum:
        ch = charCodeAt(string, pos)
        if not isSpace(ch):
            break
        pos += 1

    if pos < maximum and charCodeAt(string, pos) != 0x0A:
        if title:
            # garbage at the end of the line after title,
            # but it could still be a valid reference if we roll back
            title = ""
            pos = destEndPos
            lines = destEndLineNo
            while pos < maximum:
                ch = charCodeAt(string, pos)
                if not isSpace(ch):
                    break
                pos += 1

    if pos < maximum and charCodeAt(string, pos) != 0x0A:
        # garbage at the end of the line
        return False

    label = normalizeReference(string[1:labelEnd])
    if not label:
        # CommonMark 0.20 disallows empty labels
        return False

    # Reference can not terminate anything. This check is for safety only.
    if silent:
        return True

    if "references" not in state.env:
        state.env["references"] = {}

    state.line = startLine + lines + 1

    if label not in state.env["references"]:
        state.env["references"][label] = AttrDict(
            {"title": title, "href": href, "map": [startLine, state.line]}
        )
    else:
        state.env.setdefault("duplicate_refs", []).append(
            AttrDict(
                {
                    "title": title,
                    "href": href,
                    "label": label,
                    "map": [startLine, state.line],
                }
            )
        )

    state.parentType = oldParentType

    return True
