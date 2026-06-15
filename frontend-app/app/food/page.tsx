"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function FoodPage() {
  const router = useRouter();
  const [restaurants, setRestaurants] = useState<any[]>([]);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [cuisine, setCuisine] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [rr, sr] = await Promise.all([
          fetch(`${API}/food/restaurants`).then(r => r.json()),
          fetch(`${API}/food/suppliers`).then(r => r.json()),
        ]);
        setRestaurants(Array.isArray(rr) ? rr : rr?.value || []);
        setSuppliers(Array.isArray(sr) ? sr : sr?.value || []);
      } catch (_) {}
      setLoading(false);
    }
    load();
  }, []);

  const filtered = cuisine
    ? restaurants.filter((r: any) => r.cuisine_type === cuisine)
    : restaurants;

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 32px"}}>
        <div style={{display:"flex",alignItems:"center",gap:8,cursor:"pointer"}} onClick={()=>router.push("/")}>
          <div style={{width:28,height:28,background:"#4A7FD4",borderRadius:7,display:"flex",alignItems:"center",justifyContent:"center"}}>
            <span style={{color:"#fff",fontSize:14,fontWeight:700}}>C</span>
          </div>
          <span style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.8}}>cadde</span>
        </div>
        <div style={{marginLeft:32,display:"flex",gap:24}}>
          <span className="nav-link" style={{fontSize:13,color:"#4A7FD4",fontWeight:600,cursor:"pointer"}} onClick={()=>router.push("/food")}>Yemek</span>
          <span className="nav-link" style={{fontSize:13,color:"#5A7499",cursor:"pointer",fontWeight:500}} onClick={()=>router.push("/hotels")}>Konaklama</span>
          <span className="nav-link" style={{fontSize:13,color:"#5A7499",cursor:"pointer",fontWeight:500}} onClick={()=>router.push("/search")}>Keşfet</span>
        </div>
      </nav>

      <div style={{padding:"24px 32px",display:"flex",gap:24}}>
        <div style={{flex:1}}>
          <h1 style={{fontSize:24,fontWeight:700,letterSpacing:-0.8,marginBottom:12}}>🍽️ Restoranlar</h1>
          <div style={{display:"flex",gap:8,marginBottom:20,flexWrap:"wrap"}}>
            {["","Turk","Kebab","Pizza","Fast Food"].map(c=>(
              <button key={c} onClick={()=>setCuisine(c)} style={{padding:"6px 14px",background:cuisine===c?"#4A7FD4":"#fff",color:cuisine===c?"#fff":"#5A7499",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,fontWeight:500,cursor:"pointer",fontFamily:"inherit"}}>{c||"Tümü"}</button>
            ))}
          </div>

          {loading ? <p>Yükleniyor...</p> : filtered.length === 0 ? (
            <div style={{padding:20,textAlign:"center",color:"#8FAAC8",fontSize:14}}>Restoran bulunamadı</div>
          ) : filtered.map((r: any) => (
            <div key={r.id} className="biz-card" onClick={()=>router.push(`/food/${r.id}`)} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:16,marginBottom:12,cursor:"pointer",transition:"all .15s"}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"start"}}>
                <div>
                  <div style={{fontSize:16,fontWeight:600}}>{r.name}</div>
                  <div style={{fontSize:12,color:"#8FAAC8",marginTop:4}}>{r.cuisine_type} {r.is_open ? "🟢 Açık" : "🔴 Kapalı"}</div>
                  <div style={{fontSize:12,color:"#5A7499",marginTop:6}}>
                    <i className="ti ti-star" style={{color:"#FFD43B"}}/> {r.rating?.toFixed(1) || "0.0"}
                    {r.min_order_amount > 0 && <span style={{marginLeft:12}}>Min. ₺{r.min_order_amount}</span>}
                  </div>
                </div>
                <div style={{textAlign:"right"}}>
                  <div style={{fontSize:18,fontWeight:700,color:"#4A7FD4"}}>₺{r.delivery_fee?.toFixed(1)}</div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>teslimat</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div style={{width:320}}>
          <h2 style={{fontSize:18,fontWeight:700,letterSpacing:-0.5,marginBottom:12}}>Tedarikçiler</h2>
          {suppliers.slice(0,5).map((s: any) => (
            <div key={s.id} className="biz-card" onClick={()=>router.push(`/food/suppliers/${s.slug}`)} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:14,marginBottom:10,cursor:"pointer"}}>
              <div style={{fontSize:14,fontWeight:600}}>{s.company_name}</div>
              <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>{s.supplier_type === "home_chef" ? "🏠 Ev Yemekçisi" : s.supplier_type === "producer" ? "🌿 Üretici" : "🏭 Ticari"}</div>
              <div style={{fontSize:11,color:"#5A7499",marginTop:4}}>{s.city} · ⭐ {s.rating?.toFixed(1) || "0.0"}</div>
            </div>
          ))}
          <button onClick={()=>router.push("/food/suppliers")} style={{width:"100%",padding:"8px",background:"none",border:"1px solid #D6E4FA",borderRadius:8,fontSize:12,color:"#4A7FD4",fontWeight:600,cursor:"pointer",fontFamily:"inherit"}}>Tüm Tedarikçiler →</button>
        </div>
      </div>
    </main>
  );
}
