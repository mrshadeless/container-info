from flask import Flask
import socket
import os
import requests

app = Flask(__name__)

@app.route("/")
def container_info():
    hostname = os.environ.get("HOSTNAME", "Unavailable")
    ip_address = "Unavailable"

    # Try ECS Metadata v4
    try:
        metadata_uri = os.environ.get("ECS_CONTAINER_METADATA_URI_V4")
        if metadata_uri:
            metadata = requests.get(f"{metadata_uri}/task").json()
            ip_address = metadata["Containers"][0]["Networks"][0]["IPv4Addresses"][0]
    except Exception as e:
        ip_address = f"Error: {e}"

    # Get env variables safely
    env_vars = os.environ
    env_string = ""
    for k, v in env_vars.items():
        try:
            env_string += f"{k}: {v}\n"
        except Exception as e:
            env_string += f"{k}: <Error: {e}>\n"

    return f"""
    <h1>Container Information</h1>
    <ul>
        <li><strong>Hostname:</strong> {hostname}</li>
        <li><strong>IP Address:</strong> {ip_address}</li>
        <li><strong>Environment Variables:</strong><br>
            <pre>{env_string}</pre>
        </li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
