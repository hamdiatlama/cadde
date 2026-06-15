"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const OTA_PLATFORMS = [
  { code: "booking_com", name: "Booking.com", icon: "ti-brand-booking", color: "#003580" },
  { code: "airbnb", name: "Airbnb", icon: "ti-home", color: "#FF5A5F" },
  { code: "expedia", name: "Expedia", icon: "ti-world", color: "#FFC01E" },
  { code: "hotels_com", name: "Hotels.com", icon: "ti-building", color: "#E4322C" },
  { code: "tripadvisor", name: "Tripadvisor", icon: "ti-star", color: "#00E0C7" },
  { code: "trivago", name: "Trivago", icon: "ti-mist", color: "#E32851" },
];

export default function ChannelManagerPage() {
  const router = useRouter();
  const [channels, setChannels] = useState<any[]>([]);
  const [connections, setConnections] = useState<any[]>([]);
  const [listings, setListings] = useState<any[]>([]);
  const [bookings, setBookings] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);
  const [syncLogs, setSyncLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [hotelId, setHotelId] = useState("1");
  const [msg, setMsg] = useState("");
  const [activeTab, setActiveTab] = useState<"channels" | "listings" | "bookings" | "analytics">("channels");

  useEffect(() => {
    loadAll();
  }, [hotelId]);

  async function loadAll() {
    setLoading(true);
    setMsg("");
    try {
      const [chRes, connRes, listRes, bookRes, analRes] = await Promise.all([
        fetch(`${API}/channel-manager/channels`),
        fetch(`${API}/channel-manager/connections/${hotelId}`),
        fetch(`${API}/channel-manager/listings/${hotelId}`),
        fetch(`${API}/channel-manager/bookings/${hotelId}`),
        fetch(`${API}/channel-manager/analytics/${hotelId}`),
      ]);
      if (chRes.ok) setChannels(await chRes.json());
      if (connRes.ok) setConnections(await connRes.json());
      if (listRes.ok) setListings(await listRes.json());
      if (bookRes.ok) setBookings(await bookRes.json());
      if (analRes.ok) setAnalytics(await analRes.json());
    } catch (_) {}
    setLoading(false);
  }

  async function handleConnect(channelId: number) {
    try {
      const res = await fetch(`${API}/channel-manager/connect?hotel_id=${hotelId}&ota_channel_id=${channelId}`, { method: "POST" });
      if (res.ok) {
        setMsg("✅ Bağlantı başarılı");
        loadAll();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Bağlantı başarısız"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleDisconnect(connectionId: number) {
    try {
      const res = await fetch(`${API}/channel-manager/disconnect/${connectionId}`, { method: "POST" });
      if (res.ok) {
        setMsg("✅ Bağlantı kesildi");
        loadAll();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "İşlem başarısız"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  async function handleSync(connectionId: number, type: "availability" | "rates" | "bookings") {
    try {
      const res = await fetch(`${API}/channel-manager/sync/${type}/${connectionId}`, { method: "POST" });
      if (res.ok) {
        setMsg(`✅ ${type === "availability" ? "Müsaitlik" : type === "rates" ? "Fiyat" : "Rezervasyon"} senkronize edildi`);
        loadAll();
      } else {
        const err = await res.json();
        setMsg("❌ " + (err.detail || "Senkronizasyon başarısız"));
      }
    } catch (_) {
      setMsg("❌ Bağlantı hatası");
    }
  }

  function isConnected(channelId: number) {
    return connections.some(c => c.ota_channel_id === channelId && c.is_active);
  }

  function getConnectionByChannel(channelId: number) {
    return connections.find(c => c.ota_channel_id === channelId && c.is_active);
  }

  function getChannelName(id: number) {
    const ch = channels.find(c => c.id === id);
    return ch?.name || `Kanal #${id}`;
  }

  function getStatusColor(s: string) {
    switch (s) {
      case "connected": return "#22c55e";
      case "disconnected": return "#ef4444";
      default: return "#8FAAC8";
    }
  }

  function getStatusLabel(s: string) {
    switch (s) {
      case "connected": return "Bağlı";
      case "disconnected": return "Bağlı Değil";
      default: return s;
    }
  }

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css" />
      <style>{`
        .cm-card { transition: all .15s; }
        .cm-card:hover { border-color: #4A7FD4; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(74,127,212,0.08); }
        .tab-active { border-bottom: 2px solid #4A7FD4; color: #4A7FD4 !important; }
      `}</style>

      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }} onClick={() => router.push("/")}>
          <div style={{ width: 28, height: 28, background: "#4A7FD4", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.8 }}>cadde</span>
        </div>
        <div style={{ marginLeft: 32, display: "flex", gap: 24 }}>
          <span style={{ fontSize: 13, color: "#5A7499", cursor: "pointer", fontWeight: 500 }} onClick={() => router.push("/hotels")}>Konaklama</span>
          <span style={{ fontSize: 13, color: "#4A7FD4", fontWeight: 600, cursor: "pointer" }}>Kanal Yönetimi</span>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 12, color: "#8FAAC8" }}>Otel ID:</span>
          <input type="number" value={hotelId} onChange={e => setHotelId(e.target.value)}
            style={{ width: 60, padding: "6px 8px", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 13, fontFamily: "inherit", outline: "none" }} />
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "24px 32px" }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: -0.8, marginBottom: 4 }}>Kanal Yöneticisi</h1>
        <p style={{ fontSize: 13, color: "#8FAAC8", marginBottom: 20 }}>OTA entegrasyonlarını yönetin, fiyat ve müsaitlik senkronizasyonu yapın</p>

        {msg && (
          <div style={{ padding: "10px 16px", background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, marginBottom: 16, fontSize: 13, fontWeight: 500 }}>
            {msg}
          </div>
        )}

        {/* Tabs */}
        <div style={{ display: "flex", gap: 24, borderBottom: "1px solid #D6E4FA", marginBottom: 24 }}>
          {[
            { key: "channels" as const, label: "Kanallar", icon: "ti-plug" },
            { key: "listings" as const, label: "İlanlar", icon: "ti-list" },
            { key: "bookings" as const, label: "OTA Rezervasyonlar", icon: "ti-calendar" },
            { key: "analytics" as const, label: "Analytics", icon: "ti-chart-bar" },
          ].map(tab => (
            <div key={tab.key} onClick={() => setActiveTab(tab.key)}
              className={activeTab === tab.key ? "tab-active" : ""}
              style={{ display: "flex", alignItems: "center", gap: 6, padding: "10px 0", fontSize: 13, fontWeight: 600, color: "#5A7499", cursor: "pointer", borderBottom: "2px solid transparent", marginBottom: -1 }}>
              <i className={`ti ${tab.icon}`} style={{ fontSize: 16 }} />
              {tab.label}
            </div>
          ))}
        </div>

        {loading ? (
          <p style={{ color: "#8FAAC8", fontSize: 14 }}>Yükleniyor...</p>
        ) : activeTab === "channels" ? (
          <>
            {/* Available OTA platforms */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 12, marginBottom: 24 }}>
              {channels.length === 0 ? (
                OTA_PLATFORMS.map(pf => {
                  const _ch = channels.find(c => c.code === pf.code);
                  const chId = _ch?.id;
                  const connected = _ch ? isConnected(_ch.id) : false;
                  const conn = _ch ? getConnectionByChannel(_ch.id) : null;
                  return (
                    <div key={pf.code} className="cm-card" style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 16 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                        <div style={{ width: 40, height: 40, borderRadius: 8, background: `${pf.color}15`, border: `1px solid ${pf.color}30`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                          <i className={`ti ${pf.icon}`} style={{ fontSize: 20, color: pf.color }} />
                        </div>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontSize: 14, fontWeight: 600 }}>{pf.name}</div>
                          <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 2 }}>{pf.code.replace("_", ".")}</div>
                        </div>
                        {connected && conn ? (
                          <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: "#22c55e15", color: "#22c55e", border: "1px solid #22c55e30" }}>
                            <i className="ti ti-circle-filled" style={{ fontSize: 6, marginRight: 4 }} />Bağlı
                          </span>
                        ) : (
                          chId ? (
                            <button onClick={() => handleConnect(chId)}
                              style={{ padding: "6px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                              Bağlan
                            </button>
                          ) : (
                            <span style={{ fontSize: 11, color: "#8FAAC8" }}>Kullanılamaz</span>
                          )
                        )}
                      </div>
                      {connected && conn && (
                        <div style={{ marginTop: 12, borderTop: "1px solid #D6E4FA", paddingTop: 12, display: "flex", gap: 6, flexWrap: "wrap" }}>
                          <button onClick={() => handleSync(conn.id, "availability")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-cloud-up" style={{ fontSize: 13 }} />Müsaitlik
                          </button>
                          <button onClick={() => handleSync(conn.id, "rates")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-currency-dollar" style={{ fontSize: 13 }} />Fiyat
                          </button>
                          <button onClick={() => handleSync(conn.id, "bookings")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-download" style={{ fontSize: 13 }} />Rezervasyon
                          </button>
                          <button onClick={() => handleDisconnect(conn.id)}
                            style={{ padding: "5px 10px", background: "#FEF2F2", border: "1px solid #FECACA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#ef4444", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4, marginLeft: "auto" }}>
                            <i className="ti ti-plug-off" style={{ fontSize: 13 }} />Kes
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })
              ) : (
                channels.map(ch => {
                  const connected = isConnected(ch.id);
                  const conn = getConnectionByChannel(ch.id);
                  const pf = OTA_PLATFORMS.find(p => p.code === ch.code);
                  const icon = pf?.icon || "ti-plug";
                  const color = pf?.color || "#4A7FD4";
                  return (
                    <div key={ch.id} className="cm-card" style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 16 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                        <div style={{ width: 40, height: 40, borderRadius: 8, background: `${color}15`, border: `1px solid ${color}30`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                          <i className={`ti ${icon}`} style={{ fontSize: 20, color }} />
                        </div>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontSize: 14, fontWeight: 600 }}>{ch.name}</div>
                          <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 2 }}>{ch.code}</div>
                        </div>
                        {connected && conn ? (
                          <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: "#22c55e15", color: "#22c55e", border: "1px solid #22c55e30" }}>
                            <i className="ti ti-circle-filled" style={{ fontSize: 6, marginRight: 4 }} />Bağlı
                          </span>
                        ) : (
                          <button onClick={() => handleConnect(ch.id)}
                            style={{ padding: "6px 14px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" }}>
                            Bağlan
                          </button>
                        )}
                      </div>
                      {connected && conn && (
                        <div style={{ marginTop: 12, borderTop: "1px solid #D6E4FA", paddingTop: 12, display: "flex", gap: 6, flexWrap: "wrap" }}>
                          <button onClick={() => handleSync(conn.id, "availability")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-cloud-up" style={{ fontSize: 13 }} />Müsaitlik
                          </button>
                          <button onClick={() => handleSync(conn.id, "rates")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-currency-dollar" style={{ fontSize: 13 }} />Fiyat
                          </button>
                          <button onClick={() => handleSync(conn.id, "bookings")}
                            style={{ padding: "5px 10px", background: "#EEF4FF", border: "1px solid #D6E4FA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#4A7FD4", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4 }}>
                            <i className="ti ti-download" style={{ fontSize: 13 }} />Rezervasyon
                          </button>
                          <button onClick={() => handleDisconnect(conn.id)}
                            style={{ padding: "5px 10px", background: "#FEF2F2", border: "1px solid #FECACA", borderRadius: 6, fontSize: 11, fontWeight: 600, color: "#ef4444", cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 4, marginLeft: "auto" }}>
                            <i className="ti ti-plug-off" style={{ fontSize: 13 }} />Kes
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>

            {/* Connected channels summary */}
            {connections.filter(c => c.is_active).length > 0 && (
              <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 16 }}>
                <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 6 }}>
                  <i className="ti ti-plug-connected" style={{ color: "#4A7FD4" }} />Bağlı Kanallar
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {connections.filter(c => c.is_active).map(conn => (
                    <div key={conn.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 12px", background: "#EEF4FF", borderRadius: 8 }}>
                      <i className="ti ti-circle-filled" style={{ fontSize: 8, color: getStatusColor(conn.status) }} />
                      <span style={{ fontSize: 13, fontWeight: 600, flex: 1 }}>{conn.channel_name || getChannelName(conn.ota_channel_id)}</span>
                      <span style={{ fontSize: 11, color: "#8FAAC8" }}>{getStatusLabel(conn.status)}</span>
                      {conn.last_sync_at && (
                        <span style={{ fontSize: 11, color: "#8FAAC8" }}>Son: {new Date(conn.last_sync_at).toLocaleDateString("tr-TR")}</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : activeTab === "listings" ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {listings.length === 0 ? (
              <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10 }}>
                <i className="ti ti-list" style={{ fontSize: 32, display: "block", marginBottom: 8 }} />
                Henüz ilan bulunmuyor. Bir kanala bağlanarak ilan oluşturun.
              </div>
            ) : (
              listings.map(l => (
                <div key={l.id} className="cm-card" style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 16 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 600 }}>{l.listing_title || `İlan #${l.id}`}</div>
                      <div style={{ fontSize: 12, color: "#8FAAC8", marginTop: 4 }}>
                        <i className="ti ti-id" style={{ fontSize: 11, marginRight: 4 }} />{l.external_listing_id || "Harici ID yok"}
                      </div>
                    </div>
                    <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 20, background: l.status === "active" ? "#22c55e15" : "#FEF2F2", color: l.status === "active" ? "#22c55e" : "#ef4444", border: l.status === "active" ? "1px solid #22c55e30" : "1px solid #FECACA" }}>
                      {l.status === "active" ? "Aktif" : "Pasif"}
                    </span>
                  </div>
                  {l.external_url && (
                    <div style={{ marginTop: 8, fontSize: 12 }}>
                      <i className="ti ti-external-link" style={{ fontSize: 11, marginRight: 4 }} />
                      <a href={l.external_url} target="_blank" rel="noopener noreferrer" style={{ color: "#4A7FD4" }}>{l.external_url}</a>
                    </div>
                  )}
                  {l.last_synced_at && (
                    <div style={{ marginTop: 6, fontSize: 11, color: "#8FAAC8" }}>
                      <i className="ti ti-clock" style={{ fontSize: 11, marginRight: 4 }} />Son senkron: {new Date(l.last_synced_at).toLocaleString("tr-TR")}
                    </div>
                  )}
                  {l.sync_errors && (
                    <div style={{ marginTop: 6, fontSize: 11, color: "#ef4444", background: "#FEF2F2", padding: "6px 10px", borderRadius: 6 }}>
                      <i className="ti ti-alert-triangle" style={{ fontSize: 11, marginRight: 4 }} />{l.sync_errors}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        ) : activeTab === "bookings" ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {bookings.length === 0 ? (
              <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10 }}>
                <i className="ti ti-calendar-off" style={{ fontSize: 32, display: "block", marginBottom: 8 }} />
                Henüz OTA rezervasyonu bulunmuyor.
              </div>
            ) : (
              bookings.map(b => (
                <div key={b.id} className="cm-card" style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 16 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 600 }}>{b.guest_name || "İsimsiz"}</div>
                      <div style={{ fontSize: 12, color: "#8FAAC8", marginTop: 2 }}>{b.guest_email || "Email yok"}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontSize: 15, fontWeight: 700, color: "#4A7FD4" }}>{b.total_price?.toLocaleString("tr-TR")} {b.currency || "TRY"}</div>
                      <span style={{ fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 20, background: b.status === "confirmed" ? "#22c55e15" : "#EEF4FF", color: b.status === "confirmed" ? "#22c55e" : "#8FAAC8", border: "1px solid #D6E4FA" }}>
                        {b.status}
                      </span>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 16, marginTop: 8, fontSize: 12, color: "#5A7499" }}>
                    <span><i className="ti ti-calendar" style={{ fontSize: 11, marginRight: 4 }} />{b.check_in ? new Date(b.check_in).toLocaleDateString("tr-TR") : "?"} - {b.check_out ? new Date(b.check_out).toLocaleDateString("tr-TR") : "?"}</span>
                    <span><i className="ti ti-users" style={{ fontSize: 11, marginRight: 4 }} />{b.adults} yetişkin{b.children > 0 ? `, ${b.children} çocuk` : ""}</span>
                  </div>
                  <div style={{ marginTop: 8, fontSize: 11, color: "#8FAAC8", display: "flex", gap: 12 }}>
                    <span><i className="ti ti-id" style={{ fontSize: 10, marginRight: 4 }} />{b.external_booking_id}</span>
                    {b.synced_to_pms && (
                      <span style={{ color: "#22c55e" }}><i className="ti ti-check" style={{ fontSize: 10 }} />PMS ile senkron</span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          /* Analytics */
          <div>
            {analytics ? (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
                  <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 20 }}>
                    <div style={{ fontSize: 12, color: "#8FAAC8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}>Toplam Rezervasyon</div>
                    <div style={{ fontSize: 32, fontWeight: 700, color: "#4A7FD4", marginTop: 4 }}>{analytics.total_bookings}</div>
                  </div>
                  <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, padding: 20 }}>
                    <div style={{ fontSize: 12, color: "#8FAAC8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}>Toplam Gelir</div>
                    <div style={{ fontSize: 32, fontWeight: 700, color: "#22c55e", marginTop: 4 }}>₺{analytics.total_revenue?.toLocaleString("tr-TR") || "0"}</div>
                  </div>
                </div>

                <div style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10, overflow: "hidden" }}>
                  <div style={{ padding: 16, borderBottom: "1px solid #D6E4FA", fontSize: 14, fontWeight: 600 }}>
                    <i className="ti ti-chart-pie" style={{ marginRight: 6, color: "#4A7FD4" }} />Kanallara Göre Dağılım
                  </div>
                  {Object.keys(analytics.channels || {}).length === 0 ? (
                    <div style={{ padding: 24, textAlign: "center", color: "#8FAAC8", fontSize: 13 }}>
                      Henüz veri bulunmuyor
                    </div>
                  ) : (
                    <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
                      {Object.entries(analytics.channels).map(([name, data]: [string, any]) => (
                        <div key={name} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                          <div style={{ flex: 1 }}>
                            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                              <span style={{ fontSize: 13, fontWeight: 600 }}>{name}</span>
                              <span style={{ fontSize: 13, color: "#5A7499" }}>{data.booking_count} rezervasyon · ₺{data.revenue?.toLocaleString("tr-TR") || "0"}</span>
                            </div>
                            <div style={{ height: 8, background: "#EEF4FF", borderRadius: 4, overflow: "hidden" }}>
                              <div style={{ height: "100%", width: `${analytics.total_bookings > 0 ? (data.booking_count / analytics.total_bookings) * 100 : 0}%`, background: "#4A7FD4", borderRadius: 4, transition: "width .3s" }} />
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div style={{ padding: 40, textAlign: "center", color: "#8FAAC8", fontSize: 14, background: "#fff", border: "1px solid #D6E4FA", borderRadius: 10 }}>
                <i className="ti ti-chart-bar-off" style={{ fontSize: 32, display: "block", marginBottom: 8 }} />
                Analytics verisi bulunamadı
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
