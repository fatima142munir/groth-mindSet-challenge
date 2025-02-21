def uvStreamlitProject() -> None:
    import streamlit as st
    import random
    import pandas as pd
    # Import Altair for chart visualization
    import altair as alt  

    # Leaderboard File
    LEADERBOARD_FILE = "guessing_game_leaderboard.csv"

    # Function to save user score
    def save_score(username, attempts):
        try:
            leaderboard = pd.read_csv(LEADERBOARD_FILE)
        except FileNotFoundError:
            leaderboard = pd.DataFrame(columns=["Name", "Attempts"])
        
        new_entry = pd.DataFrame({"Name": [username], "Attempts": [attempts]})
        leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)
        leaderboard = leaderboard.sort_values(by="Attempts", ascending=True).reset_index(drop=True)
        leaderboard.to_csv(LEADERBOARD_FILE, index=False)
        st.session_state.leaderboard = leaderboard  # Store updated leaderboard in session state immediately

    # Function to show leaderboard table
    def show_leaderboard():
        if "leaderboard" not in st.session_state:
            try:
                leaderboard = pd.read_csv(LEADERBOARD_FILE)
                st.session_state.leaderboard = leaderboard
            except FileNotFoundError:
                st.session_state.leaderboard = pd.DataFrame(columns=["Name", "Attempts"])
        
        st.write("### 🏆 Leaderboard (Top 10)")
        st.dataframe(st.session_state.leaderboard.head(10).set_index("Name"), use_container_width=True)

        # Show leaderboard graph
        show_leaderboard_graph()

    # Function to display leaderboard graph
    def show_leaderboard_graph():
        if "leaderboard" in st.session_state and not st.session_state.leaderboard.empty:
            top_leaderboard = st.session_state.leaderboard.head(10)  # Show only top 10 players
            
            chart = alt.Chart(top_leaderboard).mark_bar().encode(
                x=alt.X("Name:N", sort="-y", title="Player Name"),  # Names on X-axis
                y=alt.Y("Attempts:Q", title="Attempts (Lower is better)"),  # Attempts on Y-axis
                color=alt.Color("Attempts:Q", scale=alt.Scale(scheme="blues"))  # Color scale
            ).properties(title="Leaderboard - Attempts vs. Players", width=600)

            st.altair_chart(chart, use_container_width=True)

    # Add styling
    st.markdown("""
        <style>
            .stApp {background-color: #f5f7fa;}
            h1 {color: #4CAF50; text-align: center;}
            .stButton>button {background-color: #4CAF50; color: white; width: 100%; border-radius: 8px;}
            .stTextInput>div>div>input {border-radius: 8px; padding: 10px;}
        </style>
    """, unsafe_allow_html=True)

    st.title("🎯 Number Guessing Game")
    st.write("### Try to guess the number between 1 and 10!")

    if "target_number" not in st.session_state:
        st.session_state.target_number = random.randint(1, 10)
        st.session_state.attempts = 0
        st.session_state.username = ""
        st.session_state.game_won = False  # Track game state

    def reset_game():
        st.session_state.target_number = random.randint(1, 10)
        st.session_state.attempts = 0
        st.session_state.username = ""
        st.session_state.game_won = False
        st.rerun()

    st.write("## 🎮 Make a Guess")
    user_guess = st.number_input("Enter your guess:", min_value=1, max_value=10, step=1, format="%d")
    if st.button("Submit Guess"):
        st.session_state.attempts += 1
        if user_guess < st.session_state.target_number:
            st.warning("🔼 Too low! Try again.")
        elif user_guess > st.session_state.target_number:
            st.warning("🔽 Too high! Try again.")
        else:
            st.session_state.game_won = True
            st.success(f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts.")

    if st.session_state.game_won:
        st.session_state.username = st.text_input("Enter your name for the leaderboard:", value=st.session_state.username)
        if st.button("Save Score & Restart") and st.session_state.username:
            save_score(st.session_state.username, st.session_state.attempts)
            st.success("✅ Your score has been saved!")
            reset_game()

    show_leaderboard()

uvStreamlitProject()


