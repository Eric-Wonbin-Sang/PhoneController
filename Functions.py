

def add_to_layout(layout, *widget_list):
    for widget in widget_list:
        layout.add_widget(widget)
    return layout


def str_to_float(data_str):
    try:
        return float(data_str)
    except ValueError:
        return None
