import streamlit as st
import pandas as pd
import requests
import time

def get_server_data(place_id):
    url = f"https://games.roblox.com/v1/games/{place_id}/servers/Public?limit=100"
    return requests.get(url).json().get("data", [])

def get_filtered_servers(place_id, max_ping=9999, max_current_players=10):
    servers = get_server_data(place_id)
    filtered = []
    for server in servers:
        ping = server.get("ping")
        current_players = server.get("playing", 0)
        max_players_server = server.get("maxPlayers", 0)
        job_id = server.get("id")

        if (ping is None or ping <= max_ping) and current_players <= max_current_players:
            filtered.append({
                "Job ID": f"roblox://placeId={place_id}&serverId={job_id}",
                "Ping (ms)": ping if ping is not None else "Unknown",
                "Players": current_players,
                "Max Capacity": max_players_server
            })
    return filtered


st.set_page_config(page_title="Ro-Live Scanner", layout="wide")
st.title("🎫 Ro-Live Server Scanner")

place_id = st.text_input("Place ID", value="123456789")
ping_threshold = st.number_input("Max Ping (ms)", min_value=0, value=300)
player_threshold = st.number_input("Max Players", min_value=0, value=10)
refresh_rate = st.number_input("Refresh every (seconds)", min_value=5, value=30)
start_loop = st.checkbox("Start Scanning")

if start_loop and place_id:
    placeholder = st.empty()
    while start_loop:
        with placeholder.container():
            st.info("Scanning for good servers...")
            filtered_servers = get_filtered_servers(int(place_id), int(ping_threshold), int(player_threshold))
            if filtered_servers:
                st.success(f"Found {len(filtered_servers)} good servers!")
                st.dataframe(pd.DataFrame(filtered_servers))
            else:
                st.warning("No good servers found at this moment.")
        time.sleep(refresh_rate)
