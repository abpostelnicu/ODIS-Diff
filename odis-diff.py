#!/usr/bin/python

import os
import sys
import json


HTML_FILE = """
<HTML>
{head}
<BODY>
{body_content}
</BODY>
</HTML>
"""

MODULE_NAME = """<h1 style="color: #2e6c80;">{module_name}:</h1>"""
CODING = """<h2 style="color: #2e6c80;">{name}:</h2>"""

HEAD = """
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
"""

TABLE = """
<table>
  <tr>
    <th>Coding Binary/Text</th>
    <th>Original</th>
    <th>Other</th>
  </tr>
  <tr>
  {content}
  </tr>
</table>
"""

ROW = """
<tr>
    <td>{name}</td>
    <td>{left_val}</td>
    <td>{right_val}</td>
  </tr>
"""


def loadJson(path):
    data = None
    with open(path) as json_file:
        data = json.load(json_file)

    return data


def diffCoding(base_coding, other_coding):
    base_coding = {
        element["display_name"]: element
        for element in sorted(base_coding, key=lambda element: element.get("display_name"))
    }
    other_coding = {
        element["display_name"]: element
        for element in sorted(other_coding, key=lambda element: element.get("display_name"))
    }

    html_elements = ""

    def buildHtmlLine(diff_name, diff_value_left, diff_value_right):
        return ROW.format(
            name=diff_name,
            left_val=diff_value_left if not None else "",
            right_val=diff_value_right if not None else "",
        )

    for key, element in base_coding.items():
        other_element = other_coding.get(key, None)
        # "bin_value" or "display_name"
        if element.get("hex_value", None) is not None:
            coding_type = element.get("bin_value", None)
            if other_element is not None:
                coding_type_other = other_element.get("bin_value", None)
                if coding_type != coding_type_other:
                    html_elements += buildHtmlLine(
                        diff_name=key,
                        diff_value_left=coding_type,
                        diff_value_right=coding_type_other,
                    )
                    continue
        elif element.get("display_value", None) is not None:
            coding_type = element.get("display_value", None)
            if other_element is not None:
                coding_type_other = other_element.get("display_value", None)
                if coding_type != coding_type_other:
                    html_elements += buildHtmlLine(
                        diff_name=key,
                        diff_value_left=coding_type,
                        diff_value_right=coding_type_other,
                    )
                    continue

    if len(html_elements) > 0:
        return TABLE.format(content=html_elements)

    return ""


def diffEcu(base_ecu, other_ecu):
    # Diff the coding
    html_body = ""
    for blocks in base_ecu["ecu_master"]:
        if blocks["@type"] == "ident":
            pass
        elif blocks["@type"] == "adaptions_read":
            pass
        elif blocks["@type"] == "coding_read":
            html_body += diffCoding(
                base_ecu["ecu_master"][1]["values"], other_ecu["ecu_master"][1]["values"]
            )
    if len(html_body) > 0:
        return CODING.format(name="Coding") + html_body

    return ""


def beginCompare(base_ecus, other_ecus):
    html_body = ""
    for ecu_id, base_ecu in base_ecus.items():
        # Based on the ecu_id match it in `other_ecus`
        other_ecu = other_ecus.get(ecu_id, None)
        if other_ecu is None:
            continue

        html_body += MODULE_NAME.format(
            module_name="Analyzing ECU {} - {}".format(ecu_id, base_ecu["ecu_name"])
        )
        print("Analyzing ECU {} - {}".format(ecu_id, base_ecu["ecu_name"]))
        html_body += diffEcu(base_ecu=base_ecu, other_ecu=other_ecu)

    return html_body


def main():
    if len(sys.argv) < 3:
        print("Please use: odis-diff.py file1 file2")

    base_json = loadJson(sys.argv[1])

    if base_json is None:
        print("{} is an invalid json".format(sys.argv[1]))
        return 1

    other_json = loadJson(sys.argv[2])
    if other_json is None:
        print("{} is an invalid json".format(sys.argv[2]))
        return 1

    base_ecus = sorted(
        base_json["vehicle"]["communications"]["ecus"]["ecu"], key=lambda obj: obj.get("ecu_id")
    )

    # List to dict
    base_ecus = {element["ecu_id"]: element for element in base_ecus}

    other_ecus = sorted(
        other_json["vehicle"]["communications"]["ecus"]["ecu"], key=lambda obj: obj.get("ecu_id")
    )

    # List to dict
    other_ecus = {element["ecu_id"]: element for element in other_ecus}

    html = HTML_FILE.format(
        head=HEAD, body_content=beginCompare(base_ecus=base_ecus, other_ecus=other_ecus)
    )

    with open("result.html", "w") as fd:
        fd.write(html)


if __name__ == "__main__":
    main()
