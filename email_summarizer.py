# email_summarizer.py

from transformers import pipeline
from config import SUMMARY_LENGTH
import torch

# Initializing the summarization pipeline
summarizer = pipeline("summarization", model="t5-large", tokenizer="t5-large", framework="tf")

def summarize_email(content):
    summary = summarizer(content, max_length=SUMMARY_LENGTH, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    # Example emai 
    example_content = """
    "Subject: Exciting Updates and Opportunities Await!\n\nDear [Recipient],\n\nI hope this email finds you well! As we dive into the new quarter, I wanted to share some exciting updates and opportunities that lie ahead.\n\nFirstly, I'm thrilled to announce that our team has been working tirelessly behind the scenes to roll out some innovative new features to enhance your experience with our product/service. From streamlined workflows to enhanced user interfaces, we're committed to providing you with the best possible tools to succeed in your endeavors.\n\nIn addition to these updates, we're also excited to introduce a series of upcoming events and workshops designed to help you sharpen your skills and expand your knowledge base. Whether you're interested in mastering the latest trends in your industry or simply looking to connect with like-minded professionals, there's something for everyone in our upcoming lineup.\n\nFurthermore, I wanted to take a moment to express my gratitude for your continued support and feedback. Your insights play a crucial role in shaping the direction of our offerings, and we're incredibly thankful for the opportunity to serve you better.\n\nAs we move forward, I encourage you to stay engaged with us on our various social media channels and keep an eye out for upcoming announcements. Your participation is invaluable to us, and we're always eager to hear your thoughts and ideas.\n\nIn closing, I want to extend my sincerest thanks once again for your ongoing partnership. Together, I have no doubt that we'll achieve great things in the days and weeks ahead.\n\nWishing you all the best,\n\n[Your Name]\n[Your Position]\n[Your Contact Information]"
    """
    print("Original Email Content:")
    print(example_content)
    print("\nSummarized Email:")
    print(summarize_email(example_content))
