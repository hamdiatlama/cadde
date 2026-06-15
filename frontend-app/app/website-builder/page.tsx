"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function WebsiteBuilderPage() {
  const router = useRouter();
  const [hotelId, setHotelId] = useState("");
  const [website, setWebsite] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("settings");
  const [msg, setMsg] = useState("");

  const [settings, setSettings] = useState({
    primary_color: "#4A7FD4",
    secondary_color: "#EEF4FF",
    font_family: "Space Grotesk",
    logo_url: "",
    hero_image_url: "",
    about_text: "",
  });
  const [pages, setPages] = useState<any[]>([]);
  const [editPage, setEditPage] = useState<any>(null);
  const [pageContent, setPageContent] = useState("");
  const [seo, setSeo] = useState<any>(null);
  const [seoForm, setSeoForm] = useState({ meta_title: "", meta_description: "", meta_keywords: "" });
  const [widget, setWidget] = useState<any>(null);
  const [embedCode, setEmbedCode] = useState("");
  const [seoAnalysis, setSeoAnalysis] = useState<any>(null);

  async function loadWebsite() {
    if (!hotelId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/website-builder/website/${hotelId}`);
      if (res.ok) {
        const data = await res.json();
        setWebsite(data);
        setSettings({
          primary_color: data.primary_color || "#4A7FD4",
          secondary_color: data.secondary_color || "#EEF4FF",
          font_family: data.font_family || "Space Grotesk",
          logo_url: data.logo_url || "",
          hero_image_url: data.hero_image_url || "",
          about_text: data.about_text || "",
        });
        setPages(data.pages || []);
        if (data.seo) {
          setSeo(data.seo);
          setSeoForm({
            meta_title: data.seo.meta_title || "",
            meta_description: data.seo.meta_description || "",
            meta_keywords: data.seo.meta_keywords || "",
          });
        }
        if (data.booking_widget) setWidget(data.booking_widget);
      } else setMsg("❌ Site bulunamadı");
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
    setLoading(false);
  }

  async function handleCreate() {
    if (!hotelId) return;
    try {
      const params = new URLSearchParams({ hotel_id: hotelId });
      const res = await fetch(`${API}/website-builder/website?${params}`, { method: "POST" });
      if (res.ok) {
        setMsg("✅ Site oluşturuldu");
        await loadWebsite();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleUpdateSettings() {
    if (!hotelId) return;
    try {
      const params = new URLSearchParams(settings as any);
      const res = await fetch(`${API}/website-builder/website/${hotelId}?${params}`, { method: "PUT" });
      if (res.ok) {
        setMsg("✅ Ayarlar kaydedildi");
        await loadWebsite();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handlePublish() {
    if (!hotelId) return;
    try {
      const res = await fetch(`${API}/website-builder/website/${hotelId}/publish`, { method: "POST" });
      if (res.ok) {
        setMsg("✅ Site yayınlandı");
        await loadWebsite();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleUpdatePage() {
    if (!editPage) return;
    try {
      const params = new URLSearchParams();
      if (pageContent) params.set("content", pageContent);
      const res = await fetch(`${API}/website-builder/pages/${editPage.id}?${params}`, { method: "PUT" });
      if (res.ok) {
        setMsg("✅ Sayfa güncellendi");
        await loadWebsite();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleUpdateSeo() {
    if (!seo) return;
    try {
      const params = new URLSearchParams(seoForm);
      const res = await fetch(`${API}/website-builder/seo/${seo.id}?${params}`, { method: "PUT" });
      if (res.ok) {
        setMsg("✅ SEO güncellendi");
        await loadWebsite();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleUpdateWidget() {
    if (!widget) return;
    try {
      const params = new URLSearchParams({ is_enabled: String(!widget.is_enabled) });
      const res = await fetch(`${API}/website-builder/widget/${widget.id}?${params}`, { method: "PUT" });
      if (res.ok) {
        setMsg("✅ Widget güncellendi");
        await loadWebsite();
      }
    } catch (_) {}
  }

  async function handleEmbedUpdate(widgetType: string) {
    if (!widget) return;
    try {
      const params = new URLSearchParams({ widget_type: widgetType });
      const res = await fetch(`${API}/website-builder/widget/${widget.id}?${params}`, { method: "PUT" });
      if (res.ok) {
        setMsg("✅ Widget tipi güncellendi");
        await loadWebsite();
      }
    } catch (_) {}
  }

  async function loadEmbedCode() {
    if (!hotelId) return;
    try {
      const res = await fetch(`${API}/website-builder/embed/${hotelId}`);
      if (res.ok) {
        const data = await res.json();
        setEmbedCode(data.embed_code || "");
        await navigator.clipboard?.writeText(data.embed_code || "");
        setMsg("✅ Embed kodu kopyalandı");
      }
    } catch (_) {}
  }

  async function loadSeoAnalysis() {
    if (!hotelId) return;
    try {
      const res = await fetch(`${API}/website-builder/seo-analysis/${hotelId}`);
      if (res.ok) setSeoAnalysis(await res.json());
    } catch (_) {}
  }

  useEffect(() => {
    if (hotelId && website) {
      loadEmbedCode();
      loadSeoAnalysis();
    }
  }, [website]);

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
        <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.8, marginBottom: 4 }}>Web Sitesi Oluşturucu</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20 }}>Oteliniz için özelleştirilmiş web sitesi yönetimi</p>

        <div style={{ display: "flex", gap: 12, marginBottom: 20, alignItems: "center", flexWrap: "wrap" }}>
          <input type="number" placeholder="Otel ID" value={hotelId} onChange={e => setHotelId(e.target.value)} style={{ width: 120, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
          <button onClick={handleCreate} disabled={!hotelId} style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
            <i className="ti ti-plus" /> Site Oluştur
          </button>
          <button onClick={loadWebsite} disabled={!hotelId} style={{ padding: "8px 14px", background: "#fff", color: "#4A7FD4", border: "1px solid #4A7FD4", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
            <i className="ti ti-refresh" /> Yükle
          </button>
        </div>

        {msg && (
          <div style={{ padding: "10px 14px", borderRadius: 8, background: msg.includes("✅") ? "#dcfce7" : "#fef2f2", color: msg.includes("✅") ? "#16a34a" : "#dc2626", fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
            {msg.replace("✅ ", "").replace("❌ ", "")}
          </div>
        )}

        {loading && <p style={{ fontSize: 13, color: "#8FAAC8" }}>Yükleniyor...</p>}

        {website && (
          <>
            <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
              {[
                { key: "settings", label: "Site Ayarları", icon: "ti-settings" },
                { key: "pages", label: "Sayfalar", icon: "ti-file" },
                { key: "seo", label: "SEO", icon: "ti-search" },
                { key: "widget", label: "Rezervasyon Widget", icon: "ti-calendar" },
                { key: "embed", label: "Embed Kodu", icon: "ti-code" },
              ].map(t => (
                <button key={t.key} onClick={() => { setTab(t.key); setMsg(""); }} style={{ padding: "8px 16px", background: tab === t.key ? "#4A7FD4" : "#fff", color: tab === t.key ? "#fff" : "#5A7499", border: `1px solid ${tab === t.key ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                  <i className={`ti ${t.icon}`} style={{ fontSize: 14 }} /> {t.label}
                </button>
              ))}
            </div>

            {tab === "settings" && (
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 600 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
                  <div style={{ width: 12, height: 12, borderRadius: "50%", background: settings.primary_color }} />
                  <span style={{ fontSize: 16, fontWeight: 700 }}>{website.subdomain}</span>
                  {website.is_published ? (
                    <span style={{ fontSize: 11, fontWeight: 700, padding: "3px 10px", borderRadius: 20, background: "#dcfce7", color: "#16a34a" }}>Yayında</span>
                  ) : (
                    <span style={{ fontSize: 11, fontWeight: 700, padding: "3px 10px", borderRadius: 20, background: "#fef3c7", color: "#d97706" }}>Taslak</span>
                  )}
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120 }}>Birincil Renk</label>
                    <input type="color" value={settings.primary_color} onChange={e => setSettings(p => ({ ...p, primary_color: e.target.value }))} style={{ width: 40, height: 32, border: "1px solid #D6E4FA", borderRadius: 6, cursor: "pointer" }} />
                    <input type="text" value={settings.primary_color} onChange={e => setSettings(p => ({ ...p, primary_color: e.target.value }))} style={{ width: 100, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120 }}>İkincil Renk</label>
                    <input type="color" value={settings.secondary_color} onChange={e => setSettings(p => ({ ...p, secondary_color: e.target.value }))} style={{ width: 40, height: 32, border: "1px solid #D6E4FA", borderRadius: 6, cursor: "pointer" }} />
                    <input type="text" value={settings.secondary_color} onChange={e => setSettings(p => ({ ...p, secondary_color: e.target.value }))} style={{ width: 100, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120 }}>Font</label>
                    <select value={settings.font_family} onChange={e => setSettings(p => ({ ...p, font_family: e.target.value }))} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                      <option value="Space Grotesk">Space Grotesk</option>
                      <option value="Inter">Inter</option>
                      <option value="Poppins">Poppins</option>
                      <option value="DM Sans">DM Sans</option>
                    </select>
                  </div>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120 }}>Logo URL</label>
                    <input type="text" placeholder="https://..." value={settings.logo_url} onChange={e => setSettings(p => ({ ...p, logo_url: e.target.value }))} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120 }}>Hero Görseli</label>
                    <input type="text" placeholder="https://..." value={settings.hero_image_url} onChange={e => setSettings(p => ({ ...p, hero_image_url: e.target.value }))} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 120, paddingTop: 8 }}>Hakkımızda</label>
                    <textarea placeholder="Otel açıklaması..." value={settings.about_text} onChange={e => setSettings(p => ({ ...p, about_text: e.target.value }))} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 80 }} />
                  </div>
                  <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
                    <button onClick={handleUpdateSettings} style={{ padding: "10px 20px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                      <i className="ti ti-device-floppy" /> Kaydet
                    </button>
                    <button onClick={handlePublish} style={{ padding: "10px 20px", background: "#16a34a", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                      <i className="ti ti-world" /> {website.is_published ? "Tekrar Yayınla" : "Yayınla"}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {tab === "pages" && (
              <div style={{ display: "flex", gap: 24 }}>
                <div style={{ width: 280, flexShrink: 0 }}>
                  <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Sayfalar</h2>
                  {pages.length === 0 ? (
                    <p style={{ fontSize: 13, color: "#8FAAC8" }}>Sayfa bulunamadı</p>
                  ) : pages.map((p: any) => (
                    <div key={p.id} style={{ padding: "10px 12px", background: editPage?.id === p.id ? "#fff" : "transparent", border: `1px solid ${editPage?.id === p.id ? "#4A7FD4" : "transparent"}`, borderRadius: 8, cursor: "pointer", marginBottom: 4, display: "flex", alignItems: "center", gap: 8 }} onClick={() => { setEditPage(p); setPageContent(p.content || ""); }}>
                      <i className="ti ti-file" style={{ fontSize: 14, color: "#4A7FD4" }} />
                      <div>
                        <div style={{ fontSize: 13, fontWeight: 600 }}>{p.title}</div>
                        <div style={{ fontSize: 10, color: "#8FAAC8" }}>/ {p.slug}</div>
                      </div>
                    </div>
                  ))}
                </div>

                {editPage && (
                  <div style={{ flex: 1, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24 }}>
                    <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 12 }}>{editPage.title}</h2>
                    <textarea placeholder="JSON içerik blokları..." value={pageContent} onChange={e => setPageContent(e.target.value)} style={{ width: "100%", minHeight: 300, padding: "12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "'Space Grotesk',monospace", outline: "none", resize: "vertical" }} />
                    <button onClick={handleUpdatePage} style={{ marginTop: 12, padding: "10px 20px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                      <i className="ti ti-device-floppy" /> İçeriği Kaydet
                    </button>
                  </div>
                )}
              </div>
            )}

            {tab === "seo" && (
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 600 }}>
                <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 16 }}>SEO Ayarları</h2>
                {seoAnalysis && (
                  <div style={{ marginBottom: 16, padding: "12px 14px", borderRadius: 8, background: seoAnalysis.score >= 80 ? "#dcfce7" : seoAnalysis.score >= 50 ? "#fef3c7" : "#fef2f2", border: `1px solid ${seoAnalysis.score >= 80 ? "#86efac" : seoAnalysis.score >= 50 ? "#fde68a" : "#fca5a5"}` }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                      <i className={`ti ${seoAnalysis.score >= 80 ? "ti-circle-check" : "ti-alert-triangle"}`} style={{ color: seoAnalysis.score >= 80 ? "#16a34a" : seoAnalysis.score >= 50 ? "#d97706" : "#dc2626" }} />
                      <span style={{ fontSize: 14, fontWeight: 700 }}>SEO Skoru: {seoAnalysis.score}/100</span>
                    </div>
                    {seoAnalysis.issues.length > 0 && (
                      <div style={{ fontSize: 11, color: "#5A7499" }}>
                        {seoAnalysis.issues.map((issue: string, i: number) => (
                          <div key={i}>• {issue}</div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                  <div>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", display: "block", marginBottom: 4 }}>Meta Başlık</label>
                    <input type="text" value={seoForm.meta_title} onChange={e => setSeoForm(p => ({ ...p, meta_title: e.target.value }))} style={{ width: "100%", padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <div>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", display: "block", marginBottom: 4 }}>Meta Açıklama</label>
                    <textarea value={seoForm.meta_description} onChange={e => setSeoForm(p => ({ ...p, meta_description: e.target.value }))} style={{ width: "100%", padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 60 }} />
                  </div>
                  <div>
                    <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", display: "block", marginBottom: 4 }}>Anahtar Kelimeler</label>
                    <input type="text" value={seoForm.meta_keywords} onChange={e => setSeoForm(p => ({ ...p, meta_keywords: e.target.value }))} style={{ width: "100%", padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  </div>
                  <button onClick={handleUpdateSeo} style={{ marginTop: 8, padding: "10px 20px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                    <i className="ti ti-device-floppy" /> SEO Kaydet
                  </button>
                </div>
              </div>
            )}

            {tab === "widget" && (
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 600 }}>
                <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 16 }}>Rezervasyon Widget</h2>
                {widget && (
                  <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 100 }}>Widget Tipi</span>
                      <select value={widget.widget_type} onChange={e => handleEmbedUpdate(e.target.value)} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                        <option value="iframe">iframe</option>
                        <option value="popup">Popup</option>
                        <option value="inline">Inline</option>
                      </select>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", width: 100 }}>Durum</span>
                      <button onClick={handleUpdateWidget} style={{ padding: "6px 14px", borderRadius: 6, border: "none", fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", background: widget.is_enabled ? "#dcfce7" : "#fef3c7", color: widget.is_enabled ? "#16a34a" : "#d97706" }}>
                        {widget.is_enabled ? "Aktif" : "Pasif"}
                      </button>
                    </div>
                    {widget.embed_code && (
                      <div>
                        <label style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", display: "block", marginBottom: 4 }}>Mevcut Embed Kodu</label>
                        <pre style={{ padding: "10px 12px", background: "#EEF4FF", borderRadius: 6, fontSize: 11, overflowX: "auto", border: "1px solid #D6E4FA", whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{widget.embed_code}</pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {tab === "embed" && (
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 700 }}>
                <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>Embed Kodu</h2>
                <p style={{ fontSize: 12, color: "#8FAAC8", marginBottom: 16 }}>Bu kodu harici sitenize ekleyerek rezervasyon widget'ını gömebilirsiniz.</p>
                {embedCode ? (
                  <>
                    <pre style={{ padding: "14px 16px", background: "#1A2B4A", color: "#EEF4FF", borderRadius: 8, fontSize: 11, overflowX: "auto", whiteSpace: "pre-wrap", wordBreak: "break-all", marginBottom: 12 }}>{embedCode}</pre>
                    <button onClick={() => { navigator.clipboard?.writeText(embedCode); setMsg("✅ Kod kopyalandı"); }} style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                      <i className="ti ti-copy" /> Kopyala
                    </button>
                  </>
                ) : (
                  <p style={{ fontSize: 13, color: "#8FAAC8" }}>Embed kodu oluşturulamadı</p>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}
