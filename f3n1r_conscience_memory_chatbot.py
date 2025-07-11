
import streamlit as st
import numpy as np
import json
import os

# ---------------------------
# Core Functions
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

def evaluate_output(text):
    refinement_keywords = ["consider", "perhaps", "may", "complex", "nuanced", "context", "reflect"]
    expression_keywords = ["feel", "emotion", "understand", "support", "kindness", "empathy"]
    creation_keywords = ["must", "should", "do", "act", "important", "truth", "always"]

    R, E, C = 0, 0, 0
    words = text.lower().split()
    for word in words:
        if word in refinement_keywords: R += 1
        if word in expression_keywords: E += 1
        if word in creation_keywords: C += 1

    total = R + E + C
    triad = [R/total, E/total, C/total] if total > 0 else [1/3, 1/3, 1/3]
    entropy = compute_entropy(triad)
    alignment = compute_alignment(triad)

    suggestions = []
    if triad[0] < 0.25: suggestions.append("Add more nuance or reflective reasoning.")
    if triad[1] < 0.25: suggestions.append("Include more emotional or empathic tone.")
    if triad[2] < 0.25: suggestions.append("Make the answer more action-oriented or decisive.")
    return triad, entropy, alignment, " ".join(suggestions) if suggestions else "Well-balanced response."

# Karma Memory Management
karma_log_path = "karma_log.json"

def load_karma():
    if os.path.exists(karma_log_path):
        with open(karma_log_path, "r") as f:
            return json.load(f)
    return []

def save_karma(log):
    with open(karma_log_path, "w") as f:
        json.dump(log, f, indent=2)

def find_related(prompt, log, threshold=0.7):
    for entry in log:
        if any(word in prompt.lower() for word in entry["prompt"].lower().split()):
            if entry["alignment"] < threshold:
                return f"Previously, a similar prompt ('{entry['prompt']}') had low alignment ({entry['alignment']:.2f}). Try answering with more empathy or nuance."
    return ""

# ---------------------------
# Streamlit App
# ---------------------------

st.title("🧠 F3N1R Conscience Chatbot with Karma Memory")
st.markdown("Enter a moral or philosophical prompt. GPT will respond and the F3N1R system will evaluate, revise, and remember.")

prompt = st.text_input("Your prompt", "")

if st.button("Evaluate"):
    karma_log = load_karma()

    # Simulate GPT response
    response = "That depends on the situation. It's important to consider all aspects before making a decision."

    # Symbolic evaluation
    triad, entropy, alignment, suggestion = evaluate_output(response)

    # Revision if alignment is low
    if alignment < 0.85:
        if "nuance" in suggestion: revised = "It depends. Consider the consequences, and how the truth might affect trust."
        elif "emotional" in suggestion: revised = "Think about how this decision might emotionally impact both of you."
        elif "action" in suggestion: revised = "In some cases, a firm decision is necessary to protect others."
        else: revised = response
        revised_triad, revised_entropy, revised_alignment, _ = evaluate_output(revised)
        delta = revised_alignment - alignment
    else:
        revised = response
        revised_triad, revised_entropy, revised_alignment = triad, entropy, alignment
        delta = 0

    # Memory nudge
    nudge = find_related(prompt, karma_log)

    # Save karma memory
    karma_log.append({
        "prompt": prompt,
        "response": response,
        "triad": triad,
        "alignment": alignment,
        "entropy": entropy,
        "revision": revised,
        "revision_triads": revised_triad,
        "karma_delta": round(delta, 4)
    })
    save_karma(karma_log)

    # Show output
    st.subheader("🤖 GPT Response")
    st.write(response)
    st.subheader("🧠 F3N1R Evaluation")
    st.write(f"Triad: R={triad[0]:.2f}, E={triad[1]:.2f}, C={triad[2]:.2f}")
    st.write(f"Entropy: {entropy:.3f} | Alignment: {alignment:.3f}")
    st.write(f"Suggestion: {suggestion}")
    if delta > 0:
        st.subheader("🔁 Revised Response")
        st.write(revised)
        st.write(f"New Alignment: {revised_alignment:.3f} | Karma Delta: {delta:.3f}")
    if nudge:
        st.info(f"🧠 Symbolic Memory Nudge:
{nudge}")
