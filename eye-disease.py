import streamlit as st

# Define the symptoms for each disease
symptoms = {
    "glaucoma": ["blurred vision", "halos around lights", "eye pain", "nausea", "redness in the eye"],
    "uveitis": ["eye redness", "eye pain", "light sensitivity", "blurred vision", "floaters"],
    "cataracts": ["clouded vision", "difficulty seeing at night", "sensitivity to light", "seeing halos around lights", "fading or yellowing of colors"],
    "bulged eyes": ["protruding eyes", "dry eyes", "difficulty closing eyes", "double vision", "eye pain"],
    "crossed eyes": ["misaligned eyes", "double vision", "eye strain", "headaches", "difficulty with depth perception"]
}

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = {disease: 0 for disease in symptoms}
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# Define the questions
questions = [
    "Do you experience blurred vision?",
    "Do you see halos around lights?",
    "Do you have eye pain?",
    "Do you feel nausea?",
    "Do you have redness in the eye?",
    "Do you have light sensitivity?",
    "Do you see floaters?",
    "Do you have clouded vision?",
    "Do you have difficulty seeing at night?",
    "Do you have sensitivity to light?",
    "Do you have fading or yellowing of colors?",
    "Do you have protruding eyes?",
    "Do you have dry eyes?",
    "Do you have difficulty closing eyes?",
    "Do you have double vision?",
    "Do you have eye strain?",
    "Do you have headaches?",
    "Do you have difficulty with depth perception?"
]

# Map questions to diseases
question_to_disease = {
    0: ["glaucoma", "uveitis", "cataracts"],  # Blurred vision
    1: ["glaucoma", "cataracts"],  # Halos around lights
    2: ["glaucoma", "uveitis"],  # Eye pain
    3: ["glaucoma"],  # Nausea
    4: ["uveitis"],  # Redness in the eye
    5: ["uveitis", "cataracts"],  # Light sensitivity
    6: ["uveitis"],  # Floaters
    7: ["cataracts"],  # Clouded vision
    8: ["cataracts"],  # Difficulty seeing at night
    9: ["uveitis", "cataracts"],  # Sensitivity to light
    10: ["cataracts"],  # Fading or yellowing of colors
    11: ["bulged eyes"],  # Protruding eyes
    12: ["bulged eyes"],  # Dry eyes
    13: ["bulged eyes"],  # Difficulty closing eyes
    14: ["crossed eyes"],  # Double vision
    15: ["crossed eyes"],  # Eye strain
    16: ["glaucoma"],  # Headaches
    17: ["crossed eyes"]  # Difficulty with depth perception
}

# Display the current question
if st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]
    st.write(f"Question {st.session_state.question_index + 1}: {current_question}")

    # Display the options as radio buttons
    selected_option = st.radio("Choose an option:", ["Yes", "No"])

    # Process the response
    if st.button("Submit"):
        if selected_option == "Yes":
            for disease in question_to_disease[st.session_state.question_index]:
                st.session_state.responses[disease] += 1

        # Move to the next question
        st.session_state.question_index += 1
        st.rerun()
else:
    # Calculate the results
    results = {}
    for disease, count in st.session_state.responses.items():
        relevant_questions = sum(disease in question_to_disease[q] for q in range(len(questions)))
        results[disease] = (count / relevant_questions) * 100 if relevant_questions > 0 else 0

    likely_disease = max(results, key=results.get)
    confidence_level = results[likely_disease]

    # Display the results
    st.write(f"The most likely disease is **{likely_disease}** with a confidence level of **{confidence_level:.2f}%**.")

    # Reset for a new quiz
    if st.button("Restart Quiz"):
        st.session_state.responses = {disease: 0 for disease in symptoms}
        st.session_state.question_index = 0
        st.rerun()
