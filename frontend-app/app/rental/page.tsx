'use client';
import { useState, useEffect } from 'react';
const API = 'http://127.0.0.1:8000';
const CATEGORIES = [
  { value: '', label: 'Tümü' }, { value: 'car', label: 'Oto Kiralama' },
  { value: 'motorcycle', label: 'Motor Kiralama' }, { value: 'scooter', label: 'Skuter Kiralama' },
  { value: 'boat', label: 'Tekne Kiralama' }, { value: 'caravan', label: 'Karavan Kiralama' },
  { value: 'plane', label: 'Ucak Kiralama' },
];
export default function RentalPage() {
  const [vehicles, setVehicles] = useState([]); const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(false);
  async function search() {
    setLoading(true);
    try {
      const p = new URLSearchParams(); if (category) p.set('category', category);
      const r = await fetch(API + '/rental/vehicles?' + p); setVehicles(await r.json());
    } catch (_) {} finally { setLoading(false); }
  }
  useEffect(() => { search(); }, []);
  return (<div className='p-4 max-w-6xl mx-auto'>
    <h1 className='text-2xl font-bold mb-4'>Kiralama</h1>
    <select value={category} onChange={e => setCategory(e.target.value)}
      className='border p-2 rounded mb-4'>{CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}</select>
    <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
      {(vehicles || []).map(v => <div key={v.id} className='border rounded p-3'>
        <span className='text-xs bg-gray-100 px-2 py-1 rounded'>{CATEGORIES.find(c => c.value === v.category)?.label || v.category}</span>
        <h3 className='font-semibold mt-1'>{v.brand} {v.model}</h3>
        <p className='text-sm text-gray-600'>{v.year} | {v.color}</p>
        <p className='text-blue-600 font-bold mt-2'>{v.daily_price?.toLocaleString()} {v.currency || 'TRY'}/gun</p>
      </div>)}
    </div>
  </div>);
}
