with open('templates/SmartSpend.html', 'r', encoding='utf-8') as f:
    content = f.read()

# CSS Patch
css_add = """
        /* ===========================
           DEMO MODAL
           =========================== */
        #demoOverlay {
            position: fixed; inset: 0; z-index: 2100;
            background: rgba(6, 13, 18, 0.88); backdrop-filter: blur(24px);
            display: flex; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none; transition: opacity var(--med) var(--ease);
            padding: 1rem;
        }
        #demoOverlay.open { opacity: 1; pointer-events: all; }
        #demoModalBox {
            background: var(--base-card); border: 1px solid var(--base-border); border-radius: 28px;
            width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto;
            box-shadow: var(--clay-shadow-lg), 0 0 80px rgba(57, 255, 126, 0.12);
            transform: translateY(40px) scale(0.96); transition: transform var(--med) var(--ease);
            position: relative;
        }
        #demoOverlay.open #demoModalBox { transform: translateY(0) scale(1); }
        #demoModalBox::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); border-radius: 28px 28px 0 0; }
        .demo-modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem 1.75rem 0; }
        .demo-modal-header-left { display: flex; align-items: center; gap: 10px; }
        .demo-modal-title { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800; }
        .demo-tab-bar { display: flex; gap: 0; padding: 1rem 1.75rem 0; border-bottom: 1px solid var(--base-border); overflow-x: auto; }
        #demoOverlay .demo-tab { padding: 0.625rem 1.1rem; font-size: 0.82rem; font-weight: 600; background: none; border: none; border-bottom: 2px solid transparent; color: var(--base-muted); cursor: pointer; font-family: inherit; transition: all 0.2s; white-space: nowrap; margin-bottom: -1px; }
        #demoOverlay .demo-tab.active { color: var(--accent); border-bottom-color: var(--accent); }
        #demoOverlay .demo-tab:hover { color: var(--base-text); }
        .demo-panel { padding: 1.75rem; }
        .demo-video-player { background: var(--base-surface); border: 1px solid var(--base-border); border-radius: 18px; overflow: hidden; margin-bottom: 1rem; box-shadow: var(--clay-shadow); }
        .demo-video-screen { background: linear-gradient(135deg, #052e16 0%, #0c1a22 50%, #0a1a12 100%); height: 240px; display: flex; align-items: center; justify-content: center; position: relative; cursor: pointer; }
        .demo-video-screen::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at center, rgba(57,255,126,0.08), transparent 70%); }
        .demo-video-thumb { text-align: center; position: relative; z-index: 1; }
        .demo-video-thumb .thumb-title { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 800; margin-bottom: 0.5rem; }
        .demo-video-thumb .thumb-sub { font-size: 0.78rem; color: var(--base-muted); }
        .demo-video-controls { display: flex; align-items: center; gap: 1rem; padding: 0.875rem 1.1rem; background: var(--base-card); }
        #demoPlayBtn { width: 38px; height: 38px; border-radius: 50%; border: none; background: rgba(57,255,126,0.15); color: var(--accent); font-size: 0.9rem; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: all 0.2s; }
        #demoPlayBtn:hover { background: rgba(57,255,126,0.25); transform: scale(1.08); }
        .demo-progress-track { flex: 1; height: 4px; background: var(--base-surface); border-radius: 2px; overflow: hidden; cursor: pointer; }
        #demoProgress { height: 100%; width: 0%; background: linear-gradient(90deg, var(--accent), var(--green-400)); border-radius: 2px; transition: width 0.5s linear; }
        #demoTimestamp { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--base-muted); flex-shrink: 0; }
        .demo-chapters { display: flex; flex-direction: column; gap: 0.5rem; }
        .demo-chapter { display: flex; align-items: center; gap: 0.875rem; padding: 0.75rem 1rem; background: var(--base-surface); border: 1px solid var(--base-border); border-radius: 12px; cursor: pointer; transition: all 0.2s; font-size: 0.83rem; }
        .demo-chapter:hover { border-color: var(--accent); background: var(--accent-dim); }
        .demo-chapter-ts { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--accent); flex-shrink: 0; }
        .demo-feature-card { background: var(--base-card); border: 1.5px solid var(--base-border); border-radius: 16px; padding: 1rem; cursor: pointer; transition: all .25s var(--ease); text-align: center; box-shadow: var(--clay-shadow); }
        .demo-feature-card:hover, .demo-feature-card.selected { border-color: var(--accent); background: var(--accent-dim); transform: translateY(-3px); box-shadow: var(--clay-shadow-lg); }
        .demo-feature-card .dfc-icon { font-size: 1.5rem; margin-bottom: 6px; }
        .demo-feature-card .dfc-label { font-size: 0.75rem; font-weight: 700; }
        #demoPreview { background: var(--base-surface); border: 1px solid var(--base-border); border-radius: 16px; padding: 1.25rem; min-height: 140px; margin-top: 1rem; transition: opacity 0.3s; }
        .demo-day-btn { flex: 1; min-width: 60px; padding: .5rem .25rem; background: var(--base-card); border: 1.5px solid var(--base-border); border-radius: 10px; font-size: .68rem; color: var(--base-muted); cursor: pointer; font-family: inherit; text-align: center; transition: all .2s; line-height: 1.4; box-shadow: var(--clay-shadow); }
        .demo-day-btn.active, .demo-day-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-dim); }
        .demo-time-btn { padding: .6rem 1rem; background: var(--base-card); border: 1.5px solid var(--base-border); border-radius: 10px; font-size: .8rem; font-weight: 600; color: var(--base-muted); cursor: pointer; font-family: inherit; transition: all .2s; box-shadow: var(--clay-shadow); }
        .demo-time-btn.active, .demo-time-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-dim); }
        .demo-book-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--base-muted); margin-bottom: 0.625rem; }
        @keyframes fp-pop { 0% { transform: scale(0.6); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        #fpToast { position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%) translateY(80px); z-index: 9999; display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1.5rem; background: var(--base-card); border: 1px solid var(--base-border); border-radius: 100px; box-shadow: var(--clay-shadow-lg); font-size: 0.875rem; font-weight: 600; white-space: nowrap; pointer-events: none; transition: transform 0.4s var(--ease), opacity 0.4s; opacity: 0; }
        #fpToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
        #fpToast.success { border-color: rgba(57,255,126,0.3); color: var(--accent); }
        #fpToast.error { border-color: rgba(255,100,100,0.3); color: #ff6b6b; }
        @media (max-width: 640px) { #demoModalBox { margin: 0 .75rem; } }
"""
if "/* DEMO MODAL */" not in content and "#demoOverlay {" not in content:
    content = content.replace("    </style>", css_add + "    </style>")

# HTML + JS Patch
html_and_js_add = """
    <!-- ===========================
         DEMO MODAL  ← ADDED
         =========================== -->
    <div id="demoOverlay" onclick="handleDemoOverlayClick(event)">
        <div id="demoModalBox">
            <div class="demo-modal-header">
                <div class="demo-modal-header-left">
                    <div class="logo-icon" style="width:32px;height:32px;font-size:0.9rem;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--green-600));display:flex;align-items:center;justify-content:center;">💸</div>
                    <span class="demo-modal-title">SmartSpend Demo</span>
                </div>
                <button class="modal-close" onclick="closeDemoModal()" style="position:static">✕</button>
            </div>
            <div class="demo-tab-bar">
                <button class="demo-tab active" onclick="switchDemoTab(this,'video')">▶ Watch Demo</button>
                <button class="demo-tab" onclick="switchDemoTab(this,'features')">✦ Feature Tour</button>
                <button class="demo-tab" onclick="switchDemoTab(this,'book')">📅 Book a Call</button>
            </div>
            <div id="demoPanelVideo" class="demo-panel">
                <div class="demo-video-player">
                    <div class="demo-video-screen" onclick="toggleDemoPlay(this)">
                        <div class="demo-video-thumb">
                            <div style="width:64px;height:64px;border-radius:50%;background:rgba(57,255,126,0.15);border:2px solid rgba(57,255,126,0.3);display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;font-size:1.5rem">▶</div>
                            <div class="thumb-title">SmartSpend Product Demo</div>
                            <div class="thumb-sub">3 min 42 sec · See the full app in action</div>
                        </div>
                    </div>
                    <div class="demo-video-controls">
                        <button id="demoPlayBtn" onclick="toggleDemoPlay(this)">&#9654;</button>
                        <div class="demo-progress-track" onclick="scrubDemo(event, this)">
                            <div id="demoProgress"></div>
                        </div>
                        <span id="demoTimestamp">0:00 / 3:42</span>
                    </div>
                </div>
                <div style="font-size:0.72rem;font-weight:700;color:var(--base-muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.625rem">Chapters</div>
                <div class="demo-chapters">
                    <div class="demo-chapter" onclick="jumpDemo(0)"><span class="demo-chapter-ts">0:00</span><span>Introduction & Overview</span></div>
                    <div class="demo-chapter" onclick="jumpDemo(30)"><span class="demo-chapter-ts">0:30</span><span>Adding Transactions (Voice, OCR, Manual)</span></div>
                    <div class="demo-chapter" onclick="jumpDemo(90)"><span class="demo-chapter-ts">1:30</span><span>AI Insights & Budget Alerts</span></div>
                    <div class="demo-chapter" onclick="jumpDemo(160)"><span class="demo-chapter-ts">2:40</span><span>Analytics Dashboard & Export</span></div>
                    <div class="demo-chapter" onclick="jumpDemo(210)"><span class="demo-chapter-ts">3:30</span><span>Pricing & Getting Started</span></div>
                </div>
            </div>
            <div id="demoPanelFeatures" class="demo-panel" style="display:none">
                <p style="font-size:0.85rem;color:var(--base-muted);margin-bottom:1rem">Click any feature to see a live preview.</p>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem">
                    <div class="demo-feature-card selected" onclick="highlightFeature(this,'dashboard')"><div class="dfc-icon">📊</div><div class="dfc-label">Dashboard</div></div>
                    <div class="demo-feature-card" onclick="highlightFeature(this,'ai')"><div class="dfc-icon">🤖</div><div class="dfc-label">AI Insights</div></div>
                    <div class="demo-feature-card" onclick="highlightFeature(this,'ocr')"><div class="dfc-icon">📸</div><div class="dfc-label">OCR Scan</div></div>
                    <div class="demo-feature-card" onclick="highlightFeature(this,'voice')"><div class="dfc-icon">🎙️</div><div class="dfc-label">Voice Entry</div></div>
                    <div class="demo-feature-card" onclick="highlightFeature(this,'budget')"><div class="dfc-icon">🎯</div><div class="dfc-label">Budgets</div></div>
                    <div class="demo-feature-card" onclick="highlightFeature(this,'analytics')"><div class="dfc-icon">📈</div><div class="dfc-label">Analytics</div></div>
                </div>
                <div id="demoPreview">
                    <div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">📊 Dashboard Preview</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem">
                        <div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid rgba(57,255,126,.2)">
                            <div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Total Balance</div>
                            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#39ff7e">₹1,28,450</div>
                        </div>
                        <div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid var(--base-border)">
                            <div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Income</div>
                            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#4ade80">₹85,000</div>
                        </div>
                        <div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid var(--base-border)">
                            <div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Expenses</div>
                            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#ff6b6b">₹43,240</div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="demoPanelBook" class="demo-panel" style="display:none">
                <div id="demoPanelBookContent">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
                        <div>
                            <div class="demo-book-label">Your Details</div>
                            <div class="form-group"><label class="form-label">Full Name</label><input class="form-input" type="text" id="bookName" placeholder="Arjun Sharma" /></div>
                            <div class="form-group"><label class="form-label">Work Email</label><input class="form-input" type="email" id="bookEmail" placeholder="you@company.com" /></div>
                            <div class="form-group"><label class="form-label">Company / Team Size</label><input class="form-input" type="text" id="bookCompany" placeholder="e.g. Acme Corp · 10 people" /></div>
                        </div>
                        <div>
                            <div class="demo-book-label">Pick a Date</div>
                            <div style="display:flex;gap:0.4rem;margin-bottom:1rem;flex-wrap:wrap">
                                <button class="demo-day-btn active" onclick="selectDay(this,'Mon 14 Apr')">Mon<br><strong>14</strong></button>
                                <button class="demo-day-btn" onclick="selectDay(this,'Tue 15 Apr')">Tue<br><strong>15</strong></button>
                                <button class="demo-day-btn" onclick="selectDay(this,'Wed 16 Apr')">Wed<br><strong>16</strong></button>
                                <button class="demo-day-btn" onclick="selectDay(this,'Thu 17 Apr')">Thu<br><strong>17</strong></button>
                                <button class="demo-day-btn" onclick="selectDay(this,'Fri 18 Apr')">Fri<br><strong>18</strong></button>
                            </div>
                            <div class="demo-book-label">Pick a Time (IST)</div>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem">
                                <button class="demo-time-btn active" onclick="selectTime(this,'10:00 AM')">10:00 AM</button>
                                <button class="demo-time-btn" onclick="selectTime(this,'11:30 AM')">11:30 AM</button>
                                <button class="demo-time-btn" onclick="selectTime(this,'2:00 PM')">2:00 PM</button>
                                <button class="demo-time-btn" onclick="selectTime(this,'4:00 PM')">4:00 PM</button>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top:1.25rem">
                        <button onclick="bookDemo()" style="width:100%;padding:.9rem;background:linear-gradient(135deg,var(--accent),var(--green-500));color:#060d12;font-weight:700;font-size:.95rem;border-radius:var(--clay-radius-sm);border:none;cursor:pointer;font-family:inherit;box-shadow:0 6px 24px var(--accent-glow);transition:all .2s">📅 Confirm Demo Booking</button>
                        <p style="text-align:center;font-size:0.75rem;color:var(--base-muted);margin-top:.75rem">30-minute live demo with a SmartSpend product specialist. Free, no pressure.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="fpToast"></div>

    <script>
        function openDemoModal() { document.getElementById('demoOverlay').classList.add('open'); document.body.style.overflow = 'hidden'; }
        function closeDemoModal() { document.getElementById('demoOverlay').classList.remove('open'); document.body.style.overflow = ''; stopDemoPlay(); }
        function handleDemoOverlayClick(e) { if (e.target === document.getElementById('demoOverlay')) closeDemoModal(); }
        function switchDemoTab(btn, tab) {
            document.querySelectorAll('.demo-tab').forEach(b => b.classList.remove('active')); btn.classList.add('active');
            document.querySelectorAll('.demo-panel').forEach(p => p.style.display = 'none');
            var capitalized = tab.charAt(0).toUpperCase() + tab.slice(1);
            document.getElementById('demoPanel' + capitalized).style.display = 'block';
            if (tab !== 'video') stopDemoPlay();
        }
        var demoPlayTimer = null; var demoPlaySeconds = 0; var demoPlaying = false;
        function toggleDemoPlay() {
            demoPlaying = !demoPlaying; var btn = document.getElementById('demoPlayBtn');
            if (demoPlaying) {
                btn.innerHTML = '⏸'; btn.style.background = 'rgba(57,255,126,.25)';
                demoPlayTimer = setInterval(function() {
                    demoPlaySeconds += 1; var totalSec = 222; var pct = Math.min(100, (demoPlaySeconds / totalSec) * 100);
                    document.getElementById('demoProgress').style.width = pct + '%';
                    var m = Math.floor(demoPlaySeconds / 60); var s = demoPlaySeconds % 60;
                    document.getElementById('demoTimestamp').textContent = m + ':' + (s < 10 ? '0' : '') + s + ' / 3:42';
                    if (demoPlaySeconds >= totalSec) { stopDemoPlay(); showToastFpMain('Demo ended! Ready to get started?', 'success'); }
                }, 1000);
            } else { stopDemoPlay(); }
        }
        function stopDemoPlay() { clearInterval(demoPlayTimer); demoPlaying = false; var btn = document.getElementById('demoPlayBtn'); if (btn) { btn.innerHTML = '&#9654;'; btn.style.background = 'rgba(57,255,126,.15)'; } }
        function jumpDemo(seconds) {
            stopDemoPlay(); demoPlaySeconds = seconds; var totalSec = 222;
            document.getElementById('demoProgress').style.width = Math.min(100, (seconds / totalSec) * 100) + '%';
            var m = Math.floor(seconds / 60); var s = seconds % 60;
            document.getElementById('demoTimestamp').textContent = m + ':' + (s < 10 ? '0' : '') + s + ' / 3:42';
        }
        function scrubDemo(e, track) {
            var rect = track.getBoundingClientRect(); var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            demoPlaySeconds = Math.round(pct * 222); document.getElementById('demoProgress').style.width = (pct * 100) + '%';
            var m = Math.floor(demoPlaySeconds / 60); var s = demoPlaySeconds % 60;
            document.getElementById('demoTimestamp').textContent = m + ':' + (s < 10 ? '0' : '') + s + ' / 3:42';
        }
        var selectedDay = 'Mon 14 Apr'; var selectedTime = '10:00 AM';
        function selectDay(btn, day) { document.querySelectorAll('.demo-day-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active'); selectedDay = day; }
        function selectTime(btn, time) { document.querySelectorAll('.demo-time-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active'); selectedTime = time; }
        
        var PREVIEWS = {
            dashboard: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">📊 Dashboard Preview</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem"><div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid rgba(57,255,126,.2)"><div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Total Balance</div><div style="font-family:\\\'Syne\\\',sans-serif;font-size:1.4rem;font-weight:800;color:#39ff7e">₹1,28,450</div></div><div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid var(--base-border)"><div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Income</div><div style="font-family:\\\'Syne\\\',sans-serif;font-size:1.4rem;font-weight:800;color:#4ade80">₹85,000</div></div><div style="background:var(--base-card);border-radius:14px;padding:1rem;border:1px solid var(--base-border)"><div style="font-size:.7rem;color:var(--base-muted);margin-bottom:4px">Expenses</div><div style="font-family:\\\'Syne\\\',sans-serif;font-size:1.4rem;font-weight:800;color:#ff6b6b">₹43,240</div></div></div>',
            ai: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">🤖 AI Insight Preview</div><div style="background:linear-gradient(135deg,rgba(57,255,126,.06),var(--base-card));border:1px solid rgba(57,255,126,.2);border-radius:16px;padding:1.25rem"><p style="font-size:.9rem;color:var(--base-text);line-height:1.65">You\\\'ve spent <strong style="color:var(--accent)">₹8,420</strong> on dining — 40% above your ₹6,000 goal. Your biggest splurges were on <strong style="color:var(--accent)">weekends</strong>. Try meal-prepping Sunday to save ~₹2,000/month. 🍳</p></div>',
            ocr: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">📸 OCR Scan Preview</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem"><div style="background:var(--base-card);border-radius:14px;padding:1.25rem;border:1px solid var(--base-border);text-align:center"><div style="font-size:2rem;margin-bottom:.5rem">🧾</div><div style="font-size:.75rem;color:var(--base-muted)">Receipt uploaded</div><div style="font-size:.7rem;color:var(--accent);margin-top:.25rem">Processing...</div></div><div style="background:var(--accent-dim);border-radius:14px;padding:1.25rem;border:1px solid rgba(57,255,126,.2)"><div style="font-size:.7rem;color:var(--accent);font-weight:700;margin-bottom:.375rem">✓ Extracted</div><div style="font-size:1.1rem;font-weight:700;color:var(--accent)">₹2,340</div><div style="font-size:.75rem;color:var(--base-muted)">Amazon Fresh · Food<br>Apr 6, 2026</div></div></div>',
            voice: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">🎙️ Voice Entry Preview</div><div style="background:var(--base-card);border:1px solid var(--base-border);border-radius:14px;padding:1.25rem;margin-bottom:.75rem;font-size:.875rem;color:var(--base-muted);font-style:italic">"Spent 850 rupees on dinner at Social"</div><div style="background:var(--accent-dim);border:1px solid rgba(57,255,126,.2);border-radius:14px;padding:1rem"><div style="font-size:.75rem;color:var(--accent);font-weight:700;margin-bottom:4px">✓ Logged Successfully</div><div style="font-size:.85rem">Dining · ₹850 · Social Offline · Apr 10</div></div>',
            budget: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">🎯 Budget Tracker Preview</div><div style="display:flex;flex-direction:column;gap:.625rem"><div><div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:5px"><span>🍕 Food & Dining</span><span style="color:var(--base-muted)">₹8,420 / ₹12,000</span></div><div style="height:8px;background:var(--base-surface);border-radius:100px;overflow:hidden"><div style="width:70%;height:100%;background:linear-gradient(90deg,#39ff7e,#22c55e);border-radius:100px"></div></div></div><div><div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:5px"><span>🛍️ Shopping</span><span style="color:#ff6b6b">₹9,800 / ₹8,000</span></div><div style="height:8px;background:var(--base-surface);border-radius:100px;overflow:hidden"><div style="width:100%;height:100%;background:linear-gradient(90deg,#ff5f5f,#ef4444);border-radius:100px"></div></div></div><div><div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:5px"><span>🚗 Transport</span><span style="color:var(--base-muted)">₹4,200 / ₹5,000</span></div><div style="height:8px;background:var(--base-surface);border-radius:100px;overflow:hidden"><div style="width:84%;height:100%;background:linear-gradient(90deg,#fbbf24,#f59e0b);border-radius:100px"></div></div></div></div>',
            analytics: '<div style="font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem">📈 Analytics Preview</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.625rem"><div style="background:var(--base-card);border-radius:12px;padding:.75rem;border:1px solid var(--base-border);text-align:center"><div style="font-size:.65rem;color:var(--base-muted);margin-bottom:3px">Savings Rate</div><div style="font-family:\\\'Syne\\\',sans-serif;font-weight:800;color:var(--accent)">34.2%</div></div><div style="background:var(--base-card);border-radius:12px;padding:.75rem;border:1px solid var(--base-border);text-align:center"><div style="font-size:.65rem;color:var(--base-muted);margin-bottom:3px">Net Worth</div><div style="font-family:\\\'Syne\\\',sans-serif;font-weight:800;color:var(--accent)">+18.4%</div></div><div style="background:var(--base-card);border-radius:12px;padding:.75rem;border:1px solid var(--base-border);text-align:center"><div style="font-size:.65rem;color:var(--base-muted);margin-bottom:3px">Avg Daily</div><div style="font-family:\\\'Syne\\\',sans-serif;font-weight:800">₹2,402</div></div><div style="background:var(--base-card);border-radius:12px;padding:.75rem;border:1px solid var(--base-border);text-align:center"><div style="font-size:.65rem;color:var(--base-muted);margin-bottom:3px">Transactions</div><div style="font-family:\\\'Syne\\\',sans-serif;font-weight:800">247</div></div></div>',
        };
        function highlightFeature(card, type) {
            document.querySelectorAll('.demo-feature-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            var preview = document.getElementById('demoPreview');
            preview.style.opacity = '0';
            setTimeout(function() { preview.innerHTML = PREVIEWS[type] || ''; preview.style.opacity = '1'; }, 150);
        }
        var _toastTimer = null;
        function showToastFpMain(msg, type) {
            var toast = document.getElementById('fpToast');
            if (!toast) return;
            toast.textContent = (type === 'success' ? '✓  ' : '✕  ') + msg;
            toast.className = 'show ' + (type || '');
            clearTimeout(_toastTimer);
            _toastTimer = setTimeout(function() { toast.classList.remove('show'); }, 3200);
        }
        function bookDemo() {
            var name  = document.getElementById('bookName').value.trim();
            var email = document.getElementById('bookEmail').value.trim();
            if (!name)  { document.getElementById('bookName').focus();  showToastFpMain('Please enter your name', 'error');  return; }
            if (!email || !email.includes('@')) { document.getElementById('bookEmail').focus(); showToastFpMain('Please enter a valid email', 'error'); return; }
            document.getElementById('demoPanelBookContent').innerHTML =
                '<div style="text-align:center;padding:2rem 0">' +
                  '<div style="width:72px;height:72px;border-radius:50%;background:rgba(57,255,126,.1);border:2px solid rgba(57,255,126,.28);display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem;animation:fp-pop .45s var(--ease)">' +
                    '<svg width="30" height="30" fill="none" stroke="var(--accent)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>' +
                  '</div>' +
                  '<div style="font-family:\\\'Syne\\\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:.5rem">Booking Confirmed! 🎉</div>' +
                  '<div style="font-size:.875rem;color:var(--base-muted);line-height:1.65;max-width:340px;margin:0 auto 1.5rem">' +
                    'Your demo is booked for <strong style="color:var(--base-text)">' + selectedDay + ' at ' + selectedTime + ' IST</strong>. ' +
                    'A calendar invite has been sent to <strong style="color:var(--accent)">' + email + '</strong>.' +
                  '</div>' +
                  '<button onclick="closeDemoModal()" style="padding:.85rem 2rem;background:linear-gradient(135deg,var(--accent),var(--green-500));color:#060d12;font-weight:700;font-size:.95rem;border-radius:var(--clay-radius);border:none;cursor:pointer;font-family:inherit;box-shadow:0 8px 24px var(--accent-glow)">Close</button>' +
                '</div>';
            showToastFpMain('Demo booked successfully!', 'success');
        }
    </script>
"""

if "id=\"demoOverlay\"" not in content:
    content = content.replace("</body>", html_and_js_add + "\n</body>")

with open('templates/SmartSpend.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully.")
