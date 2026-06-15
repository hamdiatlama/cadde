"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const PLATFORM_NAMES: Record<string, string> = {
  booking_com: "Booking.com",
  google: "Google",
  tripadvisor: "TripAdvisor",
  expedia: "Expedia",
};

const PLATFORM_ICONS: Record<string, string> = {
  booking_com: "ti-building",
  google: "ti-brand-google",
  tripadvisor: "ti-brand-tripadvisor",
  expedia: "ti-plane",
};

export default function ReputationPage() {
  const router = useRouter();
  const [hotelId, setHotelId] = useState("1");
  const [dashboard, setDashboard] = useState<any>(null);
  const [reviews, setReviews] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [sentiment, setSentiment] = useState<any>(null);
  const [tab, setTab] = useState("dashboard");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const [filterPlatform, setFilterPlatform] = useState("");
  const [filterSentiment, setFilterSentiment] = useState("");

  const [responseText, setResponseText] = useState("");
  const [respondingReview, setRespondingReview] = useState<number | null>(null);

  const [importForm, setImportForm] = useState({ platform: "booking_com", reviewer_name: "", rating: 5, comment: "" });

  useEffect(() => {
    if (!hotelId) return;
    async function load() {
      setLoading(true);
      try {
        const [dashRes, revRes, alertRes, sentRes] = await Promise.all([
          fetch(`${API}/reputation/${hotelId}`),
          fetch(`${API}/reputation/${hotelId}/reviews`),
          fetch(`${API}/reputation/${hotelId}/alerts`),
          fetch(`${API}/reputation/${hotelId}/sentiment`),
        ]);
        if (dashRes.ok) setDashboard(await dashRes.json());
        if (revRes.ok) setReviews(await revRes.json());
        if (alertRes.ok) setAlerts(await alertRes.json());
        if (sentRes.ok) setSentiment(await sentRes.json());
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, [hotelId]);

  async function handleImportReview() {
    if (!importForm.reviewer_name || !importForm.comment) return;
    try {
      const res = await fetch(`${API}/reputation/${hotelId}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...importForm, external_review_id: `ext_${Date.now()}` }),
      });
      if (res.ok) {
        setMsg("Değerlendirme içe aktarıldı");
        setImportForm({ platform: "booking_com", reviewer_name: "", rating: 5, comment: "" });
        const revRes = await fetch(`${API}/reputation/${hotelId}/reviews`);
        if (revRes.ok) setReviews(await revRes.json());
      } else {
        const err = await res.json();
        setMsg("Hata: " + (err.detail || "Bilinmeyen hata"));
      }
    } catch (_) {
      setMsg("Bağlantı hatası");
    }
  }

  async function handleRespond(reviewId: number) {
    if (!responseText.trim()) return;
    try {
      const res = await fetch(`${API}/reputation/reviews/${reviewId}/respond`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ response_text: responseText }),
      });
      if (res.ok) {
        setMsg("Yanıt kaydedildi");
        setResponseText("");
        setRespondingReview(null);
        const revRes = await fetch(`${API}/reputation/${hotelId}/reviews`);
        if (revRes.ok) setReviews(await revRes.json());
      } else {
        const err = await res.json();
        setMsg("Hata: " + (err.detail || "Bilinmeyen hata"));
      }
    } catch (_) {
      setMsg("Bağlantı hatası");
    }
  }

  async function handleResolveAlert(alertId: number) {
    try {
      const res = await fetch(`${API}/reputation/alerts/${alertId}/resolve`, { method: "PUT" });
      if (res.ok) {
        setMsg("Uyarı çözüldü");
        const alertRes = await fetch(`${API}/reputation/${hotelId}/alerts`);
        if (alertRes.ok) setAlerts(await alertRes.json());
      }
    } catch (_) {}
  }

  async function handleRecalculate() {
    try {
      const res = await fetch(`${API}/reputation/${hotelId}/recalculate`, { method: "POST" });
      if (res.ok) {
        setMsg("Puan yeniden hesaplandı");
        const dashRes = await fetch(`${API}/reputation/${hotelId}`);
        if (dashRes.ok) setDashboard(await dashRes.json());
      }
    } catch (_) {}
  }

  async function handleFilter() {
    const params = new URLSearchParams();
    if (filterPlatform) params.set("platform", filterPlatform);
    if (filterSentiment) params.set("sentiment", filterSentiment);
    try {
      const res = await fetch(`${API}/reputation/${hotelId}/reviews?${params}`);
      if (res.ok) setReviews(await res.json());
    } catch (_) {}
  }

  const profile = dashboard?.profile;
  const platformScores = profile?.platform_scores || {};
  const sentimentBreakdown = sentiment?.breakdown || {};
  const sentimentKeywords = sentiment?.keywords || [];
  const sentimentCategories = sentiment?.categories || [];

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "24px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 }}>
          <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.8 }}>İtibar Yönetimi</h1>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <input type="number" value={hotelId} onChange={e => setHotelId(e.target.value)}
              style={{ width: 80, padding: "6px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
            <span style={{ fontSize: 12, color: "#8FAAC8" }}>Otel ID</span>
          </div>
        </div>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20 }}>Çevrimiçi itibar takibi ve yönetimi</p>

        <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
          {[
            { key: "dashboard", label: "Dashboard", icon: "ti-dashboard" },
            { key: "reviews", label: "Değerlendirmeler", icon: "ti-message" },
            { key: "import", label: "İçe Aktar", icon: "ti-upload" },
            { key: "sentiment", label: "Duygu Analizi", icon: "ti-heart-rate" },
            { key: "alerts", label: "Uyarılar", icon: "ti-alert-triangle" },
          ].map(t => (
            <button key={t.key} onClick={() => { setTab(t.key); setMsg(""); }}
              style={{ padding: "8px 16px", background: tab === t.key ? "#4A7FD4" : "#fff", color: tab === t.key ? "#fff" : "#5A7499", border: `1px solid ${tab === t.key ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
              <i className={`ti ${t.icon}`} style={{ fontSize: 14 }} /> {t.label}
            </button>
          ))}
        </div>

        {msg && (
          <div style={{ padding: "10px 14px", borderRadius: 8, background: msg.includes("❌") || msg.includes("Hata") ? "#fef2f2" : "#dcfce7", color: msg.includes("❌") || msg.includes("Hata") ? "#dc2626" : "#16a34a", fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
            {msg}
          </div>
        )}

        {loading && <p style={{ fontSize: 13, color: "#8FAAC8" }}>Yükleniyor...</p>}

        {tab === "dashboard" && !loading && (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 12, marginBottom: 20 }}>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "16px" }}>
                <i className="ti ti-star" style={{ fontSize: 18, color: "#f59e0b" }} />
                <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>Genel Puan</div>
                <div style={{ fontSize: 24, fontWeight: 700, marginTop: 2 }}>{profile?.overall_score?.toFixed(1) || "0.0"}</div>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "16px" }}>
                <i className="ti ti-message" style={{ fontSize: 18, color: "#4A7FD4" }} />
                <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>Toplam Değerlendirme</div>
                <div style={{ fontSize: 24, fontWeight: 700, marginTop: 2 }}>{profile?.review_count || 0}</div>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "16px" }}>
                <i className="ti ti-message-reply" style={{ fontSize: 18, color: "#16a34a" }} />
                <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>Yanıtlama Oranı</div>
                <div style={{ fontSize: 24, fontWeight: 700, marginTop: 2 }}>{((profile?.response_rate || 0) * 100).toFixed(0)}%</div>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "16px" }}>
                <i className="ti ti-clock" style={{ fontSize: 18, color: "#8b5cf6" }} />
                <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>Ort. Yanıt Süresi</div>
                <div style={{ fontSize: 24, fontWeight: 700, marginTop: 2 }}>{profile?.avg_response_time_hours ? `${profile.avg_response_time_hours}s` : "-"}</div>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 12, marginBottom: 20 }}>
              {Object.keys(PLATFORM_NAMES).map(p => (
                <div key={p} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "14px 16px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <i className={`ti ${PLATFORM_ICONS[p] || "ti-world"}`} style={{ fontSize: 14, color: "#4A7FD4" }} />
                    <span style={{ fontSize: 11, color: "#8FAAC8" }}>{PLATFORM_NAMES[p]}</span>
                  </div>
                  <div style={{ fontSize: 18, fontWeight: 700, marginTop: 4 }}>
                    {platformScores[p]?.toFixed(1) || "-"}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
              <button onClick={handleRecalculate}
                style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                <i className="ti ti-refresh" /> Puanı Yenile
              </button>
            </div>

            {dashboard?.recent_reviews && dashboard.recent_reviews.length > 0 && (
              <div style={{ marginBottom: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Son Değerlendirmeler</h3>
                {dashboard.recent_reviews.slice(0, 5).map((r: any) => (
                  <div key={r.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "10px 14px", marginBottom: 6 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, padding: "2px 6px", borderRadius: 4, background: "#e0e7ff", color: "#4A7FD4" }}>{PLATFORM_NAMES[r.platform] || r.platform}</span>
                      <span style={{ fontSize: 12, fontWeight: 700, color: "#f59e0b" }}>{"★".repeat(Math.round(r.rating))}{"☆".repeat(5 - Math.round(r.rating))}</span>
                      <span style={{ fontSize: 11, color: "#8FAAC8" }}>{r.reviewer_name}</span>
                      {r.is_responded && <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 6px", borderRadius: 10, background: "#dcfce7", color: "#16a34a" }}>Yanıtlandı</span>}
                    </div>
                    <p style={{ fontSize: 12, color: "#5A7499", margin: 0 }}>{r.comment?.substring(0, 120)}{r.comment?.length > 120 ? "..." : ""}</p>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {tab === "reviews" && !loading && (
          <>
            <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
              <select value={filterPlatform} onChange={e => setFilterPlatform(e.target.value)}
                style={{ padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff", outline: "none" }}>
                <option value="">Tüm Platformlar</option>
                {Object.entries(PLATFORM_NAMES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
              <select value={filterSentiment} onChange={e => setFilterSentiment(e.target.value)}
                style={{ padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff", outline: "none" }}>
                <option value="">Tüm Duygular</option>
                <option value="positive">Pozitif</option>
                <option value="neutral">Nötr</option>
                <option value="negative">Negatif</option>
              </select>
              <button onClick={handleFilter}
                style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                <i className="ti ti-filter" style={{ marginRight: 4 }} />Filtrele
              </button>
            </div>

            {reviews.length === 0 ? (
              <p style={{ fontSize: 13, color: "#8FAAC8" }}>Henüz değerlendirme yok</p>
            ) : reviews.map((r: any) => (
              <div key={r.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "12px 14px", marginBottom: 8 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 11, fontWeight: 700, padding: "2px 6px", borderRadius: 4, background: "#e0e7ff", color: "#4A7FD4" }}>{PLATFORM_NAMES[r.platform] || r.platform}</span>
                  <span style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b" }}>{"★".repeat(Math.round(r.rating))}{"☆".repeat(5 - Math.round(r.rating))}</span>
                  <span style={{ fontSize: 12, fontWeight: 600 }}>{r.reviewer_name}</span>
                  {r.sentiment && (
                    <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 8px", borderRadius: 10, background: r.sentiment === "positive" ? "#dcfce7" : r.sentiment === "negative" ? "#fef2f2" : "#fef3c7", color: r.sentiment === "positive" ? "#16a34a" : r.sentiment === "negative" ? "#dc2626" : "#d97706" }}>
                      {r.sentiment === "positive" ? "Pozitif" : r.sentiment === "negative" ? "Negatif" : "Nötr"}
                    </span>
                  )}
                  {r.is_responded && <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 6px", borderRadius: 10, background: "#dcfce7", color: "#16a34a" }}>Yanıtlandı</span>}
                </div>
                {r.title && <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 2 }}>{r.title}</div>}
                <p style={{ fontSize: 12, color: "#5A7499", margin: "0 0 4px 0" }}>{r.comment}</p>
                {r.response && (
                  <div style={{ marginTop: 6, padding: "8px 10px", background: "#f0f4ff", borderRadius: 6, borderLeft: "3px solid #4A7FD4" }}>
                    <span style={{ fontSize: 10, fontWeight: 600, color: "#4A7FD4" }}>Yanıtınız:</span>
                    <p style={{ fontSize: 11, color: "#5A7499", margin: "2px 0 0 0" }}>{r.response}</p>
                  </div>
                )}
                {!r.is_responded && (
                  <div style={{ marginTop: 8 }}>
                    {respondingReview === r.id ? (
                      <div>
                        <textarea value={responseText} onChange={e => setResponseText(e.target.value)} placeholder="Yanıtınızı yazın..."
                          style={{ width: "100%", padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 60, boxSizing: "border-box" }} />
                        <div style={{ display: "flex", gap: 6, marginTop: 6 }}>
                          <button onClick={() => handleRespond(r.id)}
                            style={{ padding: "6px 12px", background: "#16a34a", color: "#fff", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                            <i className="ti ti-send" style={{ marginRight: 4 }} />Gönder
                          </button>
                          <button onClick={() => { setRespondingReview(null); setResponseText(""); }}
                            style={{ padding: "6px 12px", background: "#fff", color: "#5A7499", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                            İptal
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button onClick={() => setRespondingReview(r.id)}
                        style={{ padding: "6px 12px", background: "#fff", color: "#4A7FD4", border: "1px solid #4A7FD4", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                        <i className="ti ti-message-reply" style={{ marginRight: 4 }} />Yanıtla
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </>
        )}

        {tab === "import" && !loading && (
          <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 500 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16 }}>Değerlendirme İçe Aktar</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <select value={importForm.platform} onChange={e => setImportForm(p => ({ ...p, platform: e.target.value }))}
                style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                <option value="booking_com">Booking.com</option>
                <option value="google">Google</option>
                <option value="tripadvisor">TripAdvisor</option>
                <option value="expedia">Expedia</option>
              </select>
              <input type="text" placeholder="İsim *" value={importForm.reviewer_name} onChange={e => setImportForm(p => ({ ...p, reviewer_name: e.target.value }))}
                style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 12, color: "#5A7499" }}>Puan:</span>
                <select value={importForm.rating} onChange={e => setImportForm(p => ({ ...p, rating: parseInt(e.target.value) }))}
                  style={{ padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 13, fontFamily: "inherit", background: "#fff", outline: "none" }}>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              </div>
              <textarea placeholder="Yorum *" value={importForm.comment} onChange={e => setImportForm(p => ({ ...p, comment: e.target.value }))}
                style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 80 }} />
              <button onClick={handleImportReview}
                style={{ padding: "12px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", marginTop: 8 }}>
                <i className="ti ti-upload" style={{ marginRight: 6 }} />İçe Aktar
              </button>
            </div>
          </div>
        )}

        {tab === "sentiment" && !loading && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 12, marginBottom: 20 }}>
              {["positive", "neutral", "negative"].map(s => {
                const data = sentimentBreakdown[s] || { count: 0, avg_score: 0 };
                const colors: Record<string, { bg: string; icon: string; text: string }> = {
                  positive: { bg: "#dcfce7", icon: "ti-mood-smile", text: "#16a34a" },
                  neutral: { bg: "#fef3c7", icon: "ti-mood-empty", text: "#d97706" },
                  negative: { bg: "#fef2f2", icon: "ti-mood-sad", text: "#dc2626" },
                };
                const c = colors[s];
                return (
                  <div key={s} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "14px 16px" }}>
                    <i className={`ti ${c.icon}`} style={{ fontSize: 18, color: c.text }} />
                    <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>{s === "positive" ? "Pozitif" : s === "negative" ? "Negatif" : "Nötr"}</div>
                    <div style={{ fontSize: 18, fontWeight: 700, marginTop: 2 }}>{data.count}</div>
                    <div style={{ fontSize: 11, color: "#8FAAC8" }}>Puan: {data.avg_score?.toFixed(2) || "0"}</div>
                  </div>
                );
              })}
            </div>

            {sentimentCategories.length > 0 && (
              <div style={{ marginBottom: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Kategori Bazında Analiz</h3>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))", gap: 8 }}>
                  {sentimentCategories.map((c: any) => (
                    <div key={c.category} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "10px 14px", textAlign: "center" }}>
                      <div style={{ fontSize: 12, fontWeight: 600, color: "#4A7FD4", marginBottom: 4 }}>{c.category}</div>
                      <div style={{ fontSize: 16, fontWeight: 700 }}>{c.avg_score?.toFixed(1) || "0"}</div>
                      <div style={{ fontSize: 10, color: "#8FAAC8" }}>{c.count} yorum</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {sentimentKeywords.length > 0 && (
              <div style={{ marginBottom: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Anahtar Kelimeler</h3>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {sentimentKeywords.slice(0, 30).map((kw: any) => (
                    <span key={kw.keyword} style={{ padding: "4px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600, background: kw.positive > kw.negative ? "#dcfce7" : kw.negative > kw.positive ? "#fef2f2" : "#f3f4f6", color: kw.positive > kw.negative ? "#16a34a" : kw.negative > kw.positive ? "#dc2626" : "#6b7280", border: "1px solid #D6E4FA" }}>
                      {kw.keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {tab === "alerts" && !loading && (
          <div>
            {alerts.length === 0 ? (
              <p style={{ fontSize: 13, color: "#8FAAC8" }}>Aktif uyarı yok</p>
            ) : alerts.filter(a => !a.is_resolved).length === 0 ? (
              <p style={{ fontSize: 13, color: "#8FAAC8" }}>Tüm uyarılar çözüldü</p>
            ) : alerts.filter(a => !a.is_resolved).map((a: any) => (
              <div key={a.id} style={{ background: "#fff", border: `1px solid ${a.severity === "high" ? "#fca5a5" : a.severity === "medium" ? "#fcd34d" : "#d1d5db"}`, borderLeft: `4px solid ${a.severity === "high" ? "#dc2626" : a.severity === "medium" ? "#f59e0b" : "#6b7280"}`, borderRadius: 8, padding: "12px 14px", marginBottom: 8, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 2 }}>
                    <i className={`ti ${a.alert_type === "negative_review" ? "ti-message-exclamation" : a.alert_type === "rating_drop" ? "ti-trending-down" : "ti-chart-infographic"}`} style={{ fontSize: 14, color: a.severity === "high" ? "#dc2626" : "#f59e0b" }} />
                    <span style={{ fontSize: 12, fontWeight: 600 }}>{a.alert_type === "negative_review" ? "Negatif Yorum" : a.alert_type === "rating_drop" ? "Puan Düşüşü" : "Yoğunluk Artışı"}</span>
                    <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 6px", borderRadius: 4, background: a.severity === "high" ? "#fef2f2" : a.severity === "medium" ? "#fef3c7" : "#f3f4f6", color: a.severity === "high" ? "#dc2626" : a.severity === "medium" ? "#d97706" : "#6b7280" }}>
                      {a.severity === "high" ? "Yüksek" : a.severity === "medium" ? "Orta" : "Düşük"}
                    </span>
                  </div>
                  <p style={{ fontSize: 12, color: "#5A7499", margin: 0 }}>{a.message}</p>
                </div>
                <button onClick={() => handleResolveAlert(a.id)}
                  style={{ padding: "6px 12px", background: "#16a34a", color: "#fff", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", flexShrink: 0 }}>
                  <i className="ti ti-check" style={{ marginRight: 4 }} />Çöz
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
