'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function ProtectionPage() {
  const [status, setStatus] = useState<any>(null);
  const [claims, setClaims] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/protection/status').then(r => r.json()).then(setStatus);
    fetch('/api/protection/claims').then(r => r.json()).then(setClaims);
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Alici Korumasi</h1>

      {status && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-2">Koruma Durumunuz</h2>
          <p className="text-sm mb-4">{status.coverage}</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div><p className="text-2xl font-bold">{status.total_orders}</p><p className="text-sm">Toplam Siparis</p></div>
            <div><p className="text-2xl font-bold">{status.return_requests}</p><p className="text-sm">Iade Talebi</p></div>
            <div><p className="text-2xl font-bold">{status.open_disputes}</p><p className="text-sm">Aktif Uyusmazlik</p></div>
            <div><p className="text-2xl font-bold">{status.claim_window_days} gun</p><p className="text-sm">Talep Suresi</p></div>
          </div>
        </div>
      )}

      <Link href="/protection/claim" className="bg-red-600 text-white px-6 py-3 rounded-lg inline-block mb-8 hover:bg-red-700">
        Hasar / Hatali Urun Bildir
      </Link>

      <h2 className="text-xl font-semibold mb-4">Taleplerim</h2>
      {claims.length === 0 && <p className="text-gray-500">Henuz talep yok</p>}
      <div className="space-y-3">
        {claims.map((c: any) => (
          <div key={c.id} className="border rounded-lg p-4">
            <div className="flex justify-between">
              <p className="font-semibold">{c.reason}</p>
              <span className={'px-2 py-1 rounded text-sm ' + (c.status === 'open' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800')}>
                {c.status === 'open' ? 'Incelemede' : 'Co-zuldu'}
              </span>
            </div>
            {c.resolution && <p className="text-sm text-gray-600 mt-2">Co-zu:m {c.resolution}</p>}
            <p className="text-xs text-gray-400 mt-1">{c.created_at}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
