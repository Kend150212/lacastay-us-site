#!/usr/bin/env python3
"""
LacaStay US-site app mockups — rebuilt 2026-10-12 per Ken's request.
Granular live-dashboard philosophy: ONE DATA object (believable placeholder
numbers) drives every mockup; change data here, never in the markup.
Outputs (exact pixels):
  assets/img/app-dashboard.png          1080x1920  (overwrite)
  assets/img/app-calendar.png           1080x1920  (new)
  assets/img/app-dashboard-desktop.png  1600x1000  (new)
  assets/img/app-calendar-desktop.png   1600x1000  (new)
  assets/img/app-chat.png                 1080x1920  (new)
  assets/img/app-staff-checkin.png        1080x1920  (new)
"""
import os
from pathlib import Path
from PIL import Image

ROOT = Path("/home/hatch/workspace/lacastay-us-site")
IMG = ROOT / "assets" / "img"
MOCK = ROOT / "mockups"
MOCK.mkdir(exist_ok=True)

# ---------------------------------------------------------------- DATA ----
# All believable placeholder numbers live here. Same numbers across phone +
# desktop so the "product" feels consistent. Source names: demo-bookings.json
DATA = {
    "greeting": "Hello, LacaStay Admin",
    "location": "Laca Stay",
    "date_label": "Mon, Oct 12",
    "stats": [
        {"icon": "dollar", "tile": "orange", "value": "$1,284", "label": "Revenue"},
        {"icon": "calendar", "tile": "orange", "value": "23", "label": "Bookings"},
        {"icon": "check", "tile": "green", "value": "14", "label": "Completed"},
        {"icon": "clock", "tile": "blue", "value": "9", "label": "Upcoming"},
    ],
    # healthy week, no zero bars (believable placeholder numbers)
    "week": [
        {"day": "S", "value": 820}, {"day": "M", "value": 965},
        {"day": "T", "value": 1140}, {"day": "W", "value": 890},
        {"day": "T", "value": 1284}, {"day": "F", "value": 1055},
        {"day": "S", "value": 740},
    ],
    "upcoming": [
        {"name": "Jessica Miller", "service": "Gel Manicure", "tech": "Anna",
         "time": "2:30 PM", "badge": "Confirmed"},
        {"name": "Ashley Thompson", "service": "Spa Pedicure", "tech": "Linda",
         "time": "3:00 PM", "badge": "Confirmed"},
        {"name": "Megan Brown", "service": "Gel Manicure + Nail Art", "tech": "Mai",
         "time": "3:30 PM", "badge": "Pending"},
        {"name": "Lauren Garcia", "service": "Spa Pedicure", "tech": "Anna",
         "time": "4:00 PM", "badge": "Confirmed"},
        {"name": "Nicole Martinez", "service": "Acrylic Fill", "tech": "Linda",
         "time": "4:30 PM", "badge": "Confirmed"},
    ],
    # week calendar: tech -> color, bookings spread Mon-Fri 9AM-7PM
    "techs": {"Anna": "#F97316", "Linda": "#3B82F6", "Mai": "#14B8A6"},
    "week_cal": {
        "Mon 12": [
            ("9:00", "Jessica Miller", "Gel Mani", "Anna"),
            ("9:00", "Ashley Thompson", "Spa Pedi", "Linda"),
            ("9:30", "Brittany Davis", "Acrylic Set", "Mai"),
            ("10:00", "Samantha Wilson", "Gel Fill", "Anna"),
            ("11:00", "Lauren Garcia", "Spa Pedi", "Anna"),
            ("12:30", "Rachel Kim", "Pedi + Paraffin", "Anna"),
            ("2:00", "Danielle Lewis", "Mani + Pedi", "Anna"),
            ("3:30", "Christina Allen", "Acrylic Set", "Anna"),
            ("5:00", "Courtney Wright", "Manicure", "Anna"),
        ],
        "Tue 13": [
            ("9:00", "Hannah Lee", "Gel Mani", "Mai"),
            ("10:15", "Emily Johnson", "Dip Powder", "Linda"),
            ("11:30", "Nicole Martinez", "Acrylic Fill", "Linda"),
            ("1:00", "Amanda White", "Full Set + Design", "Linda"),
            ("2:30", "Kimberly Walker", "Dip Powder", "Linda"),
            ("4:00", "Tiffany Young", "Spa Pedi", "Linda"),
            ("5:30", "Amber Scott", "Pedicure", "Linda"),
        ],
        "Wed 14": [
            ("9:30", "Olivia Parker", "Gel Mani", "Mai"),
            ("10:30", "Megan Brown", "Gel Mani + Art", "Mai"),
            ("12:00", "Sophia Bennett", "Dip Powder", "Mai"),
            ("1:30", "Stephanie Clark", "Gel Pedi", "Mai"),
            ("3:00", "Melissa Hall", "Gel Mani", "Mai"),
            ("4:30", "Vanessa King", "Gel Fill", "Mai"),
            ("6:00", "Jamie Torres", "Gel Mani", "Mai"),
        ],
        "Thu 15": [
            ("9:00", "Grace Nelson", "Spa Pedi", "Linda"),
            ("10:00", "Chloe Adams", "Gel Fill", "Anna"),
            ("11:00", "Lily Carter", "Acrylic Set", "Mai"),
            ("12:00", "Ella Mitchell", "Dip Powder", "Linda"),
            ("2:00", "Ava Roberts", "Gel Mani", "Anna"),
            ("3:30", "Mia Turner", "Spa Pedi", "Linda"),
            ("5:00", "Zoe Phillips", "Gel Mani", "Mai"),
        ],
        "Fri 16": [
            ("9:00", "Nora Campbell", "Full Set", "Anna"),
            ("10:30", "Ruby Evans", "Gel Mani + Art", "Mai"),
            ("12:00", "Stella Edwards", "Spa Pedi", "Linda"),
            ("1:30", "Hazel Collins", "Dip Powder", "Anna"),
            ("3:00", "Violet Stewart", "Acrylic Fill", "Mai"),
            ("4:30", "Aurora Morris", "Gel Pedi", "Linda"),
            ("6:00", "Luna Rogers", "Gel Mani", "Anna"),
        ],
    },
    "ai_calls": [
        {"caller": "(703) 555-0142", "result": "Booked · Gel Mani · Thu 2:00 PM", "time": "1:12 PM"},
        {"caller": "(571) 555-0188", "result": "Booked · Spa Pedi · Fri 10:30 AM", "time": "12:47 PM"},
        {"caller": "(202) 555-0119", "result": "Rescheduled · Dip Powder", "time": "11:05 AM"},
        {"caller": "(703) 555-0164", "result": "Answered · pricing question", "time": "10:31 AM"},
    ],
}
HOURS = ["9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p"]


def t2row(t):
    """'2:30 PM' or '14:00'/'2:00' (24h-ish) -> grid row offset in hours from 9am."""
    parts = t.split(" ")
    hm = parts[0]
    ap = parts[1] if len(parts) > 1 else None
    h, m = map(int, hm.split(":"))
    if ap:
        if ap == "PM" and h != 12:
            h += 12
    else:
        # bare hour in week calendar = daytime shop hours: 9-11 AM, 12-6 PM
        if h < 9:
            h += 12
    return (h + m / 60) - 9


# ------------------------------------------------------------- owl crop ----
def make_owl():
    logo = Image.open(IMG / "lacastay-logo.png").convert("RGBA")
    owl = logo.crop((0, 0, 205, 200))
    bbox = owl.getbbox()
    owl = owl.crop(bbox)
    out = MOCK / "owl.png"
    owl.save(out)
    return out.name


# --------------------------------------------------------------- icons ----
# Inline Lucide-style line icons (no emoji anywhere)
ICONS = {
    "dollar": '<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "chat": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "more": '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "chevl": '<polyline points="15 18 9 12 15 6"/>',
    "chevr": '<polyline points="9 18 15 12 9 6"/>',
    "chevd": '<polyline points="6 9 12 15 18 9"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
}


def icon(name, size=24, color="currentColor", sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


FONT = ("<link rel='preconnect' href='https://fonts.googleapis.com'>"
        "<link href='https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap' rel='stylesheet'>")

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Nunito',system-ui,-apple-system,'Segoe UI',sans-serif;color:#1F2937;-webkit-font-smoothing:antialiased}
.page{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;background:linear-gradient(160deg,#FDF6EA 0%,#FBEFD9 60%,#F9E4C6 100%);position:relative;overflow:hidden}
.blob{position:absolute;border-radius:50%;background:#F6DCB4;opacity:.55;filter:blur(2px)}
h1.hero{font-size:62px;font-weight:900;color:#7A2E0E;letter-spacing:-.5px;margin:56px 0 34px;text-align:center}
.phone{width:830px;height:1480px;background:#0B0B0C;border-radius:96px;padding:30px;box-shadow:0 40px 90px rgba(120,60,10,.28), inset 0 0 0 3px #2a2a2c}
.screen{width:100%;height:100%;background:#F8F9FB;border-radius:68px;overflow:hidden;position:relative;display:flex;flex-direction:column}
.notch{position:absolute;top:26px;left:50%;transform:translateX(-50%);width:150px;height:34px;background:#0B0B0C;border-radius:20px;z-index:5}
.statusbar{display:flex;justify-content:space-between;align-items:center;padding:20px 44px 6px;font-weight:800;font-size:23px}
.sb-icons{display:flex;gap:10px;align-items:center}
"""

APP_CSS = """
.apphead{padding:6px 32px 0}
.greet{font-size:20px;color:#6B7280;font-weight:600}
.apptitle{font-size:42px;font-weight:900;letter-spacing:-.5px;margin:0 0 10px}
.locpill{display:inline-flex;align-items:center;gap:8px;background:#FFF1E2;color:#9A3412;font-weight:800;font-size:19px;padding:8px 20px;border-radius:999px}
.daterow{display:flex;align-items:center;justify-content:center;gap:14px;margin:12px 0 2px}
.datebtn{width:46px;height:46px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.datepill{display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:10px 20px;font-weight:800;font-size:21px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.todaypill{background:#FFF1E2;color:#C2410C;font-weight:800;font-size:19px;padding:10px 20px;border-radius:999px}
.statgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:12px 28px 0}
.statcard{background:#fff;border-radius:24px;padding:16px 20px;box-shadow:0 3px 14px rgba(0,0,0,.05)}
.tile{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}
.tile.orange{background:#FFF1E2}.tile.green{background:#DCFCE7}.tile.blue{background:#DBEAFE}
.tile.orange svg{stroke:#F97316}.tile.green svg{stroke:#16A34A}.tile.blue svg{stroke:#2563EB}
.statval{font-size:38px;font-weight:900;letter-spacing:-.5px}
.statlabel{font-size:19px;color:#6B7280;font-weight:600}
.chartcard{background:#fff;border-radius:24px;margin:10px 28px 0;padding:18px 22px 10px;box-shadow:0 3px 14px rgba(0,0,0,.05)}
.charttitle{font-size:23px;font-weight:800;display:flex;align-items:center;gap:10px;margin-bottom:16px}
.bars{display:flex;align-items:flex-end;justify-content:space-between;height:168px;padding:0 6px}
.barcol{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1}
.barval{font-size:15px;color:#9CA3AF;font-weight:700}
.bar{width:42px;border-radius:10px;background:linear-gradient(180deg,#FB923C,#F97316);min-height:12px}
.bar.max{background:linear-gradient(180deg,#F97316,#EA580C);box-shadow:0 6px 16px rgba(249,115,22,.35)}
.barday{font-size:17px;color:#6B7280;font-weight:700}
.apptsec{padding:8px 30px 0}
.apptsec h3{font-size:27px;font-weight:900;margin-bottom:10px}
.apptrow{display:flex;align-items:center;gap:14px;background:#fff;border-radius:20px;padding:12px 16px;margin-bottom:8px;box-shadow:0 3px 12px rgba(0,0,0,.05)}
.avatar{width:56px;height:56px;border-radius:50%;background:#FFF1E2;color:#C2410C;font-weight:900;font-size:23px;display:flex;align-items:center;justify-content:center;flex:none}
.apptinfo{flex:1;min-width:0}
.apptname{font-size:21px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.apptsub{font-size:17px;color:#6B7280;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.apptright{text-align:right;flex:none}
.appttime{font-size:19px;font-weight:800}
.badge{display:inline-block;font-size:14px;font-weight:800;padding:4px 12px;border-radius:999px;margin-top:4px}
.badge.ok{background:#DCFCE7;color:#15803D}
.badge.pend{background:#FEF3C7;color:#B45309}
.tabbar{margin-top:auto;background:#fff;border-top:1px solid #EEF0F3;display:flex;justify-content:space-around;align-items:flex-end;padding:10px 8px 22px}
.tab{display:flex;flex-direction:column;align-items:center;gap:4px;color:#9CA3AF;font-size:16px;font-weight:700}
.tab.active{color:#F97316}
.fab{width:84px;height:84px;border-radius:50%;background:linear-gradient(180deg,#FB923C,#F97316);display:flex;align-items:center;justify-content:center;margin-top:-46px;box-shadow:0 12px 28px rgba(249,115,22,.45)}
"""

# ------------------------------------------------- phone dashboard ----
def phone_dashboard():
    d = DATA
    stats = ""
    tcol = {"orange": None, "green": None, "blue": None}
    for s in d["stats"]:
        stats += f"""
        <div class="statcard">
          <div class="tile {s['tile']}">{icon(s['icon'], 32, sw=2.2)}</div>
          <div class="statval">{s['value']}</div>
          <div class="statlabel">{s['label']}</div>
        </div>"""
    vmax = max(b["value"] for b in d["week"])
    bars = ""
    for b in d["week"]:
        h = int(100 * b["value"] / vmax) + 10
        cls = "bar max" if b["value"] == vmax else "bar"
        bars += (f'<div class="barcol"><div class="barval">${b["value"]:,}</div>'
                 f'<div class="{cls}" style="height:{h}px"></div>'
                 f'<div class="barday">{b["day"]}</div></div>')
    rows = ""
    for a in d["upcoming"][:4]:
        init = "".join(w[0] for w in a["name"].split()[:2])
        bc = "ok" if a["badge"] == "Confirmed" else "pend"
        rows += f"""
        <div class="apptrow">
          <div class="avatar">{init}</div>
          <div class="apptinfo">
            <div class="apptname">{a['name']}</div>
            <div class="apptsub">{a['service']} · {a['tech']}</div>
          </div>
          <div class="apptright">
            <div class="appttime">{a['time']}</div>
            <span class="badge {bc}">{a['badge']}</span>
          </div>
        </div>"""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}</style></head>
<body><div class="page" style="width:1080px;height:1920px">
<div class="blob" style="width:300px;height:300px;left:-100px;bottom:60px"></div>
<div class="blob" style="width:280px;height:280px;right:-90px;bottom:300px"></div>
<h1 class="hero">Your business at a glance</h1>
<div class="phone"><div class="screen"><div class="notch"></div>
  <div class="statusbar"><span>15:05</span>
    <div class="sb-icons">
      <svg width="34" height="22" viewBox="0 0 34 22" fill="#111"><rect x="0" y="12" width="5" height="10" rx="1"/><rect x="8" y="8" width="5" height="14" rx="1"/><rect x="16" y="4" width="5" height="18" rx="1"/><rect x="24" y="0" width="5" height="22" rx="1" opacity=".35"/></svg>
      <svg width="30" height="22" viewBox="0 0 30 22" fill="none" stroke="#111" stroke-width="2.4"><path d="M4 8a15 15 0 0 1 22 0M8 12.5a10 10 0 0 1 14 0M12 17a5 5 0 0 1 6 0"/><circle cx="15" cy="20" r="1.6" fill="#111" stroke="none"/></svg>
      <svg width="44" height="22" viewBox="0 0 44 22"><rect x="1" y="1" width="36" height="20" rx="6" fill="none" stroke="#111" stroke-width="2" opacity=".4"/><rect x="4" y="4" width="24" height="14" rx="3.5" fill="#111"/><rect x="39" y="7" width="4" height="8" rx="2" fill="#111" opacity=".4"/></svg>
    </div></div>
  <div class="apphead">
    <div class="greet">{d['greeting']}</div>
    <div class="apptitle">Today's overview</div>
    <span class="locpill">{icon('pin', 22, '#C2410C', 2.2)} {d['location']} {icon('chevd', 18, '#C2410C', 2.5)}</span>
    <div class="daterow">
      <div class="datebtn">{icon('chevl', 24, '#374151', 2.4)}</div>
      <div class="datepill">{icon('calendar', 24, '#F97316', 2.2)} {d['date_label']} {icon('chevd', 18, '#9CA3AF', 2.5)}</div>
      <div class="datebtn">{icon('chevr', 24, '#374151', 2.4)}</div>
      <div class="todaypill">Today</div>
    </div>
  </div>
  <div class="statgrid">{stats}</div>
  <div class="chartcard">
    <div class="charttitle">{icon('zap', 26, '#F97316', 2.2)} Revenue — last 7 days</div>
    <div class="bars">{bars}</div>
  </div>
  <div class="apptsec"><h3>Upcoming appointments</h3>{rows}</div>
  <div class="tabbar">
    <div class="tab active">{icon('home', 34, '#F97316', 2.2)}<span>Home</span></div>
    <div class="tab">{icon('calendar', 34, sw=2)}<span>Appointments</span></div>
    <div class="fab">{icon('plus', 44, '#fff', 2.6)}</div>
    <div class="tab">{icon('chat', 34, sw=2)}<span>Connect</span></div>
    <div class="tab">{icon('more', 34, sw=2)}<span>More</span></div>
  </div>
</div></div>
<div style="height:36px"></div>
<img src="owl.png" style="height:150px" alt="LacaStay owl">
</div></body></html>"""


# -------------------------------------------------- phone calendar ----
CAL_CSS = """
.calhead{padding:8px 34px 0}
.caltitle{font-size:46px;font-weight:900;margin:2px 0 14px}
.weekstrip{display:flex;justify-content:space-between;background:#fff;border-radius:26px;padding:16px 12px;margin:6px 30px 0;box-shadow:0 3px 14px rgba(0,0,0,.05)}
.wday{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;padding:10px 0;border-radius:16px}
.wday.today{background:#FFF1E2}
.wd{font-size:19px;font-weight:700;color:#9CA3AF}
.wn{font-size:25px;font-weight:900}
.wday.today .wn{color:#C2410C}
.techrow{display:flex;gap:12px;padding:16px 30px 0;align-items:center}
.techpill{display:flex;align-items:center;gap:8px;font-size:20px;font-weight:800;padding:10px 20px;border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.dot{width:16px;height:16px;border-radius:50%}
.calgrid{flex:1;margin:16px 30px 0;background:#fff;border-radius:26px;box-shadow:0 3px 14px rgba(0,0,0,.05);overflow:hidden;display:flex}
.gutter{width:64px;flex:none;background:#FAFAFB}
.ghour{font-size:15px;color:#9CA3AF;font-weight:700;text-align:right;padding-right:8px;height:86px;transform:translateY(-8px)}
.daycol{flex:1;border-left:1px solid #F1F2F4;position:relative}
.dayname{text-align:center;font-size:17px;font-weight:800;color:#6B7280;padding:10px 0;border-bottom:1px solid #F1F2F4;background:#FAFAFB}
.bwrap{position:relative;height:860px}
.blk{position:absolute;left:5px;right:5px;border-radius:12px;padding:8px 9px;color:#fff;font-size:15px;font-weight:800;line-height:1.25;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.blk small{display:block;font-weight:700;font-size:12.5px;opacity:.92}
"""


def phone_calendar():
    d = DATA
    days = list(d["week_cal"].keys())
    dates = ["12", "13", "14", "15", "16", "17", "18"]
    dnames = ["M", "T", "W", "T", "F", "S", "S"]
    strip = ""
    for i, (dn, dt) in enumerate(zip(dnames, dates)):
        cls = "wday today" if i == 0 else "wday"
        strip += f'<div class="{cls}"><div class="wd">{dn}</div><div class="wn">{dt}</div></div>'
    techs = "".join(
        f'<div class="techpill"><span class="dot" style="background:{c}"></span>{t}</div>'
        for t, c in d["techs"].items())
    gutter = "".join(f'<div class="ghour">{h}</div>' for h in HOURS)
    cols = ""
    for day in days[:5]:
        blks = ""
        for t, name, svc, tech in d["week_cal"][day]:
            top = int(t2row(t) * 86)
            first = name.split()[0]
            blks += (f'<div class="blk" style="top:{top}px;height:76px;background:{d["techs"][tech]}">'
                     f'{t}<small>{first} · {svc}</small></div>')
        cols += (f'<div class="daycol"><div class="dayname">{day.split()[0]}</div>'
                 f'<div class="bwrap">{blks}</div></div>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}{CAL_CSS}</style></head>
<body><div class="page" style="width:1080px;height:1920px">
<div class="blob" style="width:300px;height:300px;left:-100px;bottom:60px"></div>
<div class="blob" style="width:280px;height:280px;right:-90px;bottom:300px"></div>
<h1 class="hero">Your week, fully booked</h1>
<div class="phone"><div class="screen"><div class="notch"></div>
  <div class="statusbar"><span>15:05</span>
    <div class="sb-icons">
      <svg width="34" height="22" viewBox="0 0 34 22" fill="#111"><rect x="0" y="12" width="5" height="10" rx="1"/><rect x="8" y="8" width="5" height="14" rx="1"/><rect x="16" y="4" width="5" height="18" rx="1"/><rect x="24" y="0" width="5" height="22" rx="1" opacity=".35"/></svg>
      <svg width="44" height="22" viewBox="0 0 44 22"><rect x="1" y="1" width="36" height="20" rx="6" fill="none" stroke="#111" stroke-width="2" opacity=".4"/><rect x="4" y="4" width="24" height="14" rx="3.5" fill="#111"/><rect x="39" y="7" width="4" height="8" rx="2" fill="#111" opacity=".4"/></svg>
    </div></div>
  <div class="calhead">
    <div class="greet">{DATA['greeting']}</div>
    <div class="caltitle">Calendar</div>
  </div>
  <div class="weekstrip">{strip}</div>
  <div class="techrow">{techs}
    <div class="todaypill" style="margin-left:auto">+ New</div></div>
  <div class="calgrid"><div class="gutter" style="padding-top:48px">{gutter}</div>{cols}</div>
  <div class="tabbar">
    <div class="tab">{icon('home', 34, sw=2)}<span>Home</span></div>
    <div class="tab active">{icon('calendar', 34, '#F97316', 2.2)}<span>Appointments</span></div>
    <div class="fab">{icon('plus', 44, '#fff', 2.6)}</div>
    <div class="tab">{icon('chat', 34, sw=2)}<span>Connect</span></div>
    <div class="tab">{icon('more', 34, sw=2)}<span>More</span></div>
  </div>
</div></div>
<div style="height:36px"></div>
<img src="owl.png" style="height:150px" alt="LacaStay owl">
</div></body></html>"""


# ------------------------------------------------- desktop shared ----
DESK_CSS = """
.dpage{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(140deg,#1E293B 0%,#334155 55%,#7C2D12 130%);position:relative;overflow:hidden}
.dblob{position:absolute;border-radius:50%;background:#F97316;opacity:.14;filter:blur(60px)}
.browser{width:1440px;height:880px;background:#F8F9FB;border-radius:22px;overflow:hidden;box-shadow:0 50px 120px rgba(0,0,0,.5);display:flex;flex-direction:column;z-index:2}
.chrome{background:#E8EAEE;display:flex;align-items:center;gap:14px;padding:14px 20px}
.tl{display:flex;gap:8px}
.tl span{width:15px;height:15px;border-radius:50%}
.urlbar{flex:1;background:#fff;border-radius:10px;padding:9px 18px;font-size:16px;font-weight:700;color:#6B7280;display:flex;align-items:center;gap:10px}
.dbody{flex:1;display:flex;min-height:0}
.sidebar{width:228px;background:#111827;color:#CBD5E1;display:flex;flex-direction:column;padding:22px 14px;flex:none}
.brand{display:flex;align-items:center;gap:10px;padding:4px 10px 20px}
.brand img{height:34px}
.brand b{color:#fff;font-size:20px;font-weight:900}
.navitem{display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:12px;font-size:16.5px;font-weight:700;margin-bottom:2px}
.navitem.active{background:#F97316;color:#fff}
.navitem svg{flex:none}
.sideuser{margin-top:auto;background:#1F2937;border-radius:14px;padding:12px 14px;display:flex;align-items:center;gap:10px}
.sideuser .avatar{width:44px;height:44px;font-size:17px}
.main{flex:1;padding:26px 30px;overflow:hidden;min-width:0}
.dhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.dhead h2{font-size:30px;font-weight:900}
.dhead p{font-size:15.5px;color:#6B7280;font-weight:600}
.dstats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px}
.dcard{background:#fff;border-radius:18px;padding:18px 20px;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.dval{font-size:34px;font-weight:900}
.dlabel{font-size:14.5px;color:#6B7280;font-weight:600}
.drow{display:flex;gap:16px}
.dchart{flex:1.6;background:#fff;border-radius:18px;padding:20px 22px 12px;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.dchart h4{font-size:18px;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.dbars{display:flex;align-items:flex-end;justify-content:space-between;height:190px}
.dbarcol{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1}
.dbar{width:52px;border-radius:10px;background:linear-gradient(180deg,#FB923C,#F97316)}
.dbar.max{background:linear-gradient(180deg,#F97316,#EA580C);box-shadow:0 6px 16px rgba(249,115,22,.35)}
.dbarval{font-size:13px;color:#9CA3AF;font-weight:700}
.dbarday{font-size:14px;color:#6B7280;font-weight:700}
.dside{flex:1;display:flex;flex-direction:column;gap:16px;min-width:0}
.dpanel{background:#fff;border-radius:18px;padding:18px 20px;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.dpanel h4{font-size:18px;font-weight:800;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.dappt{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid #F1F2F4}
.dappt:last-child{border:none}
.dappt .avatar{width:46px;height:46px;font-size:18px}
.dappt .apptname{font-size:16px}
.dappt .apptsub{font-size:13.5px}
.dappt .appttime{font-size:14.5px}
.callrow{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid #F1F2F4}
.callrow:last-child{border:none}
.callic{width:40px;height:40px;border-radius:12px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;flex:none}
.callrow b{font-size:15px}.callrow p{font-size:13.5px;color:#6B7280;font-weight:600}
.calltime{margin-left:auto;font-size:13px;color:#9CA3AF;font-weight:700;flex:none}
"""


def desktop_dashboard():
    d = DATA
    cards = ""
    for s in d["stats"]:
        cards += f"""<div class="dcard"><div class="tile {s['tile']}" style="width:46px;height:46px;border-radius:13px;margin-bottom:10px">{icon(s['icon'], 24, sw=2.2)}</div><div class="dval">{s['value']}</div><div class="dlabel">{s['label']} · today</div></div>"""
    vmax = max(b["value"] for b in d["week"])
    bars = ""
    for b in d["week"]:
        h = int(140 * b["value"] / vmax) + 10
        cls = "dbar max" if b["value"] == vmax else "dbar"
        bars += (f'<div class="dbarcol"><div class="dbarval">${b["value"]:,}</div>'
                 f'<div class="{cls}" style="height:{h}px"></div><div class="dbarday">{b["day"]}</div></div>')
    rows = ""
    for a in d["upcoming"][:4]:
        init = "".join(w[0] for w in a["name"].split()[:2])
        bc = "ok" if a["badge"] == "Confirmed" else "pend"
        rows += f"""<div class="dappt"><div class="avatar">{init}</div>
        <div class="apptinfo"><div class="apptname">{a['name']}</div>
        <div class="apptsub">{a['service']} · {a['tech']}</div></div>
        <div class="apptright"><div class="appttime">{a['time']}</div>
        <span class="badge {bc}" style="font-size:12px">{a['badge']}</span></div></div>"""
    calls = ""
    for c in d["ai_calls"]:
        calls += f"""<div class="callrow"><div class="callic">{icon('phone', 20, '#16A34A', 2.2)}</div>
        <div><b>{c['caller']}</b><p>{c['result']}</p></div><span class="calltime">{c['time']}</span></div>"""
    nav = "".join(
        f'<div class="navitem{" active" if n == "Dashboard" else ""}">{icon(ic, 20, sw=2)}<span>{n}</span></div>'
        for n, ic in [("Dashboard", "home"), ("Calendar", "calendar"), ("Appointments", "users"),
                      ("AI Calls", "phone"), ("Messages", "chat"), ("Reviews", "star"), ("Settings", "settings")])
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}{DESK_CSS}</style></head>
<body><div class="dpage" style="width:1600px;height:1000px">
<div class="dblob" style="width:600px;height:600px;left:-150px;top:-100px"></div>
<div class="dblob" style="width:500px;height:500px;right:-100px;bottom:-150px"></div>
<div class="browser">
  <div class="chrome"><div class="tl"><span style="background:#FF5F57"></span><span style="background:#FEBC2E"></span><span style="background:#28C840"></span></div>
  <div class="urlbar">{icon('globe', 16, '#9CA3AF', 2)} app.lacastay.com/dashboard</div></div>
  <div class="dbody">
    <div class="sidebar">
      <div class="brand"><img src="owl.png" alt=""><b>LacaStay</b></div>
      {nav}
      <div class="sideuser"><div class="avatar">LA</div><div><b style="color:#fff;font-size:15px">Laca Stay</b><p style="font-size:13px">Admin</p></div></div>
    </div>
    <div class="main">
      <div class="dhead"><div><h2>Today's overview</h2><p>Monday, October 12 · Laca Stay · Nail Salon</p></div>
      <div class="todaypill" style="font-size:15px">+ New booking</div></div>
      <div class="dstats">{cards}</div>
      <div class="drow">
        <div class="dchart"><h4>{icon('zap', 20, '#F97316', 2.2)} Revenue — last 7 days</h4><div class="dbars">{bars}</div></div>
        <div class="dside">
          <div class="dpanel"><h4>{icon('calendar', 20, '#F97316', 2.2)} Upcoming appointments</h4>{rows}</div>
          <div class="dpanel"><h4>{icon('phone', 20, '#16A34A', 2.2)} AI calls answered today <span class="badge ok" style="font-size:12px;margin-left:auto">12 calls</span></h4>{calls}</div>
        </div>
      </div>
    </div>
  </div>
</div></div></body></html>"""


# ------------------------------------------------- desktop calendar ---
DCAL_CSS = """
.dcalhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.dcalhead h2{font-size:30px;font-weight:900}
.dcalhead p{font-size:15.5px;color:#6B7280;font-weight:600}
.dcalnav{display:flex;align-items:center;gap:12px}
.dcalgrid{background:#fff;border-radius:18px;box-shadow:0 2px 10px rgba(0,0,0,.05);overflow:hidden;display:flex;height:640px}
.dgutter{width:70px;flex:none;background:#FAFAFB;padding-top:56px}
.dghour{font-size:13px;color:#9CA3AF;font-weight:700;text-align:right;padding-right:10px;height:58px;transform:translateY(-7px)}
.ddaycol{flex:1;border-left:1px solid #F1F2F4;position:relative}
.ddaycol.todaycol{background:#FFF9F2}
.ddayname{text-align:center;font-size:14.5px;font-weight:800;color:#6B7280;padding:12px 0 8px;border-bottom:1px solid #F1F2F4;background:#FAFAFB}
.ddaycol.todaycol .ddayname{background:#FFF1E2;color:#C2410C}
.dbwrap{position:relative;height:584px}
.dblk{position:absolute;left:6px;right:6px;border-radius:10px;padding:5px 8px;color:#fff;font-size:13px;font-weight:800;line-height:1.25;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.dblk small{display:block;font-weight:700;font-size:11px;opacity:.92}
"""


def desktop_calendar():
    d = DATA
    days = list(d["week_cal"].keys())
    full = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    gutter = "".join(f'<div class="dghour">{h}</div>' for h in HOURS)
    cols = ""
    for i, day in enumerate(days):
        blks = ""
        for t, name, svc, tech in d["week_cal"][day]:
            top = int(t2row(t) * 58)
            first = name.split()[0]
            blks += (f'<div class="dblk" style="top:{top}px;height:44px;background:{d["techs"][tech]}">'
                     f'{first} · {svc}<small>{t} · {tech}</small></div>')
        cls = "ddaycol todaycol" if i == 0 else "ddaycol"
        cols += (f'<div class="{cls}"><div class="ddayname">{full[i]}<br><span style="font-size:12px">{day.split()[1]}</span></div>'
                 f'<div class="dbwrap">{blks}</div></div>')
    techs = "".join(
        f'<div class="techpill" style="font-size:15px"><span class="dot" style="background:{c}"></span>{t}</div>'
        for t, c in d["techs"].items())
    nav = "".join(
        f'<div class="navitem{" active" if n == "Calendar" else ""}">{icon(ic, 20, sw=2)}<span>{n}</span></div>'
        for n, ic in [("Dashboard", "home"), ("Calendar", "calendar"), ("Appointments", "users"),
                      ("AI Calls", "phone"), ("Messages", "chat"), ("Reviews", "star"), ("Settings", "settings")])
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}{DESK_CSS}{DCAL_CSS}</style></head>
<body><div class="dpage" style="width:1600px;height:1000px">
<div class="dblob" style="width:600px;height:600px;left:-150px;top:-100px"></div>
<div class="dblob" style="width:500px;height:500px;right:-100px;bottom:-150px"></div>
<div class="browser">
  <div class="chrome"><div class="tl"><span style="background:#FF5F57"></span><span style="background:#FEBC2E"></span><span style="background:#28C840"></span></div>
  <div class="urlbar">{icon('globe', 16, '#9CA3AF', 2)} app.lacastay.com/calendar</div></div>
  <div class="dbody">
    <div class="sidebar">
      <div class="brand"><img src="owl.png" alt=""><b>LacaStay</b></div>
      {nav}
      <div class="sideuser"><div class="avatar">LA</div><div><b style="color:#fff;font-size:15px">Laca Stay</b><p style="font-size:13px">Admin</p></div></div>
    </div>
    <div class="main">
      <div class="dcalhead"><div><h2>Calendar</h2><p>Week of Oct 12 – Oct 18 · 3 technicians</p></div>
      <div class="dcalnav">{techs}
        <div class="datebtn" style="width:40px;height:40px">{icon('chevl', 20, '#374151', 2.4)}</div>
        <div class="datebtn" style="width:40px;height:40px">{icon('chevr', 20, '#374151', 2.4)}</div>
        <div class="todaypill" style="font-size:15px">+ New booking</div></div></div>
      <div class="dcalgrid"><div class="dgutter">{gutter}</div>{cols}</div>
    </div>
  </div>
</div></div></body></html>"""



# ------------------------------------------------------ phone chat ----
CHAT_CSS = """
.chathead{display:flex;align-items:center;gap:14px;padding:10px 28px 12px;background:#fff;border-bottom:1px solid #EEF0F3}
.chatback{width:44px;height:44px;border-radius:50%;background:#F3F4F6;display:flex;align-items:center;justify-content:center}
.chatavatar{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#FB923C,#EA580C);display:flex;align-items:center;justify-content:center;flex:none}
.chatavatar img{width:40px;height:40px}
.chatname{font-size:24px;font-weight:900}
.chatstatus{font-size:16px;color:#16A34A;font-weight:700;display:flex;align-items:center;gap:6px}
.chatstatus .dot{width:10px;height:10px;border-radius:50%;background:#16A34A}
.chatbody{flex:1;padding:18px 26px;overflow:hidden;display:flex;flex-direction:column;gap:12px;background:#F8F9FB}
.datediv{align-self:center;font-size:15px;color:#9CA3AF;font-weight:700;background:#EEF0F3;padding:6px 18px;border-radius:999px}
.cmsg{max-width:78%;padding:14px 18px;border-radius:22px;font-size:20px;font-weight:600;line-height:1.45;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.cmsg.left{align-self:flex-start;background:#fff;border-bottom-left-radius:8px;color:#1F2937}
.cmsg.right{align-self:flex-end;background:linear-gradient(135deg,#FB923C,#F97316);color:#fff;border-bottom-right-radius:8px}
.cmsg.ai-left{align-self:flex-start;background:#FFF7ED;border:1px solid #FED7AA;border-bottom-left-radius:8px;color:#7C2D12}
.ctime{font-size:13px;color:#9CA3AF;font-weight:700;margin-top:4px}
.cmsg.right + .ctime{align-self:flex-end}
.cmsg.left + .ctime,.cmsg.ai-left + .ctime{align-self:flex-start}
.typing{align-self:flex-start;background:#fff;border-radius:22px;border-bottom-left-radius:8px;padding:16px 20px;display:flex;gap:7px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.typing span{width:11px;height:11px;border-radius:50%;background:#9CA3AF;opacity:.5}
.quickrow{display:flex;gap:10px;padding:4px 0}
.quick{font-size:17px;font-weight:800;color:#C2410C;background:#FFF1E2;border:1.5px solid #FDBA74;padding:10px 20px;border-radius:999px}
.chatinput{display:flex;align-items:center;gap:12px;padding:14px 22px;background:#fff;border-top:1px solid #EEF0F3}
.inputbox{flex:1;background:#F3F4F6;border-radius:999px;padding:16px 24px;font-size:19px;color:#9CA3AF;font-weight:600}
.sendbtn{width:60px;height:60px;border-radius:50%;background:linear-gradient(180deg,#FB923C,#F97316);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(249,115,22,.4);flex:none}
"""


def phone_chat():
    d = DATA
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}{CHAT_CSS}</style></head>
<body><div class="page" style="width:1080px;height:1920px">
<div class="blob" style="width:300px;height:300px;left:-100px;bottom:60px"></div>
<div class="blob" style="width:280px;height:280px;right:-90px;bottom:300px"></div>
<h1 class="hero">AI chat, day &amp; night</h1>
<div class="phone"><div class="screen"><div class="notch"></div>
  <div class="statusbar"><span>15:05</span>
    <div class="sb-icons">
      <svg width="34" height="22" viewBox="0 0 34 22" fill="#111"><rect x="0" y="12" width="5" height="10" rx="1"/><rect x="8" y="8" width="5" height="14" rx="1"/><rect x="16" y="4" width="5" height="18" rx="1"/><rect x="24" y="0" width="5" height="22" rx="1" opacity=".35"/></svg>
      <svg width="30" height="22" viewBox="0 0 30 22" fill="none" stroke="#111" stroke-width="2.4"><path d="M4 8a15 15 0 0 1 22 0M8 12.5a10 10 0 0 1 14 0M12 17a5 5 0 0 1 6 0"/><circle cx="15" cy="20" r="1.6" fill="#111" stroke="none"/></svg>
      <svg width="44" height="22" viewBox="0 0 44 22"><rect x="1" y="1" width="36" height="20" rx="6" fill="none" stroke="#111" stroke-width="2" opacity=".4"/><rect x="4" y="4" width="24" height="14" rx="3.5" fill="#111"/><rect x="39" y="7" width="4" height="8" rx="2" fill="#111" opacity=".4"/></svg>
    </div></div>
  <div class="chathead">
    <div class="chatback">{icon('chevl', 24, '#374151', 2.4)}</div>
    <div class="chatavatar"><img src="owl.png" alt=""></div>
    <div style="flex:1"><div class="chatname">Laca AI</div>
      <div class="chatstatus"><span class="dot"></span>Online · replies instantly</div></div>
    {icon('phone', 28, '#F97316', 2)}
  </div>
  <div class="chatbody">
    <div class="datediv">Today</div>
    <div class="cmsg right">Hi! Do you have any openings for a gel manicure tomorrow afternoon?</div>
    <div class="ctime">2:12 PM</div>
    <div class="cmsg ai-left">Hi Jessica! Yes — I have tomorrow at 2:30 PM or 4:15 PM with Anna. Which works better for you?</div>
    <div class="ctime">2:12 PM</div>
    <div class="cmsg right">2:30 works for me!</div>
    <div class="ctime">2:13 PM</div>
    <div class="cmsg ai-left">You&apos;re booked for tomorrow at 2:30 PM with Anna. I&apos;ll text you a reminder the day before. See you then!</div>
    <div class="ctime">2:13 PM</div>
    <div class="quickrow"><div class="quick">Reschedule</div><div class="quick">Add a pedi</div><div class="quick">Get directions</div></div>
    <div class="typing"><span></span><span style="opacity:.75"></span><span></span></div>
  </div>
  <div class="chatinput">
    <div class="inputbox">Type a message…</div>
    <div class="sendbtn">{icon('zap', 28, '#fff', 2.4)}</div>
  </div>
  <div class="tabbar">
    <div class="tab">{icon('home', 34, sw=2)}<span>Home</span></div>
    <div class="tab">{icon('calendar', 34, sw=2)}<span>Appointments</span></div>
    <div class="fab">{icon('plus', 44, '#fff', 2.6)}</div>
    <div class="tab active">{icon('chat', 34, '#F97316', 2.2)}<span>Connect</span></div>
    <div class="tab">{icon('more', 34, sw=2)}<span>More</span></div>
  </div>
</div></div>
<div style="height:36px"></div>
<img src="owl.png" style="height:150px" alt="LacaStay owl">
</div></body></html>"""


# ------------------------------------------------- phone staff -------
STAFF_CSS = """
.staffhead{padding:8px 30px 0}
.stafftitle{font-size:44px;font-weight:900;margin:2px 0 4px}
.staffsub{font-size:19px;color:#6B7280;font-weight:600;margin-bottom:12px}
.dutycard{background:linear-gradient(135deg,#FB923C,#EA580C);border-radius:24px;margin:6px 28px 0;padding:20px 24px;color:#fff;box-shadow:0 8px 24px rgba(249,115,22,.35);display:flex;align-items:center;gap:18px}
.dutynum{font-size:52px;font-weight:900}
.dutylabel{font-size:19px;font-weight:700;opacity:.95;line-height:1.35}
.stafflist{flex:1;padding:16px 28px 0;overflow:hidden}
.staffrow{display:flex;align-items:center;gap:16px;background:#fff;border-radius:22px;padding:16px 18px;margin-bottom:12px;box-shadow:0 3px 12px rgba(0,0,0,.05)}
.savatar{width:66px;height:66px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:25px;flex:none;position:relative}
.savatar .presence{position:absolute;bottom:2px;right:2px;width:18px;height:18px;border-radius:50%;border:3px solid #fff}
.sinfo{flex:1;min-width:0}
.sname{font-size:23px;font-weight:800}
.srole{font-size:17px;color:#6B7280;font-weight:600}
.stime{font-size:16px;font-weight:800;color:#15803D}
.stime.off{color:#9CA3AF}
.checkinbtn{font-size:17px;font-weight:800;color:#EA580C;background:#FFF7ED;border:2px solid #FDBA74;padding:12px 24px;border-radius:999px;flex:none}
"""


def phone_staff_checkin():
    staff = [
        ("Anna Nguyen", "Nail Tech · Chair 1", "AN", "#FFF1E2", "#C2410C", "8:55 AM", True, False),
        ("Linda Tran", "Nail Tech · Chair 2", "LT", "#DBEAFE", "#1D4ED8", "9:02 AM", True, False),
        ("Mai Pham", "Nail Tech · Chair 3", "MP", "#D1FAE5", "#047857", "9:15 AM", True, False),
        ("David Lee", "Receptionist", "DL", "#F3F4F6", "#6B7280", None, False, False),
        ("Sofia Garcia", "Nail Tech · Chair 4", "SG", "#F3F4F6", "#9CA3AF", None, False, True),
    ]
    rows = ""
    for name, role, init, bg, fg, t, onduty, dayoff in staff:
        if dayoff:
            right = '<div class="stime off">Day off</div>'
            pres = ''
        elif onduty:
            right = f'<div class="stime">On duty · {t}</div>'
            pres = '<span class="presence" style="background:#16A34A"></span>'
        else:
            right = '<div class="checkinbtn">Check in</div>'
            pres = '<span class="presence" style="background:#D1D5DB"></span>'
        rows += f"""
        <div class="staffrow">
          <div class="savatar" style="background:{bg};color:{fg}">{init}{pres}</div>
          <div class="sinfo"><div class="sname">{name}</div><div class="srole">{role}</div></div>
          {right}
        </div>"""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT}
<style>{BASE_CSS}{APP_CSS}{STAFF_CSS}</style></head>
<body><div class="page" style="width:1080px;height:1920px">
<div class="blob" style="width:300px;height:300px;left:-100px;bottom:60px"></div>
<div class="blob" style="width:280px;height:280px;right:-90px;bottom:300px"></div>
<h1 class="hero">Who&apos;s on duty</h1>
<div class="phone"><div class="screen"><div class="notch"></div>
  <div class="statusbar"><span>15:05</span>
    <div class="sb-icons">
      <svg width="34" height="22" viewBox="0 0 34 22" fill="#111"><rect x="0" y="12" width="5" height="10" rx="1"/><rect x="8" y="8" width="5" height="14" rx="1"/><rect x="16" y="4" width="5" height="18" rx="1"/><rect x="24" y="0" width="5" height="22" rx="1" opacity=".35"/></svg>
      <svg width="30" height="22" viewBox="0 0 30 22" fill="none" stroke="#111" stroke-width="2.4"><path d="M4 8a15 15 0 0 1 22 0M8 12.5a10 10 0 0 1 14 0M12 17a5 5 0 0 1 6 0"/><circle cx="15" cy="20" r="1.6" fill="#111" stroke="none"/></svg>
      <svg width="44" height="22" viewBox="0 0 44 22"><rect x="1" y="1" width="36" height="20" rx="6" fill="none" stroke="#111" stroke-width="2" opacity=".4"/><rect x="4" y="4" width="24" height="14" rx="3.5" fill="#111"/><rect x="39" y="7" width="4" height="8" rx="2" fill="#111" opacity=".4"/></svg>
    </div></div>
  <div class="staffhead">
    <div class="apptitle">Staff check-in</div>
    <div class="staffsub">Monday, Oct 12 · Laca Stay</div>
  </div>
  <div class="dutycard">
    <div class="dutynum">3/5</div>
    <div class="dutylabel">team members<br>on duty right now</div>
    <div style="margin-left:auto">{icon('users', 44, '#fff', 2)}</div>
  </div>
  <div class="stafflist">{rows}</div>
  <div class="tabbar">
    <div class="tab">{icon('home', 34, sw=2)}<span>Home</span></div>
    <div class="tab">{icon('calendar', 34, sw=2)}<span>Appointments</span></div>
    <div class="fab">{icon('plus', 44, '#fff', 2.6)}</div>
    <div class="tab">{icon('chat', 34, sw=2)}<span>Connect</span></div>
    <div class="tab active">{icon('more', 34, '#F97316', 2.2)}<span>More</span></div>
  </div>
</div></div>
<div style="height:36px"></div>
<img src="owl.png" style="height:150px" alt="LacaStay owl">
</div></body></html>"""


# ---------------------------------------------------------------- render -
def render():
    from playwright.sync_api import sync_playwright
    jobs = [
        ("dash.html", phone_dashboard(), 1080, 1920, IMG / "app-dashboard.png"),
        ("cal.html", phone_calendar(), 1080, 1920, IMG / "app-calendar.png"),
        ("dash-desk.html", desktop_dashboard(), 1600, 1000, IMG / "app-dashboard-desktop.png"),
        ("cal-desk.html", desktop_calendar(), 1600, 1000, IMG / "app-calendar-desktop.png"),
        ("chat.html", phone_chat(), 1080, 1920, IMG / "app-chat.png"),
        ("staff.html", phone_staff_checkin(), 1080, 1920, IMG / "app-staff-checkin.png"),
    ]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, html, w, h, out in jobs:
            (MOCK / name).write_text(html)
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            pg.goto((MOCK / name).as_uri(), wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(out))
            pg.close()
            im = Image.open(out)
            print(f"saved {out.name}: {im.size}")
        b.close()


if __name__ == "__main__":
    owl = make_owl()
    print("owl:", owl)
    render()
