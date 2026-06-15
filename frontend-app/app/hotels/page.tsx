"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const PROPERTY_TYPES = [
  { value: "", label: "Tümü" },
  { value: "hotel", label: "Otel" },
  { value: "pansiyon", label: "Pansiyon" },
  { value: "villa", label: "Villa" },
  { value: "yazlik", label: "Yazlık" },
  { value: "bungalov", label: "Bungalov" },
  { value: "apart_otel", label: "Apart Otel" },
  { value: "tiny_house", label: "Tiny House" },
  { value: "dag_evi", label: "Dağ Evi" },
  { value: "oda_kiralama", label: "Oda Kiralama" },
  { value: "tatil_koyu", label: "Tatil Köyü" },
  { value: "koy_evi", label: "Köy Evi" },
];

export default function HotelsPage() {
  const router = useRouter();
  const [hotels, setHotels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [city, setCity] = useState("");
  const [propertyType, setPropertyType] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [guests, setGuests] = useState("");
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const params = new URLSearchParams();
        if (city) params.set("city", city);
        if (propertyType) params.set("property_type", propertyType);
        if (sortBy) params.set("sort_by", sortBy);
        if (guests) params.set("guests", guests);
        if (checkIn) params.set("check_in", checkIn);
        if (checkOut) params.set("check_out", checkOut);
        params.set("per_page", "50");

        const res = await fetch(`${API}/hotels/?${params}`);
        const data = await res.json();
        setHotels(Array.isArray(data) ? data : data?.value || []);
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, [city, propertyType, sortBy, guests, checkIn, checkOut]);

  function getTypeLabel(val: string) {
    const t = PROPERTY_TYPES.find(p => p.value === val);
    return t ? t.label : val;
  }

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <style>{`
        .h-card { transition: all .15s; }
        .h-card:hover { border-color: #4A7FD4; transform: translateY(-2px); box-shadow: 0 4px 16px rgba(74,127,212,0.1); }
      `}</style>

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#4A7FD4", fontWeight: 600, cursor: "pointer" }}>Konaklama</span>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/food")}>Yemek</span>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/search")}>Keşfet</span>
        </div>
      </nav>

      <div style={{ padding: "24px 32px", maxWidth: 1200, margin: "0 auto" }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: -1, marginBottom: 4 }}>Konaklama</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 24 }}>Oteller, villalar, bungalovlar ve daha fazlası</p>

        <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden", flex: 1, maxWidth: 280 }}>
            <i className="ti ti-map-pin" style={{ padding: "0 10px", color: "#8FAAC8", fontSize: 16 }} />
            <input type="text" placeholder="Şehir" value={city} onChange={e => setCity(e.target.value)} style={{ flex: 1, border: "none", outline: "none", background: "transparent", fontFamily: "inherit", fontSize: 13, color: "#1A2B4A", padding: "10px 0" }} />
          </div>
          <select value={propertyType} onChange={e => setPropertyType(e.target.value)} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, color: "#1A2B4A", background: "#fff", fontFamily: "inherit", cursor: "pointer", outline: "none" }}>
            {PROPERTY_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
          <div style={{ display: "flex", alignItems: "center", background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
            <i className="ti ti-users" style={{ padding: "0 10px", color: "#8FAAC8", fontSize: 16 }} />
            <input type="number" min="1" placeholder="Misafir" value={guests} onChange={e => setGuests(e.target.value)} style={{ width: 80, border: "none", outline: "none", background: "transparent", fontFamily: "inherit", fontSize: 13, color: "#1A2B4A", padding: "10px 0" }} />
          </div>
          <input type="date" value={checkIn} onChange={e => setCheckIn(e.target.value)} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, color: "#1A2B4A", background: "#fff", fontFamily: "inherit", outline: "none" }} />
          <input type="date" value={checkOut} onChange={e => setCheckOut(e.target.value)} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, color: "#1A2B4A", background: "#fff", fontFamily: "inherit", outline: "none" }} />
          <select value={sortBy} onChange={e => setSortBy(e.target.value)} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, color: "#1A2B4A", background: "#fff", fontFamily: "inherit", cursor: "pointer", outline: "none" }}>
            <option value="created_at">En Yeni</option>
            <option value="rating">Puana Göre</option>
            <option value="popular">Popüler</option>
            <option value="featured">Öne Çıkan</option>
            <option value="price_asc">Fiyat (Düşükten Yükseğe)</option>
            <option value="price_desc">Fiyat (Yüksekten Düşüğe)</option>
          </select>
        </div>

        {loading ? (
          <p style={{ color: "#8FAAC8", fontSize: 14 }}>Yükleniyor...</p>
        ) : hotels.length === 0 ? (
          <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14 }}>Konaklama bulunamadı</div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 4 }}>{hotels.length} sonuç</div>
            {hotels.map((h: any) => (
              <div key={h.id} className="h-card" onClick={() => router.push(`/hotels/${h.slug || h.id}`)} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20, display: "flex", gap: 20, cursor: "pointer" }}>
                <div style={{ width: 140, height: 100, borderRadius: 8, background: "#EEF4FF", border: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, overflow: "hidden" }}>
                  <i className="ti ti-building" style={{ fontSize: 36, color: "#4A7FD4" }} />
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <div>
                      <div style={{ fontSize: 16, fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}>
                        {h.name}
                        <span style={{ fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                          {getTypeLabel(h.property_type)}
                        </span>
                      </div>
                      <div style={{ fontSize: 12, color: "#8FAAC8", marginTop: 4, display: "flex", alignItems: "center", gap: 6 }}>
                        <i className="ti ti-map-pin" style={{ fontSize: 12 }} /> {h.city || "Belirtilmemiş"}
                        {h.star_rating > 0 && (
                          <span style={{ marginLeft: 8 }}>{"★".repeat(Math.min(h.star_rating, 5))}</span>
                        )}
                      </div>
                    </div>
                    <div style={{ textAlign: "right", flexShrink: 0 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 4, justifyContent: "flex-end" }}>
                        <i className="ti ti-star" style={{ color: "#FFD43B", fontSize: 14 }} />
                        <span style={{ fontSize: 16, fontWeight: 700 }}>{h.rating?.toFixed(1) || "0.0"}</span>
                        <span style={{ fontSize: 11, color: "#8FAAC8" }}>({h.review_count || 0})</span>
                      </div>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 6, marginTop: 10, flexWrap: "wrap" }}>
                    <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                      <i className="ti ti-bed" style={{ fontSize: 11, marginRight: 4 }} />Konaklama
                    </span>
                    {h.check_in_time && (
                      <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                        <i className="ti ti-clock" style={{ fontSize: 11, marginRight: 4 }} />Giriş: {h.check_in_time}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
