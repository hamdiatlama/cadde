"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const STATUS_LABELS: Record<string, string> = {
  pending: "Bekliyor", confirmed: "Onaylandı",
  checked_in: "Giriş", checked_out: "Çıkış", cancelled: "İptal",
};

export default function HotelDashboard() {
  const router = useRouter();
  const [hotels, setHotels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("hotels");
  const [selectedHotelId, setSelectedHotelId] = useState<number | null>(null);
  const [bookings, setBookings] = useState<any[]>([]);
  const [rooms, setRooms] = useState<any[]>([]);
  const [msg, setMsg] = useState("");

  const [newHotel, setNewHotel] = useState({ name: "", city: "", property_type: "hotel", description: "", phone: "", email: "" });
  const [newRoom, setNewRoom] = useState({ name: "", max_guests: "2", base_price: "", bed_type: "", quantity: "1" });

  useEffect(() => {
    async function loadHotels() {
      try {
        const res = await fetch(`${API}/hotels/admin/all`);
        const data = await res.json();
        setHotels(Array.isArray(data) ? data : data?.value || []);
      } catch (_) {}
      setLoading(false);
    }
    loadHotels();
  }, []);

  useEffect(() => {
    if (!selectedHotelId) return;
    async function loadData() {
      try {
        const [bRes, rRes] = await Promise.all([
          fetch(`${API}/hotels/${selectedHotelId}/bookings`),
          fetch(`${API}/hotels/${selectedHotelId}/rooms`),
        ]);
        const bData = await bRes.json();
        const rData = await rRes.json();
        setBookings(Array.isArray(bData) ? bData : bData?.value || []);
        setRooms(Array.isArray(rData) ? rData : rData?.value || []);
      } catch (_) {}
    }
    loadData();
  }, [selectedHotelId]);

  async function handleCreateHotel() {
    try {
      const res = await fetch(`${API}/hotels/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newHotel),
      });
      if (res.ok) {
        const data = await res.json();
        setHotels(prev => [...prev, data]);
        setNewHotel({ name: "", city: "", property_type: "hotel", description: "", phone: "", email: "" });
        setMsg("✅ Otel oluşturuldu");
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleCreateRoom() {
    if (!selectedHotelId) return;
    try {
      const res = await fetch(`${API}/hotels/${selectedHotelId}/rooms`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...newRoom, max_guests: parseInt(newRoom.max_guests), base_price: parseFloat(newRoom.base_price), quantity: parseInt(newRoom.quantity) }),
      });
      if (res.ok) {
        const data = await res.json();
        setRooms(prev => [...prev, data]);
        setNewRoom({ name: "", max_guests: "2", base_price: "", bed_type: "", quantity: "1" });
        setMsg("✅ Oda eklendi");
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleUpdateStatus(bookingId: number, status: string) {
    try {
      const res = await fetch(`${API}/hotels/bookings/${bookingId}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      if (res.ok) {
        setBookings(prev => prev.map(b => b.id === bookingId ? { ...b, status } : b));
        setMsg(`✅ Durum: ${STATUS_LABELS[status] || status}`);
      }
    } catch (_) {}
  }

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
        <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.8, marginBottom: 4 }}>Otel Paneli</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20 }}>İşletme yönetimi</p>

        <div style={{ display: "flex", gap: 6, marginBottom: 20 }}>
          {[
            { key: "hotels", label: "Otel Listesi", icon: "ti-building" },
            { key: "create", label: "Yeni Otel", icon: "ti-plus" },
          ].map(t => (
            <button key={t.key} onClick={() => { setTab(t.key); setMsg(""); }} style={{ padding: "8px 16px", background: tab === t.key ? "#4A7FD4" : "#fff", color: tab === t.key ? "#fff" : "#5A7499", border: `1px solid ${tab === t.key ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
              <i className={`ti ${t.icon}`} style={{ fontSize: 14 }} /> {t.label}
            </button>
          ))}
        </div>

        {msg && (
          <div style={{ padding: "10px 14px", borderRadius: 8, background: msg.includes("✅") ? "#dcfce7" : "#fef2f2", color: msg.includes("✅") ? "#16a34a" : "#dc2626", fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
            {msg.replace("✅ ", "").replace("❌ ", "")}
          </div>
        )}

        {tab === "hotels" && (
          <div style={{ display: "flex", gap: 24 }}>
            <div style={{ width: 320, flexShrink: 0 }}>
              <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Otellerim</h2>
              {loading ? <p style={{ fontSize: 13, color: "#8FAAC8" }}>Yükleniyor...</p> : hotels.length === 0 ? (
                <p style={{ fontSize: 13, color: "#8FAAC8" }}>Henüz otel eklemediniz</p>
              ) : hotels.map((h: any) => (
                <div key={h.id} onClick={() => setSelectedHotelId(h.id)} style={{ padding: "12px 14px", background: selectedHotelId === h.id ? "#fff" : "transparent", border: `1px solid ${selectedHotelId === h.id ? "#4A7FD4" : "transparent"}`, borderRadius: 8, cursor: "pointer", marginBottom: 6 }}>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>{h.name}</div>
                  <div style={{ fontSize: 11, color: "#8FAAC8" }}>{h.city} · ★ {h.rating?.toFixed(1) || "0.0"}</div>
                </div>
              ))}
            </div>

            {selectedHotelId && (
              <div style={{ flex: 1 }}>
                <div style={{ marginBottom: 20 }}>
                  <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Rezervasyonlar</h2>
                  {bookings.length === 0 ? (
                    <p style={{ fontSize: 13, color: "#8FAAC8" }}>Rezervasyon yok</p>
                  ) : bookings.map((b: any) => (
                    <div key={b.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 14, marginBottom: 8 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <div>
                          <div style={{ fontSize: 13, fontWeight: 600 }}>No: {b.booking_no}</div>
                          <div style={{ fontSize: 12, color: "#8FAAC8" }}>{b.check_in?.slice(0, 10)} → {b.check_out?.slice(0, 10)} · {b.adults || 1} misafir</div>
                          <div style={{ fontSize: 12, color: "#5A7499", marginTop: 4 }}>₺{b.total_price?.toFixed(0)}</div>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                          <span style={{ fontSize: 11, fontWeight: 700, padding: "3px 8px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                            {STATUS_LABELS[b.status] || b.status}
                          </span>
                          {b.status === "pending" && (
                            <button onClick={() => handleUpdateStatus(b.id, "confirmed")} style={{ padding: "5px 10px", background: "#22c55e", color: "#fff", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                              Onayla
                            </button>
                          )}
                          {b.status === "confirmed" && (
                            <button onClick={() => handleUpdateStatus(b.id, "checked_in")} style={{ padding: "5px 10px", background: "#3b82f6", color: "#fff", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                              Giriş Yap
                            </button>
                          )}
                          {b.status === "checked_in" && (
                            <button onClick={() => handleUpdateStatus(b.id, "checked_out")} style={{ padding: "5px 10px", background: "#8FAAC8", color: "#fff", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                              Çıkış Yap
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div>
                  <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Odalar</h2>
                  <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
                    <input type="text" placeholder="Oda adı" value={newRoom.name} onChange={e => setNewRoom(p => ({ ...p, name: e.target.value }))} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                    <input type="number" placeholder="Fiyat" value={newRoom.base_price} onChange={e => setNewRoom(p => ({ ...p, base_price: e.target.value }))} style={{ width: 100, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                    <button onClick={handleCreateRoom} style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                      <i className="ti ti-plus" style={{ fontSize: 12 }} /> Ekle
                    </button>
                  </div>
                  {rooms.map((r: any) => (
                    <div key={r.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "10px 14px", marginBottom: 6, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <span style={{ fontSize: 13, fontWeight: 600 }}>{r.name}</span>
                        <span style={{ fontSize: 11, color: "#8FAAC8", marginLeft: 8 }}>{r.max_guests} kişi · {r.bed_type || "Standart"}</span>
                      </div>
                      <span style={{ fontSize: 14, fontWeight: 700, color: "#4A7FD4" }}>₺{r.base_price?.toFixed(0)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {tab === "create" && (
          <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 500 }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <input type="text" placeholder="Otel Adı *" value={newHotel.name} onChange={e => setNewHotel(p => ({ ...p, name: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <input type="text" placeholder="Şehir *" value={newHotel.city} onChange={e => setNewHotel(p => ({ ...p, city: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
                <select value={newHotel.property_type} onChange={e => setNewHotel(p => ({ ...p, property_type: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                  <option value="hotel">Otel</option>
                  <option value="pansiyon">Pansiyon</option>
                  <option value="villa">Villa</option>
                  <option value="bungalov">Bungalov</option>
                  <option value="apart_otel">Apart Otel</option>
                </select>
              </div>
              <textarea placeholder="Açıklama" value={newHotel.description} onChange={e => setNewHotel(p => ({ ...p, description: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 80 }} />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <input type="text" placeholder="Telefon" value={newHotel.phone} onChange={e => setNewHotel(p => ({ ...p, phone: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
                <input type="email" placeholder="E-posta" value={newHotel.email} onChange={e => setNewHotel(p => ({ ...p, email: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              </div>
              <button onClick={handleCreateHotel} style={{ padding: "12px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", marginTop: 8 }}>
                <i className="ti ti-plus" style={{ marginRight: 6 }} />Otel Oluştur
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
