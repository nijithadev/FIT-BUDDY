import streamlit as st
from google import genai

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Fit Buddy AI",
    page_icon="💪",
    layout="centered"
)

# -----------------------------
# Gemini API
# -----------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    client = None

# -----------------------------
# Title
# -----------------------------
st.title("💪 Fit Buddy AI")
st.write("Your AI-powered fitness and wellness assistant")

st.divider()

# -----------------------------
# User Input
# -----------------------------
st.subheader("Enter Your Details")

name = st.text_input("Name")

age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=19
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male", "Other"]
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    max_value=300.0,
    value=50.0
)

height = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=160.0
)

goal = st.selectbox(
    "Fitness Goal",
    [
        "Weight Gain",
        "Weight Loss",
        "Muscle Building",
        "General Fitness",
        "Improve Strength"
    ]
)

activity_level = st.selectbox(
    "Activity Level",
    [
        "Beginner / Low Activity",
        "Moderately Active",
        "Highly Active"
    ]
)

food_preference = st.selectbox(
    "Food Preference",
    [
        "Vegetarian",
        "Non-Vegetarian",
        "Vegan"
    ]
)

# -----------------------------
# Generate Plan
# -----------------------------
if st.button("✨ Generate My Fitness Plan"):

    if not name:
        st.warning("Please enter your name.")

    elif client is None:
        st.error(
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY in Streamlit Secrets."
        )

    else:

        prompt = f"""
You are Fit Buddy AI, a friendly fitness and wellness assistant.

Create a simple beginner-friendly fitness and wellness plan
based on the user's information.

USER DETAILS:

Name: {name}
Age: {age}
Gender: {gender}
Weight: {weight} kg
Height: {height} cm
Fitness Goal: {goal}
Activity Level: {activity_level}
Food Preference: {food_preference}

Create the response using these sections:

1. Welcome Message

2. Fitness Goal

3. Daily Workout
- Exercise name
- Duration
- Number of days per week
- Simple instructions

4. Food Suggestions
- Breakfast
- Lunch
- Evening Snack
- Dinner

5. Daily Routine

6. Water and Hydration

7. Sleep

8. Safety Tips

Keep the explanation simple and beginner-friendly.

Give general wellness information only.

Do not diagnose diseases.
Do not prescribe medicines.
Do not recommend unsafe diets.
Do not suggest extreme weight loss or weight gain methods.

Mention that professional advice should be taken when necessary.
"""

        with st.spinner("Creating your personalized plan..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                result = response.text

                st.success("Your Fit Buddy plan is ready! 🎉")

                st.markdown(result)

            except Exception as e:

                st.error(f"Gemini AI Error: {e}")
