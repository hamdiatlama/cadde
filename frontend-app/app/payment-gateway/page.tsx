"use client";
import { useState, useEffect } from "react";

export default function PaymentGatewayPage() {
  const [tab, setTab] = useState("providers");
  const [providers, setProviders] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [payouts, setPayouts] = useState<any[]>([]);
  const [balance, setBalance] = useState<any>(null);
  const [report, setReport] = useState<any[]>([]);
  const [hotelId, setHotelId] = useState("");
  const [merchantProvider, setMerchantProvider] = useState("");
  const [merchantApiKey, setMerchantApiKey] = useState("");
  const [merchantSecret, setMerchantSecret] = useState("");
  const [merchantId, setMerchantId] = useState("");
  const [payBookingId, setPayBookingId] = useState("");
  const [payAmount, setPayAmount] = useState("");
  const [payMethod, setPayMethod] = useState("card");
  const [payCardNo, setPayCardNo] = useState("");
  const [payoutAmount, setPayoutAmount] = useState("");
  const [payoutIban, setPayoutIban] = useState("");
  const [payoutHolder, setPayoutHolder] = useState("");
  const [payoutBank, setPayoutBank] = useState("");
  const [reportFrom, setReportFrom] = useState("");
  const [reportTo, setReportTo] = useState("");
  const [msg, setMsg] = useState("");

  useEffect(() => { loadProviders(); }, []);

  async function api(path: string, opts?: any) {
    const res = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || "Request failed"); }
    return res.json();
  }

  async function loadProviders() {
    try { setProviders(await api("/payment-gateway/providers")); } catch (e: any) { setMsg(e.message); }
  }

  async function loadTransactions() {
    try { setTransactions(await api(`/payment-gateway/transactions${hotelId ? `?hotel_id=${hotelId}` : ""}`)); } catch (e: any) { setMsg(e.message); }
  }

  async function loadPayouts() {
    if (!hotelId) return;
    try { setPayouts(await api(`/payment-gateway/payouts/${hotelId}`)); } catch (e: any) { setMsg(e.message); }
  }

  async function loadBalance() {
    if (!hotelId) return;
    try { setBalance(await api(`/payment-gateway/balance/${hotelId}`)); } catch (e: any) { setMsg(e.message); }
  }

  async function loadReport() {
    if (!hotelId || !reportFrom || !reportTo) return;
    try { setReport(await api(`/payment-gateway/report/${hotelId}?date_from=${reportFrom}&date_to=${reportTo}`)); } catch (e: any) { setMsg(e.message); }
  }

  async function handleCreateMerchant() {
    try {
      const params = new URLSearchParams({ hotel_id: hotelId, provider_id: merchantProvider });
      if (merchantApiKey) params.append("api_key", merchantApiKey);
      if (merchantSecret) params.append("api_secret", merchantSecret);
      if (merchantId) params.append("merchant_id", merchantId);
      await api(`/payment-gateway/merchant?${params}`, { method: "POST" });
      setMsg("Merchant account created!");
    } catch (e: any) { setMsg(e.message); }
  }

  async function handlePay() {
    try {
      const params = new URLSearchParams({ booking_id: payBookingId, amount: payAmount, payment_method: payMethod });
      if (payCardNo) params.append("card_number", payCardNo);
      await api(`/payment-gateway/pay?${params}`, { method: "POST" });
      setMsg("Payment processed!");
    } catch (e: any) { setMsg(e.message); }
  }

  async function handlePayout() {
    try {
      const params = new URLSearchParams({ hotel_id: hotelId, amount: payoutAmount, iban: payoutIban });
      if (payoutHolder) params.append("account_holder", payoutHolder);
      if (payoutBank) params.append("bank_name", payoutBank);
      await api(`/payment-gateway/payout?${params}`, { method: "POST" });
      setMsg("Payout requested!");
    } catch (e: any) { setMsg(e.message); }
  }

  const STYLE = {
    fontFamily: "'Space Grotesk',sans-serif",
    background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A", padding: 24,
  };

  const card: React.CSSProperties = {
    background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8,
    padding: 20, marginBottom: 16,
  };

  const input: React.CSSProperties = {
    width: "100%", padding: "8px 12px", border: "1px solid #D6E4FA", borderRadius: 6,
    fontFamily: "inherit", fontSize: 13, color: "#1A2B4A", background: "#fff",
    outline: "none", marginBottom: 8, boxSizing: "border-box",
  };

  const btn: React.CSSProperties = {
    padding: "8px 16px", background: "#4A7FD4", color: "#fff",
    border: "none", borderRadius: 6, fontFamily: "inherit", fontSize: 13,
    fontWeight: 600, cursor: "pointer",
  };

  const label: React.CSSProperties = { fontSize: 11, fontWeight: 600, color: "#5A7499", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4, display: "block" };

  const tabs = [
    { key: "providers", label: "Sağlayıcılar", icon: "ti-building-bank" },
    { key: "merchant", label: "Merchant", icon: "ti-link" },
    { key: "transactions", label: "İşlemler", icon: "ti-receipt" },
    { key: "balance", label: "Bakiye", icon: "ti-wallet" },
    { key: "payout", label: "Payout", icon: "ti-coin" },
    { key: "report", label: "Rapor", icon: "ti-report-analytics" },
  ];

  return (
    <main style={STYLE}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <i className="ti ti-credit-card" style={{ fontSize: 24, color: "#4A7FD4" }} />
        <h1 style={{ fontSize: 20, fontWeight: 700, letterSpacing: -0.5 }}>Payment Gateway</h1>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 20, flexWrap: "wrap" }}>
        {tabs.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              padding: "8px 14px", borderRadius: 6, border: "1px solid #D6E4FA",
              background: tab === t.key ? "#4A7FD4" : "#fff",
              color: tab === t.key ? "#fff" : "#5A7499",
              fontFamily: "inherit", fontSize: 12, fontWeight: 600, cursor: "pointer",
            }}
          ><i className={`ti ${t.icon}`} style={{ fontSize: 16 }} /> {t.label}</button>
        ))}
      </div>

      {msg && (
        <div style={{ ...card, background: "#E8F5E9", border: "1px solid #A5D6A7", color: "#2E7D32", fontSize: 13 }}>
          {msg}
          <span style={{ float: "right", cursor: "pointer" }} onClick={() => setMsg("")}>✕</span>
        </div>
      )}

      <div style={{ ...card, display: "flex", gap: 8, alignItems: "center" }}>
        <label style={label}>Hotel ID</label>
        <input style={{ ...input, width: 120, margin: 0 }} value={hotelId} onChange={e => setHotelId(e.target.value)} />
      </div>

      {/* PROVIDERS */}
      {tab === "providers" && (
        <div style={card}>
          <h2 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
            <i className="ti ti-building-bank" style={{ color: "#4A7FD4" }} /> Ödeme Sağlayıcıları
          </h2>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: "#EEF4FF", textAlign: "left" }}>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>ID</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Name</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Code</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Currencies</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Fee %</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Active</th>
              </tr>
            </thead>
            <tbody>
              {providers.map(p => (
                <tr key={p.id} style={{ borderTop: "1px solid #D6E4FA" }}>
                  <td style={{ padding: "8px 12px" }}>{p.id}</td>
                  <td style={{ padding: "8px 12px", fontWeight: 500 }}>{p.name}</td>
                  <td style={{ padding: "8px 12px" }}><code>{p.code}</code></td>
                  <td style={{ padding: "8px 12px" }}>{p.supported_currencies}</td>
                  <td style={{ padding: "8px 12px" }}>%{p.fee_percentage}</td>
                  <td style={{ padding: "8px 12px" }}>
                    {p.is_active ? <span style={{ color: "#2E7D32" }}>✓</span> : <span style={{ color: "#C62828" }}>✕</span>}
                  </td>
                </tr>
              ))}
              {providers.length === 0 && (
                <tr><td colSpan={6} style={{ padding: 16, textAlign: "center", color: "#8FAAC8" }}>No providers loaded</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* MERCHANT */}
      {tab === "merchant" && (
        <div style={card}>
          <h2 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
            <i className="ti ti-link" style={{ color: "#4A7FD4" }} /> Merchant Hesap Bağlama
          </h2>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <div>
              <label style={label}>Provider ID</label>
              <input style={input} value={merchantProvider} onChange={e => setMerchantProvider(e.target.value)} placeholder="1 (Stripe) / 2 (Iyzico) / 3 (PayTR)" />
            </div>
            <div>
              <label style={label}>Merchant ID</label>
              <input style={input} value={merchantId} onChange={e => setMerchantId(e.target.value)} />
            </div>
            <div>
              <label style={label}>API Key</label>
              <input style={input} value={merchantApiKey} onChange={e => setMerchantApiKey(e.target.value)} />
            </div>
            <div>
              <label style={label}>API Secret</label>
              <input style={input} value={merchantSecret} onChange={e => setMerchantSecret(e.target.value)} />
            </div>
          </div>
          <button style={btn} onClick={handleCreateMerchant}>Hesap Bağla</button>
        </div>
      )}

      {/* TRANSACTIONS */}
      {tab === "transactions" && (
        <div style={card}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
            <h2 style={{ fontSize: 14, fontWeight: 600, display: "flex", alignItems: "center", gap: 8 }}>
              <i className="ti ti-receipt" style={{ color: "#4A7FD4" }} /> İşlem Listesi
            </h2>
            <button style={btn} onClick={loadTransactions}>Yükle</button>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: "#EEF4FF", textAlign: "left" }}>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Ref</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Amount</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Fee</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Net</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Method</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Status</th>
                <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Date</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(t => (
                <tr key={t.id} style={{ borderTop: "1px solid #D6E4FA" }}>
                  <td style={{ padding: "8px 12px" }}><code>{t.reference_no}</code></td>
                  <td style={{ padding: "8px 12px" }}>{t.amount} {t.currency}</td>
                  <td style={{ padding: "8px 12px" }}>{t.fee}</td>
                  <td style={{ padding: "8px 12px" }}>{t.net_amount}</td>
                  <td style={{ padding: "8px 12px" }}>{t.payment_method}</td>
                  <td style={{ padding: "8px 12px" }}>
                    <span style={{
                      padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600,
                      background: t.status === "success" ? "#E8F5E9" : t.status === "pending" ? "#FFF8E1" : t.status === "refunded" ? "#FFEBEE" : "#F5F5F5",
                      color: t.status === "success" ? "#2E7D32" : t.status === "pending" ? "#F57F17" : t.status === "refunded" ? "#C62828" : "#666",
                    }}>{t.status}</span>
                  </td>
                  <td style={{ padding: "8px 12px", color: "#8FAAC8", fontSize: 12 }}>{t.created_at?.slice(0, 10)}</td>
                </tr>
              ))}
              {transactions.length === 0 && (
                <tr><td colSpan={7} style={{ padding: 16, textAlign: "center", color: "#8FAAC8" }}>No transactions</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* BALANCE */}
      {tab === "balance" && (
        <div>
          <div style={card}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <h2 style={{ fontSize: 14, fontWeight: 600, display: "flex", alignItems: "center", gap: 8 }}>
                <i className="ti ti-wallet" style={{ color: "#4A7FD4" }} /> Bakiye
              </h2>
              <button style={btn} onClick={loadBalance}>Göster</button>
            </div>
          </div>
          {balance && (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
              {[
                { label: "Toplam Kazanç", value: `${balance.total_earned} TL`, icon: "ti-currency-dollar", color: "#2E7D32" },
                { label: "Bekleyen", value: `${balance.pending} TL`, icon: "ti-clock", color: "#F57F17" },
                { label: "Toplam Ücret", value: `${balance.total_fees} TL`, icon: "ti-percentage", color: "#C62828" },
                { label: "Net Bakiye", value: `${balance.net_balance} TL`, icon: "ti-wallet", color: "#4A7FD4" },
              ].map(b => (
                <div key={b.label} style={{ ...card, textAlign: "center" }}>
                  <i className={`ti ${b.icon}`} style={{ fontSize: 28, color: b.color, marginBottom: 8 }} />
                  <div style={{ fontSize: 22, fontWeight: 700, color: b.color }}>{b.value}</div>
                  <div style={{ fontSize: 11, color: "#8FAAC8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.8 }}>{b.label}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* PAYOUT */}
      {tab === "payout" && (
        <div>
          <div style={card}>
            <h2 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
              <i className="ti ti-coin" style={{ color: "#4A7FD4" }} /> Payout Talebi
            </h2>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              <div>
                <label style={label}>Tutar (TL)</label>
                <input style={input} value={payoutAmount} onChange={e => setPayoutAmount(e.target.value)} />
              </div>
              <div>
                <label style={label}>IBAN</label>
                <input style={input} value={payoutIban} onChange={e => setPayoutIban(e.target.value)} />
              </div>
              <div>
                <label style={label}>Hesap Sahibi</label>
                <input style={input} value={payoutHolder} onChange={e => setPayoutHolder(e.target.value)} />
              </div>
              <div>
                <label style={label}>Banka Adı</label>
                <input style={input} value={payoutBank} onChange={e => setPayoutBank(e.target.value)} />
              </div>
            </div>
            <button style={btn} onClick={handlePayout}>Talep Gönder</button>
          </div>

          <div style={card}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
              <h2 style={{ fontSize: 14, fontWeight: 600 }}>Payout Geçmişi</h2>
              <button style={btn} onClick={loadPayouts}>Yükle</button>
            </div>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
              <thead>
                <tr style={{ background: "#EEF4FF", textAlign: "left" }}>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>ID</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Amount</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Fee</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Net</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Status</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>IBAN</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Date</th>
                </tr>
              </thead>
              <tbody>
                {payouts.map(p => (
                  <tr key={p.id} style={{ borderTop: "1px solid #D6E4FA" }}>
                    <td style={{ padding: "8px 12px" }}>{p.id}</td>
                    <td style={{ padding: "8px 12px" }}>{p.amount} TL</td>
                    <td style={{ padding: "8px 12px" }}>{p.fee}</td>
                    <td style={{ padding: "8px 12px" }}>{p.net_amount}</td>
                    <td style={{ padding: "8px 12px" }}>
                      <span style={{
                        padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600,
                        background: p.status === "completed" ? "#E8F5E9" : p.status === "processing" ? "#FFF8E1" : "#F5F5F5",
                        color: p.status === "completed" ? "#2E7D32" : p.status === "processing" ? "#F57F17" : "#666",
                      }}>{p.status}</span>
                    </td>
                    <td style={{ padding: "8px 12px" }}>{p.iban}</td>
                    <td style={{ padding: "8px 12px", color: "#8FAAC8", fontSize: 12 }}>{p.created_at?.slice(0, 10)}</td>
                  </tr>
                ))}
                {payouts.length === 0 && (
                  <tr><td colSpan={7} style={{ padding: 16, textAlign: "center", color: "#8FAAC8" }}>No payouts yet</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* REPORT */}
      {tab === "report" && (
        <div style={card}>
          <h2 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
            <i className="ti ti-report-analytics" style={{ color: "#4A7FD4" }} /> Rapor
          </h2>
          <div style={{ display: "flex", gap: 8, marginBottom: 12, alignItems: "flex-end" }}>
            <div>
              <label style={label}>Başlangıç</label>
              <input type="date" style={{ ...input, width: 160 }} value={reportFrom} onChange={e => setReportFrom(e.target.value)} />
            </div>
            <div>
              <label style={label}>Bitiş</label>
              <input type="date" style={{ ...input, width: 160 }} value={reportTo} onChange={e => setReportTo(e.target.value)} />
            </div>
            <button style={btn} onClick={loadReport}>Getir</button>
          </div>
          {report.length > 0 && (
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
              <thead>
                <tr style={{ background: "#EEF4FF", textAlign: "left" }}>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Tarih</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>İşlem</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Tutar</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Ücret</th>
                  <th style={{ padding: "8px 12px", fontWeight: 600, color: "#5A7499" }}>Net</th>
                </tr>
              </thead>
              <tbody>
                {report.map(r => (
                  <tr key={r.date} style={{ borderTop: "1px solid #D6E4FA" }}>
                    <td style={{ padding: "8px 12px" }}>{r.date}</td>
                    <td style={{ padding: "8px 12px" }}>{r.transaction_count}</td>
                    <td style={{ padding: "8px 12px" }}>{r.amount} TL</td>
                    <td style={{ padding: "8px 12px" }}>{r.fee} TL</td>
                    <td style={{ padding: "8px 12px", fontWeight: 600 }}>{r.net} TL</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {report.length === 0 && <div style={{ color: "#8FAAC8", fontSize: 13 }}>Select date range and fetch report</div>}
        </div>
      )}
    </main>
  );
}
