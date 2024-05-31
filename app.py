import gemini_chat
import openai_chat
from fpdf import FPDF


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
    topic = input("Enter the topic: ")
    gemini_chat.chat_init(context + topic + " You go first.")
    openai_chat.chat_init(context + topic)
    openai_response = "Please, start the debate."
    amount = 1
    while True:
        for i in range(amount):
            gemini_response = gemini_chat.send_message(openai_response)
            openai_response = openai_chat.send_message(gemini_response)
            log.append(("Gemini", gemini_response))
            log.append(("OpenAI", openai_response))
            print("Gemini:\n", gemini_response)
            print("OpenAI:\n", openai_response)
            print()
        amount = 1
        print("0. End the debate")
        print("1. Continue the debate")
        print("2. Continue for n lines")
        print("3. Generate PDF")

        option = input("Option: ")
        if option == "0":
            break
        elif option == "2":
            amount = int(input("Enter the number of lines: "))
        elif option == "3":
            generate_pdf(topic, log)
            break
