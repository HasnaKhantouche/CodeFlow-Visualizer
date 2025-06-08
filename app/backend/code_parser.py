import requests

def parse_code_to_flowchart(code: str, model: str = "mistral") -> str:
    """
    Sends code to a local Ollama model and returns the full flowchart description.
    """
    prompt = (
        "Convert the following code into a step-by-step flowchart description using the format Start -> Step1 -> Step2 -> ... -> End for linear code, and for any if/else or similar conditions (including nested conditions), always use explicit branches in this format: [Condition?] -> [Yes: ...] / [No: ...], specifying what each branch means in plain English without using variable names or code, and do not add any corrections or explanations, only describe each step in plain English without referring to any code or data structure names, do not include any code snippets, variable names, class attributes, object fields, or return values—just describe the logic steps in plain English such as 'Return an error message' or 'Call the classifier', summarize each step in one short phrase, keep each step short and general, if there are multiple conditions show each as a separate branch in the above format, if there is no logic or control flow output: 'No flowchart steps: only data structure definitions found.', and do not invent any logic, steps, or conditions if the code only defines classes, data structures, or variables. Code:\n"
        "For loops (for, while, or recursion), clearly show that steps are repeated by using phrases like 'Repeat for each item', 'Repeat while condition holds', or 'Call the function again'. "
        "Never skip loop behavior or recursion. "
        f"{code}\n"
        "Flowchart:"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    response.raise_for_status()
    result = response.json()
    return result["response"].strip()

if __name__ == "__main__":
    code = """
function getDayName(dayNumber) {
    switch(dayNumber) {
        case 0:
            return "Sunday";
        case 1:
            return "Monday";
        default:
            return "Unknown";
    }
}

function main() {
    try {
        for (let i = 0; i < 3; i++) {
            console.log(getDayName(i));
        }
    } catch (e) {
        console.log("An error occurred");
    }
}

"""
    flowchart = parse_code_to_flowchart(code)
    print("Flowchart description:")
    print(flowchart)