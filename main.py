import speech_recognition as sr
from transformers import pipeline
from email_reader import search_emails, connect_to_email
from speech_output import speak
from url_handler import filter_urls, open_url
from email_summarizer import summarize_email

# Initialize an LLM pipeline for generating and interpreting suggestions
action_generator = pipeline("text-generation")   #model="gpt-model-for-email-actions"
action_interpreter = pipeline("zero-shot-classification") #model="facebook/bart-large-mnli"

def listen_to_action():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please speak your action now.")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that. Could you repeat?")
    except sr.RequestError as e:
        speak(f"Error with the speech recognition service: {e}")

def main():
    mail = connect_to_email()
    emails = [
    (
        'subject1', 
        'Dear User, We are excited to announce the launch of our new product. You can learn more about it on our website: https://www.example.com/new-product. We believe this product will revolutionize the way you work. Best, The Team'
    ), 
    (
        'subject2', 
        'Hello, We are hosting a webinar next week to discuss the latest trends in our industry. We would love for you to join us. You can register for the webinar at this link: https://www.example.com/webinar. Looking forward to seeing you there. Regards, The Webinar Team'
    ),
    (
        'subject3',
        'Dear Student, We are pleased to inform you about an exciting internship opportunity at Harvard University. This is a great chance to gain valuable experience and make connections in your field of interest. You can find more details and apply on our website: https://www.harvard.edu. Best, The Internship Team'
    )
    ]
    if not emails:
        speak("No new relevant emails.")
        return

    for _, email_content in emails:
        summary = summarize_email(email_content)
        speak(f"Summary: {summary}")

        # Generate dynamic actions
        suggested_actions = action_generator(f"Suggest actions for this email content: {email_content}")
        speak("Here are some actions you might consider: " + suggested_actions[0]['generated_text'])

        user_action = listen_to_action()
        if user_action:
            # Interpret the user's spoken action using zero-shot classification
            actions = ["reply", "register", "schedule", "ignore"]
            results = action_interpreter(user_action, candidate_labels=actions)
            chosen_action = results['labels'][0]

            if chosen_action == "register":
                urls = filter_urls(email_content)
                if urls:
                    if len(urls) > 1:
                        speak("There are multiple URLs available. I will read them out now.")
                        for i, url in enumerate(urls):
                            speak(f"URL {i+1}: {url}")
                        speak("Please say the number of the URL you want to open.")
                        url_indices = [str(i+1) for i in range(len(urls))]
                        chosen_url_index = action_interpreter(listen_to_action(), candidate_labels=url_indices)['labels'][0]
                        chosen_url = urls[int(chosen_url_index) - 1]
                    else:
                        chosen_url = urls[0]
                    speak("Would you like to proceed to the registration page?")
                    if "yes" in listen_to_action().lower():
                        speak(f"Redirecting you to {chosen_url}")
                        open_url(chosen_url)
                    else:
                        speak("No valid URLs found for registration.")

            elif chosen_action == "reply":
                speak("Redirecting you to your email to reply.")
                open_url(f"https://mail.google.com/mail/u/0/#inbox")

            # we can add more actions as needed
            elif chosen_action == "schedule":
                speak("Would you like me to open the calendar for you?")
                if "yes" in listen_to_action().lower():
                    speak("Redirecting you to your calendar.")
                    open_url("https://calendar.google.com")

            elif chosen_action == "ignore":
                speak("No action will be taken.")
