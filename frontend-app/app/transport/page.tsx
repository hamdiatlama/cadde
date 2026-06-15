"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const VEHICLE_TYPES = [
  { value: "", label: "Tümü", icon: "ti-arrows-exchange" },
  { value: "bus", label: "Otobüs", icon: "ti-bus" },
  { value: "minibus", label: "Minibüs", icon: "ti-bus" },
  { value: "dolmus", label: "Dolmuş", icon: "ti-car" },
  { value: "train", label: "Tren", icon: "ti-train" },
  { value: "high_speed_train", label: "Hızlı Tren", icon: "ti-train" },
  { value: "airplane", label: "Uçak", icon: "ti-plane" },
  { value: "ferry", label: "Gemi/Feribot", icon: "ti-ship" },
];

export default function TransportPage() {
  const router = useRouter();
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [vehicleType, setVehicleType] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [stations, setStations] = useState<any[]>([]);
  const [originId, setOriginId] = useState<number | null>(null);
  const [destId, setDestId] = useState<number | null>(null);
  const [originSuggestions, setOriginSuggestions] = useState<any[]>([]);
  const [destSuggestions, setDestSuggestions] = useState<any[]>([]);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    async function loadStations() {
      try {
        const res = await fetch(`${API}/transport/stations`);
        const data = await res.json();
        setStations(Array.isArray(data) ? data : []);
      } catch (_) {}
    }
    loadStations();
  }, []);

  function handleOriginChange(val: string) {
    setOrigin(val);
    setOriginId(null);
    if (val.length < 2) { setOriginSuggestions([]); return; }
    setOriginSuggestions(stations.filter(s =>
      s.name.toLowerCase().includes(val.toLowerCase()) ||
      s.city.toLowerCase().includes(val.toLowerCase())
    ).slice(0, 8));
  }

  function handleDestChange(val: string) {
    setDestination(val);
    setDestId(null);
    if (val.length < 2) { setDestSuggestions([]); return; }
    setDestSuggestions(stations.filter(s =>
      s.name.toLowerCase().includes(val.toLowerCase()) ||
      s.city.toLowerCase().includes(val.toLowerCase())
    ).slice(0, 8));
  }

  async function handleSearch() {
    if (!originId || !destId) return;
    setLoading(true);
    setSearched(true);
    try {
      const params = new URLSearchParams({ origin_id: String(originId), destination_id: String(destId), date });
      if (vehicleType) params.set("vehicle_type", vehicleType);
      const res = await fetch(`${API}/transport/search?${params}`);
      const data = await res.json();
      setResults(Array.isArray(data) ? data : []);
    } catch (_) {}
    setLoading(false);
  }

  function getVehicleLabel(val: string) {
    const v = VEHICLE_TYPES.find(t => t.value === val);
    return v ? v.label : val;
  }

  function getVehicleIcon(val: string) {
    const v = VEHICLE_TYPES.find(t => t.value === val);
    return v ? v.icon : "ti-arrows-exchange";
  }

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <style>{`
        .trip-card:hover { border-color: #4A7FD4; transform: translateY(-2px); box-shadow: 0 4px 16px rgba(74,127,212,0.1); }
        .suggestion { transition: background .1s; }
        .suggestion:hover { background: #EEF4FF; }
      `}</style>

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#4A7FD4", fontWeight: 600, cursor: "pointer" }}>Ulaşım</span>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/hotels")}>Konaklama</span>
        </div>
      </nav>

      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "24px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 }}>
          <h1 style={{ fontSize: 26, fontWeight: 700, letterSpacing: -0.8, margin: 0 }}>Ulaşım</h1>
          <button onClick={() => router.push("/transport/dashboard")} style={{ padding: "7px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
            <i className="ti ti-building" style={{ fontSize: 14 }} /> Firma Paneli
          </button>
        </div>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20, display: "flex", alignItems: "center", gap: 8 }}>
          Otobüs, minibüs, dolmuş, tren, hızlı tren, uçak, feribot — tüm firmaların seferleri
          <span style={{ fontSize: 10, fontWeight: 700, padding: "2px 8px", borderRadius: 12, background: "#fef3c7", color: "#d97706", border: "1px solid #fde68a" }}>%2 KOMISYON</span>
        </p>

        <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 20, marginBottom: 20 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr auto 1fr auto auto", gap: 12, alignItems: "end" }}>
            <div style={{ position: "relative" }}>
              <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Nereden</label>
              <input type="text" value={origin} onChange={e => handleOriginChange(e.target.value)} placeholder="Şehir veya istasyon" style={{ width: "100%", padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              {originSuggestions.length > 0 && (
                <div style={{ position: "absolute", top: "100%", left: 0, right: 0, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, zIndex: 10, marginTop: 4, overflow: "hidden" }}>
                  {originSuggestions.map(s => (
                    <div key={s.id} className="suggestion" style={{ padding: "8px 12px", cursor: "pointer", fontSize: 13, borderBottom: "1px solid #EEF4FF" }}
                      onClick={() => { setOrigin(`${s.city} - ${s.name}`); setOriginId(s.id); setOriginSuggestions([]); }}>
                      <span style={{ fontWeight: 600 }}>{s.city}</span> <span style={{ color: "#8FAAC8" }}>{s.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div style={{ padding: "10px 0", cursor: "pointer", color: "#4A7FD4" }} onClick={() => {
              const tmpO = origin; const tmpD = destination; const tmpOi = originId; const tmpDi = destId;
              setOrigin(tmpD); setDestination(tmpO); setOriginId(tmpDi); setDestId(tmpOi);
            }}><i className="ti ti-arrows-left-right" style={{ fontSize: 20 }} /></div>

            <div style={{ position: "relative" }}>
              <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Nereye</label>
              <input type="text" value={destination} onChange={e => handleDestChange(e.target.value)} placeholder="Şehir veya istasyon" style={{ width: "100%", padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              {destSuggestions.length > 0 && (
                <div style={{ position: "absolute", top: "100%", left: 0, right: 0, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, zIndex: 10, marginTop: 4, overflow: "hidden" }}>
                  {destSuggestions.map(s => (
                    <div key={s.id} className="suggestion" style={{ padding: "8px 12px", cursor: "pointer", fontSize: 13, borderBottom: "1px solid #EEF4FF" }}
                      onClick={() => { setDestination(`${s.city} - ${s.name}`); setDestId(s.id); setDestSuggestions([]); }}>
                      <span style={{ fontWeight: 600 }}>{s.city}</span> <span style={{ color: "#8FAAC8" }}>{s.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>Tarih</label>
              <input type="date" value={date} onChange={e => setDate(e.target.value)} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
            </div>

            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" }}>&nbsp;</label>
              <button onClick={handleSearch} style={{ padding: "10px 24px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                <i className="ti ti-search" style={{ marginRight: 6 }} />Ara
              </button>
            </div>
          </div>

          <div style={{ display: "flex", gap: 6, marginTop: 14, flexWrap: "wrap" }}>
            {VEHICLE_TYPES.filter(v => v.value).map(v => (
              <span key={v.value} onClick={() => setVehicleType(vehicleType === v.value ? "" : v.value)} style={{ display: "inline-flex", alignItems: "center", gap: 5, padding: "5px 12px", background: vehicleType === v.value ? "#4A7FD4" : "#fff", border: `1px solid ${vehicleType === v.value ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 20, fontSize: 12, color: vehicleType === v.value ? "#fff" : "#5A7499", cursor: "pointer", fontWeight: 500, transition: "all .15s" }}>
                <i className={`ti ${v.icon}`} style={{ fontSize: 12 }} /> {v.label}
              </span>
            ))}
          </div>
        </div>

        {loading ? (
          <p style={{ color: "#8FAAC8", fontSize: 14 }}>Yükleniyor...</p>
        ) : searched && results.length === 0 ? (
          <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14 }}>
            <i className="ti ti-search-off" style={{ fontSize: 32, display: "block", marginBottom: 8 }} />
            Sefer bulunamadı
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {searched && <div style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 4 }}>{results.length} sefer bulundu</div>}
            {results.map((s: any) => (
              <div key={s.id} className="trip-card" onClick={() => router.push(`/transport/${s.id}`)} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 18, cursor: "pointer", transition: "all .15s" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div style={{ width: 44, height: 44, borderRadius: 10, background: "#EEF4FF", border: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "center" }}>
                      <i className={`ti ${getVehicleIcon(s.vehicle_type)}`} style={{ fontSize: 22, color: "#4A7FD4" }} />
                    </div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 600, display: "flex", alignItems: "center", gap: 6 }}>
                        {s.company_name || "Firma"}
                        <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 6px", borderRadius: 12, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>
                          {getVehicleLabel(s.vehicle_type)}
                        </span>
                        {(s.vehicle_type === "airplane" || s.vehicle_type === "train" || s.vehicle_type === "high_speed_train") && (
                          <span style={{ fontSize: 9, fontWeight: 700, padding: "2px 6px", borderRadius: 12, background: "#fef3c7", color: "#d97706", border: "1px solid #fde68a", letterSpacing: 0.3 }}>ACENTE</span>
                        )}
                      </div>
                      <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 2 }}>{s.vehicle_number || ""}</div>
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 20, fontWeight: 700, color: "#4A7FD4" }}>₺{s.base_price?.toFixed(0)}</div>
                    <div style={{ fontSize: 11, color: "#8FAAC8" }}>{s.available_seats} koltuk</div>
                  </div>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 10, paddingTop: 10, borderTop: "1px solid #EEF4FF" }}>
                  <div style={{ fontSize: 18, fontWeight: 700 }}>{s.departure_time?.slice(0, 5)}</div>
                  <div style={{ flex: 1, height: 1, background: "#D6E4FA", position: "relative" }}>
                    <div style={{ position: "absolute", top: -4, right: 0, width: 8, height: 8, borderRadius: "50%", background: "#4A7FD4" }} />
                    <div style={{ position: "absolute", top: -4, left: 0, width: 8, height: 8, borderRadius: "50%", background: "#4A7FD4" }} />
                  </div>
                  <div style={{ fontSize: 18, fontWeight: 700 }}>{s.arrival_time?.slice(0, 5)}</div>
                  <span style={{ fontSize: 11, color: "#8FAAC8", marginLeft: "auto" }}>{s.duration_minutes} dk</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
