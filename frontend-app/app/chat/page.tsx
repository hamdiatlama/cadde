'use client';
import { useState } from 'react';

const conversations = [
  { id: 1, name: 'Mehmet Usta', lastMsg: 'Ürün ne zaman kargoya verilecek?', time: '12:34', unread: 2, online: true },
  { id: 2, name: 'Ayşe Tekstil', lastMsg: 'Faturanız ektedir', time: 'Dün', unread: 0, online: false },
  { id: 3, name: 'Ali Bey', lastMsg: 'Teşekkürler, elime ulaştı', time: 'Dün', unread: 0, online: false },
  { id: 4, name: 'Zeynep Hanım', lastMsg: 'Renk seçeneği var mı?', time: '2 gün önce', unread: 1, online: true },
  { id: 5, name: 'Can Market', lastMsg: 'Toplu siparişte indirim...', time: '3 gün önce', unread: 0, online: false },
];

const messages = [
  { id: 1, sender: 'them', text: 'Merhaba, ürünü inceledim', time: '12:30' },
  { id: 2, sender: 'me', text: 'Merhaba, bir sorunuz mu var?', time: '12:31' },
  { id: 3, sender: 'them', text: 'Ürün ne zaman kargoya verilecek?', time: '12:34' },
  { id: 4, sender: 'them', text: 'Acaba bugün gönderim yapabilecek misiniz?', time: '12:35' },
];

export default function ChatPage() {
  const [activeConv, setActiveConv] = useState(conversations[0]);
  const [input, setInput] = useState('');

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Mesajlaşma</h1>
      <div className="border rounded-lg flex h-[600px] overflow-hidden">
        <div className="w-80 border-r flex-shrink-0 overflow-y-auto">
          {conversations.map(c => (
            <div
              key={c.id}
              onClick={() => setActiveConv(c)}
              className={`p-4 border-b cursor-pointer transition-colors ${activeConv.id === c.id ? 'bg-blue-50' : 'hover:bg-gray-50'}`}
            >
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-semibold">
                    {c.name[0]}
                  </div>
                  {c.online && <div className="w-3 h-3 bg-green-500 rounded-full absolute -top-0.5 -right-0.5 border-2 border-white" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-sm">{c.name}</span>
                    <span className="text-xs text-gray-400">{c.time}</span>
                  </div>
                  <p className="text-sm text-gray-500 truncate">{c.lastMsg}</p>
                </div>
                {c.unread > 0 && (
                  <span className="bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{c.unread}</span>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex-1 flex flex-col">
          <div className="p-4 border-b bg-white">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-semibold">
                {activeConv.name[0]}
              </div>
              <div>
                <p className="font-semibold">{activeConv.name}</p>
                <p className="text-xs text-green-600">{activeConv.online ? 'Çevrimiçi' : 'Çevrimdışı'}</p>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
            {messages.map(m => (
              <div key={m.id} className={`flex ${m.sender === 'me' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-md rounded-lg px-4 py-2 text-sm ${m.sender === 'me' ? 'bg-blue-600 text-white' : 'bg-white border'}`}>
                  <p>{m.text}</p>
                  <p className={`text-xs mt-1 ${m.sender === 'me' ? 'text-blue-200' : 'text-gray-400'}`}>{m.time}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="border-t p-4 bg-white flex gap-2">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Mesajınızı yazın..."
              className="flex-1 border rounded-lg px-4 py-2 text-sm outline-none focus:border-blue-400"
              onKeyDown={e => e.key === 'Enter' && setInput('')}
            />
            <button
              onClick={() => setInput('')}
              className="bg-blue-600 text-white px-5 py-2 rounded-lg text-sm hover:bg-blue-700"
            >
              Gönder
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
