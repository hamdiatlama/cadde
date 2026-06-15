'use client';
import { useState } from 'react';

const tiers = [
  { name: 'Bronz', minPoints: 0, color: 'bg-amber-600', textColor: 'text-amber-600', benefits: 'Standart puan kazanımı' },
  { name: 'Gümüş', minPoints: 1000, color: 'bg-gray-400', textColor: 'text-gray-500', benefits: '%10 ekstra puan, özel kampanyalar' },
  { name: 'Altın', minPoints: 5000, color: 'bg-yellow-500', textColor: 'text-yellow-600', benefits: '%25 ekstra puan, ücretsiz kargo' },
  { name: 'Platin', minPoints: 15000, color: 'bg-purple-600', textColor: 'text-purple-600', benefits: '%50 ekstra puan, öncelikli destek, özel etkinlikler' },
];

const pointHistory = [
  { id: 1, date: '2026-06-14', description: 'Sipariş #ORD-2026-0421', points: 120, type: 'earned' },
  { id: 2, date: '2026-06-12', description: 'Sipariş #ORD-2026-0418', points: 85, type: 'earned' },
  { id: 3, date: '2026-06-10', description: 'Puan Kullanımı - İndirim', points: -200, type: 'spent' },
  { id: 4, date: '2026-06-08', description: 'Doğum Günü Bonus Puanı', points: 500, type: 'earned' },
  { id: 5, date: '2026-06-05', description: 'Sipariş #ORD-2026-0412', points: 200, type: 'earned' },
  { id: 6, date: '2026-06-01', description: 'Arkadaş Tavsiye Bonusu', points: 250, type: 'earned' },
];

export default function LoyaltyPage() {
  const [tab, setTab] = useState<'overview' | 'history'>('overview');
  const totalPoints = 3200;
  const currentTier = tiers[1];

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Sadakat Programı</h1>
      <p className="text-gray-500 mb-6">Her alışverişte puan kazanın, ayrıcalıkların tadını çıkarın</p>

      <div className="grid gap-6 md:grid-cols-3 mb-8">
        <div className="bg-gradient-to-br from-purple-600 to-indigo-700 text-white rounded-xl p-6 shadow-lg">
          <p className="text-sm opacity-80 mb-1">Toplam Puan</p>
          <p className="text-3xl font-bold">{totalPoints.toLocaleString()}</p>
          <p className="text-sm mt-2 opacity-80">{currentTier.name} üyesi</p>
        </div>
        <div className="border rounded-lg p-4 text-center">
          <p className="text-sm text-gray-500 mb-1">Harcanabilir Puan</p>
          <p className="text-2xl font-bold text-purple-700">{totalPoints.toLocaleString()}</p>
          <p className="text-xs text-gray-400 mt-1">= {(totalPoints / 100).toFixed(2)} TL</p>
        </div>
        <div className="border rounded-lg p-4 text-center">
          <p className="text-sm text-gray-500 mb-1">Sonraki Seviye</p>
          <p className="text-2xl font-bold text-amber-600">Altın</p>
          <div className="bg-gray-200 rounded-full h-2 mt-3">
            <div className="bg-amber-500 rounded-full h-2" style={{ width: `${Math.min(100, (totalPoints / 5000) * 100)}%` }}></div>
          </div>
          <p className="text-xs text-gray-400 mt-1">{5000 - totalPoints} puan kaldı</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6">
        {(['overview', 'history'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'overview' ? 'Seviyeler' : 'Puan Geçmişi'}
          </button>
        ))}
      </div>

      {tab === 'overview' && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {tiers.map(t => {
            const unlocked = totalPoints >= t.minPoints;
            const current = currentTier.name === t.name;
            return (
              <div key={t.name} className={`border rounded-lg p-5 text-center ${current ? 'ring-2 ring-purple-500 bg-purple-50' : unlocked ? '' : 'opacity-50'}`}>
                <div className={`w-10 h-10 rounded-full ${t.color} mx-auto mb-3 flex items-center justify-center text-white text-sm font-bold`}>
                  {t.name[0]}
                </div>
                <h3 className="font-bold text-lg">{t.name}</h3>
                <p className={`text-xs font-semibold mb-2 ${t.textColor}`}>{t.minPoints.toLocaleString()} puandan başlar</p>
                <p className="text-xs text-gray-500">{t.benefits}</p>
                {current && <span className="inline-block mt-2 text-xs bg-purple-200 text-purple-700 px-2 py-0.5 rounded-full">Seviyeniz</span>}
              </div>
            );
          })}
        </div>
      )}

      {tab === 'history' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-left p-3 text-sm font-semibold">Açıklama</th>
                <th className="text-right p-3 text-sm font-semibold">Puan</th>
              </tr>
            </thead>
            <tbody>
              {pointHistory.map(h => (
                <tr key={h.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">{h.date}</td>
                  <td className="p-3 text-sm">{h.description}</td>
                  <td className={`p-3 text-sm text-right font-semibold ${h.points > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {h.points > 0 ? '+' : ''}{h.points}
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
