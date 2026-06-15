"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function MultiPropertyPage() {
  const router = useRouter();
  const [groups, setGroups] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("groups");
  const [selectedGroupId, setSelectedGroupId] = useState<number | null>(null);
  const [groupDetail, setGroupDetail] = useState<any>(null);
  const [dashboard, setDashboard] = useState<any>(null);
  const [msg, setMsg] = useState("");

  const [newGroup, setNewGroup] = useState({ name: "", description: "" });
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("staff");

  useEffect(() => {
    async function loadGroups() {
      try {
        const res = await fetch(`${API}/multi-property/groups`);
        const data = await res.json();
        setGroups(Array.isArray(data) ? data : []);
      } catch (_) {}
      setLoading(false);
    }
    loadGroups();
  }, []);

  useEffect(() => {
    if (!selectedGroupId) return;
    async function loadDetail() {
      try {
        const [dRes, dashRes] = await Promise.all([
          fetch(`${API}/multi-property/groups/${selectedGroupId}`),
          fetch(`${API}/multi-property/groups/${selectedGroupId}/dashboard`),
        ]);
        if (dRes.ok) setGroupDetail(await dRes.json());
        if (dashRes.ok) setDashboard(await dashRes.json());
      } catch (_) {}
    }
    loadDetail();
  }, [selectedGroupId]);

  async function handleCreateGroup() {
    if (!newGroup.name) return;
    try {
      const params = new URLSearchParams({ name: newGroup.name });
      if (newGroup.description) params.set("description", newGroup.description);
      const res = await fetch(`${API}/multi-property/groups?${params}`, { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        setGroups(prev => [...prev, data]);
        setNewGroup({ name: "", description: "" });
        setMsg("✅ Grup oluşturuldu");
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleInvite() {
    if (!inviteEmail || !selectedGroupId) return;
    try {
      const params = new URLSearchParams({ email: inviteEmail, role: inviteRole });
      const res = await fetch(`${API}/multi-property/groups/${selectedGroupId}/invite?${params}`, { method: "POST" });
      if (res.ok) {
        setInviteEmail("");
        setMsg("✅ Davet gönderildi");
        const dRes = await fetch(`${API}/multi-property/groups/${selectedGroupId}`);
        if (dRes.ok) setGroupDetail(await dRes.json());
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Hata"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleDeleteGroup(gid: number) {
    try {
      const res = await fetch(`${API}/multi-property/groups/${gid}`, { method: "DELETE" });
      if (res.ok) {
        setGroups(prev => prev.filter(g => g.id !== gid));
        if (selectedGroupId === gid) { setSelectedGroupId(null); setGroupDetail(null); setDashboard(null); }
        setMsg("✅ Grup silindi");
      }
    } catch (_) {}
  }

  async function handleRemoveHotel(hotelId: number) {
    if (!selectedGroupId) return;
    try {
      const res = await fetch(`${API}/multi-property/groups/${selectedGroupId}/hotels/${hotelId}`, { method: "DELETE" });
      if (res.ok) {
        setMsg("✅ Otel çıkarıldı");
        const dRes = await fetch(`${API}/multi-property/groups/${selectedGroupId}`);
        if (dRes.ok) setGroupDetail(await dRes.json());
      }
    } catch (_) {}
  }

  async function handleGenerateReport() {
    if (!selectedGroupId) return;
    try {
      const res = await fetch(`${API}/multi-property/groups/${selectedGroupId}/report`, { method: "POST" });
      if (res.ok) {
        setMsg("✅ Rapor oluşturuldu");
        const dashRes = await fetch(`${API}/multi-property/groups/${selectedGroupId}/dashboard`);
        if (dashRes.ok) setDashboard(await dashRes.json());
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
        <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.8, marginBottom: 4 }}>Çoklu Mülk Yönetimi</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20 }}>Grup bazında otel ve performans yönetimi</p>

        <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
          {[
            { key: "groups", label: "Gruplar", icon: "ti-building" },
            { key: "create", label: "Yeni Grup", icon: "ti-plus" },
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

        {tab === "groups" && (
          <div style={{ display: "flex", gap: 24 }}>
            <div style={{ width: 320, flexShrink: 0 }}>
              <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Gruplarım</h2>
              {loading ? <p style={{ fontSize: 13, color: "#8FAAC8" }}>Yükleniyor...</p> : groups.length === 0 ? (
                <p style={{ fontSize: 13, color: "#8FAAC8" }}>Henüz grup oluşturmadınız</p>
              ) : groups.map((g: any) => (
                <div key={g.id} style={{ padding: "12px 14px", background: selectedGroupId === g.id ? "#fff" : "transparent", border: `1px solid ${selectedGroupId === g.id ? "#4A7FD4" : "transparent"}`, borderRadius: 8, cursor: "pointer", marginBottom: 6 }} onClick={() => setSelectedGroupId(g.id)}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ fontSize: 14, fontWeight: 600 }}>{g.name}</div>
                    <button onClick={e => { e.stopPropagation(); handleDeleteGroup(g.id); }} style={{ background: "none", border: "none", cursor: "pointer", color: "#dc2626", fontSize: 14, fontFamily: "inherit" }}>
                      <i className="ti ti-trash" />
                    </button>
                  </div>
                  {g.description && <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 2 }}>{g.description}</div>}
                </div>
              ))}
            </div>

            {selectedGroupId && groupDetail && (
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", gap: 12, marginBottom: 16, flexWrap: "wrap" }}>
                  <button onClick={handleGenerateReport} style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                    <i className="ti ti-report" /> Rapor Oluştur
                  </button>
                </div>

                {dashboard && (
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 12, marginBottom: 20 }}>
                    {[
                      { label: "Toplam Gelir", value: `₺${dashboard.total_revenue?.toLocaleString() || "0"}`, icon: "ti-currency-dollar" },
                      { label: "Toplam Rezervasyon", value: dashboard.total_bookings || "0", icon: "ti-calendar" },
                      { label: "Ort. Doluluk", value: `${dashboard.avg_occupancy || "0"}%`, icon: "ti-chart-bar" },
                      { label: "Ort. RevPAR", value: `₺${dashboard.avg_revpar?.toFixed(2) || "0"}`, icon: "ti-trending-up" },
                      { label: "Bağlı Otel", value: dashboard.total_hotels || "0", icon: "ti-building" },
                    ].map((s, i) => (
                      <div key={i} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: "14px 16px" }}>
                        <i className={`ti ${s.icon}`} style={{ fontSize: 18, color: "#4A7FD4" }} />
                        <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 4 }}>{s.label}</div>
                        <div style={{ fontSize: 18, fontWeight: 700, marginTop: 2 }}>{s.value}</div>
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ marginBottom: 20 }}>
                  <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Bağlı Oteller</h2>
                  {(!groupDetail.members || groupDetail.members.length === 0) ? (
                    <p style={{ fontSize: 13, color: "#8FAAC8" }}>Bu grupta otel yok</p>
                  ) : groupDetail.members.map((m: any) => (
                    <div key={m.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "10px 14px", marginBottom: 6, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <span style={{ fontSize: 13, fontWeight: 600 }}>Otel #{m.hotel_id}</span>
                        <span style={{ fontSize: 11, color: "#8FAAC8", marginLeft: 8 }}>Rol: {m.role}</span>
                        {m.is_primary && <span style={{ fontSize: 11, color: "#4A7FD4", marginLeft: 6, fontWeight: 600 }}>Birincil</span>}
                      </div>
                      <button onClick={() => handleRemoveHotel(m.hotel_id)} style={{ background: "none", border: "none", cursor: "pointer", color: "#dc2626", fontFamily: "inherit" }}>
                        <i className="ti ti-x" />
                      </button>
                    </div>
                  ))}
                </div>

                <div style={{ marginBottom: 20 }}>
                  <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Davet Gönder</h2>
                  <div style={{ display: "flex", gap: 8 }}>
                    <input type="email" placeholder="E-posta adresi" value={inviteEmail} onChange={e => setInviteEmail(e.target.value)} style={{ flex: 1, padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none" }} />
                    <select value={inviteRole} onChange={e => setInviteRole(e.target.value)} style={{ padding: "8px 10px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 12, fontFamily: "inherit", outline: "none", background: "#fff" }}>
                      <option value="staff">Personel</option>
                      <option value="manager">Yönetici</option>
                      <option value="owner">Sahip</option>
                    </select>
                    <button onClick={handleInvite} style={{ padding: "8px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
                      <i className="ti ti-send" /> Davet Et
                    </button>
                  </div>
                </div>

                {groupDetail.invites && groupDetail.invites.length > 0 && (
                  <div>
                    <h2 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, color: "#5A7499" }}>Bekleyen Davetler</h2>
                    {groupDetail.invites.map((inv: any) => (
                      <div key={inv.id} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: "10px 14px", marginBottom: 6, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <div>
                          <span style={{ fontSize: 13, fontWeight: 600 }}>{inv.email}</span>
                          <span style={{ fontSize: 11, color: "#8FAAC8", marginLeft: 8 }}>Rol: {inv.role}</span>
                        </div>
                        <span style={{ fontSize: 11, fontWeight: 700, padding: "3px 8px", borderRadius: 20, background: inv.status === "pending" ? "#fef3c7" : inv.status === "accepted" ? "#dcfce7" : "#fef2f2", color: inv.status === "pending" ? "#d97706" : inv.status === "accepted" ? "#16a34a" : "#dc2626", border: "1px solid #D6E4FA" }}>
                          {inv.status === "pending" ? "Bekliyor" : inv.status === "accepted" ? "Kabul" : "Süresi Doldu"}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {tab === "create" && (
          <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 12, padding: 24, maxWidth: 500 }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <input type="text" placeholder="Grup Adı *" value={newGroup.name} onChange={e => setNewGroup(p => ({ ...p, name: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
              <textarea placeholder="Açıklama" value={newGroup.description} onChange={e => setNewGroup(p => ({ ...p, description: e.target.value }))} style={{ padding: "10px 12px", border: "1px solid #D6E4FA", borderRadius: 8, fontSize: 13, fontFamily: "inherit", outline: "none", resize: "vertical", minHeight: 80 }} />
              <button onClick={handleCreateGroup} style={{ padding: "12px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", marginTop: 8 }}>
                <i className="ti ti-plus" style={{ marginRight: 6 }} />Grup Oluştur
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
