"use client";
import { useState } from "react";

export default function GuestCheckoutPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email) setSubmitted(true);
  }

  return (
    <main className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Misafir Olarak Öde</h1>
      <p className="text-sm text-gray-500 mb-8">Siparişinizi tamamlamak için e-posta adresinizi girin.</p>
      {submitted ? (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-green-800 text-sm">
          Sipariş bilgileriniz <strong>{email}</strong> adresine gönderilecek.
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">E-posta</label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="ornek@email.com"
            />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 transition-colors">
            Devam Et
          </button>
        </form>
      )}
    </main>
  );
}
