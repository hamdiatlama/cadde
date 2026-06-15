"use client";
import { useRouter, useParams } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const VEHICLE_LABELS: Record<string, string> = {
  bus: "Otobüs", minibus: "Minibüs", dolmus: "Dolmuş",
  train: "Tren", high_speed_train: "Hızlı Tren",
  airplane: "Uçak", private_jet: "Özel Jet", helicopter: "Helikopter", ferry: "Feribot",
};

export default function ScheduleDetailPage() {
  const router = useRouter();
  const params = useParams();
  const [schedule, setSchedule] = useState<any>(null);
  const [seats, setSeats] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSeat, setSelectedSeat] = useState<any>(null);
  const [passenger, setPassenger] = useState({ name: "", surname: "", idNo: "", phone: "", email: "" });
  const [buyMsg, setBuyMsg] = useState("");
  const [buySuccess, setBuySuccess] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [sRes, seatsRes] = await Promise.all([
          fetch(`${API}/transport/schedules/${params.scheduleId}`),
          fetch(`${API}/transport/schedules/${params.scheduleId}/seats`),
        ]);
        const sData = await sRes.json();
        const seatsData = await seatsRes.json();
        setSchedule(sData.schedule || sData);
        setSeats(Array.isArray(seatsData) ? seatsData : []);
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, [params.scheduleId]);

  async function handleBuy() {
    if (!selectedSeat || !passenger.name) {
      setBuyMsg("Lütfen koltuk seçin ve yolcu bilgilerini girin");
      return;
    }
    try {
      const params_data = new URLSearchParams({
        schedule_id: String(params.scheduleId),
        seat_id: String(selectedSeat.id),
        passenger_name: passenger.name,
        passenger_surname: passenger.surname,
        passenger_id_no: passenger.idNo,
        passenger_phone: passenger.phone,
        passenger_email: passenger.email,
      });
      const res = await fetch(`${API}/transport/buy?${params_data}`, { method: "POST" });
      if (res.ok) {
        setBuySuccess(true);
        setBuyMsg("✅ Bilet satın alındı!");
      } else {
        const err = await res.json();
        setBuyMsg("❌ " + (err.detail || "Satın alma başarısız"));
      }
    } catch (_) {
      setBuyMsg("❌ Bağlantı hatası");
    }
  }

  if (loading) return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", padding: 40, color: "#8FAAC8" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      Yükleniyor...
    </main>
  );

  if (!schedule) return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", padding: 40, color: "#8FAAC8" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      Sefer bulunamadı
    </main>
  );

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
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/transport")}>Ulaşım</span>
        </div>
      </nav>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "24px 32px" }}>
        <span onClick={() => router.push("/transport")} style={{ fontSize: 12, color: "#4A7FD4", cursor: "pointer", fontWeight: 600, display: "inline-flex", alignItems: "center", gap: 4, marginBottom: 16 }}>
          <i className="ti ti-arrow-left" style={{ fontSize: 14 }} /> Ulaşım
        </span>

        <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20, marginBottom: 20 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
            <div>
              <span style={{ fontSize: 12, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                {VEHICLE_LABELS[schedule.vehicle_type] || schedule.vehicle_type}
              </span>
              {schedule.vehicle_number && <span style={{ marginLeft: 8, fontSize: 12, color: "#8FAAC8" }}>{schedule.vehicle_number}</span>}
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, color: "#4A7FD4" }}>₺{schedule.base_price?.toFixed(0)}</div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 24, fontWeight: 700 }}>{schedule.departure_time?.slice(0, 5)}</div>
              <div style={{ fontSize: 11, color: "#8FAAC8" }}>{schedule.departure_date?.slice(0, 10)}</div>
              <div style={{ fontSize: 11, color: "#5A7499" }}>{schedule.origin_name || "Kalkış"}</div>
            </div>
            <div style={{ flex: 1, display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#4A7FD4" }} />
              <div style={{ flex: 1, height: 2, background: "#D6E4FA" }} />
              <span style={{ fontSize: 11, color: "#8FAAC8", whiteSpace: "nowrap" }}>{schedule.duration_minutes} dk</span>
              <div style={{ flex: 1, height: 2, background: "#D6E4FA" }} />
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#4A7FD4" }} />
            </div>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 24, fontWeight: 700 }}>{schedule.arrival_time?.slice(0, 5)}</div>
              <div style={{ fontSize: 11, color: "#8FAAC8" }}>{schedule.departure_date?.slice(0, 10)}</div>
              <div style={{ fontSize: 11, color: "#5A7499" }}>{schedule.destination_name || "Varış"}</div>
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: "#8FAAC8" }}>
            <i className="ti ti-users" style={{ marginRight: 4 }} /> {schedule.available_seats} koltuk müsait
          </div>
        </div>

        {buySuccess ? (
          <div style={{ padding: 40, textAlign: "center", background: "#dcfce7", borderRadius: 12, border: "1px solid #86efac" }}>
            <i className="ti ti-circle-check" style={{ fontSize: 48, color: "#22c55e", display: "block", marginBottom: 8 }} />
            <div style={{ fontSize: 18, fontWeight: 700, color: "#16a34a", marginBottom: 4 }}>Bilet Satın Alındı!</div>
            <div style={{ fontSize: 13, color: "#15803d" }}>Bilet numaranız: {buyMsg.replace("✅ ", "")}</div>
            <button onClick={() => router.push("/transport")} style={{ marginTop: 16, padding: "8px 20px", background: "#22c55e", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
              Yeni Arama
            </button>
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 360px", gap: 20 }}>
            <div>
              <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>Koltuk Seçimi</h2>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20 }}>
                <div style={{ display: "flex", gap: 8, marginBottom: 16, justifyContent: "center" }}>
                  <span style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#5A7499" }}>
                    <div style={{ width: 14, height: 14, borderRadius: 4, background: "#22c55e" }} /> Müsait
                  </span>
                  <span style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#5A7499" }}>
                    <div style={{ width: 14, height: 14, borderRadius: 4, background: "#D6E4FA" }} /> Dolu
                  </span>
                  <span style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#5A7499" }}>
                    <div style={{ width: 14, height: 14, borderRadius: 4, background: "#4A7FD4" }} /> Seçili
                  </span>
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8, maxWidth: 320, margin: "0 auto" }}>
                  {seats.map((seat: any) => (
                    <div key={seat.id} onClick={() => seat.is_available && setSelectedSeat(seat)}
                      style={{ padding: "10px 0", textAlign: "center", borderRadius: 8, cursor: seat.is_available ? "pointer" : "not-allowed", background: selectedSeat?.id === seat.id ? "#4A7FD4" : seat.is_available ? "#fff" : "#EEF4FF", border: `1px solid ${selectedSeat?.id === seat.id ? "#4A7FD4" : seat.is_available ? "#D6E4FA" : "#EEF4FF"}`, color: selectedSeat?.id === seat.id ? "#fff" : seat.is_available ? "#1A2B4A" : "#C4D4E8", fontSize: 12, fontWeight: 600, transition: "all .15s" }}>
                      {seat.seat_number}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 12 }}>Yolcu Bilgileri</h3>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <input type="text" placeholder="Ad *" value={passenger.name} onChange={e => setPassenger(p => ({ ...p, name: e.target.value }))}
                    style={{ padding: "9px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  <input type="text" placeholder="Soyad" value={passenger.surname} onChange={e => setPassenger(p => ({ ...p, surname: e.target.value }))}
                    style={{ padding: "9px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  <input type="text" placeholder="TC Kimlik No" value={passenger.idNo} onChange={e => setPassenger(p => ({ ...p, idNo: e.target.value }))}
                    style={{ padding: "9px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  <input type="tel" placeholder="Telefon" value={passenger.phone} onChange={e => setPassenger(p => ({ ...p, phone: e.target.value }))}
                    style={{ padding: "9px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                  <input type="email" placeholder="E-posta" value={passenger.email} onChange={e => setPassenger(p => ({ ...p, email: e.target.value }))}
                    style={{ padding: "9px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                </div>

                {selectedSeat && (
                  <div style={{ marginTop: 14, padding: 12, background: "#EEF4FF", borderRadius: 8 }}>
                    <div style={{ fontSize: 12, color: "#5A7499" }}>Seçilen Koltuk: <b>{selectedSeat.seat_number}</b></div>
                    <div style={{ fontSize: 12, color: "#5A7499" }}>Sınıf: {selectedSeat.seat_class || "Economy"}</div>
                    <div style={{ fontSize: 18, fontWeight: 700, color: "#4A7FD4", marginTop: 6 }}>₺{(selectedSeat.price || schedule.base_price)?.toFixed(0)}</div>
                  </div>
                )}

                <button onClick={handleBuy} style={{ width: "100%", marginTop: 14, padding: "12px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 14, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                  <i className="ti ti-ticket" style={{ marginRight: 6 }} /> Satın Al
                </button>

                {buyMsg && (
                  <div style={{ marginTop: 10, fontSize: 12, fontWeight: 600, textAlign: "center", color: buyMsg.includes("✅") ? "#22c55e" : "#ef4444" }}>
                    {buyMsg}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
