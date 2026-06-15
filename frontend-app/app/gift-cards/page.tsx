'use client';
import { useState } from 'react';

const cardTemplates = [50, 100, 200, 500, 1000];

const myCards = [
  { code: 'HED-4A8B-2C1D', balance: 200, created: '2026-06-01', expires: '2026-12-01' },
  { code: 'HED-7F3E-9A0B', balance: 50, created: '2026-06-10', expires: '2026-12-10' },
];

export default function GiftCardsPage() {
  const [tab, setTab] = useState<'create' | 'redeem' | 'balance'>('create');
  const [amount, setAmount] = useState(100);
  const [redeemCode, setRedeemCode] = useState('');
  const [balanceCode, setBalanceCode] = useState('');
  const [balanceResult, setBalanceResult] = useState<{ code: string; balance: number } | null>(null);

  function handleCreate() {
    alert(`${amount} TL değerinde hediye çeki oluşturuldu!`);
  }

  function handleRedeem() {
    if (redeemCode.trim()) alert(`${redeemCode} kodu başarıyla kullanıldı!`);
  }

  function handleCheckBalance() {
    const card = myCards.find(c => c.code === balanceCode);
    if (card) setBalanceResult({ code: card.code, balance: card.balance });
    else setBalanceResult(null);
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Hediye Çekleri</h1>
      <p className="text-gray-500 mb-6">Hediye çeki oluşturun, kullanın ve bakiye sorgulayın</p>

      <div className="flex gap-2 mb-6">
        {(['create', 'redeem', 'balance'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'create' ? 'Çek Oluştur' : t === 'redeem' ? 'Kullan' : 'Bakiye Sorgula'}
          </button>
        ))}
      </div>

      {tab === 'create' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Yeni Hediye Çeki Oluştur</h2>
          <div className="flex gap-3 mb-4 flex-wrap">
            {cardTemplates.map(a => (
              <button key={a} onClick={() => setAmount(a)}
                className={`px-5 py-2 rounded-lg border text-sm font-semibold ${amount === a ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 text-gray-700 hover:border-blue-400'}`}>
                {a} TL
              </button>
            ))}
          </div>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-sm text-gray-600">veya</span>
            <input type="number" value={amount} onChange={e => setAmount(Number(e.target.value))}
              className="border rounded-lg p-2 w-32 text-sm" min={10} />
          </div>
          <button onClick={handleCreate} className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700">
            {amount} TL Değerinde Çek Oluştur
          </button>
        </div>
      )}

      {tab === 'redeem' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Hediye Çeki Kullan</h2>
          <p className="text-sm text-gray-500 mb-3">Hediye çeki kodunuzu girin ve bakiyeyi hesabınıza tanımlayın.</p>
          <div className="flex gap-2">
            <input value={redeemCode} onChange={e => setRedeemCode(e.target.value.toUpperCase())}
              placeholder="Örn: HED-XXXX-XXXX" className="border p-2 flex-1 rounded text-sm font-mono uppercase" />
            <button onClick={handleRedeem} className="bg-green-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-green-700">
              Kullan
            </button>
          </div>
        </div>
      )}

      {tab === 'balance' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Bakiye Sorgula</h2>
          <div className="flex gap-2 mb-4">
            <input value={balanceCode} onChange={e => setBalanceCode(e.target.value.toUpperCase())}
              placeholder="Kodu girin" className="border p-2 flex-1 rounded text-sm font-mono uppercase" />
            <button onClick={handleCheckBalance} className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700">
              Sorgula
            </button>
          </div>
          {balanceResult && (
            <div className="bg-green-50 border border-green-200 rounded p-4">
              <p className="font-semibold">{balanceResult.code}</p>
              <p className="text-2xl font-bold text-green-700">{balanceResult.balance.toLocaleString()} TL</p>
            </div>
          )}
        </div>
      )}

      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Çeklerim</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Kod</th>
                <th className="text-right p-3 text-sm font-semibold">Bakiye</th>
                <th className="text-left p-3 text-sm font-semibold">Oluşturma</th>
                <th className="text-left p-3 text-sm font-semibold">Geçerlilik</th>
              </tr>
            </thead>
            <tbody>
              {myCards.map(c => (
                <tr key={c.code} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-mono">{c.code}</td>
                  <td className="p-3 text-sm text-right font-semibold text-green-600">{c.balance} TL</td>
                  <td className="p-3 text-sm">{c.created}</td>
                  <td className="p-3 text-sm">{c.expires}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
