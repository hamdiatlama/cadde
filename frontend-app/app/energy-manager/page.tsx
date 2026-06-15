"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Meter = { id: number; hotel_id: number; meter_type: string; meter_name: string; location: string; unit: string; is_active: boolean };
type Reading = { id: number; meter_id: number; reading_value: number; unit: string; reading_date: string; source: string };
type Report = { id: number; report_date: string; total_electricity_kwh: number; total_water_m3: number; total_gas_m3: number; total_cost: number; electricity_cost: number; water_cost: number; gas_cost: number; occupancy_rate: number; cost_per_occupied_room: number };
type Rule = { id: number; rule_name: string; trigger_type: string; conditions: any; actions: any; estimated_savings_percent: number; is_active: boolean };
type Cert = { id: number; certification_name: string; issuing_body: string; certificate_number: string; awarded_date: string; expiry_date: string; is_verified: boolean };
type Dashboard = { today: any; this_month: any; this_year: any; total_cost: number; occupancy_rate: number; cost_per_occupied_room: number; meter_count: number; active_rules: number; verified_certifications: number; certs: Cert[] };

export default function EnergyManagerPage() {
  const router = useRouter();
  const hotel_id = 1;

  const [meters, setMeters] = useState<Meter[]>([]);
  const [readings, setReadings] = useState<Reading[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [rules, setRules] = useState<Rule[]>([]);
  const [certs, setCerts] = useState<Cert[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [summary, setSummary] = useState({ electricity: 0, water: 0, gas: 0 });
  const [tab, setTab] = useState("dashboard");

  const [readingMeterId, setReadingMeterId] = useState(0);
  const [readingValue, setReadingValue] = useState("");
  const [ruleName, setRuleName] = useState("");
  const [triggerType, setTriggerType] = useState("occupancy");
  const [conditions, setConditions] = useState("{}");
  const [actions, setActions] = useState("{}");
  const [savingsPct, setSavingsPct] = useState("5");

  const [certName, setCertName] = useState("");
  const [issuingBody, setIssuingBody] = useState("");
  const [certNo, setCertNo] = useState("");
  const [awarded, setAwarded] = useState("");
  const [expiry, setExpiry] = useState("");

  const [meterType, setMeterType] = useState("electricity");
  const [meterName, setMeterName] = useState("");
  const [meterLocation, setMeterLocation] = useState("");
  const [meterUnit, setMeterUnit] = useState("kWh");

  async function api(path: string, opts?: RequestInit) {
    const res = await fetch(`${API}${path}`, {
      ...opts,
      headers: { "Content-Type": "application/json", ...opts?.headers },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  function loadAll() {
    api(`/energy-manager/meters/${hotel_id}`).then(setMeters).catch(() => {});
    api(`/energy-manager/reports/${hotel_id}`).then(setReports).catch(() => {});
    api(`/energy-manager/rules/${hotel_id}`).then(setRules).catch(() => {});
    api(`/energy-manager/certifications/${hotel_id}`).then(setCerts).catch(() => {});
    api(`/energy-manager/dashboard/${hotel_id}`).then(setDashboard).catch(() => {});
    api(`/energy-manager/summary/${hotel_id}`).then(setSummary).catch(() => {});
  }

  useEffect(() => { loadAll(); }, []);

  async function handleCreateMeter() {
    const q = new URLSearchParams({ hotel_id: String(hotel_id), meter_type: meterType, meter_name: meterName, location: meterLocation, unit: meterUnit }).toString();
    await api(`/energy-manager/meters?${q}`, { method: "POST" });
    setMeterName(""); setMeterLocation(""); loadAll();
  }

  async function handleLogReading() {
    if (!readingMeterId) return;
    const q = new URLSearchParams({ meter_id: String(readingMeterId), value: readingValue, source: "manual" }).toString();
    await api(`/energy-manager/readings?${q}`, { method: "POST" });
    setReadingValue(""); loadAll();
  }

  async function handleGenerateReport() {
    await api(`/energy-manager/generate-report/${hotel_id}`, { method: "POST" });
    loadAll();
  }

  async function handleCreateRule() {
    const q = new URLSearchParams({ hotel_id: String(hotel_id), rule_name: ruleName, trigger_type: triggerType, conditions, actions, estimated_savings_percent: savingsPct }).toString();
    await api(`/energy-manager/rules?${q}`, { method: "POST" });
    setRuleName(""); loadAll();
  }

  async function handleDeleteRule(id: number) {
    await api(`/energy-manager/rules/${id}`, { method: "DELETE" });
    loadAll();
  }

  async function handleAddCert() {
    const q = new URLSearchParams({ hotel_id: String(hotel_id), certification_name: certName, issuing_body: issuingBody, certificate_number: certNo, awarded_date: awarded, expiry_date: expiry }).toString();
    await api(`/energy-manager/certifications?${q}`, { method: "POST" });
    setCertName(""); setIssuingBody(""); setCertNo(""); setAwarded(""); setExpiry(""); loadAll();
  }

  const maxConsumption = Math.max(summary.electricity, summary.water * 10, summary.gas * 10, 1);

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginRight: 40, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <span style={{ fontSize: 13, fontWeight: 600, color: "#4A7FD4" }}>Enerji Yönetimi</span>
      </nav>

      <div style={{ display: "flex", gap: 0 }}>
        <div style={{ width: 200, background: "#fff", borderRight: "1px solid #D6E4FA", minHeight: "calc(100vh - 56px)", padding: "16px 0" }}>
          {[
            { k: "dashboard", i: "ti-dashboard", l: "Dashboard" },
            { k: "meters", i: "ti-device-analytics", l: "Sayaçlar" },
            { k: "readings", i: "ti-report-analytics", l: "Okumalar" },
            { k: "reports", i: "ti-file-report", l: "Raporlar" },
            { k: "rules", i: "ti-settings-automation", l: "Tasarruf Kuralları" },
            { k: "certifications", i: "ti-certificate", l: "Sertifikalar" },
          ].map(t => (
            <div key={t.k} onClick={() => setTab(t.k)} style={{
              display: "flex", alignItems: "center", gap: 10, padding: "10px 24px", cursor: "pointer",
              fontSize: 13, fontWeight: tab === t.k ? 600 : 400,
              color: tab === t.k ? "#4A7FD4" : "#5A7499",
              background: tab === t.k ? "#EEF4FF" : "transparent",
              borderRight: tab === t.k ? "2px solid #4A7FD4" : "2px solid transparent",
            }}>
              <i className={`ti ${t.i}`} style={{ fontSize: 18 }} />
              {t.l}
            </div>
          ))}
        </div>

        <div style={{ flex: 1, padding: 24 }}>
          {tab === "dashboard" && dashboard && (
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 20 }}>Enerji Dashboard</h2>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 24 }}>
                {[
                  { i: "ti-bolt", l: "Toplam Maliyet", v: `${dashboard.total_cost.toFixed(0)} ₺`, c: "#4A7FD4" },
                  { i: "ti-bed", l: "Doluluk Oranı", v: `${(dashboard.occupancy_rate * 100).toFixed(0)}%`, c: "#22C55E" },
                  { i: "ti-coin", l: "Oda Başı Maliyet", v: `${dashboard.cost_per_occupied_room.toFixed(0)} ₺`, c: "#F59E0B" },
                  { i: "ti-certificate", l: "Sertifika", v: `${dashboard.verified_certifications} adet`, c: "#8B5CF6" },
                ].map(c => (
                  <div key={c.l} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                      <div style={{ width: 36, height: 36, borderRadius: 8, background: "#EEF4FF", display: "flex", alignItems: "center", justifyContent: "center" }}>
                        <i className={`ti ${c.i}`} style={{ fontSize: 18, color: c.c }} />
                      </div>
                      <span style={{ fontSize: 11, color: "#8FAAC8", fontWeight: 500 }}>{c.l}</span>
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 700, color: "#1A2B4A" }}>{c.v}</div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 24 }}>
                <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                  <div style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", marginBottom: 12 }}>Tüketim Özeti (Bugün)</div>
                  {[
                    { l: "Elektrik", v: dashboard.today.electricity?.toFixed(1), u: "kWh", c: "#F59E0B" },
                    { l: "Su", v: dashboard.today.water?.toFixed(1), u: "m³", c: "#22C55E" },
                    { l: "Gaz", v: dashboard.today.gas?.toFixed(1), u: "m³", c: "#EF4444" },
                  ].map(x => (
                    <div key={x.l} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #F0F4FF" }}>
                      <span style={{ fontSize: 13, color: "#5A7499" }}>{x.l}</span>
                      <span style={{ fontSize: 13, fontWeight: 600 }}>{x.v} {x.u}</span>
                    </div>
                  ))}
                </div>
                <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                  <div style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", marginBottom: 12 }}>Sertifikalar</div>
                  {dashboard.certs.length === 0 && <div style={{ fontSize: 12, color: "#8FAAC8" }}>Henüz sertifika eklenmemiş</div>}
                  {dashboard.certs.map(c => (
                    <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 8, padding: "6px 0" }}>
                      <i className="ti ti-certificate" style={{ fontSize: 16, color: c.is_verified ? "#22C55E" : "#8FAAC8" }} />
                      <span style={{ fontSize: 12, fontWeight: 500 }}>{c.certification_name}</span>
                      {c.is_verified && <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 10, background: "#DCFCE7", color: "#22C55E", fontWeight: 600 }}>Doğrulanmış</span>}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {tab === "meters" && (
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Enerji Sayaçları</h2>
              <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
                <select value={meterType} onChange={e => { setMeterType(e.target.value); setMeterUnit(e.target.value === "electricity" ? "kWh" : e.target.value === "water" ? "m3" : "cm3"); }} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff" }}>
                  <option value="electricity">Elektrik</option>
                  <option value="water">Su</option>
                  <option value="gas">Gaz</option>
                </select>
                <input placeholder="Sayaç adı" value={meterName} onChange={e => setMeterName(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 160 }} />
                <input placeholder="Konum" value={meterLocation} onChange={e => setMeterLocation(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 160 }} />
                <select value={meterUnit} onChange={e => setMeterUnit(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff" }}>
                  <option value="kWh">kWh</option>
                  <option value="m3">m³</option>
                  <option value="cm3">cm³</option>
                </select>
                <button onClick={handleCreateMeter} style={{ padding: "8px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>+ Ekle</button>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead><tr style={{ background: "#F8FAFF" }}>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Ad</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Tip</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Konum</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Birim</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Durum</th>
                  </tr></thead>
                  <tbody>
                    {meters.map(m => (
                      <tr key={m.id} style={{ borderTop: "1px solid #F0F4FF" }}>
                        <td style={{ padding: "10px 14px", fontWeight: 500 }}>{m.meter_name}</td>
                        <td style={{ padding: "10px 14px" }}>{m.meter_type}</td>
                        <td style={{ padding: "10px 14px", color: "#8FAAC8" }}>{m.location}</td>
                        <td style={{ padding: "10px 14px" }}>{m.unit}</td>
                        <td style={{ padding: "10px 14px" }}><span style={{ padding: "2px 8px", borderRadius: 10, background: m.is_active ? "#DCFCE7" : "#FEE2E2", color: m.is_active ? "#22C55E" : "#EF4444", fontSize: 10, fontWeight: 600 }}>{m.is_active ? "Aktif" : "Pasif"}</span></td>
                      </tr>
                    ))}
                    {meters.length === 0 && <tr><td colSpan={5} style={{ padding: 20, textAlign: "center", color: "#8FAAC8" }}>Sayaç bulunamadı</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tab === "readings" && (
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Okuma Gir</h2>
              <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap", alignItems: "center" }}>
                <select value={readingMeterId} onChange={e => setReadingMeterId(Number(e.target.value))} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff" }}>
                  <option value={0}>Sayaç seç</option>
                  {meters.map(m => <option key={m.id} value={m.id}>{m.meter_name} ({m.meter_type})</option>)}
                </select>
                <input placeholder="Değer" type="number" value={readingValue} onChange={e => setReadingValue(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 120 }} />
                <button onClick={handleLogReading} style={{ padding: "8px 16px", background: "#22C55E", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>Okuma Kaydet</button>
              </div>

              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Tüketim Özeti</h3>
              <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
                {[
                  { l: "Elektrik", v: summary.electricity.toFixed(1), u: "kWh", c: "#F59E0B" },
                  { l: "Su", v: summary.water.toFixed(1), u: "m³", c: "#22C55E" },
                  { l: "Gaz", v: summary.gas.toFixed(1), u: "m³", c: "#EF4444" },
                ].map(s => (
                  <div key={s.l} style={{ flex: 1, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
                      <div style={{ width: 32, height: 32, borderRadius: 8, background: "#EEF4FF", display: "flex", alignItems: "center", justifyContent: "center" }}>
                        <i className={`ti ${s.l === "Elektrik" ? "ti-bolt" : s.l === "Su" ? "ti-droplet" : "ti-flame"}`} style={{ fontSize: 16, color: s.c }} />
                      </div>
                      <span style={{ fontSize: 12, color: "#5A7499" }}>{s.l}</span>
                    </div>
                    <div style={{ fontSize: 20, fontWeight: 700 }}>{s.v} <span style={{ fontSize: 12, fontWeight: 400, color: "#8FAAC8" }}>{s.u}</span></div>
                  </div>
                ))}
              </div>

              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: "#5A7499", marginBottom: 12 }}>Tüketim Grafiği (mock bar chart)</div>
                <div style={{ display: "flex", alignItems: "flex-end", gap: 8, height: 120, padding: "0 8px" }}>
                  {[
                    { l: "Elektrik", v: summary.electricity, c: "#F59E0B" },
                    { l: "Su", v: summary.water * 10, c: "#22C55E" },
                    { l: "Gaz", v: summary.gas * 10, c: "#EF4444" },
                  ].map(b => {
                    const pct = maxConsumption > 0 ? (b.v / maxConsumption) * 100 : 10;
                    return (
                      <div key={b.l} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                        <div style={{ width: "100%", height: `${Math.max(pct, 8)}%`, background: b.c, borderRadius: "6px 6px 0 0", transition: "height 0.3s" }} />
                        <span style={{ fontSize: 10, color: "#5A7499", fontWeight: 500 }}>{b.l}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {tab === "reports" && (
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                <h2 style={{ fontSize: 18, fontWeight: 700 }}>Enerji Tüketim Raporları</h2>
                <button onClick={handleGenerateReport} style={{ padding: "8px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                  <i className="ti ti-refresh" style={{ marginRight: 4 }} /> Rapor Oluştur
                </button>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead><tr style={{ background: "#F8FAFF" }}>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Tarih</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Elektrik</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Su</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Gaz</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Toplam Maliyet</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Doluluk</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Oda Başı</th>
                  </tr></thead>
                  <tbody>
                    {reports.map(r => (
                      <tr key={r.id} style={{ borderTop: "1px solid #F0F4FF" }}>
                        <td style={{ padding: "10px 14px", fontWeight: 500 }}>{r.report_date}</td>
                        <td style={{ padding: "10px 14px" }}>{r.total_electricity_kwh.toFixed(1)} kWh</td>
                        <td style={{ padding: "10px 14px" }}>{r.total_water_m3.toFixed(1)} m³</td>
                        <td style={{ padding: "10px 14px" }}>{r.total_gas_m3.toFixed(1)} m³</td>
                        <td style={{ padding: "10px 14px", fontWeight: 600 }}>{r.total_cost.toFixed(0)} ₺</td>
                        <td style={{ padding: "10px 14px" }}>{(r.occupancy_rate * 100).toFixed(0)}%</td>
                        <td style={{ padding: "10px 14px" }}>{r.cost_per_occupied_room.toFixed(0)} ₺</td>
                      </tr>
                    ))}
                    {reports.length === 0 && <tr><td colSpan={7} style={{ padding: 20, textAlign: "center", color: "#8FAAC8" }}>Rapor bulunamadı</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tab === "rules" && (
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Tasarruf Kuralları</h2>
              <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap", alignItems: "center" }}>
                <input placeholder="Kural adı" value={ruleName} onChange={e => setRuleName(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 180 }} />
                <select value={triggerType} onChange={e => setTriggerType(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff" }}>
                  <option value="occupancy">Doluluk</option>
                  <option value="time">Zaman</option>
                  <option value="season">Mevsim</option>
                  <option value="temperature">Sıcaklık</option>
                </select>
                <input placeholder="Tahmini tasarruf %" type="number" value={savingsPct} onChange={e => setSavingsPct(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 100 }} />
                <button onClick={handleCreateRule} style={{ padding: "8px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>+ Kural Ekle</button>
              </div>
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead><tr style={{ background: "#F8FAFF" }}>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Kural</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Tetikleyici</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Tasarruf %</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>Durum</th>
                    <th style={{ padding: "10px 14px", textAlign: "left", color: "#5A7499", fontWeight: 600 }}>İşlem</th>
                  </tr></thead>
                  <tbody>
                    {rules.map(r => (
                      <tr key={r.id} style={{ borderTop: "1px solid #F0F4FF" }}>
                        <td style={{ padding: "10px 14px", fontWeight: 500 }}>{r.rule_name}</td>
                        <td style={{ padding: "10px 14px" }}><span style={{ padding: "2px 8px", borderRadius: 10, background: "#EEF4FF", color: "#4A7FD4", fontSize: 10, fontWeight: 600 }}>{r.trigger_type}</span></td>
                        <td style={{ padding: "10px 14px" }}>%{r.estimated_savings_percent}</td>
                        <td style={{ padding: "10px 14px" }}><span style={{ padding: "2px 8px", borderRadius: 10, background: r.is_active ? "#DCFCE7" : "#FEE2E2", color: r.is_active ? "#22C55E" : "#EF4444", fontSize: 10, fontWeight: 600 }}>{r.is_active ? "Aktif" : "Pasif"}</span></td>
                        <td style={{ padding: "10px 14px" }}>
                          <button onClick={() => handleDeleteRule(r.id)} style={{ padding: "4px 10px", background: "#FEE2E2", color: "#EF4444", border: "none", borderRadius: 4, fontSize: 10, fontWeight: 600, cursor: "pointer" }}>Sil</button>
                        </td>
                      </tr>
                    ))}
                    {rules.length === 0 && <tr><td colSpan={5} style={{ padding: 20, textAlign: "center", color: "#8FAAC8" }}>Kural bulunamadı</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tab === "certifications" && (
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Sürdürülebilirlik Sertifikaları</h2>
              <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap", alignItems: "center" }}>
                <select value={certName} onChange={e => setCertName(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", background: "#fff" }}>
                  <option value="">Sertifika seç</option>
                  <option value="Green Key">Green Key</option>
                  <option value="LEED">LEED</option>
                  <option value="ISO 14001">ISO 14001</option>
                  <option value="EcoLabel">EcoLabel</option>
                </select>
                <input placeholder="Veren kuruluş" value={issuingBody} onChange={e => setIssuingBody(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 160 }} />
                <input placeholder="Sertifika no" value={certNo} onChange={e => setCertNo(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", width: 140 }} />
                <input placeholder="Veriliş tarihi" type="date" value={awarded} onChange={e => setAwarded(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit" }} />
                <input placeholder="Bitiş tarihi" type="date" value={expiry} onChange={e => setExpiry(e.target.value)} style={{ padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit" }} />
                <button onClick={handleAddCert} style={{ padding: "8px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>+ Sertifika Ekle</button>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 12 }}>
                {certs.map(c => (
                  <div key={c.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                      <i className="ti ti-certificate" style={{ fontSize: 24, color: c.is_verified ? "#22C55E" : "#8FAAC8" }} />
                      <div>
                        <div style={{ fontSize: 14, fontWeight: 600 }}>{c.certification_name}</div>
                        <div style={{ fontSize: 11, color: "#8FAAC8" }}>{c.issuing_body}</div>
                      </div>
                      {c.is_verified && <span style={{ marginLeft: "auto", fontSize: 10, padding: "2px 8px", borderRadius: 10, background: "#DCFCE7", color: "#22C55E", fontWeight: 600 }}>Doğrulanmış</span>}
                    </div>
                    <div style={{ fontSize: 11, color: "#5A7499" }}>No: {c.certificate_number}</div>
                    <div style={{ fontSize: 11, color: "#5A7499" }}>{c.awarded_date} - {c.expiry_date || "Süresiz"}</div>
                  </div>
                ))}
                {certs.length === 0 && <div style={{ gridColumn: "1/-1", textAlign: "center", padding: 40, color: "#8FAAC8", fontSize: 13 }}>Henüz sertifika eklenmemiş</div>}
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
