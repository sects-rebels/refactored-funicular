#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:26:18 2025

@author: aidenhall
"""
import os
import numpy as np
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk # Import ttk for Combobox

pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice

# Voice options from the image you provided
VOICE_OPTIONS = [
    "af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore",
    "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa"
]

def generate_audio():
    audio_name = audio_name_entry.get()
    text_input = text_area.get("1.0", tk.END)
    selected_voice = voice_var.get() # Get the selected voice from Combobox

    if not audio_name:
        messagebox.showerror("Error", "Please enter an audio name.")
        return
    if not text_input.strip():
        messagebox.showerror("Error", "Please enter text to generate audio.")
        return
    if not selected_voice:
        messagebox.showerror("Error", "Please select a voice.")
        return

    generator = pipeline(
        text_input, voice=selected_voice, # Use the selected voice here
        speed=1, split_pattern=r'\n+'
    )

    all_audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)
        print(gs)
        print(ps)
        all_audio_segments.append(audio)

    combined_audio = np.concatenate(all_audio_segments, axis=0)

    output_dir = "/Users/aidenhall/Downloads"
    output_filename = f"{audio_name}.wav"
    output_path = os.path.join(output_dir, output_filename)

    try:
        sf.write(output_path, combined_audio, 24000)
        messagebox.showinfo("Success", f"Audio saved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving audio: {e}")


# --- UI Setup ---
window = tk.Tk()
window.title("Kokoro TTS Generator")

# Audio Name Input
audio_name_label = tk.Label(window, text="Audio Name:")
audio_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
audio_name_entry = tk.Entry(window, width=40)
audio_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Voice Selection Dropdown
voice_label = tk.Label(window, text="Select Voice:")
voice_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
voice_var = tk.StringVar(window) # Variable to hold the selected voice
voice_dropdown = ttk.Combobox(window, textvariable=voice_var, values=VOICE_OPTIONS, state="readonly") # "readonly" prevents manual typing
voice_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")
voice_dropdown.set(VOICE_OPTIONS[0]) # Set default voice to the first option

# Text Input Area
text_label = tk.Label(window, text="Text to Synthesize:")
text_label.grid(row=2, column=0, padx=10, pady=5, sticky="ne")
text_area = scrolledtext.ScrolledText(window, width=50, height=15)
text_area.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Generate Button
generate_button = tk.Button(window, text="Generate Audio", command=generate_audio)
generate_button.grid(row=3, column=1, pady=10)

window.mainloop()