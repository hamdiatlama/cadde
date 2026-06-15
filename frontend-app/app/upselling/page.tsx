'use client';
import { useState } from 'react';

const mockOffers = [
  { id: 1, hotel_id: 1, name: 'Oda Yükseltme', description: 'Bir üst oda kategorisine geçiş', category: 'room_upgrade', price: 500, currency: 'TRY', is_active: true, is_auto_offer: true, trigger_event: 'booking', display_order: 1 },
  { id: 2, hotel_id: 1, name: 'Kahvaltı Dahil', description: 'Açık büfe kahvaltı', category: 'breakfast', price: 150, currency: 'TRY', is_active: true, is_auto_offer: false, trigger_event: 'booking', display_order: 2 },
  { id: 3, hotel_id: 1, name: 'Havalimanı Transferi', description: 'Gidiş-dönüş transfer', category: 'transfer', price: 400, currency: 'TRY', is_active: true, is_auto_offer: false, trigger_event: 'checkin', display_order: 3 },
  { id: 4, hotel_id: 1, name: 'SPA Paketi', description: '30 dk masaj + hamam', category: 'spa', price: 350, currency: 'TRY', is_active: true, is_auto_offer: true, trigger_event: 'in_stay', display_order: 4 },
  { id: 5, hotel_id: 1, name: 'Geç Çıkış', description: 'Saat 18:00\'e kadar odada kalma', category: 'late_checkout', price: 200, currency: 'TRY', is_active: true, is_auto_offer: false, trigger_event: 'checkin', display_order: 5 },
  { id: 6, hotel_id: 1, name: 'Hoş Geldin Paketi', description: 'Meyve sepeti + şarap', category: 'welcome_package', price: 250, currency: 'TRY', is_active: false, is_auto_offer: false, trigger_event: null, display_order: 6 },
];

const mockCampaigns = [
  { id: 1, hotel_id: 1, name: 'Yaz Süper Paket', description: 'Oda + kahvaltı + SPA %20 indirimli', discount_percentage: 20, is_active: true, start_date: '2026-06-01', end_date: '2026-09-30' },
  { id: 2, hotel_id: 1, name: 'Erken Rezervasyon Avantajı', description: '30 gün önceden alınan tüm upsell\'lerde %15 indirim', discount_percentage: 15, is_active: true, start_date: '2026-01-01', end_date: '2026-12-31' },
];

const mockReport = {
  total_upsell_revenue: 12450, total_orders: 47,
  breakdown: { room_upgrade: 4500, breakfast: 2100, transfer: 3200, spa: 1750, late_checkout: 900 },
};

const categories = [
  { value: 'room_upgrade', label: 'Oda Yükseltme' },
  { value: 'breakfast', label: 'Kahvaltı' },
  { value: 'transfer', label: 'Transfer' },
  { value: 'spa', label: 'SPA' },
  { value: 'activity', label: 'Aktivite' },
  { value: 'late_checkout', label: 'Geç Çıkış' },
  { value: 'early_checkin', label: 'Erken Giriş' },
  { value: 'extra_bed', label: 'Ek Yatak' },
  { value: 'airport_shuttle', label: 'Servis' },
  { value: 'welcome_package', label: 'Hoş Geldin' },
];

const triggerEvents = [
  { value: 'booking', label: 'Rezervasyon' },
  { value: 'checkin', label: 'Giriş' },
  { value: 'in_stay', label: 'Konaklama' },
];

export default function UpsellingPage() {
  const [tab, setTab] = useState<'offers' | 'add' | 'campaigns' | 'report'>('offers');
  const [offers, setOffers] = useState(mockOffers);
  const [campaigns] = useState(mockCampaigns);
  const [report] = useState(mockReport);
  const [showOfferModal, setShowOfferModal] = useState(false);
  const [editingOffer, setEditingOffer] = useState<any>(null);
  const [bookingId, setBookingId] = useState('');
  const [selectedOfferId, setSelectedOfferId] = useState('');
  const [quantity, setQuantity] = useState('1');

  const openNewOffer = () => {
    setEditingOffer({ name: '', description: '', category: 'room_upgrade', price: 0, currency: 'TRY', is_active: true, is_auto_offer: false, trigger_event: null, display_order: 0 });
    setShowOfferModal(true);
  };

  const openEditOffer = (offer: any) => {
    setEditingOffer({ ...offer });
    setShowOfferModal(true);
  };

  const saveOffer = () => {
    if (editingOffer.id) {
      setOffers(prev => prev.map(o => o.id === editingOffer.id ? editingOffer : o));
    } else {
      setOffers(prev => [...prev, { ...editingOffer, id: Math.max(...prev.map(o => o.id)) + 1, hotel_id: 1 }]);
    }
    setShowOfferModal(false);
    setEditingOffer(null);
  };

  const toggleOffer = (id: number) => {
    setOffers(prev => prev.map(o => o.id === id ? { ...o, is_active: !o.is_active } : o));
  };

  const handleAddToBooking = () => {
    alert(`Booking #${bookingId} → Offer #${selectedOfferId} (x${quantity}) eklendi`);
  };

  const categoryLabel = (val: string) => categories.find(c => c.value === val)?.label || val;
  const triggerLabel = (val: string | null) => val ? triggerEvents.find(t => t.value === val)?.label || val : 'Yok';

  return (
    <div className="max-w-7xl mx-auto p-6 font-[family-name:var(--font-geist-sans)]">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Upselling & Ek Gelir</h1>
          <p className="text-gray-500 text-sm mt-1">Teklifler, kampanyalar ve ek gelir yönetimi</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => setTab('offers')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'offers' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Teklifler</button>
          <button onClick={() => setTab('add')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'add' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Booking'e Ekle</button>
          <button onClick={() => setTab('campaigns')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'campaigns' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Kampanyalar</button>
          <button onClick={() => setTab('report')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'report' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Gelir Raporu</button>
        </div>
      </div>

      {tab === 'offers' && (
        <>
          <div className="overflow-x-auto border rounded-lg">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="text-left p-3 text-sm font-semibold">Teklif</th>
                  <th className="text-left p-3 text-sm font-semibold">Kategori</th>
                  <th className="text-left p-3 text-sm font-semibold">Fiyat</th>
                  <th className="text-center p-3 text-sm font-semibold">Tetikleyici</th>
                  <th className="text-center p-3 text-sm font-semibold">Otomatik</th>
                  <th className="text-center p-3 text-sm font-semibold">Durum</th>
                  <th className="text-center p-3 text-sm font-semibold">İşlem</th>
                </tr>
              </thead>
              <tbody>
                {offers.map(o => (
                  <tr key={o.id} className="border-b hover:bg-gray-50">
                    <td className="p-3 text-sm font-semibold">{o.name}</td>
                    <td className="p-3 text-sm text-gray-600">
                      <span className="inline-block px-2 py-0.5 rounded text-xs font-bold bg-purple-100 text-purple-700">{categoryLabel(o.category)}</span>
                    </td>
                    <td className="p-3 text-sm">{o.currency} {o.price}</td>
                    <td className="p-3 text-sm text-center">{triggerLabel(o.trigger_event)}</td>
                    <td className="p-3 text-center">
                      {o.is_auto_offer ? (
                        <span className="text-xs px-2 py-1 rounded font-semibold bg-green-100 text-green-700">Evet</span>
                      ) : (
                        <span className="text-xs px-2 py-1 rounded font-semibold bg-gray-100 text-gray-500">Hayır</span>
                      )}
                    </td>
                    <td className="p-3 text-center">
                      <button onClick={() => toggleOffer(o.id)}
                        className={`text-xs px-2 py-1 rounded font-semibold ${o.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                        {o.is_active ? 'Aktif' : 'Pasif'}
                      </button>
                    </td>
                    <td className="p-3 text-center">
                      <button onClick={() => openEditOffer(o)}
                        className="text-xs text-blue-600 hover:underline font-medium">Düzenle</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button onClick={openNewOffer}
            className="mt-4 border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-lg p-4 w-full text-center text-sm text-gray-500 hover:text-blue-600 font-semibold transition-colors">
            + Yeni Upsell Teklifi Ekle
          </button>

          {showOfferModal && editingOffer && (
            <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50" onClick={() => setShowOfferModal(false)}>
              <div className="bg-white rounded-xl p-6 w-full max-w-lg mx-4" onClick={e => e.stopPropagation()}>
                <h3 className="text-lg font-bold mb-4">{editingOffer.id ? 'Teklifi Düzenle' : 'Yeni Teklif'}</h3>
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Teklif Adı</label>
                      <input type="text" value={editingOffer.name} onChange={e => setEditingOffer({ ...editingOffer, name: e.target.value })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Kategori</label>
                      <select value={editingOffer.category} onChange={e => setEditingOffer({ ...editingOffer, category: e.target.value })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                        {categories.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
                      </select>
                    </div>
                  </div>
                  <div>
                    <label className="text-xs font-medium text-gray-600">Açıklama</label>
                    <textarea value={editingOffer.description} onChange={e => setEditingOffer({ ...editingOffer, description: e.target.value })}
                      className="w-full border rounded-lg px-3 py-2 text-sm mt-1" rows={2} />
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Fiyat</label>
                      <input type="number" value={editingOffer.price} onChange={e => setEditingOffer({ ...editingOffer, price: parseFloat(e.target.value) || 0 })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Para Birimi</label>
                      <select value={editingOffer.currency} onChange={e => setEditingOffer({ ...editingOffer, currency: e.target.value })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                        <option value="TRY">TRY</option>
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Sıra</label>
                      <input type="number" value={editingOffer.display_order} onChange={e => setEditingOffer({ ...editingOffer, display_order: parseInt(e.target.value) || 0 })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Tetikleyici</label>
                      <select value={editingOffer.trigger_event || ''} onChange={e => setEditingOffer({ ...editingOffer, trigger_event: e.target.value || null })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                        <option value="">Yok</option>
                        {triggerEvents.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                      </select>
                    </div>
                    <div className="flex items-end pb-2">
                      <label className="flex items-center gap-2 text-sm">
                        <input type="checkbox" checked={editingOffer.is_auto_offer}
                          onChange={e => setEditingOffer({ ...editingOffer, is_auto_offer: e.target.checked })}
                          className="rounded" />
                        Otomatik Teklif
                      </label>
                    </div>
                  </div>
                </div>
                <div className="flex gap-2 mt-5">
                  <button onClick={() => setShowOfferModal(false)}
                    className="flex-1 border rounded-lg py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50">İptal</button>
                  <button onClick={saveOffer}
                    className="flex-1 bg-blue-600 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-700">Kaydet</button>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {tab === 'add' && (
        <div className="border rounded-xl p-6 max-w-md">
          <h3 className="font-semibold mb-4">Booking'e Upsell Ekle</h3>
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-600">Booking ID</label>
              <input type="number" value={bookingId} onChange={e => setBookingId(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 text-sm mt-1" placeholder="Örn: 42" />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-600">Teklif</label>
              <select value={selectedOfferId} onChange={e => setSelectedOfferId(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                <option value="">Seçiniz</option>
                {offers.filter(o => o.is_active).map(o => (
                  <option key={o.id} value={o.id}>{o.name} - {o.currency} {o.price}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs font-medium text-gray-600">Adet</label>
              <input type="number" value={quantity} onChange={e => setQuantity(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 text-sm mt-1" min="1" />
            </div>
            <button onClick={handleAddToBooking}
              className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-700 transition-colors">
              Booking'e Ekle
            </button>
          </div>
        </div>
      )}

      {tab === 'campaigns' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {campaigns.map(c => (
            <div key={c.id} className="border rounded-xl p-5 hover:shadow-sm transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold">{c.name}</h3>
                  <p className="text-sm text-gray-500 mt-1">{c.description}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded font-semibold ${c.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                  {c.is_active ? 'Aktif' : 'Pasif'}
                </span>
              </div>
              <div className="mt-3 flex items-center gap-3 text-sm text-gray-600">
                <span className="inline-block px-2 py-0.5 rounded bg-blue-100 text-blue-700 font-bold">%{c.discount_percentage} İndirim</span>
                <span>{c.start_date} → {c.end_date}</span>
              </div>
            </div>
          ))}
          <button className="border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-xl p-5 text-center text-sm text-gray-500 hover:text-blue-600 font-semibold transition-colors flex items-center justify-center">
            + Yeni Kampanya Oluştur
          </button>
        </div>
      )}

      {tab === 'report' && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="border rounded-xl p-5 bg-gradient-to-br from-blue-50 to-white">
              <p className="text-sm text-gray-500 font-medium">Toplam Ek Gelir</p>
              <p className="text-3xl font-bold mt-1">₺{report.total_upsell_revenue.toLocaleString('tr-TR')}</p>
            </div>
            <div className="border rounded-xl p-5 bg-gradient-to-br from-green-50 to-white">
              <p className="text-sm text-gray-500 font-medium">Toplam Sipariş</p>
              <p className="text-3xl font-bold mt-1">{report.total_orders}</p>
            </div>
            <div className="border rounded-xl p-5 bg-gradient-to-br from-purple-50 to-white">
              <p className="text-sm text-gray-500 font-medium">Ortalama Sipariş</p>
              <p className="text-3xl font-bold mt-1">₺{Math.round(report.total_upsell_revenue / report.total_orders).toLocaleString('tr-TR')}</p>
            </div>
          </div>

          <div className="border rounded-xl p-5">
            <h3 className="font-semibold mb-4">Kategori Bazında Dağılım</h3>
            <div className="space-y-3">
              {Object.entries(report.breakdown).map(([cat, val]) => {
                const pct = ((val as number) / report.total_upsell_revenue) * 100;
                return (
                  <div key={cat}>
                    <div className="flex items-center justify-between text-sm mb-1">
                      <span className="font-medium">{categoryLabel(cat)}</span>
                      <span className="text-gray-600">₺{(val as number).toLocaleString('tr-TR')} (%{pct.toFixed(0)})</span>
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-blue-500" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
