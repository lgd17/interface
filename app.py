import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)
BASE = os.getenv("SPORTS_API_BASE_URL","https://v2.football.sportsapipro.com").rstrip("/")
KEY = os.getenv("SPORTS_API_KEY","")
TIMEOUT = int(os.getenv("SPORTS_API_TIMEOUT","20"))

def upstream(path, params=None):
    if not KEY:
        return None, ("SPORTS_API_KEY n'est pas configurée sur Render.",503)
    try:
        r=requests.get(BASE+path,headers={"x-api-key":KEY,"Accept":"application/json"},
                       params=params,timeout=TIMEOUT)
    except requests.Timeout:
        return None,("Délai dépassé lors de l'appel API.",504)
    except requests.RequestException:
        app.logger.exception("Erreur SportsAPI")
        return None,("Impossible de joindre SportsAPI Pro.",502)
    try:
        data=r.json()
    except ValueError:
        return {"upstream_status":r.status_code,"response_preview":r.text[:1500]},(
            None if r.ok else (f"Erreur HTTP fournisseur : {r.status_code}",502))
    if not r.ok:
        return {"upstream_status":r.status_code,"upstream_response":data},(
            f"Erreur HTTP fournisseur : {r.status_code}",502)
    return data,None

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify(status="ok",service="Interface Pari Demo",api_key_configured=bool(KEY))

@app.get("/api/team-search")
def team_search():
    q=(request.args.get("q") or "").strip()
    if not q or len(q)>100:
        return jsonify(error="Indique un nom d'équipe valide dans le paramètre q."),400
    data,error=upstream("/api/search",{"q":q})
    if error:
        message,status=error
        return jsonify(error=message,details=data),status
    return jsonify(data)

import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request, Response
import requests

app = Flask(__name__)

BASE = os.getenv(
    "SPORTS_API_BASE_URL",
    "https://v2.football.sportsapipro.com"
).rstrip("/")

KEY = os.getenv("SPORTS_API_KEY", "")
TIMEOUT = int(os.getenv("SPORTS_API_TIMEOUT", "20"))


def upstream(path, params=None):
    if not KEY:
        return None, ("SPORTS_API_KEY n'est pas configurée sur Render.", 503)

    try:
        r = requests.get(
            BASE + path,
            headers={
                "x-api-key": KEY,
                "Accept": "application/json"
            },
            params=params,
            timeout=TIMEOUT
        )
    except requests.Timeout:
        return None, ("Délai dépassé lors de l'appel API.", 504)
    except requests.RequestException:
        app.logger.exception("Erreur SportsAPI")
        return None, ("Impossible de joindre SportsAPI Pro.", 502)

    try:
        data = r.json()
    except ValueError:
        data = {
            "upstream_status": r.status_code,
            "response_preview": r.text[:1500]
        }
        if not r.ok:
            return data, (f"Erreur HTTP fournisseur : {r.status_code}", 502)

    if not r.ok:
        return data, (f"Erreur HTTP fournisseur : {r.status_code}", 502)

    return data, None


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        service="Interface Pari Demo",
        api_key_configured=bool(KEY)
    )


@app.get("/api/team-search")
def team_search():
    q = (request.args.get("q") or "").strip()

    if not q or len(q) > 100:
        return jsonify(
            error="Indique un nom d'équipe valide dans le paramètre q."
        ), 400

    data, error = upstream("/api/search", {"q": q})

    if error:
        message, status = error
        return jsonify(error=message, details=data), status

    return jsonify(data)


@app.get("/api/schedule/<date_value>")
def schedule(date_value):
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        return jsonify(
            error="Date attendue au format YYYY-MM-DD."
        ), 400

    data, error = upstream("/api/schedule/" + date_value)

    if error:
        message, status = error
        return jsonify(error=message, details=data), status

    return jsonify(data)


@app.get("/api/team-logo/<int:team_id>")
def team_logo(team_id):
    if not KEY:
        return jsonify(
            error="SPORTS_API_KEY n'est pas configurée sur Render."
        ), 503

    try:
        response = requests.get(
            f"{BASE}/images/teams/{team_id}",
            headers={"x-api-key": KEY},
            timeout=TIMEOUT
        )

        if response.status_code != 200:
            return jsonify(
                error="Logo indisponible",
                upstream_status=response.status_code
            ), response.status_code

        return Response(
            response.content,
            content_type=response.headers.get(
                "Content-Type", "image/png"
            ),
            headers={"Cache-Control": "public, max-age=86400"}
        )

    except requests.RequestException:
        app.logger.exception("Erreur récupération logo")
        return jsonify(
            error="Service des images indisponible."
        ), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )

.headers.get(
                "Content-Type", "image/png"
            ),
            headers={"Cache-Control": "public, max-age=86400"}
        )

    except requests.RequestException:
        return jsonify({"error": "Image service unavailable
    "}), 502
