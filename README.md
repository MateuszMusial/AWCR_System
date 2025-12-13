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


---

<div align="center">
  <sub>**AWCR System** is released under the **MIT License**.</sub>
  
</div>
