"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function CargoPage() {
  const router = useRouter();
  const [companies, setCompanies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [trackingNo, setTrackingNo] = useState("");

  useEffect(() => {
    fetch(`${API}/cargo/companies`)
      .then(r => r.json())
      .then(d => setCompanies(Array.isArray(d) ? d : []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const searchTracking = () => {
    if (trackingNo.trim()) {
      router.push(`/cargo/tracking/${trackingNo.trim()}`);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: "0 16px", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>Kargo ve Lojistik</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>
        Gönderinizi takip edin veya kargo firmalarını keşfedin
      </p>

      <div style={{ display: "flex", gap: 8, marginBottom: 32 }}>
        <input
          placeholder="Takip numarası girin..."
          value={trackingNo}
          onChange={e => setTrackingNo(e.target.value)}
          onKeyDown={e => e.key === "Enter" && searchTracking()}
          style={{
            flex: 1, padding: "12px 16px", borderRadius: 12, border: "1px solid #d1d5db",
            fontSize: 16, outline: "none",
          }}
        />
        <button onClick={searchTracking} style={{
          padding: "12px 24px", borderRadius: 12, border: "none", background: "#3b82f6",
          color: "#fff", fontSize: 16, fontWeight: 600, cursor: "pointer",
        }}>Takip Et</button>
      </div>

      <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 16 }}>Kargo Firmaları</h2>
      {loading ? <p>Yükleniyor...</p> : (
        <div style={{ display: "grid", gap: 12 }}>
          {companies.map((c: any) => (
            <div key={c.id} style={{
              display: "flex", alignItems: "center", gap: 16,
              padding: 16, borderRadius: 12, border: "1px solid #e5e7eb",
              background: "#fff",
            }}>
              <div style={{
                width: 48, height: 48, borderRadius: "50%", background: "#3b82f6",
                display: "flex", alignItems: "center", justifyContent: "center",
                color: "#fff", fontSize: 20, fontWeight: 700,
              }}>{c.company_name[0]}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600 }}>{c.company_name}</div>
                <div style={{ fontSize: 13, color: "#6b7280" }}>
                  {c.city || "Türkiye"} • {c.shipment_count || 0} gönderi
                  {c.is_verified && " • ✅ Onaylı"}
                </div>
              </div>
              <div style={{ fontSize: 13, color: "#f59e0b" }}>
                {"★".repeat(Math.round(c.rating || 0))} {c.rating?.toFixed(1) || ""}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
