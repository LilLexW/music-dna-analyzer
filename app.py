import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from music_dna import analyze_music

st.set_page_config(
    page_title="Music DNA Analyzer",
    page_icon="🎵"
)

with st.sidebar:

    st.header("About")

    st.write(
        """
        🎵 Music DNA Analyzer

        Created by Alex Wang

        Master of Engineering Science
        (Telecommunications)

        UNSW Sydney

        Built with:

        • Python
        • Streamlit
        • Plotly
        • Pandas
        • Scikit-learn
        """
    )

st.title("🎵 Music DNA Analyzer")

with st.form("music_form"):

    songs = st.text_input(
        "Enter songs separated by commas:"
    )

    submitted = st.form_submit_button(
        "Analyze"
    )

if submitted:

    if not songs.strip():

        st.error(
            "Please enter at least one song."
        )

        st.stop()

    with st.spinner(
        "Analyzing your music taste..."
    ):

        result = analyze_music(songs)

    genre_diversity = len(
        result["genres"]
    )

    confidence = min(
        result["song_count"] * 8
        + max(0, 30 - genre_diversity * 5),
        100
    )

    st.subheader(
        "Analysis Confidence"
    )

    st.metric(
        "Analysis Confidence",
        f"{confidence}%"
    )

    if result["song_count"] < 5:

        st.warning(
            "For better accuracy, we recommend entering at least 5 songs."
        )

    elif result["song_count"] < 10:

        st.info(
            "Good sample size. More songs may improve accuracy."
        )

    else:

        st.success(
            "High confidence profile generated."
        )

    if result["not_found"]:

        st.warning(
            "Songs not found in database"
        )

        for song in result["not_found"]:

            st.write(
                "❌",
                song
            )

    st.subheader(
        "Matched Songs"
    )

    for song in result[
        "matched_songs"
    ]:

        st.write(
            "✅",
            song
        )

    st.subheader(
        "Your Music DNA"
    )

    st.metric(
        "Dominant Genre",
        result["top_genre"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Energy",
            f"{result['energy']:.2f}"
        )

    with col2:
        st.metric(
            "Positivity",
            f"{result['valence']:.2f}"
        )

    with col3:
        st.metric(
            "Groove",
            f"{result['danceability']:.2f}"
        )
        
    if result["energy"] > 0.7:
        st.write("🔥 High Energy Listener")
    elif result["energy"] > 0.4:
        st.write("🔥 Medium Energy Listener")
    else:
        st.write("🔥 Low Energy Listener")
        
    if result["valence"] > 0.65:
        st.write("😊 Positive Listener")
    elif result["valence"] > 0.25:
        st.write("😊 Reflective Listener")
    else:
        st.write("😊 Nostalgic Listener")

    if result["danceability"] > 0.7:
        st.write("💃 Dance-Oriented Listener")
    else:
        st.write("🎧 Relaxed Listener")

    st.subheader(
        "Genre Distribution"
    )

    genre_df = result["genres"].reset_index()

    genre_df.columns = [
        "Genre",
        "Count"
    ]

    fig_pie = px.pie(
        genre_df,
        values="Count",
        names="Genre",
        hole=0.4
    )

    fig_pie.update_traces(
        hovertemplate=
        "<b>%{label}</b><br>"
        "Percentage: %{percent}"
        "<extra></extra>"
    )

    fig_pie.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )
        
    st.subheader(
        "Music DNA Radar"
    )

    categories = [
        "Energy",
        "Positivity",
        "Groove",
        "Acousticness",
        "Speechiness"
    ]

    values = [
        result["energy"],
        result["valence"],
        result["danceability"],
        result["acousticness"],
        result["speechiness"]
    ]

    fig = go.Figure()

    hover_text = [
        "How energetic your music is",
        "How positive your music feels",
        "How dance-friendly your music is",
        "How acoustic your music is",
        "How speech-focused your music is"
    ]

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Music DNA",

            text=hover_text,

            hovertemplate=
            "<b>%{theta}</b><br>"
            + "Score: %{r:.2f}<br>"
            + "%{text}"
            + "<extra></extra>"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        template="plotly_dark",

        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )
    
    st.subheader(
        "🎚️ Music Taste Scores"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Energy",
            f"{result['energy']:.0%}"
        )

        st.progress(
            int(result["energy"] * 100)
        )

        st.metric(
            "Groove",
            f"{result['danceability']:.0%}"
        )

        st.progress(
            int(result["danceability"] * 100)
        )

    with col2:

        st.metric(
            "Positivity",
            f"{result['valence']:.0%}"
        )

        st.progress(
            int(result["valence"] * 100)
        )

        st.metric(
            "Acoustic",
            f"{result['acousticness']:.0%}"
        )

        st.progress(
            int(result["acousticness"] * 100)
        )

    st.metric(
        "Speech",
        f"{result['speechiness']:.0%}"
    )

    st.progress(
        int(result["speechiness"] * 100)
    )


    st.subheader(
        "🎤 Top Artists"
    )

    for artist in result[
        "top_artists"
    ].index:

        st.write(
            "🎤",
            artist
        )    
    
    st.subheader(
        "🎭 Music Personality"
    )

    if (
        result["energy"] < 0.6
        and result["valence"] < 0.4
    ):

        personality = "Night Thinker"

        description = (
            "You enjoy reflective, emotional and introspective music."
        )

    elif (
        result["energy"] > 0.7
        and result["danceability"] > 0.7
    ):

        personality = "Rhythm Chaser"

        description = (
            "You enjoy energetic music with strong rhythm and groove."
        )

    elif (
        result["acousticness"] > 0.6
    ):

        personality = "Acoustic Soul"

        description = (
            "You appreciate organic sounds and intimate songwriting."
        )

    elif (
        result["valence"] > 0.65
    ):

        personality = "Feel-Good Listener"

        description = (
            "You prefer uplifting, positive and feel-good songs."
        )

    else:

        personality = "Melodic Explorer"

        description = (
            "You enjoy a balance of melody, emotion and accessibility."
        )

    st.success(
        personality
    )

    st.write(
        description
    )
        
    st.subheader(
    "🧠 Music Insights"
)
    
    insight = []

    if result["valence"] < 0.4:

        insight.append(
            "You tend to enjoy emotionally rich and reflective music."
        )

    else:

        insight.append(
            "You generally enjoy positive and uplifting music."
        )

    if result["energy"] > 0.7:

        insight.append(
            "High-energy tracks are a major part of your listening habits."
        )

    elif result["energy"] < 0.4:

        insight.append(
            "You prefer calmer and more relaxed music."
        )

    else:

        insight.append(
            "You enjoy a balance between energy and melody."
        )

    if result["danceability"] > 0.7:

        insight.append(
            "Rhythm and groove play an important role in your music taste."
        )

    if result["acousticness"] > 0.6:

        insight.append(
            "You seem to prefer acoustic and organic instrumentation."
        )

    if result["speechiness"] > 0.25:

        insight.append(
            "You often listen to vocal-driven music with strong lyrical content."
        )

        st.write(
            "•",
            line
        )
    
    st.subheader(
        "Recommended Songs"
    )

    for song in result["recommendations"]:

        st.write(
            "🎵",
            song
        )
        
    st.divider()

    st.subheader(
        "Project Information"
    )

    st.write(
        """
        Music DNA Analyzer is a music profiling tool that
        analyzes listening preferences using Spotify audio features.

        Features:
        • Music DNA Analysis
        • Genre Visualization
        • Personality Classification
        • Song Recommendation
        """
    )
