

def add_to_layout(layout, *widget_list):
    for widget in widget_list:
        layout.add_widget(widget)
    return layout