import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

LOG_FILE = "/logs/prediction_logs.json"
TRAIN_DATA_FILE = "IMDB_Dataset.csv"

st.set_page_config(layout="wide")
st.title("COMP4705 Model Monitoring Dashboard")


@st.cache_data(ttl=10)
def load_data(log_file, train_file):
    # Load log data
    log_df = pd.DataFrame()
    if os.path.exists(log_file):
        log_entries = []
        with open(log_file, "r") as f:
            for line in f:
                try:
                    log_entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # Skip bad lines
        if log_entries:
            log_df = pd.DataFrame(log_entries)

    # Load training data
    train_df = None
    if os.path.exists(train_file):
        train_df = pd.read_csv(train_file)

    return log_df, train_df


def main():
    log_df, train_df = load_data(LOG_FILE, TRAIN_DATA_FILE)

    if log_df.empty:
        st.warning("No prediction log data!")
        return

    if train_df is None:
        st.error(f"Training data ('{TRAIN_DATA_FILE}') not found.")
        return

    st.header("Model Performance Metrics")
    correct_predictions = (
        log_df["predicted_sentiment"] == log_df["true_sentiment"]
    ).sum()
    total_predictions = len(log_df)

    # Converted the long line into a readable if/else block
    if total_predictions > 0:
        accuracy = correct_predictions / total_predictions
    else:
        accuracy = 0

    if accuracy < 0.8 and total_predictions > 0:
        # Broke this long f-string across multiple lines
        st.error(
            f"ALERT: Model accuracy ({accuracy:.2%}) has fallen below the 80% "
            "threshold!"
        )
    elif total_predictions > 0:
        # Broke this long f-string across multiple lines
        st.success(
            f"Model accuracy ({accuracy:.2%}) is above the 80% threshold."
        )

    true_positives = (
        (log_df["predicted_sentiment"] == "positive")
        & (log_df["true_sentiment"] == "positive")
    ).sum()
    false_positives = (
        (log_df["predicted_sentiment"] == "positive")
        & (log_df["true_sentiment"] == "negative")
    ).sum()

    # Converted the long line into a readable if/else block
    if (true_positives + false_positives) > 0:
        precision = true_positives / (true_positives + false_positives)
    else:
        precision = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Predictions", f"{total_predictions}")
    col2.metric("Overall Accuracy", f"{accuracy:.2%}")
    col3.metric("Precision (Positive Class)", f"{precision:.2%}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.header("Data Drift")
        # Broke this long string across multiple lines
        st.write(
            "Compares the distribution of sentence lengths between "
            "training and inference data."
        )
        train_lengths = train_df["review"].str.len()
        inference_lengths = log_df["request_text"].str.len()
        fig, ax = plt.subplots()
        # Formatted these long function calls
        ax.hist(
            train_lengths, bins=50, density=True, alpha=0.7, label="Training"
        )
        ax.hist(
            inference_lengths, bins=50, density=True, alpha=0.7, label="Infer"
        )
        ax.set_xlabel("Sentence Length")
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.header("Target Drift")
        # Broke this long string across multiple lines
        st.write(
            "Compares the distribution of predicted sentiments vs. "
            "sentiments in the training data."
        )
        train_dist = train_df["sentiment"].value_counts(normalize=True)
        inference_dist = log_df["predicted_sentiment"].value_counts(
            normalize=True
        )
        # Formatted this long DataFrame constructor
        drift_df = pd.DataFrame(
            {"Training": train_dist, "Inference": inference_dist}
        ).fillna(0)
        st.bar_chart(drift_df)

    st.divider()

    st.header("Recent Predictions Log")
    st.dataframe(log_df.tail(10))


if __name__ == "__main__":
    main()
