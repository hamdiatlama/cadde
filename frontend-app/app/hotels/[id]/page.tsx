"use client";
import { useRouter, useParams } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const PROPERTY_TYPES: Record<string, string> = {
  hotel: "Otel", pansiyon: "Pansiyon", villa: "Villa", yazlik: "Yazlık",
  bungalov: "Bungalov", apart_otel: "Apart Otel", tiny_house: "Tiny House",
  dag_evi: "Dağ Evi", oda_kiralama: "Oda Kiralama", tatil_koyu: "Tatil Köyü",
  koy_evi: "Köy Evi",
};

export default function HotelDetailPage() {
  const router = useRouter();
  const params = useParams();
  const [hotel, setHotel] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState("1");
  const [selectedRoom, setSelectedRoom] = useState<any>(null);
  const [price, setPrice] = useState<any>(null);
  const [bookingMsg, setBookingMsg] = useState("");
  const [rooms, setRooms] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API}/hotels/${params.id}`);
        const data = await res.json();
        setHotel(data);
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, [params.id]);

  useEffect(() => {
    if (!checkIn || !checkOut || !params.id) return;
    async function loadRooms() {
      try {
        const res = await fetch(`${API}/hotels/${params.id}/rooms/available?check_in=${checkIn}&check_out=${checkOut}&guests=${guests}`);
        const data = await res.json();
        setRooms(Array.isArray(data) ? data : data?.value || []);
      } catch (_) {}
    }
    loadRooms();
  }, [checkIn, checkOut, guests, params.id]);

  async function handleCalculatePrice(roomTypeId: number) {
    try {
      const res = await fetch(`${API}/hotels/${params.id}/calculate-price`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_type_id: roomTypeId, check_in: checkIn, check_out: checkOut, room_count: 1 }),
      });
      const data = await res.json();
      setPrice(data);
      setSelectedRoom(rooms.find((r: any) => r.id === roomTypeId));
    } catch (_) {
      setPrice(null);
    }
  }

  async function handleBook() {
    if (!selectedRoom || !checkIn || !checkOut) return;
    try {
      const res = await fetch(`${API}/hotels/${params.id}/book`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_type_id: selectedRoom.id, check_in: checkIn, check_out: checkOut, guests: parseInt(guests), room_count: 1 }),
      });
      if (res.ok) {
        setBookingMsg("✅ Rezervasyon başarıyla oluşturuldu!");
      } else {
        const err = await res.json();
        setBookingMsg("❌ " + (err.detail || "Rezervasyon başarısız"));
      }
    } catch (_) {
      setBookingMsg("❌ Bağlantı hatası");
    }
  }

  if (loading) return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", padding: 40, color: "#8FAAC8" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      Yükleniyor...
    </main>
  );

  if (!hotel) return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", padding: 40, color: "#8FAAC8" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      Otel bulunamadı
    </main>
  );

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <style>{`
        .room-card:hover { border-color: #4A7FD4; }
      `}</style>

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#4A7FD4", fontWeight: 600, cursor: "pointer" }} onClick={() => router.push("/hotels")}>Konaklama</span>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/food")}>Yemek</span>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "24px 32px" }}>
        <span onClick={() => router.push("/hotels")} style={{ fontSize: 12, color: "#4A7FD4", cursor: "pointer", fontWeight: 600, display: "inline-flex", alignItems: "center", gap: 4, marginBottom: 16 }}>
          <i className="ti ti-arrow-left" style={{ fontSize: 14 }} /> Konaklama
        </span>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 24 }}>
          <div style={{ height: 240, borderRadius: 12, background: "#D6E4FA", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
            <i className="ti ti-building" style={{ fontSize: 64, color: "#8FAAC8" }} />
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            {[1, 2, 3].map(i => (
              <div key={i} style={{ height: 114, borderRadius: 12, background: "#D6E4FA", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
                <i className="ti ti-photo" style={{ fontSize: 24, color: "#8FAAC8" }} />
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 360px", gap: 32 }}>
          <div>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16 }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <h1 style={{ fontSize: 26, fontWeight: 700, letterSpacing: -0.8, margin: 0 }}>{hotel.name}</h1>
                  <span style={{ fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                    {PROPERTY_TYPES[hotel.property_type] || hotel.property_type}
                  </span>
                </div>
                <div style={{ fontSize: 13, color: "#8FAAC8", display: "flex", alignItems: "center", gap: 8 }}>
                  <i className="ti ti-map-pin" style={{ fontSize: 13 }} /> {hotel.city} {hotel.star_rating > 0 && "★".repeat(Math.min(hotel.star_rating, 5))}
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 4, justifyContent: "flex-end" }}>
                  <i className="ti ti-star" style={{ color: "#FFD43B" }} />
                  <span style={{ fontSize: 20, fontWeight: 700 }}>{hotel.rating?.toFixed(1) || "0.0"}</span>
                </div>
                <div style={{ fontSize: 12, color: "#8FAAC8" }}>{hotel.review_count || 0} değerlendirme</div>
              </div>
            </div>

            {hotel.description && (
              <p style={{ fontSize: 13, color: "#5A7499", lineHeight: 1.6, marginTop: 16 }}>{hotel.description}</p>
            )}

            {hotel.owner_info && (
              <div style={{ marginTop: 20, padding: 16, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>İşletme Bilgileri</div>
                {hotel.company_name && <div style={{ fontSize: 13, fontWeight: 600, color: "#1A2B4A" }}>{hotel.company_name}</div>}
                {hotel.company_description && <div style={{ fontSize: 12, color: "#5A7499", marginTop: 4 }}>{hotel.company_description}</div>}
              </div>
            )}

            <div style={{ marginTop: 28 }}>
              <h2 style={{ fontSize: 18, fontWeight: 700, letterSpacing: -0.5, marginBottom: 14 }}>Odalar</h2>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {rooms.length === 0 ? (
                  <div style={{ fontSize: 13, color: "#8FAAC8" }}>Tarih seçerek müsait odaları görün</div>
                ) : rooms.map((r: any) => (
                  <div key={r.id} className="room-card" style={{ background: "#fff", border: `1px solid ${selectedRoom?.id === r.id ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 10, padding: 16, cursor: "pointer", transition: "all .15s" }}
                    onClick={() => handleCalculatePrice(r.id)}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <div style={{ fontSize: 15, fontWeight: 600 }}>{r.name}</div>
                        <div style={{ fontSize: 12, color: "#8FAAC8", marginTop: 4 }}>
                          <i className="ti ti-users" style={{ fontSize: 12 }} /> {r.max_guests} kişi
                          {r.bed_type && <span style={{ marginLeft: 12 }}><i className="ti ti-bed" style={{ fontSize: 12 }} /> {r.bed_type}</span>}
                          {r.size_sqm && <span style={{ marginLeft: 12 }}><i className="ti ti-maximize" style={{ fontSize: 12 }} /> {r.size_sqm}m²</span>}
                        </div>
                      </div>
                      <div style={{ textAlign: "right" }}>
                        <div style={{ fontSize: 20, fontWeight: 700, color: "#4A7FD4" }}>₺{r.base_price?.toFixed(0)}</div>
                        <div style={{ fontSize: 11, color: "#8FAAC8" }}>gecelik</div>
                      </div>
                    </div>
                    {r.amenities?.length > 0 && (
                      <div style={{ display: "flex", gap: 4, marginTop: 10, flexWrap: "wrap" }}>
                        {r.amenities.map((a: any) => (
                          <span key={a.id} style={{ fontSize: 10, fontWeight: 600, padding: "2px 8px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>{a.name}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {price && selectedRoom && (
                <div style={{ marginTop: 16, padding: 16, background: "#fff", border: "1px solid #4A7FD4", borderRadius: 10 }}>
                  <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>Fiyat Detayı</div>
                  <div style={{ fontSize: 13, color: "#5A7499" }}>
                    {price.breakdown?.map((b: any, i: number) => (
                      <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0" }}>
                        <span>{b.date} ({b.day_name})</span>
                        <span>₺{b.price?.toFixed(0)}</span>
                      </div>
                    ))}
                    <div style={{ borderTop: "1px solid #D6E4FA", marginTop: 8, paddingTop: 8, display: "flex", justifyContent: "space-between", fontWeight: 700, color: "#1A2B4A" }}>
                      <span>Toplam</span>
                      <span>₺{price.total_price?.toFixed(0)}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {(hotel.amenities?.length > 0 || hotel.services?.length > 0) && (
              <div style={{ marginTop: 28 }}>
                <h2 style={{ fontSize: 18, fontWeight: 700, letterSpacing: -0.5, marginBottom: 14 }}>Hizmetler & Olanaklar</h2>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {hotel.amenities?.map((a: any) => (
                    <span key={a.id} style={{ padding: "6px 12px", background: "#fff", border: "1px solid #D6E4FA", borderRadius: 20, fontSize: 12, color: "#5A7499" }}>
                      {a.icon && <i className={`ti ti-${a.icon}`} style={{ marginRight: 4, fontSize: 12 }} />}{a.name}
                    </span>
                  ))}
                  {hotel.services?.map((s: any) => (
                    <span key={s.id} style={{ padding: "6px 12px", background: "#EEF4FF", border: "1px solid #4A7FD4", borderRadius: 20, fontSize: 12, color: "#4A7FD4", fontWeight: 500 }}>
                      {s.icon && <i className={`ti ti-${s.icon}`} style={{ marginRight: 4, fontSize: 12 }} />}{s.name}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {hotel.reviews?.length > 0 && (
              <div style={{ marginTop: 28 }}>
                <h2 style={{ fontSize: 18, fontWeight: 700, letterSpacing: -0.5, marginBottom: 14 }}>Değerlendirmeler</h2>
                <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
                  {[
                    { label: "Temizlik", val: hotel.rating_summary?.avg_cleanliness },
                    { label: "Konfor", val: hotel.rating_summary?.avg_comfort },
                    { label: "Konum", val: hotel.rating_summary?.avg_location },
                    { label: "Personel", val: hotel.rating_summary?.avg_staff },
                    { label: "Değer", val: hotel.rating_summary?.avg_value },
                  ].map(s => s.val !== undefined && (
                    <div key={s.label} style={{ padding: "10px 14px", background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, textAlign: "center", flex: 1 }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: "#4A7FD4" }}>{(s.val as number).toFixed(1)}</div>
                      <div style={{ fontSize: 10, color: "#8FAAC8", marginTop: 2 }}>{s.label}</div>
                    </div>
                  ))}
                </div>
                {hotel.reviews.slice(0, 5).map((r: any) => (
                  <div key={r.id} style={{ padding: 14, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, marginBottom: 8 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
                      <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#EEF4FF", border: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "center" }}>
                        <i className="ti ti-user" style={{ fontSize: 14, color: "#4A7FD4" }} />
                      </div>
                      <div>
                        <div style={{ fontSize: 13, fontWeight: 600 }}>{r.user_name || "Misafir"}</div>
                        <div style={{ fontSize: 11, color: "#8FAAC8" }}>{r.created_at?.slice(0, 10)}</div>
                      </div>
                      <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 2 }}>
                        <i className="ti ti-star" style={{ color: "#FFD43B", fontSize: 12 }} />
                        <span style={{ fontSize: 14, fontWeight: 700 }}>{r.rating}</span>
                      </div>
                    </div>
                    {r.comment && <div style={{ fontSize: 12, color: "#5A7499", lineHeight: 1.5 }}>{r.comment}</div>}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div style={{ position: "sticky", top: 80 }}>
            <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20 }}>
              <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 16, letterSpacing: -0.5 }}>Rezervasyon</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Giriş</label>
                  <input type="date" value={checkIn} onChange={e => { setCheckIn(e.target.value); setPrice(null); setSelectedRoom(null); }}
                    style={{ width: "100%", padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Çıkış</label>
                  <input type="date" value={checkOut} onChange={e => { setCheckOut(e.target.value); setPrice(null); setSelectedRoom(null); }}
                    style={{ width: "100%", padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
                </div>
                <div>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Misafir</label>
                  <select value={guests} onChange={e => { setGuests(e.target.value); setPrice(null); setSelectedRoom(null); }}
                    style={{ width: "100%", padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                    {[1, 2, 3, 4, 5, 6, 7, 8].map(n => <option key={n} value={n}>{n} misafir</option>)}
                  </select>
                </div>
              </div>

              {price && selectedRoom && (
                <div style={{ marginTop: 16, paddingTop: 16, borderTop: "1px solid #D6E4FA" }}>
                  <div style={{ fontSize: 13, color: "#5A7499", marginBottom: 4 }}>{selectedRoom.name}</div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                    <span style={{ fontSize: 13, color: "#8FAAC8" }}>{checkIn} → {checkOut}</span>
                    <span style={{ fontSize: 22, fontWeight: 700, color: "#4A7FD4" }}>₺{price.total_price?.toFixed(0)}</span>
                  </div>
                  <button onClick={handleBook} style={{ width: "100%", padding: "12px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 14, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                    Rezervasyon Yap
                  </button>
                  {bookingMsg && <div style={{ marginTop: 10, fontSize: 12, fontWeight: 600, textAlign: "center", color: bookingMsg.includes("✅") ? "#22c55e" : "#ef4444" }}>{bookingMsg}</div>}
                </div>
              )}
            </div>

            {hotel.house_rules && (
              <div style={{ marginTop: 16, padding: 16, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>Ev Kuralları</div>
                <div style={{ fontSize: 12, color: "#5A7499", lineHeight: 1.5, whiteSpace: "pre-line" }}>{hotel.house_rules}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
