from textwrap import dedent

import cv2
import tkinter

import easyocr
import ttkbootstrap as ttk
from tkinter import Tk, messagebox
from ultralytics import YOLO

from threading import Thread

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style
from PIL import Image, ImageTk

from Database.DBHandler import DBHandler
from Utils.common import display_detection_info
from email_handler import EmailHandler
import logger
from GUI.session import Session

from Utils.password_utils import validate_password_strength
from Utils.data_utils import preprocess_detection_data, prepare_detection_data_for_plot, export_detection_data_to_csv


logger = logger.get_logger("GUI logger")
db_handler = DBHandler()
email_handler = None

YOLO_MODEL = "awcr_system_best_model.pt"
CAMERA_WIDTH = 900
CAMERA_HEIGHT = 650
FPS_VALUE = 25
session = Session()


class GuiHandler:
    """
    This class handles the GUI for the AWCR System.
    It creates the main window, login and register forms, statistics and the camera view.
    """
    def __init__(self):
        self.window = None
        self.frame_counter = 0
        self.last_detections = []


    def create_window(self, name: str) -> Tk | None:
        """
        Creates a new Tkinter window with the given name.
        """
        try:
            self.window = Tk()
            self.window.title(name)
            self.style = Style(theme='darkly')

            logger.debug(f"Created {self.window.title()} window successfully!")
            return self.window
        except Exception as e:
            logger.error(f"Failed to create window: {e}")
            return None

    def setup_login_register_window(self) -> None:
        """
        Set up the login or register window with all necessarily fields.
        """
        self.set_window_common_parts('Login / Register')

        login_label = tkinter.Label(self.window, text='Login/Register', font=('Rockwell', 25))
        login_label.grid(row=0, column=0, columnspan=2, pady=15, sticky="ew")

        email_label = tkinter.Label(self.window, text='Email')
        email_label.grid(row=1, column=0, columnspan=2, pady=1)

        self.email_entry = tkinter.Entry(self.window, font=('Arial', 15))
        self.email_entry.grid(row=2, column=0, columnspan=2, pady=5)

        password_label = ttk.Label(self.window, text='Password')
        password_label.grid(row=3, column=0, columnspan=2, pady=1)

        self.password_entry = tkinter.Entry(self.window, font=('Arial', 15), show='*')
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=5)

        login_button = ttk.Button(self.window,
                                  text='Login',
                                  command=self.login,
                                  bootstyle='info',
                                  width=30)
        login_button.grid(row=5, column=0, columnspan=2, pady=35, padx=5)

        register_button = ttk.Button(self.window,
                                     text='Register',
                                     command=self.setup_register_window,
                                     bootstyle='success',
                                     width=30)
        register_button.grid(row=6, column=0, columnspan=2, pady=5)

        empty_label = tkinter.Label(self.window, text='', font=('Arial', 25))
        empty_label.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")

        awcr_label = tkinter.Label(self.window, text='AWCR System', font=('Rockwell', 35))
        awcr_label.grid(row=8, column=0, columnspan=2, pady=15, sticky="ew")

        logger.debug("Login/Register window created successfully.")

    def setup_login_window(self) -> None:
        """
        Set up the login window with all necessarily fields.
        """
        self.set_window_common_parts('Login')

        login_label = tkinter.Label(self.window, text='Login', font=('Rockwell', 25))
        login_label.grid(row=0, column=0, columnspan=2, pady=15, sticky="ew")

        self.email_label_in_login = tkinter.Label(self.window, text='Email')
        self.email_label_in_login.grid(row=1, column=0, columnspan=2, pady=1)

        self.email_entry = tkinter.Entry(self.window, font=('Arial', 15))
        self.email_entry.grid(row=2, column=0, columnspan=2, pady=5)

        self.password_label_in_login = ttk.Label(self.window, text='Password')
        self.password_label_in_login.grid(row=3, column=0, columnspan=2, pady=1)

        self.password_entry = tkinter.Entry(self.window, font=('Arial', 15), show='*')
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=5)

        login_button = ttk.Button(self.window,
                                  text='Login',
                                  command=self.login,
                                  width=30)
        login_button.grid(row=5, column=0, columnspan=2, pady=35, padx=5)

        empty_label = tkinter.Label(self.window, text='', font=('Arial', 25))
        empty_label.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")

        awcr_label = tkinter.Label(self.window, text='AWCR System', font=('Rockwell', 35))
        awcr_label.grid(row=8, column=0, columnspan=2, pady=15, sticky="ew")

        logger.debug("Login window created successfully.")

    def setup_register_window(self) -> None:
        self.window.destroy()

        ttk.Style.instance = None
        self.create_window('Register form')
        self.set_window_common_parts('Register form')

        login_label = tkinter.Label(self.window, text='Register form', font=('Rockwell', 25))
        login_label.grid(row=0, column=0, columnspan=2, pady=15, sticky="ew")

        email_label = ttk.Label(self.window, text='Email')
        email_label.grid(row=1, column=0, columnspan=2, pady=1)

        self.register_email_entry = tkinter.Entry(self.window, font=('Arial', 15))
        self.register_email_entry.grid(row=2, column=0, columnspan=2, pady=5)

        register_password_label = ttk.Label(self.window, text='Password')
        register_password_label.grid(row=3, column=0, columnspan=2, pady=1)

        self.register_password_entry = tkinter.Entry(self.window, font=('Arial', 15), show='*')
        self.register_password_entry.grid(row=4, column=0, columnspan=2, pady=5)

        confirm_password_label = ttk.Label(self.window, text='Confirm Password')
        confirm_password_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.confirm_password_entry = tkinter.Entry(self.window, font=('Arial', 15), show='*')
        self.confirm_password_entry.grid(row=6, column=0, columnspan=2, pady=5)

        register_form_button = ttk.Button(self.window,
                                          text='Register',
                                          command=self.register_user,
                                          width=50)
        register_form_button.grid(row=7, column=0, columnspan=2, pady=25)

        empty_label = tkinter.Label(self.window, text='', font=('Arial', 25))
        empty_label.grid(row=8, column=0, columnspan=2, pady=15, sticky="ew")

        awcr_label = tkinter.Label(self.window, text='AWCR System', font=('Rockwell', 35))
        awcr_label.grid(row=9, column=0, columnspan=2, pady=15, sticky="ew")

        logger.debug("Register window created successfully.")

    def login(self):
        global email_handler
        email = self.email_entry.get()
        password = self.password_entry.get()

        if db_handler.user_login(email, password):
            email_handler = EmailHandler(email)
            session.assign_current_user(email)
            self.setup_main_layout()
            logger.debug(f"User {email} logged successfully!")
        else:
            messagebox.showerror("Error!", "Invalid e-mail or password!")
            logger.error(f"Invalid e-mail or password created for user: {email}")
            self.clear_login_fields()

    def clear_login_fields(self) -> None:
        """
        Clears the fields in the login window.
        """
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.email_entry.focus_set()

    def is_password_and_confirmed_password_the_same(self):
        """
        Checks if the password and confirmed password are the same.
        """
        return self.register_password_entry.get() == self.confirm_password_entry.get()

    def register_user(self) -> None:
        global email_handler

        email = self.register_email_entry.get()
        password = self.register_password_entry.get()

        password_validated, error = validate_password_strength(password)
        if not password_validated:
            messagebox.showerror("Error!", f"{error}")
            self.clear_register_fields()
            return

        if self.is_password_and_confirmed_password_the_same():
            result, message = db_handler.add_user(email, password)
            if result:
                messagebox.showinfo("Success!", message)
                logger.info(f"User {email} registered successfully!")
                email_handler = EmailHandler(email)
                email_handler.send_user_registered_information_email()
                self.window.destroy()
                self.create_window("Login")
                self.setup_login_window()
            else:
                messagebox.showerror("Error!", message)
                self.clear_register_fields()
        else:
            messagebox.showerror("Error!", "Passwords do not match!")
            self.clear_register_fields()

    def clear_register_fields(self) -> None:
        """
        Clears the fields in the register window.
        """
        self.register_email_entry.delete(0, 'end')
        self.register_password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.register_email_entry.focus_set()

    def setup_main_layout(self) -> None:
        """
        Set up the main layout of the application with camera view and menu.
        """
        self.window.destroy()

        self.window = tkinter.Tk()
        self.window.title("Camera Window")
        self.window.geometry("1280x720")
        self.model = YOLO(YOLO_MODEL)
        self.reader = easyocr.Reader(["en"])
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Can't open the camera!")
            logger.error("Error! Can't open the camera!")
            self.window.destroy()
            cv2.destroyAllWindows()
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS_VALUE)
        logger.info(f"Camera opened with resolution {CAMERA_WIDTH} x {CAMERA_HEIGHT} and {FPS_VALUE} frames per second.")

        self.setup_main_layout_fields()
        self.update_frame()
        self.window.mainloop()

    def setup_main_layout_fields(self):
        """
        Sets up the main layout fields including the tools frame and image frame.
        """
        tools_frame = self.setup_tool_frame()
        logo = Image.open("awcrLogo.png")
        logo_resized = logo.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(logo_resized)

        logged_user = tkinter.Label(tools_frame, text=f"Logged as {session.email_address}")
        logged_user.pack(pady=10)

        stats_button = tkinter.Button(tools_frame, text="Statistics", width=15, command=self.setup_statistics_window)
        stats_button.pack(pady=10)

        program_info_button = tkinter.Button(tools_frame, text="Program info", width=15, command=self.show_program_info)
        program_info_button.pack(pady=10)

        quit_button = tkinter.Button(tools_frame, text="Quit program", width=15, command=self.quit_program)
        quit_button.pack(pady=20)

        tkinter.Label(tools_frame, image=self.logo_image).pack(padx=5, pady=5)

        # Image frame
        self.image_frame = tkinter.Frame(self.window, width=1280, height=720)
        self.image_frame.pack(padx=5, pady=5, side=tkinter.RIGHT)

        tkinter.Label(self.image_frame, text="Camera view", bg="grey", font=('Rockwell', 35)).pack(padx=5, pady=5)

        self.camera_label = tkinter.Label(self.image_frame)
        self.camera_label.pack(padx=5, pady=5)

    def update_frame(self) -> None:
        """
        Reads a frame from the camera, processes it, and updates the label with the new frame.
        """
        if not self.cap.isOpened():
            logger.error("Camera is not opened!")
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame_counter += 1

            if self.frame_counter % 4 == 0:
                current_detections = []
                results = self.model(frame)

                for result in results:
                    for box in result.boxes:
                        confidence = box.conf[0]
                        class_id = int(box.cls[0])

                        if class_id == 0 and confidence > 0.55:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            plate_roi = frame[y1:y2, x1:x2]

                            ocr_result = self.reader.readtext(plate_roi, detail=0)
                            final_result = preprocess_detection_data(ocr_result)

                            detection_data = {
                                'coordinates': (x1, y1, x2, y2),
                                'confidence': confidence
                            }
                            current_detections.append(detection_data)

                            car_is_wanted, details = self.check_detected_car_is_wanted(final_result)
                            if car_is_wanted:
                                Thread(
                                    target=_handle_detected_car,
                                    args=(details,),
                                    daemon=True
                                ).start()

                self.last_detections = current_detections

            if self.last_detections:
                for detection in self.last_detections:
                    x1, y1, x2, y2 = detection.get("coordinates")
                    conf = detection.get("confidence")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"License plate: {conf:.2f}%"
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 2)

            image = Image.fromarray(frame) # costly operation
            self.camera_frame = ImageTk.PhotoImage(image=image)
            self.camera_label.config(image=self.camera_frame)
            self.camera_label.image = self.camera_frame
        self.window.after(10, self.update_frame)

    def setup_statistics_window(self) -> None:
        """
        Set up the statistics window with all necessary fields.
        """
        self.cap.release()
        self.window.quit()
        self.window.destroy()

        ttk.Style.instance = None
        self.create_window('Statistics')
        self.window.title('Statistics')
        self.window.geometry("1280x960")

        logo = Image.open("awcrLogo.png")
        logo_resized = logo.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(logo_resized)

        tools_frame = self.setup_tool_frame()
        tkinter.Label(tools_frame, text=f"Logged as {session.email_address}").pack(pady=10)

        buttons_data = [
            ("Camera View", self.setup_main_layout),
            ("Export Data", self.export_data_to_csv),
            ("Program Info", self.show_program_info),
            ("Quit program", self.quit_program)
        ]
        for text, command in buttons_data:
            padding = 20 if text == "Quit program" else 10

            tkinter.Button(
                tools_frame,
                text=text,
                width=15,
                command=command
            ).pack(pady=padding)

        self.notebook = ttk.Notebook(tools_frame)
        self.notebook.pack(expand=True, fill="both")

        tools_tab = ttk.Frame(self.notebook)
        self.period_var = tkinter.StringVar(value="Last month")

        periods = ["Today", "Last week", "Last month", "Last year"]

        for period in periods:
            tkinter.Radiobutton(
                tools_tab,
                text=period,
                variable=self.period_var,
                value=period,
                bg="lightblue",
                command=self.update_chart
            ).pack(anchor="w", padx=50, pady=20)

        tkinter.Label(tools_frame, image=self.logo_image).pack(padx=5, pady=5)
        self.notebook.add(tools_tab, text="Period")

        self.chart_frame = tkinter.Frame(self.window, width=400, height=400, bg="grey")
        self.chart_frame.pack(padx=5, pady=5, side=tkinter.RIGHT)
        tkinter.Label(
            self.chart_frame,
            text="Statistics",
            bg="grey",
            fg="white",
            font=('Rockwell', 35)
        ).pack(padx=5, pady=5)
        self.chart_frame.pack(padx=5, pady=5, side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        self.draw_chart()

    def draw_chart(self) -> None:
        """
        Draws the chart in the statistics window using matplotlib.
        """
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        self.update_chart()

    def update_chart(self):
        """
        Updates the chart based on the selected time period.
        """
        self.ax.clear()

        period = self.period_var.get()
        detections = db_handler.fetch_detections_data(period)
        result = prepare_detection_data_for_plot(detections, period)
        self.ax.clear()

        if result:
            x, y = zip(*result.items())
            self.ax.bar(x, y, color='blue')
            self.ax.set_title(f"Detections - {period}")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Number of Detections")

            total_detections = sum(y)
            max_y = max(y)
            self.ax.text(0.5, max_y * 0.9, f"Total: {total_detections}", fontsize=10, ha='center',
                         transform=self.ax.transAxes)
        else:
            self.ax.text(0.5, 0.5, "No Data Available", fontsize=12, ha='center', transform=self.ax.transAxes)
        self.canvas.draw()

    @staticmethod
    def show_program_info():
        """
        Displays the program information in a message box.
        """
        info = dedent("""\
                   Engineer's Thesis

        Cracow University of Technology

           Created by Mateusz Musiał

            \tversion 1.2


                   Date: 2025-06-12
        """)
        messagebox.showinfo("AWCR System info", info)
        logger.debug("Program info displayed.")


    def quit_program(self) -> None:
        """
        Quits the program.
        """
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.cap.release()
            self.window.quit()
            self.window.destroy()
            cv2.destroyAllWindows()

            logger.debug("Closed the application.")


    @staticmethod
    def check_detected_car_is_wanted(final_result: str) -> tuple[bool, tuple]:
        """
        Check if the detected car is wanted by fetching data from the database.
        """
        return db_handler.check_detected_car_in_database(final_result)


    def export_data_to_csv(self):
        """
        Exports the detection data to a CSV file based on the selected period.
        """
        period = self.period_var.get()
        detections = db_handler.fetch_detections_data(period)
        export_detection_data_to_csv(detections)
        messagebox.showinfo(
            "Export Completed",
            f"Detection data for period '{period}' has been exported successfully!"
        )
        logger.info("Exporting detection data to CSV.")


    def set_window_common_parts(self, window_name: str) -> None:
        """
        Sets common parts of the window such as icon and geometry.
        """
        self.icon = tkinter.PhotoImage(file="awcrLogo.png")
        self.window.title(window_name)
        self.window.geometry("800x550")
        self.window.iconphoto(True, self.icon)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)


    def setup_tool_frame(self) -> tkinter.Frame:
        """
        Sets up the tools frame in the main layout.
        """
        tools_frame = tkinter.Frame(self.window, width=350, height=400)
        tools_frame.pack(padx=10, pady=5, side=tkinter.LEFT, fill=tkinter.Y)
        ttk.Label(
            tools_frame,
            text="MENU",
            borderwidth=18,
            background='#3E4149'
        ).pack(padx=5, pady=5)
        return tools_frame


def _handle_detected_car(details: tuple) -> None:
    """
    Orchestrates the sequence of actions for a detected wanted vehicle.

    This method unpacks the vehicle details, records the detection in the database,
    updates the user interface, and sends an email notification.

    Args:
        details (tuple | None): A tuple containing vehicle specifications in the following order:
            (id, license_plate, brand, model, owner_id).
            If None, no actions are performed.
"""
    if details is not None:
        _, licence_plate, brand, model, _ = details

        db_handler.add_detection(licence_plate)
        display_detection_info(brand, model, licence_plate)
        email_handler.send_detected_car_information_email(
            brand=brand,
            model=model,
            licence_plate=licence_plate
        )

