import gradio as gr
from spam_shield import THRESHOLD, classify, explain, spam_score
def check_message(message):
    if not message.strip():
        return "Please enter a message.", 0
    result, score = classify(message)
    return result, score
def test_messages(messages):
    results = []
    mistakes = 0
    for item in messages.split("\n"):
        if "|" in item:
            actual, message = item.split("|", 1)
            actual = actual.strip().upper()
            predicted, score = classify(message)
            if actual != predicted:
                mistakes += 1
            results.append([
                message.strip(),
                actual,
                predicted,
                score,
                "Correct" if actual == predicted else "Mistake"
            ])
    return results, mistakes
with gr.Blocks(title="Bakery Help Desk Sorter") as demo:
    gr.Markdown("# Bakery Help Desk Sorter")
    gr.Markdown("### Spam Shield - Teach a Program to Spot Spam")
    gr.Markdown("Sort bakery customer messages into URGENT and NORMAL categories.")
    with gr.Tab("Check Message"):
        message = gr.Textbox(
            label="Enter Customer Message",
            placeholder="Example: My order is delayed and I need it urgently."
        )
        check_button = gr.Button("Check Message")
        category = gr.Textbox(label="Message Category")
        score = gr.Number(label="Weighted Word Score")
        check_button.click(
            check_message,
            inputs=message,
            outputs=[category, score]
        )
    with gr.Tab("Test Sorter"):
        messages = gr.Textbox(
            label="Enter Test Messages",
            lines=8,
            placeholder="URGENT | My order is delayed\nNORMAL | I want to know your menu"
        )
        test_button = gr.Button("Test All Messages")
        results = gr.Dataframe(
            headers=[
                "Message",
                "Actual Category",
                "Predicted Category",
                "Score",
                "Result"
            ],
            label="Sorting Results"
        )
        mistakes = gr.Number(label="Total Mistakes")

        test_button.click(
            test_messages,
            inputs=messages,
            outputs=[results, mistakes]
        )
    gr.Markdown("### Project developed using Python, Gradio and Spam Shield.")
demo.launch()