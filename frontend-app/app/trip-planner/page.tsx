'use client';
import { useState, useEffect } from 'react';
const API = 'http://127.0.0.1:8000';

export default function TripPlannerPage() {
  const [plans, setPlans] = useState([]);
  const [plan, setPlan] = useState(null);
  const [tab, setTab] = useState('list');
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [originCity, setOriginCity] = useState('');
  const [newSeg, setNewSeg] = useState({ origin_name: '', destination_name: '', transport_mode: 'taxi' });
  const [exploreCity, setExploreCity] = useState('');
  const [explore, setExplore] = useState(null);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => { if (tab === 'list') loadPlans(); }, [tab]);

  async function loadPlans() {
    try { const r = await fetch(API + '/trip-planner/plans?user_id=1'); setPlans(await r.json() || []); } catch (_) {}
  }

  async function createPlan() {
    try {
      const r = await fetch(API + '/trip-planner/plans', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1, name, start_date: startDate, end_date: endDate, origin_city: originCity }),
      });
      if (r.ok) { alert('Plan olusturuldu!'); loadPlans(); setTab('list'); }
    } catch (_) {}
  }

  async function loadPlan(id) {
    try { const r = await fetch(API + '/trip-planner/plans/' + id); setPlan(await r.json()); setTab('detail'); } catch (_) {}
  }

  async function addSegment() {
    if (!plan) return;
    try {
      const seq = (plan.segments || []).length + 1;
      const r = await fetch(API + '/trip-planner/segments', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trip_id: plan.plan.id, sequence: seq, ...newSeg }),
      });
      if (r.ok) { alert('Segment eklendi!'); loadPlan(plan.plan.id); }
    } catch (_) {}
  }

  async function exploreCityData() {
    if (!exploreCity) return;
    try { const r = await fetch(API + '/trip-planner/explore/' + exploreCity); setExplore(await r.json()); } catch (_) {}
  }

  async function suggestRoute() {
    try {
      const r = await fetch(API + '/trip-planner/ai/suggest-route?origin_city=' + encodeURIComponent(originCity) +
        '&dest_city=' + encodeURIComponent(exploreCity));
      setSuggestions(await r.json() || []);
    } catch (_) {}
  }

  return (<div className='p-4 max-w-6xl mx-auto'>
    <h1 className='text-2xl font-bold mb-4'>Rota Olustur</h1>
    <div className='flex gap-2 mb-4'>
      <button onClick={() => setTab('list')} className={'px-3 py-1 rounded ' + (tab === 'list' ? 'bg-blue-600 text-white' : 'bg-gray-100')}>Planlarim</button>
      <button onClick={() => setTab('new')} className={'px-3 py-1 rounded ' + (tab === 'new' ? 'bg-blue-600 text-white' : 'bg-gray-100')}>Yeni Plan</button>
      <button onClick={() => setTab('explore')} className={'px-3 py-1 rounded ' + (tab === 'explore' ? 'bg-blue-600 text-white' : 'bg-gray-100')}>Kesfet</button>
    </div>

    {tab === 'list' && <div className='grid gap-3'>
      {plans.map(p => <div key={p.id} className='border p-3 rounded cursor-pointer hover:shadow' onClick={() => loadPlan(p.id)}>
        <h3 className='font-bold'>{p.name}</h3>
        <p className='text-sm text-gray-600'>{p.start_date} - {p.end_date} | {p.origin_city}</p>
        <span className={'text-xs px-2 py-1 rounded ' + (p.status === 'draft' ? 'bg-yellow-100' : 'bg-green-100')}>{p.status}</span>
      </div>)}
    </div>}

    {tab === 'new' && <div className='max-w-md'>
      <input value={name} onChange={e => setName(e.target.value)} placeholder='Plan Adi' className='border p-2 rounded w-full mb-2' />
      <input type='date' value={startDate} onChange={e => setStartDate(e.target.value)} className='border p-2 rounded w-full mb-2' />
      <input type='date' value={endDate} onChange={e => setEndDate(e.target.value)} className='border p-2 rounded w-full mb-2' />
      <input value={originCity} onChange={e => setOriginCity(e.target.value)} placeholder='Cikis Sehri' className='border p-2 rounded w-full mb-2' />
      <button onClick={createPlan} className='bg-blue-600 text-white px-4 py-2 rounded'>Olustur</button>
      <div className='mt-4 border-t pt-4'>
        <h3 className='font-bold mb-2'>AI Rota Onerisi</h3>
        <input value={exploreCity} onChange={e => setExploreCity(e.target.value)} placeholder='Hedef Sehir' className='border p-2 rounded w-full mb-2' />
        <button onClick={suggestRoute} className='bg-green-600 text-white px-3 py-1 rounded'>Oneri Al</button>
        {suggestions.length > 0 && <div className='mt-2'>
          {suggestions.map((s, i) => <div key={i} className='flex justify-between border p-2 rounded mb-1 text-sm'>
            <span>{s.mode}</span><span>{s.distance_km} km ~ {s.duration_min} dk</span><span>{s.cost} TL</span>
          </div>)}
        </div>}
      </div>
    </div>}

    {tab === 'explore' && <div>
      <input value={exploreCity} onChange={e => setExploreCity(e.target.value)} placeholder='Sehir adi' className='border p-2 rounded mb-2' />
      <button onClick={exploreCityData} className='bg-blue-600 text-white px-3 py-1 rounded mb-4'>Kesfet</button>
      {explore && <div className='grid grid-cols-2 gap-4'>
        <div className='border p-3 rounded'><h3 className='font-bold'>Oteller ({explore.hotels?.length || 0})</h3>
          {explore.hotels?.slice(0, 5).map(h => <p key={h.id} className='text-sm'>{h.name}</p>)}</div>
        <div className='border p-3 rounded'><h3 className='font-bold'>Aktiviteler ({explore.experiences?.length || 0})</h3>
          {explore.experiences?.slice(0, 5).map(e => <p key={e.id} className='text-sm'>{e.name}</p>)}</div>
        <div className='border p-3 rounded'><h3 className='font-bold'>Istasyontar ({explore.stations?.length || 0})</h3>
          {explore.stations?.slice(0, 5).map(s => <p key={s.id} className='text-sm'>{s.name}</p>)}</div>
        <div className='border p-3 rounded'><h3 className='font-bold'>Kiralama ({explore.rentals?.length || 0})</h3>
          {explore.rentals?.slice(0, 5).map(r => <p key={r.id} className='text-sm'>{r.name}</p>)}</div>
      </div>}
    </div>}

    {tab === 'detail' && plan && <div>
      <h2 className='text-xl font-bold mb-2'>{plan.plan.name}</h2>
      <p className='text-sm text-gray-600 mb-4'>{plan.plan.start_date} - {plan.plan.end_date} | {plan.plan.origin_city}</p>

      <h3 className='font-bold mb-2'>Rota Segmentleri</h3>
      <div className='space-y-2 mb-4'>
        {(plan.segments || []).map((s, i) => <div key={s.id} className='flex items-center gap-2 border p-2 rounded'>
          <span className='bg-blue-100 text-blue-700 px-2 rounded-full text-xs'>{i + 1}</span>
          <span className='font-medium'>{s.origin_name || 'Baslangic'}</span>
          <span className='text-gray-400'>~{s.transport_mode || '?'}~</span>
          <span className='font-medium'>{s.destination_name || 'Hedef'}</span>
          {s.cost > 0 && <span className='text-sm text-gray-500 ml-auto'>{s.cost} TL</span>}
        </div>)}
      </div>

      <div className='border-t pt-4'>
        <h3 className='font-bold mb-2'>Yeni Segment Ekle</h3>
        <input value={newSeg.origin_name} onChange={e => setNewSeg({ ...newSeg, origin_name: e.target.value })} placeholder='Kalkis noktasi' className='border p-2 rounded w-full mb-1' />
        <input value={newSeg.destination_name} onChange={e => setNewSeg({ ...newSeg, destination_name: e.target.value })} placeholder='Varis noktasi' className='border p-2 rounded w-full mb-1' />
        <select value={newSeg.transport_mode} onChange={e => setNewSeg({ ...newSeg, transport_mode: e.target.value })} className='border p-2 rounded w-full mb-2'>
          <option value='walking'>Yuruyerek</option><option value='taxi'>Taksi</option><option value='bus'>Otobus</option>
          <option value='dolmus'>Dolmus</option><option value='train'>Tren</option><option value='airplane'>Ucak</option>
          <option value='ferry'>Feribot</option><option value='rental_car'>Kiralik Arac</option><option value='shuttle'>Servis</option>
        </select>
        <button onClick={addSegment} className='bg-green-600 text-white px-3 py-1 rounded'>Ekle</button>
      </div>

      <div className='mt-4 border-t pt-4'>
        <h3 className='font-bold mb-2'>Konaklama</h3>
        {(plan.stays || []).map(s => <div key={s.id} className='border p-2 rounded mb-1 text-sm'>
          {s.accommodation_name} | {s.check_in?.slice(0, 10)} - {s.check_out?.slice(0, 10)} | {s.cost} TL
        </div>)}
      </div>

      <div className='mt-4'>
        <h3 className='font-bold mb-2'>Aktiviteler</h3>
        {(plan.activities || []).map(a => <div key={a.id} className='border p-2 rounded mb-1 text-sm'>
          {a.activity_name} | {a.start_time?.slice(0, 16)} | {a.cost} TL
        </div>)}
      </div>

      <div className='mt-4'>
        <h3 className='font-bold mb-2'>Yemek</h3>
        {(plan.foods || []).map(f => <div key={f.id} className='border p-2 rounded mb-1 text-sm'>
          {f.restaurant_name} | {f.meal_time?.slice(0, 16)}
        </div>)}
      </div>

      <div className='mt-4'>
        <h3 className='font-bold mb-2'>Kiralama</h3>
        {(plan.rentals || []).map(r => <div key={r.id} className='border p-2 rounded mb-1 text-sm'>
          {r.vehicle_type} | {r.pickup_time?.slice(0, 16)} - {r.dropoff_time?.slice(0, 16)}
        </div>)}
      </div>

      <div className='mt-4'>
        <h3 className='font-bold mb-2'>Teslimat</h3>
        {(plan.deliveries || []).map(d => <div key={d.id} className='border p-2 rounded mb-1 text-sm'>
          Siparis: {d.order_no} | {d.cargo_company} | {d.tracking_no}
        </div>)}
      </div>
    </div>}
  </div>);
}
