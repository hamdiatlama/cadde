"use client";
import { useRouter, useParams } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function RestaurantPage() {
  const { restaurantId } = useParams();
  const router = useRouter();
  const [rest, setRest] = useState<any>(null);
  const [menu, setMenu] = useState<any[]>([]);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [trace, setTrace] = useState<any>(null);
  const [tab, setTab] = useState("menu");

  useEffect(() => {
    async function load() {
      try {
        const [menuR, supR] = await Promise.all([
          fetch(`${API}/food/menu/${restaurantId}`).then(r => r.json()),
          fetch(`${API}/food/restaurants/${restaurantId}/suppliers`).then(r => r.json()),
        ]);
        if (restaurantId) {
          setRest({ id: restaurantId, name: "Adana Kebap Evi" });
        }
        setMenu(Array.isArray(menuR) ? menuR : menuR?.value || []);
        setSuppliers(Array.isArray(supR) ? supR : supR?.value || []);
      } catch (_) {}
    }
    load();
  }, [restaurantId]);

  async function showTrace(itemId: number) {
    try {
      const r = await fetch(`${API}/food/trace/${itemId}`);
      setTrace(await r.json());
      setTab("trace");
    } catch (_) {}
  }

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 32px"}}>
        <span onClick={()=>router.push("/food")} style={{cursor:"pointer",fontSize:13,color:"#5A7499",fontWeight:500}}>← Restoranlar</span>
      </nav>

      <div style={{padding:"24px 32px",maxWidth:720,margin:"0 auto"}}>
        <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:20,marginBottom:20}}>
          <h1 style={{fontSize:22,fontWeight:700}}>{rest?.name || "Restoran"}</h1>
          <div style={{display:"flex",gap:8,marginTop:12}}>
            <button onClick={()=>setTab("menu")} style={{padding:"6px 14px",background:tab==="menu"?"#4A7FD4":"#fff",color:tab==="menu"?"#fff":"#5A7499",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,cursor:"pointer",fontFamily:"inherit",fontWeight:500}}>Menü</button>
            <button onClick={()=>setTab("suppliers")} style={{padding:"6px 14px",background:tab==="suppliers"?"#4A7FD4":"#fff",color:tab==="suppliers"?"#fff":"#5A7499",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,cursor:"pointer",fontFamily:"inherit",fontWeight:500}}>Tedarikçiler</button>
            <button onClick={()=>setTab("trace")} style={{padding:"6px 14px",background:tab==="trace"?"#4A7FD4":"#fff",color:tab==="trace"?"#fff":"#5A7499",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,cursor:"pointer",fontFamily:"inherit",fontWeight:500}}>İzlenebilirlik</button>
          </div>
        </div>

        {tab === "menu" && (
          <div>
            <h2 style={{fontSize:16,fontWeight:600,marginBottom:12}}>📋 Menü</h2>
            {menu.length === 0 ? <p style={{color:"#8FAAC8",fontSize:13}}>Menü öğesi bulunamadı</p> : menu.map((item: any) => (
              <div key={item.id} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:14,marginBottom:10}}>
                <div style={{display:"flex",justifyContent:"space-between"}}>
                  <div>
                    <div style={{fontSize:14,fontWeight:600}}>{item.name}</div>
                    <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>{item.category}</div>
                  </div>
                  <div style={{textAlign:"right"}}>
                    <div style={{fontSize:16,fontWeight:700,color:"#4A7FD4"}}>₺{item.price}</div>
                    <button onClick={()=>showTrace(item.id)} style={{marginTop:4,fontSize:11,color:"#4A7FD4",background:"none",border:"none",cursor:"pointer",fontFamily:"inherit",textDecoration:"underline"}}>İçindekiler</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {tab === "suppliers" && (
          <div>
            <h2 style={{fontSize:16,fontWeight:600,marginBottom:12}}>Tedarikçiler</h2>
            {suppliers.length === 0 ? <p style={{color:"#8FAAC8",fontSize:13}}>Henüz tedarikçi bağlı değil</p> : suppliers.map((s: any) => (
              <div key={s.id} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:14,marginBottom:10}}>
                <div style={{fontSize:14,fontWeight:600}}>{s.supplier_name}</div>
                <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>{s.is_preferred ? "⭐ Tercih Edilen" : "Tedarikçi"}</div>
              </div>
            ))}
          </div>
        )}

        {tab === "trace" && trace && (
          <div>
            <h2 style={{fontSize:16,fontWeight:600,marginBottom:12}}>🔍 İzlenebilirlik: {trace.menu_item_name}</h2>
            {trace.ingredients?.length > 0 ? trace.ingredients.map((ing: any) => (
              <div key={ing.id} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:14,marginBottom:10}}>
                <div style={{display:"flex",justifyContent:"space-between"}}>
                  <div>
                    <div style={{fontSize:14,fontWeight:600}}>{ing.product_name}</div>
                    <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>Tedarikçi: {ing.supplier_name}</div>
                  </div>
                  <div style={{textAlign:"right",fontSize:13,color:"#5A7499"}}>
                    {ing.quantity} {ing.unit}
                  </div>
                </div>
              </div>
            )) : <p style={{color:"#8FAAC8",fontSize:13}}>Bu menü öğesi için içerik bilgisi yok</p>}
          </div>
        )}
      </div>
    </main>
  );
}
