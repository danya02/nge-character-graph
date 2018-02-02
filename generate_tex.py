#!/ust/bin/python3
import json

# Opening file to write data to.
output = open('nge.tex', 'w')


# Defining a convenience function to write data to file.
def outp(*val, **param):
    print(*val, **param, file=output)


# Loading data JSON.
with open('nge.json') as i:
    data = json.load(i)

# TeX file start: preamble stuff
outp("\\documentclass[preview]{standalone}")
outp("% Auto-generated code, data version: {}".format(data['version']))
outp("\\usepackage[utf8]{inputenc}", "\\usepackage[OT1]{fontenc}")
outp("\\usepackage{amsmath}", "\\usepackage{amsfonts}", "\\usepackage{amssymb}", "\\usepackage{fix-cm}")
outp("\\usepackage{anyfontsize}", "\\usepackage{ccicons}", "\\usepackage{tikz}", "\\makeatletter")
outp("\\newcommand\\VBIG{\\@setfontsize\\Huge{100}{120}}", "\\newcommand\\EBIG{\\@setfontsize\\Huge{200}{240}}")
outp("\\newcommand\\BIG{\\@setfontsize\\Huge{50}{60}}", "\\newcommand\\CBig{\\@setfontsize\\Huge{25}{30}}")
outp("\\newcommand\\fontlabel{\\@setfontsize\\Huge{20}{30}}", "\\makeatother", "\\usetikzlibrary{decorations.text}")
outp("\\begin{document}", "\\begin{tikzpicture}")

# STEP 1: Header stuff

outp(
    "\\node[draw,align=center] at (0,25) {\\BIG{Relationships in} \\\\ \\VBIG{Neon Genesis Evangelion} \\\\ \\BIG{presuming major fan theories are true}};")

outp("\\node[draw,align=center] at (20,26) {\\ccbysa \\\\ This graph is distributable\\\\ under the CC-BY-SA};")
outp(
    "\\node[draw,align=center] at (20,24) {Images taken from the \\\\ Neon Genesis Evangelion wikia:\\\\ evangelion.wikia.com/};")
outp("\\node[draw,align=center] at (-20,20) {\\CBig{Legend:}};")
outp(
    "\\node[draw=green,very thick, label={\\fontlabel{Evangelion pilot}}, shape=circle,inner sep=0.5cm] (EEP) at (-16,18) {};")
outp(
    "\\node[draw=yellow,very thick, label={\\fontlabel{Evangelion unit}}, shape=circle,inner sep=0.5cm] (EEVA) at (-10,18) {};")
outp("\\node[draw=gray,very thick, label={\\fontlabel{Angel}}, shape=circle,inner sep=0.5cm] (EA) at (-4,18) {};")
outp(
    "\\node[draw=red,very thick, label={\\fontlabel{NERV employee}}, shape=circle,inner sep=0.5cm] (ENERV) at (-16,14) {};")
outp(
    "\\node[draw=black,very thick, label={\\fontlabel{Miscellaneous}}, shape=circle,inner sep=0.5cm] (EMISC) at (-10,14) {};")
outp(
    "\\path[<->] (EEP) edge[bend right=20, draw=red,very thick] node[midway, above=-2cm, sloped] {Romantic relationship} (ENERV);")
outp("\\path[->] (EEP) edge[bend right=20,draw=blue,very thick] node[midway, above, sloped] {Subordination} (EEVA);")
outp("\\path[->] (EEVA) edge[bend left=20,draw=black,very thick] node[midway, above, sloped] {Destruction} (EA);")
outp("\\path[<-] (EMISC) edge[draw=green,very thick] node[midway, above, sloped] {Creation} (EA);")
outp("\\path[<->] (EMISC) edge[draw=gray,very thick] node[midway, above, sloped] {Miscellaneous} (ENERV);")
outp("\\node[draw,align=center] at (-20,25) {\EBIG{", data['tex_version'], "}};")

# STEP 2: Nodes
nodes = {}
styles_node = {'pilot': '{draw=green,very thick}', 'evangelion': '{draw=yellow,very thick}',
               'nerv': '{draw=red,very thick}', 'angel': '{draw=gray,very thick}',
               'miscellaneous': '{draw=black,very thick}'}
for i in data['nodes_data']:
    style = styles_node[i['class']]
    outp("\\node[" + ("fill={},".format(i.get('tex_fill')) if i.get('tex_fill') else "") +
         "style=" + style + ", label={\\fontlabel{" + i.get(
        'tex_name', i[
            'name']) + "}}, shape=circle,inner sep=1cm, path picture={\\node at (path picture bounding box.center){\includegraphics[width=" +
         i['tex_width'] + "]{" + i['image'] + "}};};] (" + i['node_name'] + ") at", i['tex_pos'],
         "{};")
    nodes.update({i['name']: i['node_name']})

# STEP 3: Links
styles_link = {'romantic': '{draw=red,very thick}', 'created': '{draw=green,very thick}',
               'subordination': '{draw=blue,very thick}', 'destruction': '{draw=black,very thick}',
               'miscellaneous': '{draw=gray,very thick}'}

for i in data['links_data']:
    style = styles_link[i['type']]
    if i.get('bidirectional', 0) != -1:
        if i.get('text'):
            outp("\\path[" + ("<->" if i.get('bidirectional', 0) == 1 else "->") + "] (" + nodes[
                i['source']] + ") edge[style={}".format(style) + ((',bend {}'.format(i.get('tex_bend'))) if i.get(
                'tex_bend') else '') + "] node[midway, above, sloped] {" + i['text'] + "} (" + nodes[
                     i['target']] + ");")
        else:
            outp("\\path[" + ("<->" if i.get('bidirectional', 0) == 1 else "->") + "] (" + nodes[
                i['source']] + ") edge[style={}".format(style) + ((',bend {}'.format(i.get('tex_bend'))) if i.get(
                'tex_bend') else '') + "] node {} (" + nodes[i['target']] + ");")
# TeX file end: closing tags.
outp("\end{tikzpicture}", "\end{document}")

# Closing output file
output.close()
