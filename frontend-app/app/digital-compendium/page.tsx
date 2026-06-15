"use client";
import { useState } from "react";

const MOCK_COMPENDIUM = {
  id: 1, hotel_id: 1, is_published: true,
  welcome_message: "Hoş geldiniz! Konforlu bir konaklama dileriz.",
  wifi_ssid: "Otel-WiFi", wifi_password: "hotel2026",
  breakfast_info: "07:00-10:30 • Teras Restoran • Açık büfe",
  restaurant_info: "12:00-22:00 • Ana Restoran • Dünya mutfağı",
  room_service_info: "07:00-23:00 arası oda servisi mevcuttur",
  spa_info: "10:00-20:00 • Hamam, sauna, masaj • Önceden rezervasyon",
  gym_info: "7/24 açık • 3. katta • Kartınızla giriş",
  parking_info: "Açık otopark ücretsiz • Kapalı otopark 50₺/gün",
  house_rules: "Oda içinde sigara içilmez • Sessiz saatler 23:00-07:00",
  emergency_info: "Resepsiyon: 0 (212) 444 55 66 • Acil: 112",
  checkout_info: "Çıkış saati 12:00 • Geç çıkış talep edilebilir",
  local_attractions: { "Tarihi Yarımada": "2 km", "İstiklal Caddesi": "5 km", "Boğaz Turu": "3 km" },
  hotel_services: { "Havuz": true, "SPA": true, "Fitness": true, "Transfer": true, "Çamaşırhane": true },
  contact_info: "0 (212) 444 55 66",
};

const MOCK_PAGES = [
  { id: 1, title: "Otel Rehberi", icon: "building", sort_order: 1, content: "Otelimiz hakkında her şey..." },
  { id: 2, title: "Yeme İçme", icon: "coffee", sort_order: 2, content: "Restoran, bar, oda servisi..." },
  { id: 3, title: "Aktiviteler", icon: "activity", sort_order: 3, content: "SPA, yüzme, turlar..." },
];

const MOCK_NOTIFICATIONS = [
  { id: 1, type: "welcome", title: "Welcome!", message: "Otelimize hoş geldiniz", sent_at: "2026-06-15 14:00", is_read: false },
  { id: 2, type: "housekeeping", title: "Temizlik", message: "Odanız 14:30'da temizlenecek", sent_at: "2026-06-15 10:00", is_read: true },
  { id: 3, type: "checkout_reminder", title: "Check-out Hatırlatma", message: "Çıkış saatiniz 12:00", sent_at: "2026-06-16 08:00", is_read: false },
];

const MOCK_SERVICE_REQUESTS = [
  { id: 1, room: "205", guest: "Ali Yılmaz", category: "food", item: "Kahvaltı Tabağı", qty: 2, status: "pending", requested_at: "2026-06-15 08:30" },
  { id: 2, room: "312", guest: "Ayşe Demir", category: "cleaning", item: "Ek Havlu", qty: 3, status: "in_progress", requested_at: "2026-06-15 09:15" },
  { id: 3, room: "108", guest: "Mehmet Kaya", category: "maintenance", item: "Klima Arızası", qty: 1, status: "completed", requested_at: "2026-06-14 22:00", completed_at: "2026-06-14 23:30" },
];

export default function DigitalCompendiumPage() {
  const [tab, setTab] = useState("compendium");
  const [compendium, setCompendium] = useState(MOCK_COMPENDIUM);
  const [pages, setPages] = useState(MOCK_PAGES);
  const [editingPage, setEditingPage] = useState<any>(null);
  const [showPageModal, setShowPageModal] = useState(false);
  const [guestBookingId, setGuestBookingId] = useState("");
  const [guestView, setGuestView] = useState<any>(null);

  const statusStyle = (s: string) => {
    const m: Record<string,string> = { pending:"#F59E0B", in_progress:"#3B82F6", completed:"#10B981", cancelled:"#EF4444" };
    return { background:m[s]||"#8FAAC8", color:"#fff", fontSize:11, fontWeight:600, padding:"3px 10px", borderRadius:20, textTransform:"capitalize" as const };
  };

  const handleFieldChange = (field: string, value: any) => {
    setCompendium(prev => ({ ...prev, [field]: value }));
  };

  const openNewPage = () => {
    setEditingPage({ title: "", icon: "file", content: "", sort_order: pages.length + 1 });
    setShowPageModal(true);
  };

  const openEditPage = (p: any) => {
    setEditingPage({ ...p });
    setShowPageModal(true);
  };

  const savePage = () => {
    if (editingPage.id) {
      setPages(prev => prev.map(p => p.id === editingPage.id ? editingPage : p));
    } else {
      setPages(prev => [...prev, { ...editingPage, id: Math.max(...prev.map(p => p.id)) + 1 }]);
    }
    setShowPageModal(false);
    setEditingPage(null);
  };

  const deletePage = (id: number) => {
    setPages(prev => prev.filter(p => p.id !== id));
  };

  const viewGuestCompendium = () => {
    if (guestBookingId) {
      setGuestView({ ...compendium, pages, booking_id: guestBookingId });
    }
  };

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "24px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 24 }}>
          <i className="ti ti-book" style={{ fontSize: 24, color: "#4A7FD4" }} />
          <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.5 }}>Digital Compendium</h1>
        </div>

        {/* TABS */}
        <div style={{ display: "flex", gap: 4, marginBottom: 24, background: "#fff", borderRadius: 8, padding: 4, border: "1px solid #D6E4FA", width: "fit-content" }}>
          {[
            { key: "compendium", icon: "ti-edit", label: "Rehber Düzenle" },
            { key: "pages", icon: "ti-files", label: "Sayfalar" },
            { key: "notifications", icon: "ti-bell", label: "Bildirimler" },
            { key: "room-service", icon: "ti-room-service", label: "Oda Servisi" },
            { key: "guest-view", icon: "ti-eye", label: "Misafir Görünümü" },
          ].map(t => (
            <button key={t.key} onClick={() => setTab(t.key)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 16px", borderRadius: 6, border: "none", background: tab === t.key ? "#4A7FD4" : "transparent", color: tab === t.key ? "#fff" : "#5A7499", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer", transition: "all .15s" }}>
              <i className={`ti ${t.icon}`} style={{ fontSize: 16 }} />
              {t.label}
            </button>
          ))}
        </div>

        {/* TAB: COMPENDIUM EDIT */}
        {tab === "compendium" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h2 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-wifi" style={{ fontSize: 18, color: "#4A7FD4" }} /> WiFi & İletişim
              </h2>
              <div style={{ display: "grid", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>WiFi SSID</label>
                  <input value={compendium.wifi_ssid} onChange={e => handleFieldChange("wifi_ssid", e.target.value)} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>WiFi Şifre</label>
                  <input value={compendium.wifi_password} onChange={e => handleFieldChange("wifi_password", e.target.value)} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>İletişim (Resepsiyon)</label>
                  <input value={compendium.contact_info} onChange={e => handleFieldChange("contact_info", e.target.value)} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF" }} />
                </div>
              </div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h2 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-coffee" style={{ fontSize: 18, color: "#4A7FD4" }} /> Kahvaltı & Restoran
              </h2>
              <div style={{ display: "grid", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Kahvaltı</label>
                  <textarea value={compendium.breakfast_info} onChange={e => handleFieldChange("breakfast_info", e.target.value)} rows={3} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Restoran</label>
                  <textarea value={compendium.restaurant_info} onChange={e => handleFieldChange("restaurant_info", e.target.value)} rows={3} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Oda Servisi</label>
                  <textarea value={compendium.room_service_info} onChange={e => handleFieldChange("room_service_info", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
              </div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h2 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-spa" style={{ fontSize: 18, color: "#4A7FD4" }} /> SPA & Spor
              </h2>
              <div style={{ display: "grid", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>SPA</label>
                  <textarea value={compendium.spa_info} onChange={e => handleFieldChange("spa_info", e.target.value)} rows={3} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Fitness</label>
                  <textarea value={compendium.gym_info} onChange={e => handleFieldChange("gym_info", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
              </div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h2 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-car" style={{ fontSize: 18, color: "#4A7FD4" }} /> Otopark & Diğer
              </h2>
              <div style={{ display: "grid", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Otopark</label>
                  <textarea value={compendium.parking_info} onChange={e => handleFieldChange("parking_info", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Otel Kuralları</label>
                  <textarea value={compendium.house_rules} onChange={e => handleFieldChange("house_rules", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Acil Durum</label>
                  <textarea value={compendium.emergency_info} onChange={e => handleFieldChange("emergency_info", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Check-out Bilgisi</label>
                  <textarea value={compendium.checkout_info} onChange={e => handleFieldChange("checkout_info", e.target.value)} rows={2} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
                </div>
              </div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20, gridColumn: "1 / -1" }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                <h2 style={{ fontSize: 15, fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}>
                  <i className="ti ti-message" style={{ fontSize: 18, color: "#4A7FD4" }} /> Hoş Geldiniz Mesajı
                </h2>
                <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                  <input type="checkbox" checked={compendium.is_published} onChange={e => handleFieldChange("is_published", e.target.checked)} style={{ accentColor: "#4A7FD4" }} />
                  Yayında
                </label>
              </div>
              <textarea value={compendium.welcome_message} onChange={e => handleFieldChange("welcome_message", e.target.value)} rows={3} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, background: "#FAFCFF", resize: "vertical" }} />
              <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 16 }}>
                <button style={{ display: "flex", alignItems: "center", gap: 6, padding: "10px 24px", borderRadius: 8, border: "none", background: "#4A7FD4", color: "#fff", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                  <i className="ti ti-device-floppy" style={{ fontSize: 16 }} /> Kaydet
                </button>
              </div>
            </div>
          </div>
        )}

        {/* TAB: PAGES */}
        {tab === "pages" && (
          <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
            <div style={{ padding: "16px 20px", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span style={{ fontSize: 14, fontWeight: 600 }}>Kompendiyum Sayfaları</span>
              <button onClick={openNewPage} style={{ display: "flex", alignItems: "center", gap: 4, padding: "6px 14px", borderRadius: 6, border: "none", background: "#4A7FD4", color: "#fff", fontFamily: "inherit", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
                <i className="ti ti-plus" style={{ fontSize: 14 }} /> Yeni Sayfa
              </button>
            </div>
            {pages.sort((a, b) => a.sort_order - b.sort_order).map(p => (
              <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 16, padding: "14px 20px", borderBottom: "1px solid #EEF4FF" }}>
                <div style={{ width: 38, height: 38, borderRadius: 8, background: "#EEF4FF", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  <i className={`ti ti-${p.icon || "file"}`} style={{ fontSize: 18, color: "#4A7FD4" }} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{p.title}</div>
                  <div style={{ fontSize: 11, color: "#8FAAC8" }}>Sıra: {p.sort_order}</div>
                </div>
                <div style={{ display: "flex", gap: 6 }}>
                  <button onClick={() => openEditPage(p)} style={{ display: "flex", alignItems: "center", gap: 4, padding: "6px 10px", borderRadius: 6, border: "1px solid #D6E4FA", background: "transparent", color: "#4A7FD4", fontFamily: "inherit", fontSize: 12, cursor: "pointer" }}>
                    <i className="ti ti-edit" style={{ fontSize: 14 }} /> Düzenle
                  </button>
                  <button onClick={() => deletePage(p.id)} style={{ display: "flex", alignItems: "center", gap: 4, padding: "6px 10px", borderRadius: 6, border: "1px solid #FECACA", background: "transparent", color: "#EF4444", fontFamily: "inherit", fontSize: 12, cursor: "pointer" }}>
                    <i className="ti ti-trash" style={{ fontSize: 14 }} />
                  </button>
                </div>
              </div>
            ))}

            {showPageModal && editingPage && (
              <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }} onClick={() => setShowPageModal(false)}>
                <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: "100%", maxWidth: 480, margin: "0 16px" }} onClick={e => e.stopPropagation()}>
                  <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 16 }}>{editingPage.id ? "Sayfayı Düzenle" : "Yeni Sayfa"}</h3>
                  <div style={{ display: "grid", gap: 12 }}>
                    <div>
                      <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Başlık</label>
                      <input value={editingPage.title} onChange={e => setEditingPage({ ...editingPage, title: e.target.value })} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13 }} />
                    </div>
                    <div>
                      <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>İkon (tabler icon name)</label>
                      <input value={editingPage.icon} onChange={e => setEditingPage({ ...editingPage, icon: e.target.value })} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13 }} />
                    </div>
                    <div>
                      <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>Sıralama</label>
                      <input type="number" value={editingPage.sort_order} onChange={e => setEditingPage({ ...editingPage, sort_order: parseInt(e.target.value) || 0 })} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13 }} />
                    </div>
                    <div>
                      <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", display: "block", marginBottom: 4 }}>İçerik</label>
                      <textarea value={editingPage.content} onChange={e => setEditingPage({ ...editingPage, content: e.target.value })} rows={5} style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13, resize: "vertical" }} />
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
                    <button onClick={() => setShowPageModal(false)} style={{ flex: 1, padding: "10px", borderRadius: 8, border: "1px solid #D6E4FA", background: "transparent", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>İptal</button>
                    <button onClick={savePage} style={{ flex: 1, padding: "10px", borderRadius: 8, border: "none", background: "#4A7FD4", color: "#fff", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>Kaydet</button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB: NOTIFICATIONS */}
        {tab === "notifications" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
              <div style={{ padding: "16px 20px", borderBottom: "1px solid #D6E4FA" }}>
                <span style={{ fontSize: 14, fontWeight: 600 }}>Bildirimler</span>
              </div>
              {MOCK_NOTIFICATIONS.map(n => (
                <div key={n.id} style={{ display: "flex", alignItems: "flex-start", gap: 12, padding: "14px 20px", borderBottom: "1px solid #EEF4FF" }}>
                  <div style={{ width: 36, height: 36, borderRadius: "50%", background: n.is_read ? "#EEF4FF" : "#DBEAFE", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                    <i className={`ti ti-${n.type === "welcome" ? "hand-wave" : n.type === "housekeeping" ? "broom" : "bell"}`} style={{ fontSize: 16, color: n.is_read ? "#8FAAC8" : "#4A7FD4" }} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span style={{ fontSize: 13, fontWeight: 600 }}>{n.title}</span>
                      {!n.is_read && <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#4A7FD4", display: "inline-block" }} />}
                    </div>
                    <div style={{ fontSize: 12, color: "#5A7499", marginTop: 2 }}>{n.message}</div>
                    <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>{n.sent_at}</div>
                  </div>
                </div>
              ))}
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
                  <i className="ti ti-send" style={{ fontSize: 16, color: "#4A7FD4" }} /> Hızlı Bildirim Gönder
                </h3>
                <div style={{ display: "grid", gap: 10 }}>
                  <button style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 16px", borderRadius: 8, border: "1px solid #D6E4FA", background: "#FAFCFF", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer", textAlign: "left", transition: "all .15s" }}
                    className="hover-row">
                    <i className="ti ti-hand-wave" style={{ fontSize: 16, color: "#10B981" }} /> Welcome Mesajı Gönder
                  </button>
                  <button style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 16px", borderRadius: 8, border: "1px solid #D6E4FA", background: "#FAFCFF", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer", textAlign: "left", transition: "all .15s" }}
                    className="hover-row">
                    <i className="ti ti-door-exit" style={{ fontSize: 16, color: "#F59E0B" }} /> Check-out Hatırlatması Gönder
                  </button>
                  <button style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 16px", borderRadius: 8, border: "1px solid #D6E4FA", background: "#FAFCFF", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer", textAlign: "left", transition: "all .15s" }}
                    className="hover-row">
                    <i className="ti ti-bell-plus" style={{ fontSize: 16, color: "#8B5CF6" }} /> Özel Bildirim Oluştur
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: ROOM SERVICE */}
        {tab === "room-service" && (
          <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
            <div style={{ padding: "16px 20px", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span style={{ fontSize: 14, fontWeight: 600 }}>Oda Servisi Talepleri</span>
              <div style={{ display: "flex", gap: 6 }}>
                {["all", "pending", "in_progress", "completed"].map(s => (
                  <button key={s} style={{ padding: "4px 10px", borderRadius: 6, border: "1px solid #D6E4FA", background: "transparent", fontFamily: "inherit", fontSize: 11, fontWeight: 600, cursor: "pointer", textTransform: "capitalize" }}>
                    {s === "all" ? "Hepsi" : s === "in_progress" ? "Devam Eden" : s === "completed" ? "Tamamlanan" : "Bekleyen"}
                  </button>
                ))}
              </div>
            </div>
            {MOCK_SERVICE_REQUESTS.map(r => (
              <div key={r.id} style={{ display: "flex", alignItems: "center", gap: 16, padding: "14px 20px", borderBottom: "1px solid #EEF4FF" }}>
                <div style={{ width: 38, height: 38, borderRadius: 8, background: "#EEF4FF", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  <i className={`ti ti-${r.category === "food" ? "coffee" : r.category === "cleaning" ? "broom" : "tool"}`} style={{ fontSize: 18, color: "#4A7FD4" }} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{r.item}</div>
                  <div style={{ fontSize: 11, color: "#8FAAC8" }}>Oda {r.room} · {r.guest} · Adet: {r.qty} · {r.requested_at}</div>
                </div>
                <span style={statusStyle(r.status)}>{r.status === "pending" ? "Bekliyor" : r.status === "in_progress" ? "Devam Ediyor" : r.status === "completed" ? "Tamamlandı" : r.status}</span>
                <div style={{ display: "flex", gap: 4 }}>
                  {r.status === "pending" && (
                    <>
                      <button style={{ padding: "6px 10px", borderRadius: 6, border: "none", background: "#3B82F6", color: "#fff", fontFamily: "inherit", fontSize: 11, fontWeight: 600, cursor: "pointer" }}>
                        Başlat
                      </button>
                      <button style={{ padding: "6px 10px", borderRadius: 6, border: "none", background: "#EF4444", color: "#fff", fontFamily: "inherit", fontSize: 11, fontWeight: 600, cursor: "pointer" }}>
                        İptal
                      </button>
                    </>
                  )}
                  {r.status === "in_progress" && (
                    <button style={{ padding: "6px 10px", borderRadius: 6, border: "none", background: "#10B981", color: "#fff", fontFamily: "inherit", fontSize: 11, fontWeight: 600, cursor: "pointer" }}>
                      Tamamla
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB: GUEST VIEW */}
        {tab === "guest-view" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Misafir Görünümü</h3>
              <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
                <input
                  placeholder="Booking ID girin"
                  value={guestBookingId}
                  onChange={e => setGuestBookingId(e.target.value)}
                  style={{ flex: 1, padding: "8px 12px", borderRadius: 6, border: "1px solid #D6E4FA", fontFamily: "inherit", fontSize: 13 }}
                />
                <button onClick={viewGuestCompendium} style={{ padding: "8px 16px", borderRadius: 6, border: "none", background: "#4A7FD4", color: "#fff", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                  <i className="ti ti-eye" style={{ fontSize: 14, marginRight: 4 }} /> Görüntüle
                </button>
              </div>
              {guestView && (
                <div style={{ fontSize: 12, color: "#5A7499", lineHeight: 1.6 }}>
                  <p><strong>Booking ID:</strong> {guestView.booking_id}</p>
                  <p><strong>WiFi:</strong> {guestView.wifi_ssid} / {guestView.wifi_password}</p>
                  <p><strong>Kahvaltı:</strong> {guestView.breakfast_info}</p>
                  <p><strong>SPA:</strong> {guestView.spa_info}</p>
                  <p><strong>İletişim:</strong> {guestView.contact_info}</p>
                  <p style={{ marginTop: 8, fontWeight: 600 }}>Sayfalar ({guestView.pages.length})</p>
                  {guestView.pages.map((p: any) => (
                    <p key={p.id} style={{ marginLeft: 12 }}>• {p.title}</p>
                  ))}
                </div>
              )}
            </div>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 20 }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-device-mobile" style={{ fontSize: 16, color: "#4A7FD4" }} /> Mobil Önizleme
              </h3>
              <div style={{ maxWidth: 320, margin: "0 auto", background: "#FAFCFF", border: "1px solid #D6E4FA", borderRadius: 12, overflow: "hidden" }}>
                <div style={{ background: "#4A7FD4", color: "#fff", padding: "16px 20px" }}>
                  <div style={{ fontSize: 16, fontWeight: 700 }}>Digital Rehber</div>
                  <div style={{ fontSize: 11, opacity: 0.8, marginTop: 4 }}>Otel WiFi: {guestView?.wifi_ssid || MOCK_COMPENDIUM.wifi_ssid}</div>
                </div>
                <div style={{ padding: 12 }}>
                  {pages.sort((a, b) => a.sort_order - b.sort_order).map(p => (
                    <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", borderBottom: "1px solid #EEF4FF", cursor: "pointer" }}>
                      <i className={`ti ti-${p.icon || "file"}`} style={{ fontSize: 16, color: "#4A7FD4" }} />
                      <span style={{ fontSize: 13, fontWeight: 500 }}>{p.title}</span>
                    </div>
                  ))}
                </div>
                <div style={{ padding: "12px 16px", borderTop: "1px solid #D6E4FA", fontSize: 11, color: "#8FAAC8" }}>
                  {guestView?.contact_info || MOCK_COMPENDIUM.contact_info}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
