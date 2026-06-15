"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";
const HOTEL_ID = 1;

const TABS = [
  { key: "config", label: "AI Concierge", icon: "ti ti-settings" },
  { key: "intents", label: "Intent'ler", icon: "ti ti-bulb" },
  { key: "conversations", label: "Konu\u015fmalar", icon: "ti ti-messages" },
  { key: "kb", label: "SSS", icon: "ti ti-book" },
  { key: "sequences", label: "Otomasyon", icon: "ti ti-automation" },
  { key: "analytics", label: "Analytics", icon: "ti ti-chart-bar" },
];

const TRIGGER_EVENTS = [
  { value: "booking_confirmed", label: "Rezervasyon Onay\u0131" },
  { value: "pre_arrival", label: "Var\u0131\u015f \u00d6ncesi" },
  { value: "checkin", label: "Giri\u015f" },
  { value: "in_stay", label: "Konaklama" },
  { value: "post_checkout", label: "\u00c7\u0131k\u0131\u015f Sonras\u0131" },
];

export default function AiConciergePage() {
  const router = useRouter();
  const [tab, setTab] = useState("config");
  const [config, setConfig] = useState<any>({});
  const [intents, setIntents] = useState<any[]>([]);
  const [conversations, setConversations] = useState<any[]>([]);
  const [kbEntries, setKbEntries] = useState<any[]>([]);
  const [sequences, setSequences] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAll() {
      setLoading(true);
      try {
        const [cfg, ints, convs, kb, seqs, anl] = await Promise.all([
          fetch(`${API}/ai-concierge/config/${HOTEL_ID}`).then(r => r.ok ? r.json() : {}),
          fetch(`${API}/ai-concierge/intents/${HOTEL_ID}`).then(r => r.ok ? r.json() : []),
          fetch(`${API}/ai-concierge/conversations/${HOTEL_ID}`).then(r => r.ok ? r.json() : []),
          fetch(`${API}/ai-concierge/knowledge-base/${HOTEL_ID}`).then(r => r.ok ? r.json() : []),
          fetch(`${API}/ai-concierge/sequences/${HOTEL_ID}`).then(r => r.ok ? r.json() : []),
          fetch(`${API}/ai-concierge/analytics/${HOTEL_ID}`).then(r => r.ok ? r.json() : {}),
        ]);
        setConfig(cfg);
        setIntents(ints);
        setConversations(convs);
        setKbEntries(kb);
        setSequences(seqs);
        setAnalytics(anl);
      } catch (_) {}
      setLoading(false);
    }
    loadAll();
  }, []);

  async function updateConfig() {
    await fetch(`${API}/ai-concierge/config/${HOTEL_ID}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config),
    });
  }

  async function saveIntent(intent: any) {
    if (intent.id) {
      await fetch(`${API}/ai-concierge/intents/${intent.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(intent),
      });
    } else {
      await fetch(`${API}/ai-concierge/intents`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...intent, hotel_id: HOTEL_ID }),
      });
    }
  }

  async function saveKb(entry: any) {
    await fetch(`${API}/ai-concierge/knowledge-base`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...entry, hotel_id: HOTEL_ID }),
    });
  }

  async function saveSequence(seq: any) {
    await fetch(`${API}/ai-concierge/sequences`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...seq, hotel_id: HOTEL_ID }),
    });
  }

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <style>{`
        .card { background: #fff; border: 1px solid #D6E4FA; border-radius: 12; padding: 20; }
        .card:hover { border-color: #4A7FD4; }
        .btn { padding: 8px 16px; border-radius: 8; border: none; font-family: inherit; font-size: 13; font-weight: 600; cursor: pointer; }
        .btn-primary { background: #4A7FD4; color: #fff; }
        .btn-primary:hover { background: #3A6FC4; }
        .btn-outline { background: transparent; border: 1px solid #D6E4FA; color: #1A2B4A; }
        .btn-outline:hover { border-color: #4A7FD4; color: #4A7FD4; }
        .badge { font-size: 11; font-weight: 600; padding: 2px 10px; border-radius: 20; background: #EEF4FF; color: #4A7FD4; border: 1px solid #D6E4FA; }
        input, select, textarea { font-family: inherit; font-size: 13; padding: 8px 12px; border: 1px solid #D6E4FA; border-radius: 8; background: #fff; color: #1A2B4A; outline: none; }
        input:focus, select:focus, textarea:focus { border-color: #4A7FD4; }
        textarea { resize: vertical; min-height: 60px; }
      `}</style>

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#4A7FD4", fontWeight: 600, cursor: "pointer" }}>AI Concierge</span>
        </div>
      </nav>

      <div style={{ padding: "24px 32px", maxWidth: 1200, margin: "0 auto" }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: -1, marginBottom: 4 }}>AI Concierge</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 24 }}>Ak\u0131ll\u0131 misafir mesajla\u015fma ve concierge y\u00f6netimi</p>

        <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
          {TABS.map(t => (
            <button key={t.key} onClick={() => setTab(t.key)} className="btn" style={{
              background: tab === t.key ? "#4A7FD4" : "transparent",
              color: tab === t.key ? "#fff" : "#5A7499",
              border: tab === t.key ? "none" : "1px solid #D6E4FA",
            }}>
              <i className={t.icon} style={{ marginRight: 6, fontSize: 14 }} />{t.label}
            </button>
          ))}
        </div>

        {loading ? (
          <p style={{ color: "#8FAAC8", fontSize: 14 }}>Y\u00fckleniyor...</p>
        ) : (
          <>
            {tab === "config" && (
              <div className="card" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>AI Concierge Ayarlar\u0131</h2>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140 }}>Aktif / Pasif</span>
                  <button onClick={() => { setConfig({ ...config, is_active: !config.is_active }); setTimeout(updateConfig, 100); }} className="btn" style={{
                    background: config.is_active ? "#4A7FD4" : "#E8EDF5", color: config.is_active ? "#fff" : "#5A7499",
                  }}>
                    <i className={`ti ti-${config.is_active ? "toggle-right" : "toggle-left"}`} style={{ marginRight: 6 }} />
                    {config.is_active ? "Aktif" : "Pasif"}
                  </button>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140 }}>Dil</span>
                  <select value={config.language || "tr"} onChange={e => setConfig({ ...config, language: e.target.value })}>
                    <option value="tr">T\u00fcrk\u00e7e</option>
                    <option value="en">English</option>
                    <option value="de">Deutsch</option>
                    <option value="ru">Русский</option>
                    <option value="ar">العربية</option>
                  </select>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140 }}>Çalışma Saatleri</span>
                  <input type="time" value={config.operating_hours_start || "00:00"} onChange={e => setConfig({ ...config, operating_hours_start: e.target.value })} style={{ width: 100 }} />
                  <span style={{ color: "#8FAAC8" }}>-</span>
                  <input type="time" value={config.operating_hours_end || "23:59"} onChange={e => setConfig({ ...config, operating_hours_end: e.target.value })} style={{ width: 100 }} />
                </div>
                <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140, paddingTop: 8 }}>Karşılama Mesajı</span>
                  <textarea value={config.greeting_message || ""} onChange={e => setConfig({ ...config, greeting_message: e.target.value })} style={{ flex: 1 }} rows={3} />
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140 }}>İnsana Yönlendirme</span>
                  <span style={{ fontSize: 13, color: "#8FAAC8" }}>Mesaj sayısı:</span>
                  <input type="number" min={1} value={config.escalation_threshold || 3} onChange={e => setConfig({ ...config, escalation_threshold: parseInt(e.target.value) || 3 })} style={{ width: 60 }} />
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 140 }}>WhatsApp</span>
                  <button onClick={() => { setConfig({ ...config, whatsapp_enabled: !config.whatsapp_enabled }); setTimeout(updateConfig, 100); }} className="btn" style={{
                    background: config.whatsapp_enabled ? "#4A7FD4" : "#E8EDF5", color: config.whatsapp_enabled ? "#fff" : "#5A7499",
                  }}>
                    <i className={`ti ti-${config.whatsapp_enabled ? "toggle-right" : "toggle-left"}`} style={{ marginRight: 6 }} />
                    {config.whatsapp_enabled ? "Aktif" : "Pasif"}
                  </button>
                  {config.whatsapp_enabled && (
                    <input type="text" placeholder="+905551234567" value={config.whatsapp_number || ""} onChange={e => setConfig({ ...config, whatsapp_number: e.target.value })} style={{ width: 200 }} />
                  )}
                </div>
                <div>
                  <button onClick={updateConfig} className="btn btn-primary"><i className="ti ti-device-floppy" style={{ marginRight: 6 }} />Kaydet</button>
                </div>
              </div>
            )}

            {tab === "intents" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <div style={{ display: "flex", justifyContent: "flex-end" }}>
                  <button onClick={() => setIntents([...intents, { hotel_id: HOTEL_ID, intent_key: "", trigger_phrases: [], response_template: "", requires_human: false, is_active: true }])} className="btn btn-primary">
                    <i className="ti ti-plus" style={{ marginRight: 6 }} />Yeni Intent
                  </button>
                </div>
                {intents.map((intent, i) => (
                  <div key={i} className="card" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                      <input placeholder="intent_key" value={intent.intent_key} onChange={e => { const copy = [...intents]; copy[i] = { ...copy[i], intent_key: e.target.value }; setIntents(copy); }} style={{ width: 180 }} />
                      <label style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 4 }}>
                        <input type="checkbox" checked={intent.requires_human} onChange={e => { const copy = [...intents]; copy[i] = { ...copy[i], requires_human: e.target.checked }; setIntents(copy); }} />
                        İnsan gerekli
                      </label>
                    </div>
                    <div>
                      <div style={{ fontSize: 12, color: "#8FAAC8", marginBottom: 4 }}>Tetikleyici kelimeler (virgülle ayırın)</div>
                      <input style={{ width: "100%" }} placeholder="checkout, check-out, çıkış" value={(intent.trigger_phrases || []).join(", ")} onChange={e => { const copy = [...intents]; copy[i] = { ...copy[i], trigger_phrases: e.target.value.split(",").map((s: string) => s.trim()).filter(Boolean) }; setIntents(copy); }} />
                    </div>
                    <div>
                      <div style={{ fontSize: 12, color: "#8FAAC8", marginBottom: 4 }}>Yanıt şablonu</div>
                      <textarea style={{ width: "100%" }} rows={2} value={intent.response_template || ""} onChange={e => { const copy = [...intents]; copy[i] = { ...copy[i], response_template: e.target.value }; setIntents(copy); }} />
                    </div>
                    <div>
                      <button onClick={() => saveIntent(intent)} className="btn btn-primary"><i className="ti ti-device-floppy" style={{ marginRight: 6 }} />Kaydet</button>
                    </div>
                  </div>
                ))}
                {intents.length === 0 && <p style={{ color: "#8FAAC8", fontSize: 14, textAlign: "center", padding: 40 }}>Henüz intent eklenmemiş</p>}
              </div>
            )}

            {tab === "conversations" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {conversations.length === 0 ? (
                  <p style={{ color: "#8FAAC8", fontSize: 14, textAlign: "center", padding: 40 }}>Henüz konuşma yok</p>
                ) : (
                  conversations.map((conv: any) => (
                    <div key={conv.id} className="card">
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                          <span className="badge">{conv.channel}</span>
                          <span className="badge" style={{
                            background: conv.status === "active" ? "#E8F5E9" : conv.status === "escalated" ? "#FFF3E0" : "#EEF4FF",
                            color: conv.status === "active" ? "#2E7D32" : conv.status === "escalated" ? "#E65100" : "#4A7FD4",
                            borderColor: conv.status === "active" ? "#A5D6A7" : conv.status === "escalated" ? "#FFCC80" : "#D6E4FA",
                          }}>{conv.status}</span>
                        </div>
                        <span style={{ fontSize: 11, color: "#8FAAC8" }}>{conv.created_at?.slice(0, 10)}</span>
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: 6, maxHeight: 200, overflowY: "auto" }}>
                        {(conv.messages || []).map((m: any) => (
                          <div key={m.id} style={{
                            padding: "6px 12px", borderRadius: 8, fontSize: 13,
                            background: m.sender_type === "guest" ? "#EEF4FF" : m.sender_type === "ai" ? "#E8F5E9" : "#FFF3E0",
                            alignSelf: m.sender_type === "guest" ? "flex-start" : "flex-end",
                            maxWidth: "80%",
                          }}>
                            <div style={{ fontSize: 10, color: "#8FAAC8", marginBottom: 2 }}>
                              {m.sender_type === "guest" ? "Misafir" : m.sender_type === "ai" ? "AI" : "İnsan"}
                              {m.intent_matched && <span style={{ marginLeft: 8 }}>#{m.intent_matched}</span>}
                            </div>
                            {m.message}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {tab === "kb" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <div style={{ display: "flex", justifyContent: "flex-end" }}>
                  <button onClick={() => setKbEntries([...kbEntries, { hotel_id: HOTEL_ID, category: "", question: "", answer: "" }])} className="btn btn-primary">
                    <i className="ti ti-plus" style={{ marginRight: 6 }} />Yeni SSS
                  </button>
                </div>
                {kbEntries.map((entry, i) => (
                  <div key={i} className="card" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    <input placeholder="Kategori (genel, wifi, kahvaltı...)" value={entry.category || ""} onChange={e => { const copy = [...kbEntries]; copy[i] = { ...copy[i], category: e.target.value }; setKbEntries(copy); }} style={{ width: 250 }} />
                    <input placeholder="Soru" value={entry.question || ""} onChange={e => { const copy = [...kbEntries]; copy[i] = { ...copy[i], question: e.target.value }; setKbEntries(copy); }} />
                    <textarea placeholder="Cevap" rows={2} value={entry.answer || ""} onChange={e => { const copy = [...kbEntries]; copy[i] = { ...copy[i], answer: e.target.value }; setKbEntries(copy); }} />
                    <div><button onClick={() => saveKb(entry)} className="btn btn-primary"><i className="ti ti-device-floppy" style={{ marginRight: 6 }} />Kaydet</button></div>
                  </div>
                ))}
                {kbEntries.length === 0 && <p style={{ color: "#8FAAC8", fontSize: 14, textAlign: "center", padding: 40 }}>Henüz SSS eklenmemiş</p>}
              </div>
            )}

            {tab === "sequences" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <div style={{ display: "flex", justifyContent: "flex-end" }}>
                  <button onClick={() => setSequences([...sequences, { hotel_id: HOTEL_ID, name: "", trigger_event: "booking_confirmed", delay_hours: 0, message_template: "", channel: "in_app" }])} className="btn btn-primary">
                    <i className="ti ti-plus" style={{ marginRight: 6 }} />Yeni Sequence
                  </button>
                </div>
                {sequences.map((seq, i) => (
                  <div key={i} className="card" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                      <input placeholder="Sequence adı" value={seq.name || ""} onChange={e => { const copy = [...sequences]; copy[i] = { ...copy[i], name: e.target.value }; setSequences(copy); }} style={{ flex: 1 }} />
                      <select value={seq.trigger_event || "booking_confirmed"} onChange={e => { const copy = [...sequences]; copy[i] = { ...copy[i], trigger_event: e.target.value }; setSequences(copy); }}>
                        {TRIGGER_EVENTS.map(ev => <option key={ev.value} value={ev.value}>{ev.label}</option>)}
                      </select>
                      <input type="number" min={0} placeholder="Gecikme (saat)" value={seq.delay_hours || 0} onChange={e => { const copy = [...sequences]; copy[i] = { ...copy[i], delay_hours: parseInt(e.target.value) || 0 }; setSequences(copy); }} style={{ width: 80 }} />
                      <select value={seq.channel || "in_app"} onChange={e => { const copy = [...sequences]; copy[i] = { ...copy[i], channel: e.target.value }; setSequences(copy); }}>
                        <option value="in_app">In-App</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="email">E-posta</option>
                      </select>
                    </div>
                    <textarea placeholder="Mesaj şablonu" rows={2} value={seq.message_template || ""} onChange={e => { const copy = [...sequences]; copy[i] = { ...copy[i], message_template: e.target.value }; setSequences(copy); }} />
                    <div><button onClick={() => saveSequence(seq)} className="btn btn-primary"><i className="ti ti-device-floppy" style={{ marginRight: 6 }} />Kaydet</button></div>
                  </div>
                ))}
                {sequences.length === 0 && <p style={{ color: "#8FAAC8", fontSize: 14, textAlign: "center", padding: 40 }}>Henüz sequence eklenmemiş</p>}
              </div>
            )}

            {tab === "analytics" && (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16 }}>
                <div className="card" style={{ textAlign: "center" }}>
                  <i className="ti ti-messages" style={{ fontSize: 28, color: "#4A7FD4", marginBottom: 8 }} />
                  <div style={{ fontSize: 28, fontWeight: 700 }}>{analytics.total_conversations || 0}</div>
                  <div style={{ fontSize: 12, color: "#8FAAC8" }}>Toplam Konu\u015fma</div>
                </div>
                <div className="card" style={{ textAlign: "center" }}>
                  <i className="ti ti-circle-check" style={{ fontSize: 28, color: "#2E7D32", marginBottom: 8 }} />
                  <div style={{ fontSize: 28, fontWeight: 700 }}>{analytics.resolved || 0}</div>
                  <div style={{ fontSize: 12, color: "#8FAAC8" }}>Çözümlenen</div>
                </div>
                <div className="card" style={{ textAlign: "center" }}>
                  <i className="ti ti-alert-triangle" style={{ fontSize: 28, color: "#E65100", marginBottom: 8 }} />
                  <div style={{ fontSize: 28, fontWeight: 700 }}>{analytics.escalated || 0}</div>
                  <div style={{ fontSize: 12, color: "#8FAAC8" }}>Yönlendirilen</div>
                </div>
                <div className="card" style={{ textAlign: "center" }}>
                  <i className="ti ti-percentage" style={{ fontSize: 28, color: "#4A7FD4", marginBottom: 8 }} />
                  <div style={{ fontSize: 28, fontWeight: 700 }}>%{analytics.resolution_rate || 0}</div>
                  <div style={{ fontSize: 12, color: "#8FAAC8" }}>Çözüm Oranı</div>
                </div>
                <div className="card" style={{ textAlign: "center" }}>
                  <i className="ti ti-users" style={{ fontSize: 28, color: "#4A7FD4", marginBottom: 8 }} />
                  <div style={{ fontSize: 28, fontWeight: 700 }}>{analytics.active || 0}</div>
                  <div style={{ fontSize: 12, color: "#8FAAC8" }}>Aktif Konu\u015fma</div>
                </div>
                {analytics.common_intents && analytics.common_intents.length > 0 && (
                  <div className="card" style={{ gridColumn: "1 / -1" }}>
                    <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>En Sık Eşleşen Intent'ler</h3>
                    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                      {analytics.common_intents.map((item: any, i: number) => (
                        <div key={i} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                          <span className="badge" style={{ minWidth: 80, textAlign: "center" }}>{item.intent}</span>
                          <div style={{ flex: 1, height: 8, background: "#EEF4FF", borderRadius: 4, overflow: "hidden" }}>
                            <div style={{ height: "100%", width: `${Math.min(100, (item.count / Math.max(...analytics.common_intents.map((x: any) => x.count))) * 100)}%`, background: "#4A7FD4", borderRadius: 4 }} />
                          </div>
                          <span style={{ fontSize: 12, color: "#8FAAC8", minWidth: 30, textAlign: "right" }}>{item.count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}
