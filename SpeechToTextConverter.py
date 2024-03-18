import tkinter as tk
import speech_recognition as sr
import threading
import time

def start_conversion():
    global stop_listening
    stop_listening = False
    start_button.config(state=tk.DISABLED)  # Disable the button during speech recognition
    start_time = time.time()  # Record the start time of speech recognition

    def stop_conversion():
        global stop_listening
        stop_listening = True
        start_button.config(state=tk.NORMAL)  # Re-enable the button when speech recognition stops

    # Create a separate thread for speech recognition
    def recognize_speech():
        global stop_listening
        recognizer = sr.Recognizer()
        audio_stream = sr.Microphone()
        with audio_stream as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
            while not stop_listening:
                try:
                    audio_data = recognizer.listen(source, timeout=0.5)  # Adjust timeout for faster response
                    text = recognizer.recognize_google(audio_data, language='pa-IN')  # Punjabi language code
                    translated_text.delete(1.0, tk.END)
                    translated_text.insert(tk.END, text)
                    word_count = len(text.split())
                    words_label.config(text=f"Number of words: {word_count}")
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    translated_text.delete(1.0, tk.END)
                    translated_text.insert(tk.END, "Could not request results; {0}".format(e))
                duration = time.time() - start_time
                duration_label.config(text=f"Duration: {duration:.2f} seconds")
                root.update()  # Update the GUI to reflect changes
                if stop_listening:
                    break

        # Re-enable the button after speech recognition stops
        start_button.config(state=tk.NORMAL)

    stop_conversion_button = tk.Button(root, text="Stop Speech", command=stop_conversion, bg="#d9534f", fg="white", font=("Helvetica", 12), padx=10)
    stop_conversion_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Start the speech recognition process in a separate thread
    recognize_thread = threading.Thread(target=recognize_speech)
    recognize_thread.start()

# Create main window
root = tk.Tk()
root.title("Speech to Text Converter")
root.configure(bg="#f5f5f5")

# Button for starting speech recognition
start_button = tk.Button(root, text="Start Speech", command=start_conversion, bg="#5cb85c", fg="white", font=("Helvetica", 12), padx=10)
start_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Text widget for displaying translated text
translated_text = tk.Text(root, height=10, width=50, bg="white", fg="#333", font=("Helvetica", 14), wrap="word")
translated_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Label for displaying number of words
words_label = tk.Label(root, text="Number of words: 0", bg="#f5f5f5", fg="#333", font=("Helvetica", 12))
words_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Label for displaying duration of speech
duration_label = tk.Label(root, text="Duration: 0.00 seconds", bg="#f5f5f5", fg="#333", font=("Helvetica", 12))
duration_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Run the application
root.mainloop()
