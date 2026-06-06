"""
betPawa Virtual Sports — Entry point for both local and Render deployment.

Local:  python run.py
Render: gunicorn run:app (uses PORT env var automatically)
"""
import os, sys, logging
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from app import app, seed
from db import init_db
from match_engine import start_scheduler, create_next_matchday

# ── 1. Ensure schema exists (safe to run multiple times) ──────────────────
log.info("Initializing database schema...")
init_db(app)
log.info("Schema OK.")

# ── 2. Seed admin + demo users + first matchdays ──────────────────────────
log.info("Seeding default data...")
with app.app_context():
    try:
        seed()
        log.info("Seed OK.")
    except Exception as e:
        log.error(f"Seed error (non-fatal): {e}")

# ── 3. Start background scheduler (creates + starts matches) ──────────────
log.info("Starting match scheduler...")
start_scheduler(app)
log.info("Scheduler started.")

# ── 4. Local dev server ────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*56}")
    print(f"  betPawa Virtual Sports → http://localhost:{port}")
    print(f"  Admin : admin / admin123  →  /admin")
    print(f"  Demo  : demo  / demo123")
    print(f"{'='*56}\n")
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
