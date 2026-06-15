"use client";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function AgencyPage() {
  const [agency, setAgency] = useState<any>(null);
  const [auths, setAuths] = useState<any[]>([]);
  const [bookings, setBookings] = useState<any[]>([]);
  const [tab, setTab] = useState("dashboard");
  const [form, setForm] = useState({ company_name: "", tax_id: "", phone: "", email: "" });
  const [authForm, setAuthForm] = useState({ domain: "transport", provider_id: "", provider_name: "", commission_split: "0" });
  const [message, setMessage] = useState("");

  useEffect(() => { loadAgency(); }, []);

  async function loadAgency() {
    try {
      const res = await fetch(`${API}/agency/my?user_id=1`);
      if (res.ok) {
        const data = await res.json();
        setAgency(data);
        setForm({ company_name: data.company_name || "", tax_id: data.tax_id || "", phone: data.phone || "", email: data.email || "" });
        loadAuths(data.id);
        loadBookings(data.id);
      }
    } catch (_) {}
  }

  async function loadAuths(agencyId: number) {
    try {
      const res = await fetch(`${API}/agency/authorizations?agency_id=${agencyId}`);
      const data = await res.json();
      setAuths(Array.isArray(data) ? data : []);
    } catch (_) {}
  }

  async function loadBookings(agencyId: number) {
    try {
      const res = await fetch(`${API}/tourism/bookings?agency_id=${agencyId}`);
      const data = await res.json();
      setBookings(Array.isArray(data) ? data : []);
    } catch (_) {}
  }

  async function register() {
    try {
      const res = await fetch(`${API}/agency/register?user_id=1`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) { setMessage("Acente kaydı başarılı!"); loadAgency(); }
      else { const e = await res.json(); setMessage(e.detail || "Hata"); }
    } catch (_) { setMessage("Bağlantı hatası"); }
  }

  async function updateAgency() {
    try {
      const res = await fetch(`${API}/agency/my?user_id=1`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) { setMessage("Güncellendi!"); loadAgency(); }
      else { const e = await res.json(); setMessage(e.detail || "Hata"); }
    } catch (_) { setMessage("Bağlantı hatası"); }
  }

  async function requestAuth() {
    if (!agency) return;
    try {
      const params = new URLSearchParams({
        agency_id: String(agency.id),
        domain: authForm.domain,
        provider_id: authForm.provider_id,
        provider_name: authForm.provider_name,
        commission_split: authForm.commission_split,
      });
      const res = await fetch(`${API}/agency/authorizations?${params}`, { method: "POST" });
      if (res.ok) { setMessage("Yetki talebi gönderildi!"); loadAuths(agency.id); }
      else { const e = await res.json(); setMessage(e.detail || "Hata"); }
    } catch (_) { setMessage("Bağlantı hatası"); }
  }

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Acente Panosu</h1>
      {message && <p className="mb-2 p-2 bg-blue-50 border rounded text-sm">{message}</p>}

      {!agency ? (
        <div className="border p-4 rounded max-w-md">
          <h2 className="font-bold mb-2">Acente Kaydı</h2>
          <input value={form.company_name} onChange={e => setForm({ ...form, company_name: e.target.value })}
            placeholder="Firma Adı" className="border p-2 rounded w-full mb-2" />
          <input value={form.tax_id} onChange={e => setForm({ ...form, tax_id: e.target.value })}
            placeholder="Vergi No" className="border p-2 rounded w-full mb-2" />
          <input value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })}
            placeholder="Telefon" className="border p-2 rounded w-full mb-2" />
          <input value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
            placeholder="E-posta" className="border p-2 rounded w-full mb-2" />
          <button onClick={register} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full">
            Kaydol
          </button>
        </div>
      ) : (
        <>
          <div className="flex gap-2 mb-4">
            {["dashboard", "settings", "auth", "bookings"].map(t => (
              <button key={t} onClick={() => setTab(t)}
                className={`px-3 py-1 rounded ${tab === t ? "bg-blue-600 text-white" : "bg-gray-100"}`}>
                {t === "dashboard" ? "Genel" : t === "settings" ? "Ayarlar" : t === "auth" ? "Yetkiler" : "Rezervasyonlar"}
              </button>
            ))}
          </div>

          {tab === "dashboard" && (
            <div className="grid grid-cols-3 gap-4">
              <div className="border p-4 rounded text-center">
                <p className="text-2xl font-bold">{auths.filter(a => a.status === "approved").length}</p>
                <p className="text-sm text-gray-600">Onaylı Yetki</p>
              </div>
              <div className="border p-4 rounded text-center">
                <p className="text-2xl font-bold">{auths.filter(a => a.status === "pending").length}</p>
                <p className="text-sm text-gray-600">Bekleyen Yetki</p>
              </div>
              <div className="border p-4 rounded text-center">
                <p className="text-2xl font-bold">{bookings.length}</p>
                <p className="text-sm text-gray-600">Rezervasyon</p>
              </div>
            </div>
          )}

          {tab === "settings" && (
            <div className="max-w-md">
              <input value={form.company_name} onChange={e => setForm({ ...form, company_name: e.target.value })}
                placeholder="Firma Adı" className="border p-2 rounded w-full mb-2" />
              <input value={form.tax_id} onChange={e => setForm({ ...form, tax_id: e.target.value })}
                placeholder="Vergi No" className="border p-2 rounded w-full mb-2" />
              <input value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })}
                placeholder="Telefon" className="border p-2 rounded w-full mb-2" />
              <input value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
                placeholder="E-posta" className="border p-2 rounded w-full mb-2" />
              <button onClick={updateAgency} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Güncelle
              </button>
            </div>
          )}

          {tab === "auth" && (
            <div>
              <div className="border p-4 rounded mb-4 max-w-md">
                <h3 className="font-bold mb-2">Yetki Talebi Gönder</h3>
                <select value={authForm.domain} onChange={e => setAuthForm({ ...authForm, domain: e.target.value })}
                  className="border p-2 rounded w-full mb-2">
                  <option value="transport">Ulaşım</option>
                  <option value="tourism">Turizm / Deneyim</option>
                  <option value="hotel">Otel</option>
                  <option value="event">Etkinlik</option>
                </select>
                <input value={authForm.provider_id} onChange={e => setAuthForm({ ...authForm, provider_id: e.target.value })}
                  placeholder="Firma ID" type="number" className="border p-2 rounded w-full mb-2" />
                <input value={authForm.provider_name} onChange={e => setAuthForm({ ...authForm, provider_name: e.target.value })}
                  placeholder="Firma Adı" className="border p-2 rounded w-full mb-2" />
                <input value={authForm.commission_split} onChange={e => setAuthForm({ ...authForm, commission_split: e.target.value })}
                  placeholder="Komisyon %" type="number" className="border p-2 rounded w-full mb-2" />
                <button onClick={requestAuth} className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
                  Gönder
                </button>
              </div>
              <h3 className="font-bold mb-2">Yetkilendirmeler</h3>
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border p-2 text-left">Domain</th>
                    <th className="border p-2 text-left">Firma</th>
                    <th className="border p-2 text-left">Komisyon</th>
                    <th className="border p-2 text-left">Durum</th>
                  </tr>
                </thead>
                <tbody>
                  {auths.map(a => (
                    <tr key={a.id}>
                      <td className="border p-2">{a.domain}</td>
                      <td className="border p-2">{a.provider_name}</td>
                      <td className="border p-2">%{a.commission_split}</td>
                      <td className="border p-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          a.status === "approved" ? "bg-green-100 text-green-700" :
                          a.status === "rejected" ? "bg-red-100 text-red-700" :
                          "bg-yellow-100 text-yellow-700"
                        }`}>{a.status}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {tab === "bookings" && (
            <div>
              <h3 className="font-bold mb-2">Rezervasyonlar</h3>
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border p-2">No</th>
                    <th className="border p-2">Müşteri</th>
                    <th className="border p-2">Kişi</th>
                    <th className="border p-2">Toplam</th>
                    <th className="border p-2">Durum</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings.map(b => (
                    <tr key={b.id}>
                      <td className="border p-2">{b.booking_no}</td>
                      <td className="border p-2">{b.customer_name}</td>
                      <td className="border p-2">{b.participant_count}</td>
                      <td className="border p-2">{b.total_price?.toLocaleString()} {b.currency}</td>
                      <td className="border p-2">{b.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
