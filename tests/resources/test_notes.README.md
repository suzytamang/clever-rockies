# Test Resources

## Test Notes

### [Test Note Descriptions (source)](./test_notes/test_note_descriptions.docx)

Excerpt from source .docx file.  *Table built via https://www.tablesgenerator.com/markdown_tables*

| **Test #** | **Target Class** | **Term** | **Expected** | **Description** |
|:---:|:---:|:---:|:---:|---|
| 1 | LONELINESS | loneliness | POS | Term enclosed by commas |
| 2 | LONELINESS | loneliness | POS | Term immediately followed by / |
| 3 | LONELINESS | loneliness | POS | Term immediately preceded by / |
| 4 | LONELINESS | loneliness | POS | Term immediately preceded by - |
| 5 | ADL | difficulty eating | NOT APP | Text preceding the term contains HX modifier ‘history’. |
| 6 | ADL | difficulty eating | NEG | Term at EOL and NEGEX modifier ‘denies’ on next line but same sentence. |
| 7 | ADL | feeds him | NOT APP | Term preceded by FAM modifier ‘wife’ |
| 8 | ADL | feeds him | NEG | Term followed by NEGEX modifier ‘not’ on next line but same sentence. |
| 9 | ADL | feeds him | NOT APP | Term preceded by FAM modifier ‘wife’ on line before but same sentence. |
| 10 | ADL | help with feeding | NEG | Term preceded by NEGEX modifier ‘cannot’ and FAM modifier ‘wife’ before that. NEGEX takes precedence over FAM. |
| 11 | ADL | buttering bread | NEG | Term preceded by NEGEX modifier ‘not’ at end of previous line and FAM modifier ‘wife’ before that. |
| 12 | ADL | put on clothes | No snippet | Term followed by assessment term ‘more than half the days’. |
| 13 | CAPACITY | using meth | POS | Term immediately followed by a . (period) |
| 14 | CAPACITY | meth | No snippet | Term is partial match of ‘methods’. |
| 15 | CAPACITY | meth | No snippet | Term is partial match of ‘dimeth’. |
| 16 | CAPACITY | meth | No snippet | Term is partial match of ‘dimethylamine’. |
| 17 | CAPACITY | meth | No snippet | Term is partial match of  ‘methane’ immediately followed by a . (period) |
| 18 | DETOX | ciwa protocol | POS | Term wraps across EOL. |
| 19 | IDU | ssp | No snippet | Term is partial match of ‘ SSP2’. |
| 20 | DETOX | detox | No snippet | Term is partial match of ‘detoxing’ at BOL. |
| 21 | HOPELESS | desire to change | POS | Term immediately followed by \) |
| 22 | HOPELESS | desire to continue | NEG | NEGEX modifier ‘no’ followed by EOL before term on the next line. |
| 23 | MST | rape | No snippet | Term is partial match of ‘rapel’. |
| 24 | MST | rape | No snippet | Term is partial match of ‘rapelling’. |
| 25 | LONELINESS | loneliness | NOT APP | Term is preceded by RISK modifier ‘risk’ but with another term (‘homelessness’) and a PUNCT (comma) between them. PUNCT should be ignored. |
| 26 | PPAIN | constant pain | No snippet | Snippet contains assessment term ‘no. if yes’ |
| 27 | PPAIN | constant pain | No snippet | Snippet contains assessment term ‘no, if yes’ |
| 28 | COVID | body aches | No snippet | Snippet contains &gt; 2  left square brackets and should be considered an assessment. |
| 29 | COVID | body aches | POS | Snippet contains &lt;= 2  left square brackets and should not be considered an assessment. |
| 30 | PPAIN | constant pain | No snippet | Term is followed by boiler plate phrase ‘Scoring Pain: 1-3 Mild pain 4-6 Moderate pain &gt; 6 Severe pain’ |
| 31 | PPAIN | emotional crisis | No snippet | Term is followed by boiler plate phrase “call the Veteran's Crisis Line at 1-800-273-8255”. |
| 32 | PPAIN | emotional crisis | No snippet | Snippet contains boiler plate phrase ‘emotional crisis line’. |
| 33 | DODOUD | #PERCDATA_OUD# Pt on DOD OUD report assessed and does not meet criteria for opioid use disorder #PERCDATA_OUD# | POS | Snippet contains phrase and marker that indicate a former DoD patient was assessed for OUD and found not meeting criteria. |

[Test Notes with Metadata (one line)](./test_notes/test_notes_with_metadata_one_line.txt)

Pipe-delimited notes
TODO for DMW - Update definitions below
&lt;tiu_sid&gt;|&lt;patient_sid&gt;|&lt;sta3n&gt;|YYYY-MM-DD HH:MM:SS|&lt;note_title&gt;|1600978870383|42|F|I|&lt;test text&gt;

[Test Notes with Metadata](./test_notes/test_notes_with_metadata.csv)

Human-readable collection of notes