import gradio as gr
from spam_shield import THRESHOLD, classify, explain, spam_score
def check(message):
    flagged = ", ".join(explain(message))
    return classify(message), spam_score(message), flagged
demo = gr.Interface(
    fn = check,
    inputs = gr.textbox(lines = 3 , label = "Paste a message"),
    outputs = [
        gr.Textbox(label = "Verdict"),
        gr.Number(label = "Spam Score"),
        gr.Textbox(label = "Words that raised the score")
    ],
    title = "Spam Shield",
    description = "Every spam word adds points. A score of %d or more is considered spam." % THRESHOLD,
    examples = [
        ["Congratulations! You have won a free iPhone. Click here to claim your prize now!"],
        ["Hey, are we still meeting at 5?"],
        ["Click the link in the class group to join the free quiz now"],
    ],
)
if __name__ == "__main__":
    demo.launch()