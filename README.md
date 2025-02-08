# Important note 
This a personal open ai api key, so we added a demo to avoid trying the api yourself, kindly check the two videos

# Assumptions:
• We simulated an excel sheet that contains only some important features (as:age,Nat Id,phone num, ...)as the customers database that exists in orange data warehouse and provided the model with this data to retrive important information from it that may help in asnwering the customer questions.

• We also assume that the security condition are applied before the tool starts its job (as verifying the customer face or finger print)


# 1. Introduction
## 1.1 Project Overview
**“Borto2ana”** is an AI assistant designed for **Orange Egypt** to serve as an in-store (or public) customer service kiosk. By leveraging speech-to-speech technology in Egyptian Arabic, Borto2ana streamlines various customer requests—ranging from extracting a new SIM card to managing service options. The goal is to reduce branch crowding by offering a convenient, automated alternative for customers.
Key Objectives:

•	Provide an interactive, speech-based system for customers who prefer or need assistance in Arabic.

•	Enable quick and independent transactions, including tasks like obtaining a new SIM card.

•	Offload routine inquiries to an AI-driven service, allowing human staff to handle complex cases.

## 1.2 Why It Matters
•	Customer Convenience: Customers can quickly resolve their needs without waiting in lines.

•	Scalability: Deploying multiple kiosks can extend service availability beyond standard branch hours or even in remote locations.

•	Consistency: The AI assistant delivers the same level of service across all kiosks, reducing variability.

## 1.3 Intended Audience
This documentation is primarily for software engineers and technical teams who will install, configure, or maintain the Borto2ana system. It also offers insight for Orange Egypt project managers who need a clear overview of the solution’s capabilities and requirements.


# 2. System Requirements 
## 2.1 Software Requirements
•	Programming Language: Python 3.8+ recommended.

•	Frameworks/Libraries:

 o	PyTorch or TensorFlow 

 o	Speech Recognition library (e.g., OpenAI Whisper and OpenAI GPT-4o-mini-audio).

 o	Speech Synthesis library (e.g.,sounddevice, wavio).

 o	Tkinter

 o	Other standard Python libraries (openai, numpy,pathlib, ffmpeg,openpyxl).

# 3. Architecture Overview
 
![Untitled diagram-2025-02-08-163637](https://github.com/user-attachments/assets/dc420c76-fe8d-446f-9013-578714917f9d)


## 3.2 Components Breakdown
•	Speech Recognition (ASR):

 o	Converts real-time Egyptian Arabic audio into text.

 o	Using Whisper Model From OpenAI.

•	Dialogue/Decision Logic:

 o	Interprets the text input, determines user intent (e.g., “Get a new SIM”).

 o	Connects to Orange’s backend systems if needed.

•	Text-to-Speech (TTS):

 o	Generates responses in Egyptian Arabic.

 o	Outputs spoken language using gpt-4o-mini-audio Model

•	User Interface Layer:

 o	Could include a screen to display text-based prompts or instructions.

 o	Though Borto2ana is primarily speech-based, a minimal UI might show progress or error messages.


## 3.3 Data Flow
1.	Audio Input: The customer speaks into the kiosk microphone.
3.	ASR: The system transcribes the audio into text.
4.	Intent Analysis: The text is passed to a dialogue manager or some custom logic that detects what the user wants.
5.	Backend Interaction: If required (e.g., to trigger a SIM card dispenser), the system makes an API call or triggers hardware.
6.	Response Generation: The system composes a textual response, which then goes to the TTS engine.
7.	Audio Output: The TTS output is played back to the user.

# 4. Getting Started
## 4.1 Overview
This section helps you quickly verify that Borto2ana runs in a development environment. We’ll cover:
1.	Cloning the Repository
2.	Installing Minimal Dependencies
3.	Running a Simple Demo

## 4.2 Quick Installation
1. Clone The Repo
   
```git clone https://github.com/orange-egypt/borto2ana```


2.	Install Dependencies
   
```pip install Requirements.txt```

3.	Run the Basic Demo
   
```python Borto2ana.py```

# 5. User Guide
The User Guide focuses on how a customer interacts with Borto2ana and what functionalities are available.

## 5.1 Basic Interaction
1.	Initiating the Session:
 o	The user approaches the kiosk and either says a wake word (e.g., “Borto2ana”) or taps “Start” on a touchscreen.
2.	Speaking the Request:
 o	The user states their need in Egyptian Arabic, e.g., “عايز أطلع خط جديد” (“I want a new SIM card”).
3.	System Response:
 o	The system transcribes the request, determines the intent, and provides a spoken response, e.g., “حاضر، هطلعلك خط جديد حالاً.” (“Sure, I’ll get you a new SIM right away.”)
## 5.2 Available Services
•	Extract a SIM Card:

 o	The kiosk or an attached dispenser may provide a new SIM after confirming user details.
 
 o	The system walks the user through identification steps.
 
•	Account & Billing Inquiries (if enabled):

 o	“عايز أعرف رصيدي” (“I want to know my balance”).
 
 o	The system can retrieve the user’s account info after identification or OTP verification.

## 5.3 Common Prompts & Best Practices
•	Speak Clearly: Encourage users to talk at a normal volume and pace.

•	Confirmation Prompts: Borto2ana may confirm critical actions, e.g., “هل أنت متأكد؟” (“Are you sure?”).

•	Error Handling: If the system fails to understand, it may say, “معلش ممكن تعيد تاني؟” (“Sorry, could you repeat that?”).





