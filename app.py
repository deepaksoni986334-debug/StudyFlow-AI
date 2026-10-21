
import gradio as gr


def create_study_plan(goal, topics_text, available_minutes, priorities_text):
    if not goal or not goal.strip():
        return "Please enter your study goal."

    topics = [
        t.strip()
        for t in topics_text.replace(",", "\n").splitlines()
        if t.strip()
    ]

    if not topics:
        return "Please enter at least one topic."

    if available_minutes < 15:
        return "Please provide at least 15 minutes."

    priorities = {}

    for line in priorities_text.splitlines():
        if ":" in line:
            topic, priority = line.split(":", 1)
            priority = priority.strip().capitalize()

            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"

            priorities[topic.strip().lower()] = priority

    weights = []

    for topic in topics:
        priority = priorities.get(topic.lower(), "Medium")
        weights.append({"High": 3, "Medium": 2, "Low": 1}[priority])

    study_time = max(1, int(available_minutes * 0.9))
    break_time = available_minutes - study_time
    total_weight = sum(weights)

    allocations = [
        int(study_time * weight / total_weight)
        for weight in weights
    ]

    remaining = study_time - sum(allocations)

    for i in range(remaining):
        allocations[i % len(allocations)] += 1

    result = [
        "# 📚 STUDYFLOW AI",
        f"**Goal:** {goal}",
        f"**Available time:** {available_minutes} minutes",
        "",
        "## Your personalized study plan",
        ""
    ]

    for i, topic in enumerate(topics):
        priority = priorities.get(topic.lower(), "Medium")
        result.append(
            f"{i + 1}. **{topic}** — {allocations[i]} minutes "
            f"({priority} priority)"
        )

    result.extend([
        "",
        f"☕ **Break and review:** {break_time} minutes",
        "",
        "💡 Start with your highest-priority topic."
    ])

    return "\n".join(result)


def update_plan(goal, topics, minutes, priorities):
    return "🔄 Updated plan\n\n" + create_study_plan(
        goal, topics, minutes, priorities
    )


with gr.Blocks(title="StudyFlow AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📚 StudyFlow AI
        ### Your personal study planning companion

        Create a study schedule based on your goals, time, and priorities.
        """
    )

    with gr.Row():
        with gr.Column():
            goal = gr.Textbox(
                label="Study goal",
                value="Prepare for my Physics exam"
            )

            topics = gr.Textbox(
                label="Topics (one per line)",
                value=(
                    "Wave Optics\n"
                    "Photoelectric Effect\n"
                    "De Broglie Wavelength\n"
                    "Numerical Problems"
                ),
                lines=5
            )

            minutes = gr.Slider(
                minimum=15,
                maximum=480,
                value=180,
                step=15,
                label="Available study time (minutes)"
            )

            priorities = gr.Textbox(
                label="Topic priorities",
                value=(
                    "Wave Optics: High\n"
                    "Photoelectric Effect: Medium\n"
                    "De Broglie Wavelength: Low\n"
                    "Numerical Problems: High"
                ),
                lines=4
            )

            generate = gr.Button(
                "✨ Generate Study Plan",
                variant="primary"
            )

            adapt = gr.Button("🔄 Adapt Study Plan")

        with gr.Column():
            output = gr.Markdown(
                label="Your study plan"
            )

    inputs = [goal, topics, minutes, priorities]

    generate.click(
        fn=create_study_plan,
        inputs=inputs,
        outputs=output
    )

    adapt.click(
        fn=update_plan,
        inputs=inputs,
        outputs=output
    )

    gr.Markdown(
        """
        ---
        **Prototype:** Python + Gradio  
        **Planning method:** Rule-based time allocation  
        **AI model and voice recognition:** Not yet implemented
        """
    )


if __name__ == "__main__":
    demo.launch()
