from transformers import pipeline
from config import SUMMARY_LENGTH

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def summarize_email(content):
    """ Use a pretrained model to summarize the email content. """
    summary = summarizer(content, max_length=SUMMARY_LENGTH, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    # Taking an example email content for testing
    example_content = """
    "Subject: Exciting Updates and Opportunities Await!\n\nDear [Recipient],\n\nI hope this email finds you well! As we dive into the new quarter, I wanted to share some exciting updates and opportunities that lie ahead.\n\nFi$
    """
    print("Original Email Content:")
    print(example_content)
    print("\nSummarized Email:")
    print(summarize_email(example_content))
