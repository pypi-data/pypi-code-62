"""Process definition lists."""
from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock


def deflist_plugin(md: MarkdownIt):
    isSpace = md.utils.isSpace

    def skipMarker(state: StateBlock, line: int):
        """Search `[:~][\n ]`, returns next pos after marker on success or -1 on fail."""
        start = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        if start >= maximum:
            return -1

        # Check bullet
        marker = state.srcCharCode[start]
        start += 1
        if marker != 0x7E and marker != 0x3A:  # ~ :
            return -1

        pos = state.skipSpaces(start)

        # require space after ":"
        if start == pos:
            return -1

        # no empty definitions, e.g. "  : "
        if pos >= maximum:
            return -1

        return start

    def markTightParagraphs(state: StateBlock, idx: int):

        level = state.level + 2

        i = idx + 2
        l2 = len(state.tokens) - 2
        while i < l2:
            if (
                state.tokens[i].level == level
                and state.tokens[i].type == "paragraph_open"
            ):
                state.tokens[i + 2].hidden = True
                state.tokens[i].hidden = True
                i += 2
            i += 1

    def deflist(state: StateBlock, startLine: int, endLine: int, silent: bool):

        if silent:
            # quirk: validation mode validates a dd block only, not a whole deflist
            if state.ddIndent < 0:
                return False
            return skipMarker(state, startLine) >= 0

        nextLine = startLine + 1
        if nextLine >= endLine:
            return False

        if state.isEmpty(nextLine):
            nextLine += 1
            if nextLine >= endLine:
                return False

        if state.sCount[nextLine] < state.blkIndent:
            return False
        contentStart = skipMarker(state, nextLine)
        if contentStart < 0:
            return False

        # Start list
        listTokIdx = len(state.tokens)
        tight = True

        token = state.push("dl_open", "dl", 1)
        token.map = listLines = [startLine, 0]

        # Iterate list items
        dtLine = startLine
        ddLine = nextLine

        # One definition list can contain multiple DTs,
        # and one DT can be followed by multiple DDs.
        #
        # Thus, there is two loops here, and label is
        # needed to break out of the second one
        #
        break_outer = False

        while True:
            prevEmptyEnd = False

            token = state.push("dt_open", "dt", 1)
            token.map = [dtLine, dtLine]

            token = state.push("inline", "", 0)
            token.map = [dtLine, dtLine]
            token.content = state.getLines(
                dtLine, dtLine + 1, state.blkIndent, False
            ).strip()
            token.children = []

            token = state.push("dt_close", "dt", -1)

            while True:
                token = state.push("dd_open", "dd", 1)
                token.map = itemLines = [nextLine, 0]

                pos = contentStart
                maximum = state.eMarks[ddLine]
                offset = (
                    state.sCount[ddLine]
                    + contentStart
                    - (state.bMarks[ddLine] + state.tShift[ddLine])
                )

                while pos < maximum:
                    ch = state.srcCharCode[pos]

                    if isSpace(ch):
                        if ch == 0x09:
                            offset += 4 - offset % 4
                        else:
                            offset += 1
                    else:
                        break

                    pos += 1

                contentStart = pos

                oldTight = state.tight
                oldDDIndent = state.ddIndent
                oldIndent = state.blkIndent
                oldTShift = state.tShift[ddLine]
                oldSCount = state.sCount[ddLine]
                oldParentType = state.parentType
                state.blkIndent = state.ddIndent = state.sCount[ddLine] + 2
                state.tShift[ddLine] = contentStart - state.bMarks[ddLine]
                state.sCount[ddLine] = offset
                state.tight = True
                state.parentType = "deflist"

                state.md.block.tokenize(state, ddLine, endLine, True)

                # If any of list item is tight, mark list as tight
                if not state.tight or prevEmptyEnd:
                    tight = False

                # Item become loose if finish with empty line,
                # but we should filter last element, because it means list finish
                prevEmptyEnd = (state.line - ddLine) > 1 and state.isEmpty(
                    state.line - 1
                )

                state.tShift[ddLine] = oldTShift
                state.sCount[ddLine] = oldSCount
                state.tight = oldTight
                state.parentType = oldParentType
                state.blkIndent = oldIndent
                state.ddIndent = oldDDIndent

                token = state.push("dd_close", "dd", -1)

                itemLines[1] = nextLine = state.line

                if nextLine >= endLine:
                    break_outer = True
                    break

                if state.sCount[nextLine] < state.blkIndent:
                    break_outer = True
                    break

                contentStart = skipMarker(state, nextLine)
                if contentStart < 0:
                    break

                ddLine = nextLine

                # go to the next loop iteration:
                # insert DD tag and repeat checking

            if break_outer:
                break_outer = False
                break

            if nextLine >= endLine:
                break
            dtLine = nextLine

            if state.isEmpty(dtLine):
                break
            if state.sCount[dtLine] < state.blkIndent:
                break

            ddLine = dtLine + 1
            if ddLine >= endLine:
                break
            if state.isEmpty(ddLine):
                ddLine += 1
            if ddLine >= endLine:
                break

            if state.sCount[ddLine] < state.blkIndent:
                break
            contentStart = skipMarker(state, ddLine)
            if contentStart < 0:
                break

            # go to the next loop iteration:
            # insert DT and DD tags and repeat checking

        # Finalise list
        token = state.push("dl_close", "dl", -1)

        listLines[1] = nextLine

        state.line = nextLine

        # mark paragraphs tight if needed
        if tight:
            markTightParagraphs(state, listTokIdx)

        return True

    md.block.ruler.before(
        "paragraph", "deflist", deflist, {"alt": ["paragraph", "reference"]}
    )
