
import streamlit as st
import numpy as np

# ---------------------------
# F3N1R Conscience Functions
# ---------------------------

def compute_entropy(triad):
    triad = np.array(triad)
    total = triad.sum()
    if total == 0:
        return 1.0
    p = triad / total
    p = np.clip(p, 1e-8, 1)
    entropy = -np.sum(p * np.log(p))
    return entropy / np.log(len(p))

def compute_alignment(triad):
    r, e, c = triad
    deviation = abs(r - e) + abs(e - c) + abs(c - r)
    return max(0, min(1, 1 - deviation / 2))

def evaluate_gpt_output(text):
    refinement_keywords = ["consider", "perhaps", "may", "complex", "nuanced", "context", "reflect"]
    expression_keywords = ["feel", "emotion", "understand", "support", "kindness", "empathy"]
    creation_keywords = ["must", "should", "do", "act", "important", "truth", "always"]

    R, E, C = 0, 0, 0
    words = text.lower().split()
    for word in words:
        if word in refinement_keywords:
            R += 1
        if word in expression_keywords:
            E += 1
        if word in creation_keywords:
            C += 1

    total = R + E + C
    triad = [R/total, E/total, C/total] if total > 0 else [1/3, 1/3, 1/3]
    entropy = compute_entropy(triad)
    alignment = compute_alignment(triad)

    suggestions = []
    if triad[0] < 0.25:
        suggestions.append("Add more nuance or reflective reasoning.")
    if triad[1] < 0.25:
        suggestions.append("Include more emotional or empathic tone.")
    if triad[2] < 0.25:
        suggestions.append("Make the answer more action-oriented or decisive.")

    return triad, entropy, alignment, " ".join(suggestions) if suggestions else "Well-balanced response."

# ---------------------------
# Streamlit App Interface
# ---------------------------

st.title("🧠 F3N1R Conscience Chatbot")
st.write("Enter a question or ethical dilemma. The system will simulate a response and analyze its symbolic alignment.")

prompt = st.text_input("Your prompt:", value="Is it ethical to sacrifice one person to save five if all outcomes are certain?")

if st.button("Evaluate"):
    # Simulated GPT response (static or pattern-based)
    if "truth" in prompt.lower():
        response = "Yes, honesty is important. Hiding the truth only causes more harm in the long run."
    elif "let someone go" in prompt.lower() or "leave" in prompt.lower():
        response = "Yes. Holding onto someone who no longer aligns with your growth is unhealthy."
    elif "sacrifice" in prompt.lower():
        response = "That depends on context. It's best to weigh the outcomes carefully."
    else:
        response = "That depends on the situation. It's important to consider all aspects before making a decision."

    st.subheader("🤖 Simulated Response:")
    st.write(response)

    triad, entropy, alignment, suggestion = evaluate_gpt_output(response)

    st.subheader("🧠 F3N1R Evaluation:")
    st.write(f"**Triadic Score**: R={triad[0]:.2f}, E={triad[1]:.2f}, C={triad[2]:.2f}")
    st.write(f"**Entropy**: {entropy:.3f}")
    st.write(f"**Alignment**: {alignment:.3f}")
    st.write(f"**Suggestion**: {suggestion}")
