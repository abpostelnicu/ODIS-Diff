HTML_FILE = """
<HTML>
{head}
<BODY>
{body_content}
</BODY>
</HTML>
"""

HEADLINES = {
    "ident": """<h2>Master - 001 Identification</h2>""",
    "coding_read": """<h2>Master - 006 Read Coding</h2>""",
    "adaption_read": """<h2>Master - 007 Read Adaptions</h2>""",
}

MODULE_NAME = """<h1>{module_name}:</h1>"""

HEAD = """
<head>
    <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            font-size: 12px;
        }
        h2 {
            color: #2e3280;
            font-size: 16px;
        }

        h1 {
            color: #2e6c80;
            font-size: 20px;
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
    <tr>{content}</tr>
</table>
"""

ROW = """
<tr>
    <td>{name}</td>
    <td style="background-color:#00FF00">{left_val}</td>
    <td style="background-color:#FF0000">{right_val}</td>
</tr>
"""
