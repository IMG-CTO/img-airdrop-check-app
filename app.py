from shiny import App, ui, render
import pandas as pd

# Load data for each epoch
epoch1 = pd.read_csv("epoch1_FINAL.csv")
epoch2 = pd.read_csv("epoch2_FINAL.csv")
epoch3 = pd.read_csv("epoch3_FINAL.csv")

# Helper function to generate result messages
def generate_message(df, wallet):
    row = df[df["wallet"] == wallet]
    if not row.empty:
        data = row.iloc[0]
        if data["reward_sent"] == "YES":
            return (
                f"Wallet address {wallet} received {data['solana_amount']} Solana on {data['date_sent']}, "
                f"based on the snapshot captured on {data['snapshot_date']}."
            )
        else:
            return (
                f"Wallet address {wallet} was impacted by limitations in the manual IMG Airdrop process "
                f"for the {data['snapshot_date']} snapshot. This wallet is expected to receive {data['solana_amount']} Solana. "
                f"Please take a screenshot of this message and send it to the IMG team in the Looking For Rewards channel of the official IMG Telegram. "
                f"Please allow up to 2 calendar days to receive a response."
            )
    else:
        return (
            f"Wallet address {wallet} was not found during the {df['snapshot_date'].iloc[0]} snapshot process. "
            f"It did not contain IMG at that point in time, or received rewards in an earlier distribution."
        )

# UI
app_ui = ui.page_fluid(
    ui.h2("IMG Airdrop Checker"),
    ui.layout_columns(

        # ---------------- Epoch 1 ----------------
        ui.panel_well(
            ui.h4("Epoch 1: 05/24/25 through 06/27/25"),
            ui.input_text("wallet1", "Enter Wallet Address"),
            ui.div(
                ui.output_text("result1"),
                style=(
                    "white-space: pre-wrap; word-wrap: break-word; "
                    "background-color: #f8f9fa; padding: 10px; border-radius: 4px;"
                ),
            ),
        ),

        # ---------------- Epoch 2 ----------------
        ui.panel_well(
            ui.h4("Epoch 2: 06/27/25 through 06/30/25"),
            ui.input_text("wallet2", "Enter Wallet Address"),
            ui.div(
                ui.output_text("result2"),
                style=(
                    "white-space: pre-wrap; word-wrap: break-word; "
                    "background-color: #f8f9fa; padding: 10px; border-radius: 4px;"
                ),
            ),
        ),

        # ---------------- Epoch 3 ----------------
        ui.panel_well(
            ui.h4("Epoch 3: 06/30/25 through 07/06/25"),
            ui.input_text("wallet3", "Enter Wallet Address"),
            ui.div(
                ui.output_text("result3"),
                style=(
                    "white-space: pre-wrap; word-wrap: break-word; "
                    "background-color: #f8f9fa; padding: 10px; border-radius: 4px;"
                ),
            ),
        ),
    )
)

# Server
def server(input, output, session):
    @output
    @render.text
    def result1():
        if input.wallet1():
            return generate_message(epoch1, input.wallet1())
        return ""

    @output
    @render.text
    def result2():
        if input.wallet2():
            return generate_message(epoch2, input.wallet2())
        return ""

    @output
    @render.text
    def result3():
        if input.wallet3():
            return generate_message(epoch3, input.wallet3())
        return ""

# App
app = App(app_ui, server)
