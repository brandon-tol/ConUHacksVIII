import tkinter as tk
from tkinter import ttk
from combined import calculate_wait_time as predict_queue_duration
import combined

# Create a Tkinter window
window = tk.Tk()
window.title("Queue Duration Predictor")

# Labels
label_time = ttk.Label(window, text="Match Start Time (hh:mm:ss):")
label_time.grid(row=0, column=0, padx=10, pady=10, sticky="e")

label_weekday = ttk.Label(window, text="Day of Week:")
label_weekday.grid(row=1, column=0, padx=10, pady=10, sticky="e")

label_role = ttk.Label(window, text="Player Role:")
label_role.grid(row=2, column=0, padx=10, pady=10, sticky="e")

label_party_size = ttk.Label(window, text="Party Size:")
label_party_size.grid(row=3, column=0, padx=10, pady=10, sticky="e")

label_server = ttk.Label(window, text="Server Name:")
label_server.grid(row=4, column=0, padx=10, pady=10, sticky="e")

label_platform = ttk.Label(window, text="Platform:")
label_platform.grid(row=5, column=0, padx=10, pady=10, sticky="e")

label_outcome = ttk.Label(window, text="Matchmaking Outcome:")
label_outcome.grid(row=6, column=0, padx=10, pady=10, sticky="e")

# Entry widgets and Comboboxes
entry_time = ttk.Entry(window)
entry_time.grid(row=0, column=1, padx=10, pady=10)

combo_weekday = ttk.Combobox(window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
combo_weekday.grid(row=1, column=1, padx=10, pady=10)
combo_weekday.set("Monday")

combo_role = ttk.Combobox(window, values=["killer", "survivor"])
combo_role.grid(row=2, column=1, padx=10, pady=10)
combo_role.set("survivor")

entry_party_size = ttk.Entry(window)
entry_party_size.grid(row=3, column=1, padx=10, pady=10)

combo_server = ttk.Combobox(window, values=["AP-SOUTHEAST-1", "AP-SOUTHEAST-2", "US-WEST-1", "US-WEST-2",
                                            "EU-CENTRAL-1", "EU-CENTRAL-2", "US-EAST-1", "US-EAST-2"])
combo_server.grid(row=4, column=1, padx=10, pady=10)
combo_server.set("US-WEST-1")

combo_platform = ttk.Combobox(window, values=["xsx", "cgs", "ps5", "steam"])
combo_platform.grid(row=5, column=1, padx=10, pady=10)
combo_platform.set("steam")

combo_outcome = ttk.Combobox(window, values=["played_cancelled", "success"])
combo_outcome.grid(row=6, column=1, padx=10, pady=10)
combo_outcome.set("success")

# Entry widget for MMR_GROUP_DECILE
label_mmr = ttk.Label(window, text="MMR Group Decile:")
label_mmr.grid(row=7, column=0, padx=10, pady=10, sticky="e")

entry_mmr = ttk.Entry(window)
entry_mmr.grid(row=7, column=1, padx=10, pady=10)

predict_with_values = lambda : result_label.configure(text=predict_queue_duration(combined.timeToInt(entry_time.get()), combined.Day.fromStr(combo_weekday.get()), combo_role.get() == "killer", int(entry_party_size.get()), combined.Server(combo_server.get().upper()), combined.Platform(combo_platform.get().upper()), combined.MatchmakingOutcome(combo_outcome.get().upper()), int(entry_mmr.get()), None))

# Button to trigger prediction
predict_button = ttk.Button(window, text="Predict", command=predict_with_values)
predict_button.grid(row=8, column=0, columnspan=2, pady=10)

# Label to display prediction result
result_label = ttk.Label(window, text="")
result_label.grid(row=9, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
