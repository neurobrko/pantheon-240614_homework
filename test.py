#!/usr/bin/env python

import os
import sys
from fpdf import FPDF

script, test_data = sys.argv[1:]

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)

pdf.add_font(
    "Ubuntu",
    "",
    "test/fonts/Ubuntu-Regular.ttf",
    True,
)
pdf.add_font(
    "Ubuntu",
    "B",
    "test/fonts/Ubuntu-Bold.ttf",
    True,
)
pdf.add_font(
    "Mono",
    "",
    "test/fonts/CutiveMono-Regular.ttf",
    True,
)

pdf.add_page()
action_flag = "PDF"
output = "sample output"

with open(test_data) as file:
    for line in file:
        line = line.strip()

        if action_flag == "PDF":
            match line:
                case "PDF":
                    continue
                case "H1":
                    pdf.set_font(family="Ubuntu", style="B", size=24)
                    pdf.set_text_color(50, 50, 50)
                    line_height = 16
                case "H2":
                    pdf.set_font(family="Ubuntu", style="B", size=16)
                    pdf.set_text_color(50, 50, 50)
                    line_height = 12
                case "P":
                    pdf.set_font(family="Ubuntu", size=12)
                    pdf.set_text_color(0, 0, 0)
                    line_height = 6
                case "CLI":
                    pdf.set_font(family="Mono", size=12)
                    pdf.set_text_color(25, 25, 25)
                    line_height = 6
                case "OUTPUT":
                    pdf.multi_cell(w=0, h=line_height, txt=output, align="L", border=0)
                case "CMD":
                    action_flag = "CMD"
                case _:
                    pdf.multi_cell(w=0, h=line_height, txt=line, align="L", border=0)
        if action_flag == "CMD":
            match line:
                case "CMD":
                    continue
                case "PDF":
                    action_flag = "PDF"
                case _:
                    continue

pdf.output("test/ugen_test_report.pdf")
# output = os.popen("python3 ugen.py -o test/test_output.txt test/test_input.txt").read()
# print(output)
