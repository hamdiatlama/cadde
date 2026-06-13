"use client";
import { useState } from "react";

export default function Login() {
  const [tab, setTab] = useState<"login" | "register">("login");
  const [accountType, setAccountType] = useState("bireysel");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [registerData, setRegisterData] = useState({ full_name: "", email: "", phone: "", password: "", role: "customer" });

  async function handleLogin() {
    setLoading(true); setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Giriş başarısız");
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch (e: any) { setError(e.message); }
    setLoading(false);
  }

  async function handleRegister() {
    setLoading(true); setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...registerData, role: accountType === "bireysel" ? "customer" : accountType === "isletme" ? "seller" : "admin" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Kayıt başarısız");
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch (e: any) { setError(e.message); }
    setLoading(false);
  }

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",display:"flex",alignItems:"center",justifyContent:"center",padding:16}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",maxWidth:900,width:"100%",background:"#fff",borderRadius:12,border:"1px solid #D6E4FA",overflow:"hidden",boxShadow:"0 4px 24px rgba(74,127,212,0.08)"}}>

        {/* SOL */}
        <div style={{background:"#4A7FD4",padding:"48px 40px",display:"flex",flexDirection:"column",justifyContent:"space-between"}}>
          <div style={{display:"flex",alignItems:"center",gap:8}}>
            <div style={{width:28,height:28,background:"rgba(255,255,255,0.2)",borderRadius:7,display:"flex",alignItems:"center",justifyContent:"center"}}>
              <span style={{color:"#fff",fontSize:14,fontWeight:700}}>C</span>
            </div>
            <span style={{fontSize:18,fontWeight:700,color:"#fff"}}>cadde</span>
          </div>
          <div style={{flex:1,display:"flex",flexDirection:"column",justifyContent:"center",padding:"32px 0"}}>
            <h2 style={{fontSize:28,fontWeight:700,color:"#fff",lineHeight:1.2,letterSpacing:-1,marginBottom:12}}>
              Hayatında ne<br/>lazımsa,<br/>burada.
            </h2>
            <p style={{fontSize:14,color:"rgba(255,255,255,0.75)",lineHeight:1.6}}>
              Usta, market, taksi, otel, çiftçi — hepsi tek platformda, yakınında.
            </p>
            <div style={{display:"flex",gap:20,marginTop:32}}>
              {[{n:"24K",l:"Aktif üye"},{n:"6K+",l:"İşletme"},{n:"81",l:"İl"}].map(s=>(
                <div key={s.l}>
                  <div style={{fontSize:20,fontWeight:700,color:"#fff"}}>{s.n}</div>
                  <div style={{fontSize:11,color:"rgba(255,255,255,0.6)",marginTop:2}}>{s.l}</div>
                </div>
              ))}
            </div>
          </div>
          <div style={{fontSize:11,color:"rgba(255,255,255,0.4)"}}>© 2025 Cadde. Tüm hakları saklıdır.</div>
        </div>

        {/* SAĞ */}
        <div style={{padding:"48px 40px",display:"flex",flexDirection:"column",justifyContent:"center"}}>

          {/* TABS */}
          <div style={{display:"flex",background:"#EEF4FF",borderRadius:8,padding:4,marginBottom:28}}>
            {(["login","register"] as const).map((t,i)=>(
              <div key={t} onClick={()=>{setTab(t);setError("");}} style={{flex:1,padding:8,textAlign:"center",fontSize:13,fontWeight:600,cursor:"pointer",borderRadius:6,transition:"all .15s",background:tab===t?"#fff":"transparent",color:tab===t?"#1A2B4A":"#8FAAC8",boxShadow:tab===t?"0 1px 4px rgba(74,127,212,0.12)":"none"}}>
                {i===0?"Giriş Yap":"Üye Ol"}
              </div>
            ))}
          </div>

          {error && (
            <div style={{background:"#FEF2F2",border:"1px solid #FECACA",borderRadius:6,padding:"10px 14px",fontSize:13,color:"#DC2626",marginBottom:16}}>
              {error}
            </div>
          )}

          {tab === "login" ? (
            <div>
              <div style={{marginBottom:14}}>
                <label style={{fontSize:11,fontWeight:600,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,display:"block",marginBottom:6}}>E-posta</label>
                <div style={{display:"flex",alignItems:"center",background:"#f8faff",border:"1px solid #D6E4FA",borderRadius:6,overflow:"hidden"}}>
                  <i className="ti ti-mail" style={{padding:"0 12px",color:"#8FAAC8",fontSize:17}}/>
                  <input type="email" placeholder="ornek@email.com" value={loginData.email} onChange={e=>setLoginData({...loginData,email:e.target.value})} style={{flex:1,border:"none",outline:"none",background:"transparent",fontFamily:"inherit",fontSize:14,color:"#1A2B4A",padding:"11px 12px 11px 0"}}/>
                </div>
              </div>
              <div style={{marginBottom:8}}>
                <label style={{fontSize:11,fontWeight:600,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,display:"block",marginBottom:6}}>Şifre</label>
                <div style={{display:"flex",alignItems:"center",background:"#f8faff",border:"1px solid #D6E4FA",borderRadius:6,overflow:"hidden"}}>
                  <i className="ti ti-lock" style={{padding:"0 12px",color:"#8FAAC8",fontSize:17}}/>
                  <input type="password" placeholder="••••••••" value={loginData.password} onChange={e=>setLoginData({...loginData,password:e.target.value})} style={{flex:1,border:"none",outline:"none",background:"transparent",fontFamily:"inherit",fontSize:14,color:"#1A2B4A",padding:"11px 12px 11px 0"}}/>
                </div>
              </div>
              <div style={{textAlign:"right",marginBottom:16}}>
                <span style={{fontSize:12,color:"#4A7FD4",cursor:"pointer",fontWeight:600}}>Şifremi unuttum</span>
              </div>
              <button onClick={handleLogin} disabled={loading} style={{width:"100%",padding:13,background:"#4A7FD4",color:"#fff",border:"none",borderRadius:6,fontFamily:"inherit",fontSize:14,fontWeight:700,cursor:"pointer"}}>
                {loading ? "Giriş yapılıyor..." : "Giriş Yap"}
              </button>
              <div style={{display:"flex",alignItems:"center",gap:10,margin:"16px 0"}}>
                <div style={{flex:1,height:1,background:"#D6E4FA"}}/>
                <span style={{fontSize:11,color:"#8FAAC8",fontWeight:500}}>veya</span>
                <div style={{flex:1,height:1,background:"#D6E4FA"}}/>
              </div>
              <button style={{width:"100%",padding:10,border:"1px solid #D6E4FA",borderRadius:6,fontFamily:"inherit",fontSize:13,fontWeight:500,color:"#5A7499",background:"#fff",cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>
                <i className="ti ti-brand-google" style={{fontSize:16,color:"#EA4335"}}/> Google ile devam et
              </button>
              <div style={{textAlign:"center",fontSize:12,color:"#8FAAC8",marginTop:16}}>
                Hesabın yok mu? <span onClick={()=>setTab("register")} style={{color:"#4A7FD4",fontWeight:600,cursor:"pointer"}}>Üye ol</span>
              </div>
            </div>
          ) : (
            <div>
              <div style={{marginBottom:14}}>
                <label style={{fontSize:11,fontWeight:600,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,display:"block",marginBottom:6}}>Hesap türü</label>
                <div style={{display:"flex",gap:6}}>
                  {[{k:"bireysel",i:"ti-user",l:"Bireysel"},{k:"isletme",i:"ti-building-store",l:"İşletme"},{k:"kurum",i:"ti-building",l:"Kurum"}].map(t=>(
                    <button key={t.k} onClick={()=>setAccountType(t.k)} style={{flex:1,padding:9,border:`1px solid ${accountType===t.k?"#4A7FD4":"#D6E4FA"}`,borderRadius:6,fontFamily:"inherit",fontSize:12,fontWeight:600,color:accountType===t.k?"#4A7FD4":"#5A7499",background:accountType===t.k?"#EEF4FF":"#f8faff",cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",gap:6}}>
                      <i className={`ti ${t.i}`} style={{fontSize:15}}/>{t.l}
                    </button>
                  ))}
                </div>
              </div>
              {[
                {label:"Ad Soyad",icon:"ti-user",key:"full_name",type:"text",placeholder:"Adınız Soyadınız"},
                {label:"E-posta",icon:"ti-mail",key:"email",type:"email",placeholder:"ornek@email.com"},
                {label:"Telefon",icon:"ti-phone",key:"phone",type:"tel",placeholder:"0500 000 00 00"},
                {label:"Şifre",icon:"ti-lock",key:"password",type:"password",placeholder:"••••••••"},
              ].map(f=>(
                <div key={f.key} style={{marginBottom:12}}>
                  <label style={{fontSize:11,fontWeight:600,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,display:"block",marginBottom:6}}>{f.label}</label>
                  <div style={{display:"flex",alignItems:"center",background:"#f8faff",border:"1px solid #D6E4FA",borderRadius:6,overflow:"hidden"}}>
                    <i className={`ti ${f.icon}`} style={{padding:"0 12px",color:"#8FAAC8",fontSize:17}}/>
                    <input type={f.type} placeholder={f.placeholder} value={(registerData as any)[f.key]} onChange={e=>setRegisterData({...registerData,[f.key]:e.target.value})} style={{flex:1,border:"none",outline:"none",background:"transparent",fontFamily:"inherit",fontSize:14,color:"#1A2B4A",padding:"11px 12px 11px 0"}}/>
                  </div>
                </div>
              ))}
              <button onClick={handleRegister} disabled={loading} style={{width:"100%",padding:13,background:"#4A7FD4",color:"#fff",border:"none",borderRadius:6,fontFamily:"inherit",fontSize:14,fontWeight:700,cursor:"pointer",marginTop:4}}>
                {loading ? "Kayıt yapılıyor..." : "Üye Ol"}
              </button>
              <div style={{textAlign:"center",fontSize:12,color:"#8FAAC8",marginTop:16}}>
                Zaten hesabın var mı? <span onClick={()=>setTab("login")} style={{color:"#4A7FD4",fontWeight:600,cursor:"pointer"}}>Giriş yap</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
