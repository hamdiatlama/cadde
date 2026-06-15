"use client";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const STATUS_MAP: Record<string, { label: string; icon: string; color: string }> = {
  "hazirlaniyor": { label: "Hazırlanıyor", icon: "📦", color: "#f59e0b" },
  "teslim_alindi": { label: "Teslim Alındı", icon: "📥", color: "#3b82f6" },
  "dagitim_merkezinde": { label: "Dağıtım Merkezinde", icon: "🏭", color: "#6366f1" },
  "yolda": { label: "Yolda", icon: "🚚", color: "#8b5cf6" },
  "subede": { label: "Şubede", icon: "🏪", color: "#ec4899" },
  "subede_bekliyor": { label: "Şubede Bekliyor", icon: "🏪", color: "#f97316" },
  "teslim_edildi": { label: "Teslim Edildi", icon: "✅", color: "#22c55e" },
  "iade_edildi": { label: "İade Edildi", icon: "↩️", color: "#ef4444" },
  "iade_ediliyor": { label: "İade Ediliyor", icon: "↩️", color: "#dc2626" },
  "iade_talebi": { label: "İade Talebi Var", icon: "⚠️", color: "#f97316" },
  "iade_talebi_inceleniyor": { label: "İade İnceleniyor", icon: "🔍", color: "#a855f7" },
};

export default function CargoTrackingPage() {
  const { trackingNo } = useParams<{ trackingNo: string }>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!trackingNo) return;
    fetch(`${API}/cargo/public/tracking/${trackingNo}`)
      .then(r => r.ok ? r.json() : Promise.reject("Bulunamadı"))
      .then(setData)
      .catch(e => setError(String(e)))
      .finally(() => setLoading(false));
  }, [trackingNo]);

  if (loading) return <div style={styles.center}>Yükleniyor...</div>;
  if (error) return <div style={styles.center}>{error}</div>;
  if (!data) return <div style={styles.center}>Gönderi bulunamadı</div>;

  const st = STATUS_MAP[data.status] || { label: data.status, icon: "📋", color: "#6b7280" };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={{ ...styles.statusBadge, background: st.color }}>{st.icon} {st.label}</div>
        <h2 style={styles.trackingNo}>Takip No: {data.tracking_no}</h2>

        {data.is_fragile && (
          <div style={styles.fragileWarning}>
            ⚠️ Kırılabilir Ürün{data.sensitivity_note ? `: ${data.sensitivity_note}` : ""}
          </div>
        )}

        {data.status === "subede_bekliyor" && (
          <div style={styles.branchNotice}>
            📍 Şubede bekliyor
            {data.branch_wait_until && (
              <span> • Son teslim alma: <strong>{new Date(data.branch_wait_until).toLocaleDateString("tr-TR")}</strong></span>
            )}
          </div>
        )}

        {data.status === "iade_ediliyor" && data.refund && (
          <div style={styles.refundBox}>
            <h3>💰 İade Bilgisi</h3>
            <p>Toplam ödenen: {data.refund.total_paid?.toFixed(2)} TL</p>
            <p>Ürün bedeli: {data.refund.product_price?.toFixed(2)} TL</p>
            <p>Kargo ücreti (gidiş): -{data.refund.delivery_cost?.toFixed(2)} TL</p>
            <p>Kargo ücreti (dönüş): -{data.refund.return_cost?.toFixed(2)} TL</p>
            <p>Kargo firmasına: {data.refund.cargo_total?.toFixed(2)} TL</p>
            <p><strong>Net iade: {data.refund.net_refund?.toFixed(2)} TL</strong></p>
          </div>
        )}

        <div style={styles.infoGrid}>
          <div>
            <strong>Gönderici:</strong> {data.sender_name}
            {data.sender_city && <span> - {data.sender_city}</span>}
          </div>
          <div>
            <strong>Alıcı:</strong> {data.recipient_name} - {data.recipient_city}
          </div>
          {data.estimated_delivery && (
            <div><strong>Tahmini Teslimat:</strong> {data.estimated_delivery}</div>
          )}
        </div>

        <h3 style={styles.sectionTitle}>Kargo Takip Adımları</h3>
        <div style={styles.timeline}>
          {data.steps.map((step: any, i: number) => {
            const s = STATUS_MAP[step.status] || { label: step.status, icon: "📋", color: "#6b7280" };
            return (
              <div key={i} style={styles.timelineItem}>
                <div style={{ ...styles.timelineDot, background: s.color }} />
                <div style={styles.timelineContent}>
                  <strong>{s.icon} {s.label}</strong>
                  {step.location && <div>📍 {step.location}</div>}
                  {step.notes && <div style={styles.note}>{step.notes}</div>}
                  <div style={styles.time}>{step.time}</div>
                </div>
              </div>
            );
          })}
        </div>

        {data.survey && (
          <div style={styles.surveyBox}>
            <h3 style={styles.sectionTitle}>Teslimat Değerlendirmesi</h3>
            <p>Zamanında: {data.survey.delivered_on_time ? "✅ Evet" : "❌ Hayır"}</p>
            {data.survey.package_condition && <p>Durum: {data.survey.package_condition}</p>}
            {data.survey.is_package_damaged && <p style={{ color: "#ef4444" }}>⚠️ Hasar Tespit Edildi</p>}
            {data.survey.is_package_opened && <p style={{ color: "#f97316" }}>⚠️ Ambalaj Açılmış</p>}
            {data.survey.satisfaction_score && <p>Puan: {"⭐".repeat(data.survey.satisfaction_score)}</p>}
          </div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: 600, margin: "40px auto", padding: "0 16px", fontFamily: "sans-serif" },
  card: { background: "#fff", borderRadius: 16, padding: 24, boxShadow: "0 2px 12px rgba(0,0,0,0.08)" },
  center: { textAlign: "center", padding: 40, fontFamily: "sans-serif" },
  statusBadge: { display: "inline-block", padding: "8px 16px", borderRadius: 20, color: "#fff", fontWeight: 600, fontSize: 14 },
  trackingNo: { fontSize: 20, fontWeight: 700, margin: "12px 0" },
  fragileWarning: { background: "#fef3c7", border: "1px solid #f59e0b", borderRadius: 8, padding: "8px 12px", margin: "8px 0", fontSize: 14, color: "#92400e" },
  branchNotice: { background: "#fff7ed", border: "1px solid #f97316", borderRadius: 8, padding: "12px", margin: "8px 0", fontSize: 14, color: "#9a3412" },
  refundBox: { border: "1px solid #d1fae5", borderRadius: 8, padding: 16, marginTop: 16, fontSize: 14, background: "#f0fdf4" },
  infoGrid: { display: "flex", flexDirection: "column", gap: 8, margin: "16px 0", padding: 12, background: "#f9fafb", borderRadius: 8, fontSize: 14 },
  sectionTitle: { fontSize: 16, fontWeight: 600, margin: "20px 0 12px" },
  timeline: { position: "relative", paddingLeft: 24 },
  timelineItem: { display: "flex", gap: 12, marginBottom: 16, position: "relative" },
  timelineDot: { width: 12, height: 12, borderRadius: "50%", flexShrink: 0, marginTop: 4 },
  timelineContent: { flex: 1, fontSize: 14 },
  note: { color: "#6b7280", fontStyle: "italic", marginTop: 2 },
  time: { fontSize: 12, color: "#9ca3af", marginTop: 2 },
  surveyBox: { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginTop: 16, fontSize: 14 },
};
