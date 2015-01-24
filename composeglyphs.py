#!/usr/bin/env python

import os
import sys
import math
import getopt
import shutil
import svg_stack


statics = ['cross.svg', 'blank.svg']
templates = [
    'template-{0}_{1}-01.svg'.format((i/5)%3 +1, (i%5)+1) for i in range(15)
]
sequences = []


def compose_glyph(name, docs, template_path, glyph_path):
    doc = svg_stack.Document()
    layout = svg_stack.HBoxLayout()
    for d in docs:
        layout.addSVG(os.path.join(template_path, d))
    doc.setLayout(layout)
    doc.save('{0}.svg'.format(os.path.join(glyph_path, name)))


def main(argv):
    help_str = 'composeglyphs.py -i <template dir> -o <glyph dir>'
    template_dir = ''
    glyph_dir = ''

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", 
            ["help", "templates=", "glyphs="]
        )
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_str)
            sys.exit()
        elif opt in ("-i", "--templates"):
            template_dir = arg
        elif opt in ("-o", "--glyphs"):
            glyph_dir = arg

    if not glyph_dir or not template_dir:
        print('Template directory and glyph directory are required args:')
        print(help_str)
        sys.exit(2)

    for i, t in enumerate(templates):
        l = [templates[n*5+4] for n in range(int(math.floor(i/5)))]
        l.append(t)
        sequences.append(l)
    print('Generating glyphs from {0}*.svg'.format(template_dir))

    for i, docs in enumerate(sequences):
        compose_glyph(str(i +1), docs, template_dir, glyph_dir)

    print('Copying static vectors')
    for v in statics:
        shutil.copy2(os.path.join(template_dir, v), glyph_dir)

    print('Done!')


if __name__ == "__main__":
    main(sys.argv[1:])
