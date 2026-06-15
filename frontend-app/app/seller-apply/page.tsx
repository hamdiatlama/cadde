"use client";
import { useState } from "react";

export default function SellerApplyPage() {
  const [form, setForm] = useState({ company: "", taxNumber: "", phone: "", businessType: "" });
  const [sent, setSent] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSent(true);
  }

  if (sent) {
    return (
      <main className="max-w-xl mx-auto px-4 py-16">
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
          <div className="text-3xl mb-2">✓</div>
          <h2 className="text-lg font-semibold text-green-800">Başvurunuz Alındı</h2>
          <p className="text-sm text-green-600 mt-1">En kısa sürede değerlendirilecektir.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Satıcı Başvurusu</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Firma Adı</label>
          <input type="text" required value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Vergi Numarası</label>
          <input type="text" required value={form.taxNumber} onChange={(e) => setForm({ ...form, taxNumber: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
          <input type="tel" required value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">İşletme Türü</label>
          <select required value={form.businessType} onChange={(e) => setForm({ ...form, businessType: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Seçiniz</option>
            <option value="individual">Şahıs</option>
            <option value="limited">Limited Şirket</option>
            <option value="inc">Anonim Şirket</option>
          </select>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 transition-colors">
          Başvuruyu Gönder
        </button>
      </form>
    </main>
  );
}
