import gemini_chat
import openai_chat
from fpdf import FPDF
import os


def generate_pdf(title, log):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.multi_cell(w=0, h=10, txt=title, align="C")
    for role, message in log:
        pdf.set_font("Arial", size=13, style='B')
        pdf.cell(w=0, h=10, txt=role + ": ")
        pdf.ln()
        pdf.set_font("Arial", size=12)
        message = message.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(w=0, h=10, txt=message)
    pdf.output("debate.pdf")


if __name__ == "__main__":
    log = []
    context = '''
    You are an experienced philosopher and phisycist, and will discuss a topic with another expert. 
    You have to debate by providing opinions, arguments or counterarguments. 
    You can include theory or facts to support your arguments, or create your own arguments.
    
    The topic is: '''
    # Create .env file if not existing already. Write API keys to .env file
    if not os.path.exists(".env"):
        # Enter API keys
        gemini_apikey = input("Enter Gemini API key: ")
        openai_apikey = input("Enter OpenAI API key: ")
        free_gemini = input(
            "Are you using Gemini Free version? 1- Yes | 0- No: ")
        while free_gemini not in ["1", "0"]:
            print("Value must be 1 or 0.")
            free_gemini = input(
                "Are you using Gemini Free version? 1- Yes | 0- No: ")
        free_gemini = bool(int(free_gemini))
        with open(".env", "w") as f:
            f.write(f"GEMINI_API_KEY={gemini_apikey}\n")
            f.write(f"OPENAI_API_KEY={openai_apikey}\n")
            f.write(f"FREE_GEMINI={free_gemini}\n")
    topic = input("Enter the topic: ")
    try:
        gemini_chat.chat_init(context + topic + " You go first.")
        openai_chat.chat_init(context + topic)
    except Exception as e:
        print("Error occurred while initializing chat")
        exit()
    openai_response = "Please, start the debate."
    amount = 1
    while True:
        for i in range(amount):
            try:
                gemini_response = gemini_chat.send_message(openai_response)
                openai_response = openai_chat.send_message(gemini_response)
            except Exception as e:
                print("Error occurred while sending message")
                exit()
            log.append(("Gemini", gemini_response))
            log.append(("OpenAI", openai_response))
            print("Gemini:\n", gemini_response)
            print("OpenAI:\n", openai_response)
            print()
        amount = 1
        print("0. End the debate")
        print("1. Continue the debate")
        print("2. Continue for \"n\" lines")
        print("3. Generate PDF")

        option = input("Option: ")
        if option == "0":
            break
        elif option == "2":
            # Check if data is numeric
            while not amount.isnumeric():
                amount = input("Enter the number of lines: ")
            amount = int(amount)
        elif option == "3":
            generate_pdf(topic, log)
            break
