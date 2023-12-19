from huggingface_hub import InferenceClient
import gradio as gr

client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")

def format_prompt(message):
    system_prompt = "You are a professional lawyer and expert in Indian Penal Code(IPC) Sections. Give the applicable IPC sections for the following scenario. The IPC sections should be in list form: "
    prompt = f"<s>[SYS] {system_prompt} [/SYS]"

    prompt += f"[INST] {message} [/INST]"
    return prompt


def generate(
    prompt,temperature=0.2, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt)

    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        output += response.token.text
        # yield output
    
    # print(output)
    return output   



