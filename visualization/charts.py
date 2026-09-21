import plotly.express as px


def create_chart(result, chart):
    chart_type = chart.get("type", "none")
    x = chart.get("x")
    y = chart.get("y")
    if chart_type == "none" or x not in result.columns or y not in result.columns:
        return None
    if chart_type == "line":
        return px.line(result, x=x, y=y, markers=True)
    if chart_type == "bar":
        return px.bar(result, x=x, y=y)
    if chart_type == "scatter":
        return px.scatter(result, x=x, y=y)
    return None
