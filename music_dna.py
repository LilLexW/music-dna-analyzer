def analyze_music(songs_input):
    print("START")
    import pandas as pd
    from difflib import get_close_matches
    from sklearn.preprocessing import StandardScaler

    df = pd.read_csv("dataset.csv")

    df = df.drop_duplicates(
        subset=["track_name", "artists"]
    )

    features = [
        "danceability",
        "energy",
        "valence",
        "tempo",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness"
    ]

    scaler = StandardScaler()

    songs = songs_input.replace("，", ",").split(",")
    
    song_count = len(
        [s for s in songs if s.strip()]
    )

    selected_indices = []

    matched_songs = []

    not_found = []

    for song in songs:

        song = song.strip().lower()

        result = df[
            df["track_name"]
            .str.lower()
            .str.contains(
                song,
                na=False
            )
        ]

        if len(result) == 0:

            all_tracks = df[
                "track_name"
            ].dropna().unique()

            matches = get_close_matches(
                song,
                all_tracks,
                n=5,
                cutoff=0.6
            )

            if len(matches) > 0:

                result = df[
                    df["track_name"] == matches[0]
                ]

        if len(result) > 0:

            song_index = result["popularity"].idxmax()

            selected_indices.append(
                song_index
            )

            chosen_song = df.loc[song_index]
            
            matched_songs.append(
                f"{chosen_song['track_name']} - {chosen_song['artists']}"
            )

            print(
                f"Matched: "
                f"{chosen_song['track_name']} - "
                f"{chosen_song['artists']}"
            )

        else:

            print(
                f"Song not found: {song}"
            )
            not_found.append(song)
        
    if len(selected_indices) == 0:

        return None
        
    user_profile = df.loc[
        selected_indices
    ]
    artist_counts = user_profile[
        "artists"
    ].value_counts()

    genre_counts = user_profile[
        "track_genre"
    ].value_counts()

    avg_energy = user_profile[
        "energy"
    ].mean()

    avg_valence = user_profile[
        "valence"
    ].mean()

    avg_danceability = user_profile[
        "danceability"
    ].mean()

    print("\n===== Songs Analysed =====")
    for idx in selected_indices:

        print(
            "-",
            df.loc[idx, "track_name"],
            "|",
            df.loc[idx, "artists"]
        )
        
    print("\n===== Your Music DNA =====")

    if avg_energy > 0.7:
        print("Energy: High")
    elif avg_energy > 0.4:
        print("Energy: Medium")
    else:
        print("Energy: Low")

    if avg_valence > 0.65:
        print("Mood: Uplifting")
    elif avg_valence > 0.25:
        print("Mood: Reflective")
    else:
        print("Mood: Nostalgic")

    if avg_danceability > 0.7:
        print("Danceability: High")
    else:
        print("Danceability: Medium")

    print(
        "\nRaw Scores:"
    )

    print(
        "Energy:",
        round(avg_energy, 2)
    )

    print(
        "Valence:",
        round(avg_valence, 2)
    )

    print(
        "Danceability:",
        round(avg_danceability, 2)
    )

    if avg_energy < 0.65 and avg_valence < 0.45:

        print(
            "Listening Style: "
            "Melodic & Nostalgic"
        )

    print("\n===== Genre Mix =====")

    for genre, count in genre_counts.items():

        percentage = (
            count /
            len(user_profile)
        ) * 100

        print(
            f"{genre}: "
            f"{percentage:.0f}%"
        )
        
    print("\n===== Profile Summary =====")

    if avg_valence < 0.35:

        print(
            "You tend to enjoy reflective "
            "and emotionally rich music."
        )

    elif avg_valence < 0.65:

        print(
            "You enjoy a balance of emotional "
            "and uplifting music."
        )

    else:

        print(
            "You enjoy uplifting and "
            "positive music."
        )
        print("\n===== Recommended For You =====")

    recommendations = []

    # 用户最常听的流派
    top_genres = genre_counts.index.tolist()

    # 只保留这些流派的歌曲
    candidate_df = df[
        df["track_genre"].isin(top_genres)
    ]

    for idx, row in candidate_df.iterrows():

        if idx in selected_indices:
            continue

        if pd.isna(row["energy"]):
            continue

        if pd.isna(row["valence"]):
            continue

        if pd.isna(row["danceability"]):
            continue

        distance = (
            abs(row["energy"] - avg_energy)
            +
            abs(row["valence"] - avg_valence)
            +
            abs(row["danceability"] - avg_danceability)
            +
            abs(
                row["acousticness"]
                - user_profile["acousticness"].mean()
            )
            +
            abs(
                row["speechiness"]
                - user_profile["speechiness"].mean()
            )
        )

        recommendations.append(
            (
                distance,
                row["track_name"],
                row["artists"],
                row["track_genre"]
            )
        )

    recommendations.sort(
        key=lambda x: x[0]
    )

    top_10 = recommendations[:10]

    recommended_songs = []

    for rec in top_10:

        recommended_songs.append(
            f"{rec[1]} - {rec[2]}"
        )

    print(
        "SONG COUNT =",
        song_count
    )
    return {
        "energy": avg_energy,
        "valence": avg_valence,
        "danceability": avg_danceability,
        "acousticness": user_profile["acousticness"].mean(),
        "speechiness": user_profile["speechiness"].mean(),

        "song_count": song_count,

        "matched_songs": matched_songs,

        "not_found": not_found,

        "top_artists": artist_counts,

        "genres": genre_counts,

        "recommendations": recommended_songs
    }
