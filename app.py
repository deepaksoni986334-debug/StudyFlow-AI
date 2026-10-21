import gradio as gr


def studyflow_alexa(message, history):
    message = message.lower().strip()

    if any(word in message for word in ["45 minutes", "45 min", "only 45"]):
        minutes = 45
    elif any(word in message for word in ["1 hour", "one hour", "60 minutes"]):
        minutes = 60
    elif any(word in message for word in ["2 hours", "two hours", "120 minutes"]):
        minutes = 120
    else:
        minutes = 90

    topics = [
        "Wave Optics",
        "Photoelectric Effect",
        "De Broglie Wavelength",
        "Numerical Problems"
    ]

    priorities = {
        "Wave Optics": "High",
        "Photoelectric Effect": "Medium",
        "De Broglie Wavelength": "Low",
        "Numerical Problems": "High"
    }

    weights = {"High": 3, "Medium": 2, "Low": 1}
    study_minutes = int(minutes * 0.9)
    total_weight = sum(weights[priorities[t]] for t in topics)

    plan = [
        "# 📚 StudyFlow AI",
        "### Alexa+-style study planning simulation",
        f"**Study time available:** {minutes} minutes",
        "",
        "## Your personalized study plan"
    ]

    allocations = []
    for topic in topics:
        allocated = round(
            study_minutes * weights[priorities[topic]] / total_weight
        )
        allocations.append(allocated)

    # Ensure the allocated study minutes add up correctly.
    difference = study_minutes - sum(allocations)
    allocations[0] += difference

    for topic, allocated in zip(topics, allocations):
        plan.append(
            f"- **{topic}:** {allocated} minutes "
            f"({priorities[topic]} priority)"
        )

    plan.extend([
        "",
        f"☕ **Break and review:** {minutes - study_minutes} minutes",
        "",
        "💡 You can ask for a plan using 45 minutes, 1 hour, or 2 hours.",
        "",
        "*Prototype: rule-based planning; no real Alexa+ connection or "
        "generative AI is implemented.*"
    ])

    return "\n".join(plan)


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="StudyFlow AI | Alexa+ Demo"
) as app:
    gr.Markdown("""
    # 📚 StudyFlow AI
    ### An Alexa+-style study planning simulation

    Describe your available study time to generate a personalized plan.
    """)

    gr.ChatInterface(
        fn=studyflow_alexa,
        title="Study Assistant",
        description=(
            'Try: "I have 2 hours to prepare for Physics" '
            'or "I only have 45 minutes left."'
        )
    )

if __name__ == "__main__":
    app.launch()
