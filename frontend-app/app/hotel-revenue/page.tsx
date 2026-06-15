'use client';
import { useState } from 'react';

const mockRules = [
  { id: 1, name: 'Sezonluk - Yaz', rule_type: 'seasonal', adjustment_type: 'percentage', adjustment_value: 20, priority: 1, is_active: true, conditions: { months: '06-09' } },
  { id: 2, name: 'Son Dakika', rule_type: 'last_minute', adjustment_type: 'percentage', adjustment_value: -15, priority: 2, is_active: true, conditions: { advance_days: 3 } },
  { id: 3, name: 'Erken Rezervasyon', rule_type: 'early_bird', adjustment_type: 'percentage', adjustment_value: -10, priority: 3, is_active: true, conditions: { advance_days: 30 } },
  { id: 4, name: 'Hafta Sonu', rule_type: 'weekend', adjustment_type: 'fixed', adjustment_value: 50, priority: 4, is_active: false, conditions: { days: 'sat,sun' } },
  { id: 5, name: 'Uzun Konaklama', rule_type: 'length_of_stay', adjustment_type: 'percentage', adjustment_value: -5, priority: 5, is_active: true, conditions: { min_stay: 3 } },
  { id: 6, name: 'Doluluk Bazlı', rule_type: 'occupancy_based', adjustment_type: 'percentage', adjustment_value: 25, priority: 6, is_active: true, conditions: { threshold: 0.8 } },
];

const mockDailyRates = [
  { date: '2026-06-15', base_price: 500, dynamic_price: 600, final_price: 600, occupancy_rate: 0.85, is_boosted: true },
  { date: '2026-06-16', base_price: 500, dynamic_price: 550, final_price: 550, occupancy_rate: 0.72, is_boosted: false },
  { date: '2026-06-17', base_price: 500, dynamic_price: 500, final_price: 500, occupancy_rate: 0.45, is_boosted: false },
  { date: '2026-06-18', base_price: 500, dynamic_price: 450, final_price: 450, occupancy_rate: 0.30, is_boosted: false, is_sale: true },
  { date: '2026-06-19', base_price: 500, dynamic_price: 480, final_price: 480, occupancy_rate: 0.55, is_boosted: false },
  { date: '2026-06-20', base_price: 500, dynamic_price: 650, final_price: 650, occupancy_rate: 0.90, is_boosted: true },
  { date: '2026-06-21', base_price: 500, dynamic_price: 700, final_price: 700, occupancy_rate: 0.95, is_boosted: true },
];

export default function HotelRevenuePage() {
  const [tab, setTab] = useState<'dashboard' | 'rules' | 'rates'>('dashboard');
  const [period, setPeriod] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [rules, setRules] = useState(mockRules);
  const [showRuleModal, setShowRuleModal] = useState(false);
  const [editingRule, setEditingRule] = useState<any>(null);

  const openNewRule = () => {
    setEditingRule({ name: '', rule_type: 'seasonal', adjustment_type: 'percentage', adjustment_value: 0, priority: 0, is_active: true });
    setShowRuleModal(true);
  };

  const openEditRule = (rule: any) => {
    setEditingRule({ ...rule });
    setShowRuleModal(true);
  };

  const saveRule = () => {
    if (editingRule.id) {
      setRules(prev => prev.map(r => r.id === editingRule.id ? editingRule : r));
    } else {
      setRules(prev => [...prev, { ...editingRule, id: Math.max(...prev.map(r => r.id)) + 1 }]);
    }
    setShowRuleModal(false);
    setEditingRule(null);
  };

  const toggleRule = (id: number) => {
    setRules(prev => prev.map(r => r.id === id ? { ...r, is_active: !r.is_active } : r));
  };

  return (
    <div className="max-w-7xl mx-auto p-6 font-[family-name:var(--font-geist-sans)]">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Gelir Yönetimi</h1>
          <p className="text-gray-500 text-sm mt-1">RevPAR, ADR ve doluluk takibi</p>
        </div>
        <div className="flex items-center gap-2">
          <select value={period} onChange={e => setPeriod(e.target.value as any)}
            className="border rounded px-3 py-1.5 text-sm font-medium bg-white">
            <option value="daily">Günlük</option>
            <option value="weekly">Haftalık</option>
            <option value="monthly">Aylık</option>
          </select>
          <button onClick={() => setTab('dashboard')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'dashboard' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Dashboard</button>
          <button onClick={() => setTab('rules')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'rules' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Kurallar</button>
          <button onClick={() => setTab('rates')}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'rates' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Günlük Fiyatlar</button>
        </div>
      </div>

      {tab === 'dashboard' && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="border rounded-xl p-5 bg-gradient-to-br from-blue-50 to-white">
              <p className="text-sm text-gray-500 font-medium">RevPAR</p>
              <p className="text-3xl font-bold mt-1">₺485</p>
              <p className="text-xs text-green-600 mt-1">%12 artış</p>
            </div>
            <div className="border rounded-xl p-5 bg-gradient-to-br from-green-50 to-white">
              <p className="text-sm text-gray-500 font-medium">ADR</p>
              <p className="text-3xl font-bold mt-1">₺625</p>
              <p className="text-xs text-green-600 mt-1">%8 artış</p>
            </div>
            <div className="border rounded-xl p-5 bg-gradient-to-br from-purple-50 to-white">
              <p className="text-sm text-gray-500 font-medium">Doluluk</p>
              <p className="text-3xl font-bold mt-1">%72</p>
              <p className="text-xs text-amber-600 mt-1">%3 düşüş</p>
            </div>
          </div>

          <div className="border rounded-xl p-5 mb-6">
            <h3 className="font-semibold mb-3">Günlük Fiyat Takvimi</h3>
            <div className="grid grid-cols-7 gap-2">
              {mockDailyRates.map(r => (
                <div key={r.date} className={`border rounded-lg p-3 text-center ${r.is_boosted ? 'bg-red-50 border-red-200' : r.is_sale ? 'bg-green-50 border-green-200' : ''}`}>
                  <p className="text-xs text-gray-500">{new Date(r.date).toLocaleDateString('tr-TR', { weekday: 'short', day: 'numeric' })}</p>
                  <p className="text-lg font-bold mt-1">₺{r.final_price}</p>
                  <p className={`text-xs mt-1 ${r.is_boosted ? 'text-red-600' : r.is_sale ? 'text-green-600' : 'text-gray-500'}`}>
                    {r.is_boosted ? 'Yoğun' : r.is_sale ? 'İndirim' : 'Normal'}
                  </p>
                  <div className="mt-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${r.occupancy_rate > 0.7 ? 'bg-red-500' : r.occupancy_rate > 0.4 ? 'bg-amber-500' : 'bg-green-500'}`}
                      style={{ width: `${r.occupancy_rate * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-end">
            <button onClick={() => { setTab('rules'); }}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors">
              Rapor Oluştur
            </button>
          </div>
        </>
      )}

      {tab === 'rules' && (
        <>
          <div className="overflow-x-auto border rounded-lg">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="text-left p-3 text-sm font-semibold">Kural</th>
                  <th className="text-left p-3 text-sm font-semibold">Tür</th>
                  <th className="text-left p-3 text-sm font-semibold">Ayar</th>
                  <th className="text-center p-3 text-sm font-semibold">Öncelik</th>
                  <th className="text-center p-3 text-sm font-semibold">Durum</th>
                  <th className="text-center p-3 text-sm font-semibold">İşlem</th>
                </tr>
              </thead>
              <tbody>
                {rules.map(r => (
                  <tr key={r.id} className="border-b hover:bg-gray-50">
                    <td className="p-3 text-sm font-semibold">{r.name}</td>
                    <td className="p-3 text-sm text-gray-600">{r.rule_type}</td>
                    <td className="p-3 text-sm">
                      <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${r.adjustment_type === 'percentage' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'}`}>
                        {r.adjustment_type === 'percentage' ? `%${r.adjustment_value}` : `₺${r.adjustment_value}`}
                      </span>
                    </td>
                    <td className="p-3 text-sm text-center">{r.priority}</td>
                    <td className="p-3 text-center">
                      <button onClick={() => toggleRule(r.id)}
                        className={`text-xs px-2 py-1 rounded font-semibold ${r.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                        {r.is_active ? 'Aktif' : 'Pasif'}
                      </button>
                    </td>
                    <td className="p-3 text-center">
                      <button onClick={() => openEditRule(r)}
                        className="text-xs text-blue-600 hover:underline font-medium">Düzenle</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button onClick={openNewRule}
            className="mt-4 border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-lg p-4 w-full text-center text-sm text-gray-500 hover:text-blue-600 font-semibold transition-colors">
            + Yeni Kural Ekle
          </button>

          {showRuleModal && editingRule && (
            <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50" onClick={() => setShowRuleModal(false)}>
              <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4" onClick={e => e.stopPropagation()}>
                <h3 className="text-lg font-bold mb-4">{editingRule.id ? 'Kuralı Düzenle' : 'Yeni Kural'}</h3>
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-medium text-gray-600">Kural Adı</label>
                    <input type="text" value={editingRule.name} onChange={e => setEditingRule({ ...editingRule, name: e.target.value })}
                      className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Tür</label>
                      <select value={editingRule.rule_type} onChange={e => setEditingRule({ ...editingRule, rule_type: e.target.value })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                        <option value="seasonal">Sezonluk</option>
                        <option value="last_minute">Son Dakika</option>
                        <option value="early_bird">Erken Rezervasyon</option>
                        <option value="length_of_stay">Uzun Konaklama</option>
                        <option value="occupancy_based">Doluluk Bazlı</option>
                        <option value="weekend">Hafta Sonu</option>
                        <option value="competitor">Rakip Bazlı</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Ayar Türü</label>
                      <select value={editingRule.adjustment_type} onChange={e => setEditingRule({ ...editingRule, adjustment_type: e.target.value })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1 bg-white">
                        <option value="percentage">Yüzde</option>
                        <option value="fixed">Sabit</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Değer</label>
                      <input type="number" value={editingRule.adjustment_value} onChange={e => setEditingRule({ ...editingRule, adjustment_value: parseFloat(e.target.value) || 0 })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Öncelik</label>
                      <input type="number" value={editingRule.priority} onChange={e => setEditingRule({ ...editingRule, priority: parseInt(e.target.value) || 0 })}
                        className="w-full border rounded-lg px-3 py-2 text-sm mt-1" />
                    </div>
                  </div>
                </div>
                <div className="flex gap-2 mt-5">
                  <button onClick={() => setShowRuleModal(false)}
                    className="flex-1 border rounded-lg py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50">İptal</button>
                  <button onClick={saveRule}
                    className="flex-1 bg-blue-600 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-700">Kaydet</button>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {tab === 'rates' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-left p-3 text-sm font-semibold">Baz Fiyat</th>
                <th className="text-left p-3 text-sm font-semibold">Dinamik Fiyat</th>
                <th className="text-left p-3 text-sm font-semibold">Final Fiyat</th>
                <th className="text-center p-3 text-sm font-semibold">Doluluk</th>
                <th className="text-center p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {mockDailyRates.map(r => (
                <tr key={r.date} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-semibold">{new Date(r.date).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })}</td>
                  <td className="p-3 text-sm">₺{r.base_price}</td>
                  <td className="p-3 text-sm">₺{r.dynamic_price}</td>
                  <td className="p-3 text-sm font-bold">₺{r.final_price}</td>
                  <td className="p-3 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <span className="text-xs font-medium">{(r.occupancy_rate * 100).toFixed(0)}%</span>
                      <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${r.occupancy_rate > 0.7 ? 'bg-red-500' : r.occupancy_rate > 0.4 ? 'bg-amber-500' : 'bg-green-500'}`}
                          style={{ width: `${r.occupancy_rate * 100}%` }} />
                      </div>
                    </div>
                  </td>
                  <td className="p-3 text-center">
                    {r.is_boosted ? (
                      <span className="text-xs px-2 py-1 rounded font-semibold bg-red-100 text-red-700">Yoğun</span>
                    ) : r.is_sale ? (
                      <span className="text-xs px-2 py-1 rounded font-semibold bg-green-100 text-green-700">İndirim</span>
                    ) : (
                      <span className="text-xs px-2 py-1 rounded font-semibold bg-gray-100 text-gray-500">Normal</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
