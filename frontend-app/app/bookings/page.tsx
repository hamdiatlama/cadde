"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const STATUS_LABELS: Record<string, string> = {
  pending: "Bekliyor",
  confirmed: "Onaylandı",
  checked_in: "Giriş Yapıldı",
  checked_out: "Çıkış Yapıldı",
  cancelled: "İptal Edildi",
};

const STATUS_COLORS: Record<string, string> = {
  pending: "#f59e0b",
  confirmed: "#22c55e",
  checked_in: "#3b82f6",
  checked_out: "#8FAAC8",
  cancelled: "#ef4444",
};

export default function BookingsPage() {
  const router = useRouter();
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancelMsg, setCancelMsg] = useState("");
  const [reviewId, setReviewId] = useState<number | null>(null);
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewComment, setReviewComment] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API}/hotels/bookings/my`);
        const data = await res.json();
        setBookings(Array.isArray(data) ? data : data?.value || []);
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, []);

  async function handleCancel(bookingNo: string) {
    if (!confirm("Rezervasyonu iptal etmek istediğinize emin misiniz?")) return;
    try {
      const res = await fetch(`${API}/hotels/bookings/${bookingNo}/cancel`, { method: "POST" });
      if (res.ok) {
        setCancelMsg("✅ İptal edildi");
        setBookings(prev => prev.map(b => b.booking_no === bookingNo ? { ...b, status: "cancelled" } : b));
      } else {
        const err = await res.json();
        setCancelMsg("❌ " + (err.detail || "İptal başarısız"));
      }
    } catch (_) {
      setCancelMsg("❌ Bağlantı hatası");
    }
  }

  async function handleReview(bookingNo: string) {
    try {
      const res = await fetch(`${API}/hotels/bookings/${bookingNo}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rating: reviewRating, comment: reviewComment }),
      });
      if (res.ok) {
        setCancelMsg("✅ Değerlendirme gönderildi");
        setReviewId(null);
        setReviewComment("");
        setReviewRating(5);
      } else {
        const err = await res.json();
        setCancelMsg("❌ " + (err.detail || "Değerlendirme başarısız"));
      }
    } catch (_) {
      setCancelMsg("❌ Bağlantı hatası");
    }
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
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/hotels")}>Konaklama</span>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/food")}>Yemek</span>
        </div>
      </nav>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "24px 32px" }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: -0.8, marginBottom: 20 }}>Rezervasyonlarım</h1>

        {cancelMsg && (
          <div style={{ padding: "10px 14px", borderRadius: 8, background: cancelMsg.includes("✅") ? "#dcfce7" : "#fef2f2", color: cancelMsg.includes("✅") ? "#16a34a" : "#dc2626", fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
            {cancelMsg.replace("✅ ", "").replace("❌ ", "")}
          </div>
        )}

        {loading ? (
          <p style={{ color: "#8FAAC8", fontSize: 14 }}>Yükleniyor...</p>
        ) : bookings.length === 0 ? (
          <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14 }}>
            Henüz rezervasyonunuz yok
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {bookings.map((b: any) => (
              <div key={b.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                  <div>
                    <div style={{ fontSize: 15, fontWeight: 700, marginBottom: 2 }}>{b.hotel_name || "Otel"}</div>
                    <div style={{ fontSize: 12, color: "#8FAAC8" }}>No: {b.booking_no}</div>
                  </div>
                  <span style={{ fontSize: 11, fontWeight: 700, padding: "4px 10px", borderRadius: 20, background: `${STATUS_COLORS[b.status] || "#8FAAC8"}15`, color: STATUS_COLORS[b.status] || "#8FAAC8", border: `1px solid ${STATUS_COLORS[b.status] || "#8FAAC8"}` }}>
                    {STATUS_LABELS[b.status] || b.status}
                  </span>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, fontSize: 13, color: "#5A7499", marginBottom: 12 }}>
                  <div><i className="ti ti-calendar" style={{ fontSize: 12 }} /> {b.check_in?.slice(0, 10)} → {b.check_out?.slice(0, 10)}</div>
                  <div><i className="ti ti-users" style={{ fontSize: 12 }} /> {b.adults || 1} yetişkin</div>
                  <div><i className="ti ti-bed" style={{ fontSize: 12 }} /> {b.room_type_name || "Oda"}</div>
                  <div><i className="ti ti-currency-lira" style={{ fontSize: 12 }} /> ₺{b.total_price?.toFixed(0)}</div>
                </div>

                <div style={{ display: "flex", gap: 8, borderTop: "1px solid #D6E4FA", paddingTop: 12 }}>
                  {b.status === "confirmed" || b.status === "pending" ? (
                    <button onClick={() => handleCancel(b.booking_no)} style={{ padding: "7px 14px", background: "#fef2f2", color: "#dc2626", border: "1px solid #fecaca", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                      <i className="ti ti-x" style={{ fontSize: 12 }} /> İptal Et
                    </button>
                  ) : null}
                  {b.status === "checked_out" && (
                    <button onClick={() => setReviewId(reviewId === b.id ? null : b.id)} style={{ padding: "7px 14px", background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                      <i className="ti ti-star" style={{ fontSize: 12 }} /> Değerlendir
                    </button>
                  )}
                </div>

                {reviewId === b.id && (
                  <div style={{ marginTop: 12, padding: 14, background: "#EEF4FF", borderRadius: 8 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>Değerlendirme Yap</div>
                    <div style={{ display: "flex", gap: 4, marginBottom: 8 }}>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                        <span key={n} onClick={() => setReviewRating(n)} style={{ cursor: "pointer", fontSize: 18, color: n <= reviewRating ? "#FFD43B" : "#D6E4FA" }}>★</span>
                      ))}
                    </div>
                    <textarea value={reviewComment} onChange={e => setReviewComment(e.target.value)} placeholder="Yorumunuz..."
                      style={{ width: "100%", padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 60 }} />
                    <button onClick={() => handleReview(b.booking_no)} style={{ marginTop: 8, padding: "7px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>Gönder</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
