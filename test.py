#!/usr/bin/env python

import subprocess
import sys
from datetime import datetime
from fpdf import FPDF
from pathlib import Path

# retrieve arguments
script, test_data = sys.argv[1:]

# create pdf object
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=10)
# add fonts to pdf
pdf.add_font("Ubuntu", "", "test/fonts/Ubuntu-Regular.ttf")
pdf.add_font("Ubuntu", "B", "test/fonts/Ubuntu-Bold.ttf")
pdf.add_font("Ubuntu", "I", "test/fonts/Ubuntu-Italic.ttf")
pdf.add_font("Ubuntu", "BI", "test/fonts/Ubuntu-BoldItalic.ttf")
pdf.add_font("Mono", "", "test/fonts/RobotoMono-Regular.ttf")
# add first page
pdf.add_page()

# set variables
action_flag = "PDF"
output = ""
markdown = True
input_file = "test/test_input.txt"
output_file = "test/test_output.txt"

# parse test_data.txt
with open(test_data) as file:
    for line in file:
        line = line.strip()

        if action_flag == "PDF":
            match line:
                case "PDF":
                    continue
                case "HEAD":
                    # Header with line
                    pdf.set_font(family="Ubuntu", style="B", size=36)
                    pdf.set_text_color(150, 150, 150)
                    line_height = 24
                    pdf.cell(
                        w=190,
                        h=line_height,
                        text="TEST REPORT",
                        align="R",
                        border=0,
                        new_x="LEFT",
                        new_y="NEXT",
                        markdown=False,
                    )
                    pdf.set_line_width(0.75)
                    pdf.set_draw_color(200, 200, 200)
                    pdf.line(10, 28, 200, 28)
                case "H1":
                    # main title
                    pdf.set_font(family="Ubuntu", style="B", size=24)
                    pdf.set_text_color(50, 50, 50)
                    line_height = 16
                case "H2":
                    # subtitle
                    pdf.set_font(family="Ubuntu", style="B", size=16)
                    pdf.set_text_color(50, 50, 50)
                    line_height = 12
                case "P":
                    # paragraph
                    pdf.set_font(family="Ubuntu", size=12)
                    pdf.set_text_color(0, 0, 0)
                    line_height = 6
                    markdown = True
                case "DATE":
                    # insert date and time of running, ideally after "P"
                    date_line = f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    pdf.multi_cell(
                        w=190,
                        h=line_height,
                        text=date_line,
                        align="L",
                        border=0,
                        new_x="LEFT",
                        markdown=True,
                    )
                case "CLI":
                    # CLI formatting
                    pdf.set_font(family="Mono", size=12)
                    pdf.set_text_color(25, 25, 25)
                    line_height = 6
                    markdown = False
                case "INPUT":
                    # switch action flag and clear input file
                    action_flag = "INPUT"
                    open(input_file, "w").close()
                    markdown = False
                case "CMD":
                    # switch action flag
                    action_flag = "CMD"
                case "OUTPUT":
                    # write cli output of command. "CLI" should precede
                    # must always be after CMD line, so the stdout and stderr are used  from current command
                    if stderr:
                        pdf.multi_cell(
                            w=190,
                            h=line_height,
                            text=stderr,
                            align="L",
                            border=0,
                            new_x="LEFT",
                            markdown=markdown,
                        )
                    if stdout:
                        pdf.multi_cell(
                            w=190,
                            h=line_height,
                            text=stdout,
                            align="L",
                            border=0,
                            new_x="LEFT",
                            markdown=markdown,
                        )
                case "FILE":
                    # write content of output file
                    with open(output_file, "r") as out_file:
                        content = out_file.readlines()
                    pdf.set_font(family="Mono", size=12)
                    pdf.set_text_color(25, 25, 25)
                    line_height = 6
                    for output_line in content:
                        pdf.multi_cell(
                            w=190,
                            h=line_height,
                            text=output_line.strip(),
                            align="L",
                            border=0,
                            new_x="LEFT",
                        )
                case "END":
                    # Confirm end of report
                    pdf.set_font(family="Ubuntu", style="B", size=10)
                    pdf.set_text_color(150, 150, 150)
                    line_height = 6
                    pdf.set_line_width(0.25)
                    pdf.cell(
                        w=190,
                        h=line_height,
                        text="END OF TEST REPORT",
                        align="R",
                        border="T",
                        new_x="LEFT",
                        new_y="NEXT",
                        markdown=False,
                    )
                case _:
                    # write line to pdf
                    line = line.replace(">>script<<", script)
                    pdf.multi_cell(
                        w=190,
                        h=line_height,
                        text=line,
                        align="L",
                        border=0,
                        new_x="LEFT",
                        markdown=markdown,
                    )
        elif action_flag == "CMD":
            match line:
                case "CMD":
                    continue
                case "PDF":
                    # switch action flag
                    action_flag = "PDF"
                case _:
                    # run command and store ist output
                    line = line.replace(">>script<<", script)
                    cmd = line.split()
                    proc = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    stdout = proc.stdout.read().decode()
                    stderr = proc.stderr.read().decode()
        elif action_flag == "INPUT":
            match line:
                case "PDF":
                    action_flag = "PDF"
                case _:
                    # write input tu input_file and also to pdf
                    pdf.set_font(family="Mono", size=12)
                    pdf.set_text_color(25, 25, 25)
                    line_height = 6
                    pdf.multi_cell(
                        w=190,
                        h=line_height,
                        text=line,
                        align="L",
                        border=0,
                        new_x="LEFT",
                    )
                    line = line + "\n"
                    with open(input_file, "a") as in_file:
                        in_file.write(line)
# save pdf output
script_stem = Path(script).stem
output_filepath = f"test/{script_stem}_test_report.pdf"
pdf.output(output_filepath)
