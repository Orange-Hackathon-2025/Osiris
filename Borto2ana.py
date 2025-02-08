#General Imports

import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import wavio
import os
from openai import OpenAI
from playsound import playsound
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

# OpenAI API Key
api_key = "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"
client = OpenAI(api_key=api_key)

# Initialize conversation history
conversation_history = []

#Recording Audio to later use in Speech To Text "Whisper"
def record_audio(filename="input.wav", duration=5, samplerate=16000):
    print("Recording Audio")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wavio.write(filename, audio, samplerate, sampwidth=2)
    print("Recording Ended")

#Speech To Text Model (Changing the Speech taken from record_audio function to Speech)
def speech_to_text(audio_file="input.wav"):
    global client
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )

    print(transcription.text)
    return transcription.text

#Getting Response as text from GPT 4o and giving instructions to the LLM
def get_gpt_response(text, user_info):
    global client, conversation_history

    conversation_history.append({"role": "user", "content": text})

    system_prompt = (
        "أنت موظف خدمة عملاء في شركه اورانچ. هدفك هو مساعدة العملاء بكل استفسارتهم و مشاكلهم بخصوص خدمات الشركة و عروضها. "
        "يجب عليك الرد بلغه ودودة و مفهومة و سهلة. عندما يسأل العميل عن خدمة او عرض معين, قم بتقديم المعلومات اللازمة بالتفصيل, "
        "و اطرح اسئله استضاحيه لو احتجت تفاصيل اضافية قبل تقديم الحلول. اذا كانت المشكلة تحتاج لتحويل للفرع او الدعم الفني, "
        "قم بتوجيه العميل بشكل واضح و دقيق لأقرب فرع او الرقم المناسب. استخدم اللغة العامية المصرية مع الحفاظ على اسلوب مهني و محترم طوال الحوار.\n\n"
        f"بيانات العميل:\n"
        f"- الاسم: {user_info.get('Name', 'غير معروف')}\n"
        f"- الرقم القومي: {user_info.get('National_id', 'غير معروف')}\n"
        f"- رقم الهاتف: {user_info.get('Phone_Number', 'غير معروف')}\n"
        f"- النوع: {user_info.get('Gender', 'غير معروف')}\n"
        f"- العمر: {user_info.get('Age', 'غير معروف')}\n"
        f"- الرصيد في أورانچ كاش: {user_info.get('Orange_Cash', 'غير معروف')}\n"
        f"- الكول تون: {user_info.get('call_tone', 'غير معروف')}\n"
        f"الخدمه الحاليه: {user_info.get('Service', 'غير معروف')}\n"
    )

    conversation_history.insert(0, {"role": "system", "content": system_prompt})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history
    )

    response_text = completion.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": response_text})

    print("🔹 Customer Service Response (Text):", response_text)
    return response_text

#Text To Speech model

def text_to_speech(text, voice="onyx", output_file="response.mp3"):
    global client
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )

    with open(output_file, "wb") as file:
        file.write(response.read())

    if Path(output_file).exists():
        print(f"✅ Audio file saved: {output_file}")
        playsound(output_file)

        try:
            os.remove(output_file)

        except Exception as e:
            print(f"❌ Error deleting file {output_file}: {e}")

#Fetching user data
def fetch_user_info(national_id, data_file="Known_Cust.xlsx"):
    try:
        if not os.path.exists(data_file):
            print(f"Error: File {data_file} does not exist.")
            return None

        user_data = pd.read_excel(data_file)
        print("Columns in the dataset:", user_data.columns)

        user_data['National_id'] = user_data['National_id'].astype(str)
        national_id = str(national_id)

        user_row = user_data[user_data['National_id'] == national_id]

        if user_row.empty:
            print(f"No user found with National ID: {national_id}")
            return None

        user_info = {
            "Name": user_row.iloc[0]['Name'],
            "National_id": user_row.iloc[0]['National_id'],
            "Phone_Number": user_row.iloc[0]['Phone_Number'],
            "Gender": user_row.iloc[0]['Gender'],
            "Age": user_row.iloc[0]['Age'],
            "Orange_Cash": user_row.iloc[0]['Orange_Cash'],
            "call_tone": user_row.iloc[0]['call_tone'],
            "Service": user_row.iloc[0]['Service']
        }

        print("User information successfully fetched:", user_info)
        return user_info

    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None
#Chatting
def chat(user_info):
    while True:
        record_audio()
        user_text = speech_to_text()
        if user_text.lower() in ["خروج","bye","exit", "باي","سلام","انهي"]:
            print("👋 مع السلامه!")
            break
        response = get_gpt_response(user_text, user_info)
        text_to_speech(response)

#Registiring new users files reading
df_av_num = pd.read_excel("available_number.xlsx") #Availabile numbers (Unsold)
av_num = df_av_num['Phone Numbers'].tolist()
df_users = pd.read_excel("Known_Cust.xlsx") #Exsisting Customers Data


#Register new user
def Register(Nat_ID, Name, Age, Gender, df_users, av_num):
    if not av_num:
        print("No available numbers left!")
        return

    new_number = av_num.pop(0)

    if Nat_ID in df_users["National_id"].values:
        df_users.loc[df_users["National_id"] == Nat_ID, ["Name", "Age", "Gender", "Phone_Number","Orange_Cash","call_tone","Service"]] = [Name, Age, Gender, new_number]
        print(f"Updated user with National ID {Nat_ID}: Assigned phone number {new_number}")
    else:
        new_user = {
            "National_id": Nat_ID,
            "Name": Name,
            "Age": Age,
            "Gender": Gender,
            "Phone_Number": new_number,
            "Orange_Cash": False,
            "call_tone": False,
            "Service": "Kart El Kebir 13"
        }

        book = load_workbook("Known_Cust.xlsx")
        sheet = book.active
        sheet.append([
            new_user["National_id"],
            new_user["Name"],
            new_user["Phone_Number"],
            new_user["Gender"],
            new_user["Age"],
            new_user["call_tone"],
            new_user["Orange_Cash"],
            new_user["Service"]
        ])
        book.save(r"Known_Cust.xlsx")
        print(f"Added new user with National ID {Nat_ID}: Assigned phone number {new_number}")

    pd.DataFrame({"Phone Numbers": av_num}).to_excel("available_number.xlsx", index=False)

    print(f"Phone number {new_number} assigned to National ID {Nat_ID}.")
    user_info = fetch_user_info(Nat_ID)
    chat(user_info)

def main():

    #Existing users service
    def start_existing_customer():
        national_number = entry_existing_id.get()
        if not national_number:
            messagebox.showerror("Error", "Please enter the National ID")
            return
        user_info = fetch_user_info(national_number)
        if user_info:
            chat(user_info)

    #New Customer Service
    def start_new_customer():
        name = entry_new_name.get()
        nat_id = entry_new_id.get()
        age = entry_new_age.get()
        gender = gender_var.get()

        if not name or not nat_id or not age or not gender:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        Register(nat_id, name, age, gender, df_users, av_num)

    #GUI CODE
    root = tk.Tk()
    root.title("Orange Customer Service")
    root.geometry("600x500")
    root.configure(bg="#333333")

    title = tk.Label(root, text="Orange Customer Service", font=("Helvetica", 20, "bold"), bg="#ff6600", fg="white")
    title.pack(pady=20, fill="x")

    frame_existing = tk.Frame(root, bg="#333333")
    frame_existing.pack(pady=10, fill="x", padx=20)

    lbl_existing = tk.Label(frame_existing, text="Existing Customer", font=("Helvetica", 16), bg="#333333", fg="orange")
    lbl_existing.grid(row=0, column=0, sticky="w", pady=5)

    lbl_existing_id = tk.Label(frame_existing, text="National ID:", bg="#333333", fg="white")
    lbl_existing_id.grid(row=1, column=0, sticky="w")

    entry_existing_id = tk.Entry(frame_existing, width=30)
    entry_existing_id.grid(row=1, column=1, pady=5)

    btn_existing = tk.Button(frame_existing, text="Start", bg="#ff6600", fg="white", command=start_existing_customer)
    btn_existing.grid(row=1, column=2, padx=10)

    frame_new = tk.Frame(root, bg="#333333")
    frame_new.pack(pady=20, fill="x", padx=20)

    lbl_new = tk.Label(frame_new, text="New Customer", font=("Helvetica", 16), bg="#333333", fg="orange")
    lbl_new.grid(row=0, column=0, sticky="w", pady=5)

    lbl_new_name = tk.Label(frame_new, text="Name:", bg="#333333", fg="white")
    lbl_new_name.grid(row=1, column=0, sticky="w")

    entry_new_name = tk.Entry(frame_new, width=30)
    entry_new_name.grid(row=1, column=1, pady=5)

    lbl_new_id = tk.Label(frame_new, text="National ID:", bg="#333333", fg="white")
    lbl_new_id.grid(row=2, column=0, sticky="w")

    entry_new_id = tk.Entry(frame_new, width=30)
    entry_new_id.grid(row=2, column=1, pady=5)

    lbl_new_age = tk.Label(frame_new, text="Age:", bg="#333333", fg="white")
    lbl_new_age.grid(row=3, column=0, sticky="w")

    entry_new_age = tk.Entry(frame_new, width=30)
    entry_new_age.grid(row=3, column=1, pady=5)

    lbl_new_gender = tk.Label(frame_new, text="Gender:", bg="#333333", fg="white")
    lbl_new_gender.grid(row=4, column=0, sticky="w")

    gender_var = tk.StringVar(value="Male")
    gender_male = tk.Radiobutton(frame_new, text="Male", variable=gender_var, value="Male", bg="#333333", fg="white")
    gender_female = tk.Radiobutton(frame_new, text="Female", variable=gender_var, value="Female", bg="#333333", fg="white")
    gender_male.grid(row=4, column=1, sticky="w")
    gender_female.grid(row=5, column=1, sticky="w")

    btn_new = tk.Button(frame_new, text="Register", bg="#ff6600", fg="white", command=start_new_customer)
    btn_new.grid(row=6, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
