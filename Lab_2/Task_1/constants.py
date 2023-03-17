rxForSentences = r"((([a-x0-9\)][\.])|(\.\.\.)|(([\?!]+)))['\"\)]?" \
                 r"[\s+\n][A-X0-9'\"\(])|(((\.)|((\?)|(!)))[\"'\)]?\s*$)"
rxForNameAbbreviations = r'(\b([Mm]r|[Mm]rs|[Dd]r|[Ll]t|[Rr]ep)\.)'
rxForNonDeclarative = r'(((([\?!]+)))[\'\"\)]?[\s+\n][A-X0-9\'\"\(])|([\?!][\"\'\)]?\s*$)'
rxForWords = r'\b[\w]+\b'
rxForNumbers = r'\b[0-9]+\b'
