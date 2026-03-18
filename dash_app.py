from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import base64
import io

app = Dash(__name__)
server = app.server  # useful later if hosted internally

app.layout = html.Div(
    [
        html.H2("Student Admission & Exam Status Dashboard (Dash)"),

        html.H4("Step 3: Upload Exam Status File (Excel)"),
        dcc.Upload(
            id="upload_excel",
            children=html.Div(["Drag & Drop or ", html.A("Select an Excel file")]),
            style={
                "width": "60%",
                "height": "80px",
                "lineHeight": "80px",
                "borderWidth": "2px",
                "borderStyle": "dashed",
                "borderRadius": "10px",
                "textAlign": "center",
                "margin": "10px 0px",
            },
            multiple=False,
        ),

        html.Div(id="file_info", style={"marginTop": "10px", "fontWeight": "bold"}),
        html.Hr(),

        html.H4("Preview (Top 10 rows)"),
        html.Div(id="preview_table"),
    ],
    style={"fontFamily": "Arial", "padding": "20px"},
)


def parse_excel(contents, filename):
    """Decode uploaded file and return a DataFrame."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    if filename.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(decoded))
    else:
        raise ValueError("Please upload an Excel file (.xlsx or .xls).")


@app.callback(
    Output("file_info", "children"),
    Output("preview_table", "children"),
    Input("upload_excel", "contents"),
    State("upload_excel", "filename"),
    prevent_initial_call=True,
)
def update_output(contents, filename):
    try:
        df = parse_excel(contents, filename)

        info = f"Uploaded: {filename} | Rows: {len(df)} | Columns: {len(df.columns)}"

        # Build a simple HTML table
        header = html.Tr([html.Th(col, style={"border": "1px solid #ddd", "padding": "6px"}) for col in df.columns])

        body_rows = []
        for i in range(min(10, len(df))):
            row = html.Tr(
                [html.Td(str(df.iloc[i][col]), style={"border": "1px solid #ddd", "padding": "6px"}) for col in df.columns]
            )
            body_rows.append(row)

        table = html.Table(
            [header] + body_rows,
            style={"borderCollapse": "collapse", "width": "100%"},
        )

        return info, table

    except Exception as e:
        return f"Error: {str(e)}", ""


if __name__ == "__main__":
    # ✅ Dash 3.x uses app.run (NOT app.run_server)
    app.run(debug=True)
