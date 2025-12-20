import logging


from logger import setup_logger
from GUI.app import GuiHandler


def main():
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    setup_logger()

    gui_handler = GuiHandler()
    gui_handler.create_window("Login / Register")
    gui_handler.setup_login_register_window()
    gui_handler.window.mainloop()


if __name__ == '__main__':
    main()