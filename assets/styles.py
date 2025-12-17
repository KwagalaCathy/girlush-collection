"""
Styles and UI constants for Girlush Collections
"""
import config

# Button styles
BUTTON_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
    'bg': config.PRIMARY_COLOR,
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 20,
    'pady': 10
}

BUTTON_SECONDARY_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
    'bg': config.SECONDARY_COLOR,
    'fg': config.TEXT_COLOR,
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 15,
    'pady': 8
}

BUTTON_DANGER_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
    'bg': config.DANGER_COLOR,
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 20,
    'pady': 10
}

BUTTON_SUCCESS_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
    'bg': config.SUCCESS_COLOR,
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 20,
    'pady': 10
}

BUTTON_PRIMARY_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
    'bg': config.PRIMARY_COLOR,
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 20,
    'pady': 10
}

# Entry/Input styles
ENTRY_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
    'relief': 'solid',
    'borderwidth': 1
}

# Label styles
LABEL_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
    'bg': config.BG_COLOR
}

LABEL_TITLE_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_TITLE, 'bold'),
    'bg': config.BG_COLOR,
    'fg': config.PRIMARY_COLOR
}

LABEL_HEADING_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
    'bg': config.BG_COLOR
}

# Frame styles
FRAME_STYLE = {
    'bg': config.BG_COLOR
}

CARD_STYLE = {
    'bg': 'white',
    'relief': 'solid',
    'borderwidth': 1
}

# Treeview/Table styles
TREEVIEW_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
    'rowheight': 30
}

# Menu styles
MENU_STYLE = {
    'font': (config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
    'bg': 'white',
    'activebackground': config.SECONDARY_COLOR
}

def apply_hover_effect(widget, hover_bg, default_bg):
    """Apply hover effect to widget"""
    def on_enter(e):
        widget['background'] = hover_bg
    
    def on_leave(e):
        widget['background'] = default_bg
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)
