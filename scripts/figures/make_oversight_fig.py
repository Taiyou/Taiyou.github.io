"""Animated SVG: five ways to supervise an AI with an accelerated copy of yourself.

Usage: python3 make_oversight_fig.py OUT_DIR
Writes emulation-oversight-types.svg (EN) and emulation-oversight-types-ja.svg (JA).
Animation is CSS-only (works inside <img>), and stops under prefers-reduced-motion.
"""
import sys
from pathlib import Path

INK, TEXT, MUTED = "#0f1923", "#2c3e50", "#5f6a7d"
WARM, BORDER, GOLD, GOLD_L, TEAL = "#f4f1ec", "#e0ddd7", "#7d6430", "#c9a961", "#2a7f8a"

TXT = {
    "en": {
        "font": "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif",
        "you": "YOU", "copy": "SETTLEMENT", "ai": "CLONES ×N", "committee": "SUPERVISORS ×3",
        "you_rate": "~1 thought/s", "copy_rate": "harness · e.g. your emulation", "ai_rate": "AI agents · ~10⁶ steps/s",
        "lane_slow": "settles at your pace", "lane_fast": "every step",
        "head": "Five designs for settling what the AI clones bring back",
        "foot": "Read like a layer-2 rollup: the clones (AI agents) execute, the settlement mechanism bundles and checks, and you are the layer 1.",
        "rows": [
            ("Validium type", "only the verdict comes back;", "the log stays inside the mechanism", "source amnesia", TEAL),
            ("Optimistic type", "a summary comes back; the full log", "goes to an archive you can challenge", "accountable — if someone watches", GOLD),
            ("Validity type", "the result comes back", "with a proof it met the constraints", "accountable, cheaply — if provable", INK),
            ("Committee type", "supervisors cross-check each other;", "one source means shared blind spots", "only as diverse as its members", GOLD),
            ("Based type", "you set intent and order first;", "the mechanism just enforces it", "lineage = derived from your intent", TEAL),
        ],
        "result": "OK", "summary": "summary", "archive": "archive", "challenge": "challenge window",
        "proof": "proof", "blind": "shared blind spot", "intent": "intent",
    },
    "ja": {
        "font": "'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', 'Noto Sans CJK JP', 'Yu Gothic', Meiryo, sans-serif",
        "you": "本人", "copy": "決済の仕組み", "ai": "分身 ×N", "committee": "監督者 ×3",
        "you_rate": "毎秒〜1の思考", "copy_rate": "ハーネス（例：自分の複製）", "ai_rate": "AIエージェント・毎秒〜10⁶",
        "lane_slow": "本人のペースで決済", "lane_fast": "一歩ごと",
        "head": "AIの分身が持ち帰るものを決済する：五つの設計",
        "foot": "レイヤー2のロールアップとして読む。分身（AIエージェント）が実行し、決済の仕組みが束ねて検証し、本人がレイヤー1になる。",
        "rows": [
            ("Validium型", "結論だけが本人に戻る。", "ログは仕組みの中に留まる", "出典健忘", TEAL),
            ("Optimistic型", "要約が戻り、全ログは", "異議を申し立てられる記録庫へ", "見張りがいれば責任を負える", GOLD),
            ("Validity型", "結果に、制約を満たした", "ことの証明が添えられて戻る", "証明できる範囲で安く責任", INK),
            ("委員会型", "複数の監督者が相互に検証する。", "同じ源の監督者は死角を共有する", "多様性はメンバー次第", GOLD),
            ("Based型", "本人が先に意図と順番を決め、", "仕組みは執行と検査だけ", "来歴＝本人の意図からの派生", TEAL),
        ],
        "result": "OK", "summary": "要約", "archive": "記録庫", "challenge": "異議の期間",
        "proof": "証明", "blind": "共有された死角", "intent": "意図",
    },
}

W, ROW_H, TOP = 1200, 172, 92
X_YOU, X_COPY, X_AI = 330, 600, 960     # box left edges
BW, BH = 130, 56
SLOW_A, SLOW_B = X_YOU + BW + 8, X_COPY - 8       # you <-> copy lane
FAST_A, FAST_B = X_COPY + 180 + 8, X_AI - 8       # copy <-> AI lane
SLOW_LEN, FAST_LEN = SLOW_B - SLOW_A, FAST_B - FAST_A


def style() -> str:
    return f"""<style>
  .dot {{ animation-timing-function: linear; animation-iteration-count: infinite; }}
  .s-out {{ animation-name: s-out; animation-duration: 6s; }}
  .s-in  {{ animation-name: s-in;  animation-duration: 6s; }}
  .f-out {{ animation-name: f-out; animation-duration: 1.4s; }}
  .f-in  {{ animation-name: f-in;  animation-duration: 1.4s; }}
  .arch  {{ animation-name: arch;  animation-duration: 3s; }}
  .fill  {{ animation: fill 6s linear infinite; transform-box: fill-box; transform-origin: left; }}
  @keyframes s-out {{ 0% {{ transform: translateX(0); opacity: 0 }} 8% {{ opacity: 1 }} 92% {{ opacity: 1 }} 100% {{ transform: translateX({SLOW_LEN}px); opacity: 0 }} }}
  @keyframes s-in  {{ 0% {{ transform: translateX(0); opacity: 0 }} 8% {{ opacity: 1 }} 92% {{ opacity: 1 }} 100% {{ transform: translateX(-{SLOW_LEN}px); opacity: 0 }} }}
  @keyframes f-out {{ 0% {{ transform: translateX(0); opacity: 0 }} 10% {{ opacity: 1 }} 90% {{ opacity: 1 }} 100% {{ transform: translateX({FAST_LEN}px); opacity: 0 }} }}
  @keyframes f-in  {{ 0% {{ transform: translateX(0); opacity: 0 }} 10% {{ opacity: 1 }} 90% {{ opacity: 1 }} 100% {{ transform: translateX(-{FAST_LEN}px); opacity: 0 }} }}
  @keyframes arch  {{ 0% {{ transform: translateY(0); opacity: 0 }} 15% {{ opacity: 1 }} 85% {{ opacity: 1 }} 100% {{ transform: translateY(46px); opacity: 0 }} }}
  @keyframes fill  {{ 0% {{ transform: scaleX(0) }} 100% {{ transform: scaleX(1) }} }}
  @media (prefers-reduced-motion: reduce) {{ .dot, .fill {{ animation: none; opacity: 1 }} }}
</style>"""


def arrow(x1, x2, y, color=MUTED, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    head = (f'<path d="M{x2},{y} l-9,-5 v10 z" fill="{color}"/>' if x2 > x1
            else f'<path d="M{x2},{y} l9,-5 v10 z" fill="{color}"/>')
    return f'<path d="M{x1},{y} L{x2},{y}" stroke="{color}" stroke-width="2"{d}/>{head}'


def box(x, y, w, h, label, sub=None, fill="#fff", stroke=TEXT, color=INK, size=19, inner=False):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    if inner:
        s += f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="5" fill="none" stroke="{stroke}" stroke-width="1.2"/>'
    s += f'<text x="{x+w/2}" y="{y+h/2+7}" text-anchor="middle" font-size="{size}" font-weight="600" fill="{color}">{label}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h+20}" text-anchor="middle" font-size="13" fill="{MUTED}">{sub}</text>'
    return s


def fast_lane(y, delay0=0.0):
    """copy <-> AI: many dots, both directions, every step."""
    s = arrow(FAST_A, FAST_B, y - 10) + arrow(FAST_B, FAST_A, y + 10)
    for i in range(4):
        d = -(delay0 + i * 0.35)
        s += f'<circle class="dot f-out" style="animation-delay:{d:.2f}s" cx="{FAST_A}" cy="{y-10}" r="4" fill="#3d5a73"/>'
        s += f'<circle class="dot f-in" style="animation-delay:{d-0.17:.2f}s" cx="{FAST_B}" cy="{y+10}" r="4" fill="#3d5a73"/>'
    return s


def slow_out(y, color=MUTED, dot=None, delay=0.0):
    s = arrow(SLOW_A, SLOW_B, y - 10, color)
    if dot:
        s += f'<g class="dot s-out" style="animation-delay:{-delay:.2f}s">{dot(SLOW_A, y - 10)}</g>'
    return s


def slow_in(y, dot, delay=0.0, color=MUTED):
    s = arrow(SLOW_B, SLOW_A, y + 10, color)
    s += f'<g class="dot s-in" style="animation-delay:{-delay:.2f}s">{dot(SLOW_B, y + 10)}</g>'
    return s


def pill(x, cy, text, color):
    w = sum(15 if ord(c) > 0x2000 else 7.6 for c in text) + 26
    return (f'<rect x="{x}" y="{cy-14}" width="{w:.0f}" height="28" rx="14" fill="{color}"/>'
            f'<text x="{x + w/2:.0f}" y="{cy+5}" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">{text}</text>')


def build(lang: str) -> str:
    t = TXT[lang]
    H = TOP + ROW_H * 5 + 60
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{t["font"]}">', style(),
           f'<rect width="{W}" height="{H}" fill="#fff"/>',
           f'<text x="40" y="44" font-size="21" font-weight="600" fill="{GOLD}" letter-spacing=".02em">{t["head"]}</text>',
           f'<text x="{(SLOW_A+SLOW_B)/2}" y="78" text-anchor="middle" font-size="14" fill="{MUTED}">{t["lane_slow"]}</text>',
           f'<text x="{(FAST_A+FAST_B)/2}" y="78" text-anchor="middle" font-size="14" fill="{MUTED}">{t["lane_fast"]}</text>']

    for r, (name, l1, l2, tag, color) in enumerate(t["rows"]):
        y0 = TOP + r * ROW_H
        cy = y0 + 62                    # lane centre
        by = cy - BH / 2
        if r:
            out.append(f'<path d="M40,{y0} L{W-40},{y0}" stroke="{BORDER}" stroke-width="1"/>')
        out.append(f'<text x="40" y="{y0+40}" font-size="20" font-weight="600" fill="{color}">{name}</text>')
        out.append(f'<text x="40" y="{y0+66}" font-size="15" fill="{TEXT}">{l1}</text>')
        out.append(f'<text x="40" y="{y0+86}" font-size="15" fill="{TEXT}">{l2}</text>')
        out.append(pill(40, y0 + 118, tag, color))

        out.append(box(X_YOU, by, BW, BH, t["you"], t["you_rate"], fill=WARM, stroke=GOLD_L, color=GOLD))
        for k in (2, 1):
            out.append(f'<rect x="{X_AI+k*5}" y="{by-k*5}" width="{BW}" height="{BH}" rx="8" fill="#fff" stroke="#3d5a73" stroke-width="1.4" opacity="{0.35 if k == 2 else 0.6}"/>')
        out.append(box(X_AI, by, BW, BH, t["ai"], t["ai_rate"], stroke="#3d5a73", color="#3d5a73", size=17))
        out.append(fast_lane(cy, delay0=r * 0.2))

        result_dot = lambda x, y: f'<circle cx="{x}" cy="{y}" r="6" fill="{GOLD}"/>'
        if r == 0:      # validium: verdict only; log stays inside the copy
            out.append(box(X_COPY, by, 180, BH, t["copy"], t["copy_rate"], fill="#eaf3f4", stroke=TEAL, color=TEAL, inner=True, size=17))
            out.append(slow_out(cy))
            out.append(slow_in(cy, lambda x, y: f'<circle cx="{x}" cy="{y}" r="6" fill="{GOLD}"/><text x="{x}" y="{y+22}" text-anchor="middle" font-size="12" font-weight="600" fill="{GOLD}">{t["result"]}</text>'))
            for k in range(3):
                out.append(f'<rect x="{X_COPY+154}" y="{by+16+k*8}" width="16" height="4" rx="2" fill="{GOLD_L}"/>')
        elif r == 1:    # optimistic: summary back, log to archive, challenge window
            out.append(box(X_COPY, by, 180, BH, t["copy"], None, fill="#eaf3f4", stroke=TEAL, color=TEAL, inner=True, size=17))
            out.append(slow_out(cy))
            out.append(slow_in(cy, lambda x, y: f'<rect x="{x-14}" y="{y-6}" width="28" height="12" rx="3" fill="{GOLD}"/><text x="{x}" y="{y+22}" text-anchor="middle" font-size="12" font-weight="600" fill="{GOLD}">{t["summary"]}</text>'))
            ax, ay = X_COPY + 30, by + BH + 40
            out.append(f'<path d="M{X_COPY+90},{by+BH} L{X_COPY+90},{ay-2}" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="4 4"/>')
            for k in range(2):
                out.append(f'<rect class="dot arch" style="animation-delay:{-k*1.5:.1f}s" x="{X_COPY+84}" y="{by+BH+2}" width="12" height="5" rx="2" fill="{BORDER}"/>')
            out.append(f'<rect x="{ax}" y="{ay}" width="120" height="30" rx="5" fill="{WARM}" stroke="{GOLD_L}" stroke-width="1.5"/>')
            out.append(f'<text x="{ax+60}" y="{ay+20}" text-anchor="middle" font-size="14" fill="{GOLD}">{t["archive"]}</text>')
            # challenge window: you can reach the archive while the bar fills
            out.append(f'<path d="M{X_YOU+BW},{by+BH-8} C{X_YOU+BW+40},{by+BH-8} {X_YOU+BW+10},{ay+15} {ax-4},{ay+15}" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="5 4" fill="none"/>')
            out.append(f'<path d="M{ax-4},{ay+15} l-9,-5 v10 z" fill="{GOLD}"/>')
            bx, bw = ax + 136, 100
            out.append(f'<text x="{bx}" y="{ay+11}" font-size="12" fill="{GOLD}">{t["challenge"]}</text>')
            out.append(f'<rect x="{bx}" y="{ay+18}" width="{bw}" height="6" rx="3" fill="{BORDER}"/>')
            out.append(f'<rect class="fill" x="{bx}" y="{ay+18}" width="{bw}" height="6" rx="3" fill="{GOLD_L}"/>')
        elif r == 2:    # validity: result + proof badge
            out.append(box(X_COPY, by, 180, BH, t["copy"], t["copy_rate"], fill="#eaf3f4", stroke=TEAL, color=TEAL, inner=True, size=17))
            out.append(slow_out(cy))
            out.append(slow_in(cy, lambda x, y: f'<circle cx="{x}" cy="{y}" r="6" fill="{GOLD}"/><rect x="{x+9}" y="{y-8}" width="16" height="16" rx="3" fill="{INK}"/><path d="M{x+12},{y} l3,4 l7,-8" stroke="#fff" stroke-width="2" fill="none"/><text x="{x+17}" y="{y+24}" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}">{t["proof"]}</text>'))
        elif r == 3:    # committee: three identical copies with the same blind spot
            for k in range(3):
                yy = by - 16 + k * 14
                out.append(f'<rect x="{X_COPY}" y="{yy}" width="180" height="{BH-12}" rx="7" fill="#eaf3f4" stroke="{TEAL}" stroke-width="1.6"/>')
                out.append(f'<path d="M{X_COPY+148},{yy} L{X_COPY+170},{yy}" stroke="{GOLD}" stroke-width="4"/>')
            out.append(f'<text x="{X_COPY+90}" y="{by+BH/2+14}" text-anchor="middle" font-size="17" font-weight="600" fill="{TEAL}">{t["committee"]}</text>')
            out.append(f'<text x="{X_COPY+90}" y="{by+BH+20}" text-anchor="middle" font-size="13" fill="{MUTED}">{t["copy_rate"]}</text>')
            out.append(f'<text x="{X_COPY+159}" y="{by-26}" text-anchor="middle" font-size="12" fill="{GOLD}">{t["blind"]}</text>')
            out.append(slow_out(cy))
            out.append(slow_in(cy, result_dot))
        else:           # based: intent goes out first, copy only executes
            out.append(box(X_COPY, by, 180, BH, t["copy"], t["copy_rate"], fill="#eaf3f4", stroke=TEAL, color=TEAL, inner=True, size=17))
            out.append(slow_out(cy, color=TEAL, dot=lambda x, y: f'<circle cx="{x}" cy="{y}" r="7" fill="{TEAL}"/><text x="{x}" y="{y-12}" text-anchor="middle" font-size="12" font-weight="600" fill="{TEAL}">{t["intent"]}</text>'))
            out.append(slow_in(cy, result_dot, delay=3.0))

    out.append(f'<text x="{W/2}" y="{H-24}" text-anchor="middle" font-size="15" fill="{MUTED}">{t["foot"]}</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    d = Path(sys.argv[1])
    (d / "emulation-oversight-types.svg").write_text(build("en"))
    (d / "emulation-oversight-types-ja.svg").write_text(build("ja"))
    print("written")
