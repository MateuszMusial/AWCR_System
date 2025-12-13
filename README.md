<div align="center">
<img width="300" src="https://github.com/user-attachments/assets/5ecaad30-580f-41b6-82a6-58a6a1717e3a" alt="AWCR Logo" />
<br />
<br />

# AWCR SYSTEM
### Automated Wanted Car Recognition System

<br />
<p>
  <b>An intelligent solution for real-time license plate detection and wanted vehicle identification.</b>
</p>
</div>
<br />

<br />

## 🏗️ System Architecture

The **AWCR System** is designed with a modular architecture to ensure efficiency and scalability. It integrates camera input, AI processing, database management, and an alerting system.

<br />

<div align="center">
  <img width="70%" src="https://github.com/user-attachments/assets/a08d9260-5e67-4053-9086-e2219a4a4171" alt="System Architecture Diagram" />
</div>

<br />

### 🔹 Key Components:
* **Camera Module:** Handles real-time video stream acquisition.
* **Detection Engine:** Uses deep learning to locate and read license plates.
* **Database:** Stores records of wanted vehicles and detection logs.
* **Alert Module:** Triggers notifications when a match is found.

<br />
<br />

---

<br />

## 🛠️ Technologies Used

The **AWCR System** is built using a robust stack of open-source technologies, leveraging state-of-the-art object detection models.

<br />

<div align="center">

| **Category** | **Technologies** |
| :--- | :--- |
| **Core Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Object Detection** | ![YOLO](https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=yolo&logoColor=black) |
| **Computer Vision** | ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white) |
| **Data & Analytics** | ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) |
| **Testing** | ![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9ed9) |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) |
| **Tools & IDE** | ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![PyCharm](https://img.shields.io/badge/PyCharm-000000?style=for-the-badge&logo=pycharm&logoColor=white) |

</div>

<br />

### 📚 Key Libraries & Frameworks
* **YOLO (You Only Look Once):** Implemented for high-speed, real-time license plate detection and recognition.
* **OpenCV:** Used for image pre-processing and video stream handling.
* **Pandas:** Utilized for efficient data manipulation and managing detection logs.
* **Pytest:** Ensures code reliability and system stability through automated testing.
* **Tkinter / CustomTkinter:** Powers the user interface.

<br />

---

<br />

## 📸 Application Demonstration

Below is a visual demonstration of the system operating in real-time.

<br />

### 1. Live Camera Feed & Detection
The application identifies the license plate within the video feed and verifies it against the database.

<br />

<div align="center">
  <img width="80%" src="https://github.com/user-attachments/assets/fa2ee0a3-ba5b-43c3-926a-95cace994535" alt="Camera View 1" />
  <br /><br />
  <img width="80%" src="https://github.com/user-attachments/assets/77fea309-ad24-4ce9-876e-917910e74173" alt="Camera View 2" />
  <br /><br />
  <img width="80%" alt="image" src="https://github.com/user-attachments/assets/4ee1145a-8e4d-4ff7-8ee8-ddc2845ef0f6" alt="Camera View 3" />
</div>

<br />
<br />

### 2. Alert System (Wanted Car Detected)
When a license plate matches an entry in the "Wanted" list, the system triggers an immediate visual popup and sends an email notification.

<br />
<div align="center">
  <h4>⚠️ Desktop Notification</h4>
  <img width="80%" src="https://github.com/user-attachments/assets/b3a0b7aa-4ac7-49c7-a236-c1cab27c5ab8"/>
  <br />
  <img width="80%" src="https://github.com/user-attachments/assets/bbeec6e5-cbfe-4178-82c4-04d9e1453bb3" alt="Desktop Alert"/>
  
  <br /><br />
  
  <h4>📧 Email Alert</h4>
  <img width="80%" alt="image" src="https://github.com/user-attachments/assets/03380c8e-6c14-42d4-b4f2-deb65c4dc305" alt="Email Notification" />

</div>
<br />
<br />

---

<br />

## 🗃️ Data Management

The system maintains a structured database to track wanted vehicles and log all detection events for auditing purposes.

<br />

<div align="center">
  <img width="80%"  alt="image" src="https://github.com/user-attachments/assets/30836a9a-5cbc-4191-9600-591ec46be1b7" alt="Database Records" />
  <img width="80%" src="https://github.com/user-attachments/assets/0fdc4eee-8d2a-4e8d-9b97-0fef20e9e394"/>
  <img width="80%" alt="image" src="https://github.com/user-attachments/assets/47b28971-25aa-45a0-804b-eab54e36d278" />
</div>


<br />
<br />

---

<br />

## 🧠 AI/ML Implementation

The core of the AWCR System is a custom-trained neural network optimized for accuracy and speed.

<br />

### 1. Training Process
The model was trained over multiple epochs, optimizing the loss function to ensure precise character recognition.

<div align="center">
  <img width="90%" src="https://github.com/user-attachments/assets/c90d91b6-8866-48af-8842-83aab2b5042e" alt="Training Graphs" />
</div>

<br />

### 2. Performance Metrics
The **Confusion Matrix** below demonstrates the model's high true positive rate and low error margin during validation.

<div align="center">
  <img width="70%" src="https://github.com/user-attachments/assets/0a556a93-0ed5-4d07-902e-d331372f1149" alt="Confusion Matrix" />
</div>

<br />
<br />

<br />
<br />

---

<br />

## 🚀 Getting Started

Follow these steps to set up and run the **AWCR System** locally.

### Prerequisites

* **Python:** Version 3.9 or higher (recommended).
* **Git:** For cloning the repository.
* **A camera source** (e.g., webcam or IP camera stream URL) if testing live detection.

<br />

### 1. Installation

#### A. Clone the Repository
Open your terminal or command prompt and run the following command to download the project files:

```bash
git clone [https://github.com/YourUsername/AWCR-System.git](https://github.com/YourUsername/AWCR-System.git)
cd AWCR-System
```
---
#### B. Set Up Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
# Activate the environment:
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### C. Install Dependencies
Install all required libraries, including Pytest, YOLO, and OpenCV components:

```bash
pip install -r requirements.txt
```
<br />

### 2. Running the System
Execute the main application file to launch the Graphical User Interface (GUI):

```bash
python main.py
```

<div align="center">
  <sub>**AWCR System** is released under the **MIT License**.</sub>
  
</div>
