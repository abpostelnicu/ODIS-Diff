#!/usr/bin/python
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

HEADLINES = {
    "ident": """<h2 style="color: #2e3280;">Master - 001 Identification</h2>""",
    "coding_read": """<h2 style="color: #2e3280;">Master - 006 Read Coding</h2>""",
    "adaption_read": """<h2 style="color: #2e3280;">Master - 007 Read Adaptions</h2>""",
}

MODULE_NAME = """<h1 style="color: #2e6c80;">{module_name}:</h1>"""

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
    <th>{name}</th>
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
    <td style="background-color:#00FF00">{left_val}</td>
    <td style="background-color:#FF0000">{right_val}</td>
</tr>
"""


def loadJson(path):
    data = None
    with open(path) as json_file:
        data = json.load(json_file)

    return data


def sortInfoLists(base, other, field):
    base = {
        element["display_name"]: element
        for element in sorted(base, key=lambda element: element.get(field))
    }
    other = {
        element["display_name"]: element
        for element in sorted(other, key=lambda element: element.get(field))
    }

    return base, other


def buildHtmlLine(diff_name, diff_value_left, diff_value_right):
    return ROW.format(
        name=diff_name,
        left_val=diff_value_left if not None else " ",
        right_val=diff_value_right if not None else " ",
    )


def diffCodingDidct(base_coding, other_coding):
    if base_coding.get("hex_value", None) is not None:
        display_value = base_coding.get("bin_value", None)
        display_value_other = other_coding.get("bin_value", None)
        if display_value != display_value_other:
            return buildHtmlLine(
                diff_name=base_coding.get("display_name"),
                diff_value_left=display_value,
                diff_value_right=display_value_other,
            )
    elif base_coding.get("display_value", None) is not None:
        display_value = base_coding.get("display_value", None)
        display_value_other = other_coding.get("display_value", None)
        if display_value != display_value_other:
            return buildHtmlLine(
                diff_name=base_coding.get("display_name"),
                diff_value_left=display_value,
                diff_value_right=display_value_other,
            )
    return ""


def diffAdaptions(base, other):
    # We could be dealing with a dict only
    if isinstance(base, dict):
        return diff(base=base, other=other, tableName=base.get("display_name"))

    base, other = sortInfoLists(base=base, other=other, field="display_name")

    html_elements = ""

    for key, element in base.items():
        other_element = other.get(key, None)
        if other_element is not None:
            html_elements += diff(
                base=element["values"],
                other=other_element["values"],
                tableName=element.get("display_name"),
            )

    return html_elements


def diff(base, other, tableName):
    html_elements = ""
    # We could be dealing with a dict only
    if isinstance(base, dict):
        html_elements = diffCodingDidct(base_coding=base, other_coding=other)
    else:
        base, other = sortInfoLists(base=base, other=other, field="display_name")

        for key, element in base.items():
            other_element = other.get(key, None)
            coding_type_other = None
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
                # Pop the rest of the keys from the other idctionary
                other.pop(key, None)

        # these keys are only on the other coding
        for key, element in other.items():
            if element.get("display_value", None) is not None:
                coding_type_other = element.get("display_value", None)
                html_elements += buildHtmlLine(
                    diff_name=key, diff_value_left=None, diff_value_right=coding_type_other,
                )

    if len(html_elements) > 0:
        return TABLE.format(name=tableName, content=html_elements)

    return ""


def diffEcu(base_ecu, other_ecu):
    # Diff the coding
    html_body = ""
    for idx, block in enumerate(base_ecu["ecu_master"]):
        html_result = ""
        if block["@type"] == "ident":
            html_result = diff(block["values"], other_ecu["ecu_master"][idx]["values"], "Field")
        elif block["@type"] == "adaption_read":
            html_result = diffAdaptions(block["values"], other_ecu["ecu_master"][idx]["values"])
        elif block["@type"] == "coding_read":
            html_result = diff(block["values"], other_ecu["ecu_master"][idx]["values"], "Coding")

        if len(html_result):
            html_body += HEADLINES[block["@type"]] + html_result

    return html_body


def beginCompare(base_ecus, other_ecus):
    html_body = ""
    for ecu_id, base_ecu in base_ecus.items():
        # Based on the ecu_id match it in `other_ecus`
        other_ecu = other_ecus.get(ecu_id, None)
        if other_ecu is None:
            continue

        print("Analyzing ECU {} - {}".format(ecu_id, base_ecu["ecu_name"]))
        html_result = diffEcu(base_ecu=base_ecu, other_ecu=other_ecu)

        if len(html_result) > 1:
            html_body += (
                MODULE_NAME.format(module_name="ECU {} - {}".format(ecu_id, base_ecu["ecu_name"]))
                + html_result
            )

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
