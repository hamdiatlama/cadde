"use client";
import { useState } from "react";

const MOCK_DEVICES = [
  { id:1, hotelId:1, deviceType:"thermostat", deviceName:"Oda 101 Termostat", roomNumber:"101", manufacturer:"Nest", model:"T3000ES", serialNumber:"SN-T-001", status:"online", firmwareVersion:"6.2.0", isActive:true },
  { id:2, hotelId:1, deviceType:"smart_lock", deviceName:"Oda 101 Kilit", roomNumber:"101", manufacturer:"Yale", model:"YRD256", serialNumber:"SN-L-001", status:"online", firmwareVersion:"3.1.5", isActive:true },
  { id:3, hotelId:1, deviceType:"light", deviceName:"Oda 101 Tavan", roomNumber:"101", manufacturer:"Philips", model:"Hue White", serialNumber:"SN-LG-001", status:"online", firmwareVersion:"2.8.0", isActive:true },
  { id:4, hotelId:1, deviceType:"sensor", deviceName:"Oda 101 Hareket", roomNumber:"101", manufacturer:"Aqara", model:"RTCGQ11LM", serialNumber:"SN-S-001", status:"offline", firmwareVersion:"1.5.2", isActive:true },
  { id:5, hotelId:1, deviceType:"thermostat", deviceName:"Oda 102 Termostat", roomNumber:"102", manufacturer:"Nest", model:"T3000ES", serialNumber:"SN-T-002", status:"error", firmwareVersion:"6.2.0", isActive:true },
  { id:6, hotelId:1, deviceType:"smart_lock", deviceName:"Oda 102 Kilit", roomNumber:"102", manufacturer:"Yale", model:"YRD256", serialNumber:"SN-L-002", status:"online", firmwareVersion:"3.1.5", isActive:true },
  { id:7, hotelId:1, deviceType:"curtain", deviceName:"Oda 102 Perde", roomNumber:"102", manufacturer:"Somfy", model:"WT", serialNumber:"SN-C-001", status:"offline", firmwareVersion:"4.0.1", isActive:false },
  { id:8, hotelId:1, deviceType:"tv", deviceName:"Oda 101 TV", roomNumber:"101", manufacturer:"Samsung", model:"UE43TU8000", serialNumber:"SN-TV-001", status:"online", firmwareVersion:"T-MSMDEUC", isActive:true },
];

const MOCK_RULES = [
  { id:1, hotelId:1, name:"Check-in Konfor", triggerEvent:"checkin", conditions:{}, actions:[{deviceId:1,commandType:"set_temperature",commandValue:"22"},{deviceId:2,commandType:"unlock",commandValue:"unlock"},{deviceId:3,commandType:"light_on",commandValue:"on"}], isActive:true },
  { id:2, hotelId:1, name:"Check-out Enerji Tasarruf", triggerEvent:"checkout", conditions:{}, actions:[{deviceId:1,commandType:"set_temperature",commandValue:"18"},{deviceId:2,commandType:"lock",commandValue:"lock"},{deviceId:3,commandType:"light_off",commandValue:"off"}], isActive:true },
  { id:3, hotelId:1, name:"Sıcaklık > 30 Alarm", triggerEvent:"temperature", conditions:{maxTemp:30}, actions:[{deviceId:1,commandType:"set_temperature",commandValue:"24"}], isActive:false },
];

const MOCK_ENV = [
  { id:1, hotelId:1, roomNumber:"101", temperature:22.5, humidity:45, lightLevel:320, noiseLevel:35, occupancyDetected:true, loggedAt:"2026-06-15T10:30:00Z" },
  { id:2, hotelId:1, roomNumber:"102", temperature:24.1, humidity:50, lightLevel:180, noiseLevel:42, occupancyDetected:false, loggedAt:"2026-06-15T10:25:00Z" },
  { id:3, hotelId:1, roomNumber:"101", temperature:21.8, humidity:47, lightLevel:280, noiseLevel:38, occupancyDetected:true, loggedAt:"2026-06-15T09:30:00Z" },
];

const iconMap: Record<string,string> = {
  thermostat:"ti-temperature", smart_lock:"ti-lock", light:"ti-lamp", curtain:"ti-curtain", tv:"ti-device-tv", speaker:"ti-speaker", sensor:"ti-wifi",
};

export default function IotManagerPage() {
  const [tab, setTab] = useState("devices");
  const [devices, setDevices] = useState(MOCK_DEVICES);
  const [rules, setRules] = useState(MOCK_RULES);
  const [showDeviceForm, setShowDeviceForm] = useState(false);
  const [showRuleForm, setShowRuleForm] = useState(false);
  const [showCommand, setShowCommand] = useState<number|null>(null);
  const [formDevice, setFormDevice] = useState({deviceType:"thermostat", deviceName:"", roomNumber:"", manufacturer:"", model:"", serialNumber:""});
  const [formRule, setFormRule] = useState({name:"", triggerEvent:"checkin", actions:"", isActive:true});
  const [commandType, setCommandType] = useState("set_temperature");
  const [commandValue, setCommandValue] = useState("");

  const statusBadge = (s: string) => {
    const m: Record<string,{bg:string,cl:string}> = {online:{bg:"#D1FAE5",cl:"#10B981"},offline:{bg:"#FEE2E2",cl:"#EF4444"},error:{bg:"#FEF3C7",cl:"#F59E0B"}};
    const st = m[s]||{bg:"#F3F4F6",cl:"#6B7280"};
    return {background:st.bg,color:st.cl,fontSize:11,fontWeight:600,padding:"3px 10px",borderRadius:20,textTransform:"capitalize" as const};
  };

  const typeIcon = (t: string) => iconMap[t]||"ti-device-unknown";

  const addDevice = () => {
    setDevices(prev => [...prev, { id:Math.max(...prev.map(d=>d.id),0)+1, hotelId:1, ...formDevice, status:"offline", firmwareVersion:"1.0.0", isActive:true }]);
    setShowDeviceForm(false);
    setFormDevice({deviceType:"thermostat", deviceName:"", roomNumber:"", manufacturer:"", model:"", serialNumber:""});
  };

  const saveRule = () => {
    const actionList = formRule.actions.split(",").map(a => {
      const parts = a.trim().split(":");
      return parts.length===2 ? {commandType:parts[0],commandValue:parts[1]} : null;
    }).filter((a): a is {commandType:string;commandValue:string} => a !== null);
    const newActions = actionList.map(a => ({deviceId:1, commandType:a.commandType, commandValue:a.commandValue}));
    setRules((prev:any[]) => [...prev, { id:Math.max(...prev.map(r=>r.id),0)+1, hotelId:1, name:formRule.name, triggerEvent:formRule.triggerEvent, conditions:{maxTemp:24}, actions:newActions, isActive:formRule.isActive }]);
    setShowRuleForm(false);
    setFormRule({name:"", triggerEvent:"checkin", actions:"", isActive:true});
  };

  const toggleRule = (id: number) => {
    setRules(prev => prev.map(r => r.id===id ? {...r, isActive:!r.isActive} : r));
  };

  const sendCmd = (deviceId: number) => {
    setDevices(prev => prev.map(d => d.id===deviceId ? {...d, status: commandType==="lock"||commandType==="light_off"?"offline":"online"} : d));
    setShowCommand(null);
    setCommandType("set_temperature");
    setCommandValue("");
  };

  const onlineCount = devices.filter(d=>d.status==="online").length;
  const offlineCount = devices.filter(d=>d.status==="offline").length;
  const errorCount = devices.filter(d=>d.status==="error").length;

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>
      <div style={{maxWidth:1200,margin:"0 auto",padding:"24px 32px"}}>
        <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:24}}>
          <i className="ti ti-devices" style={{fontSize:24,color:"#4A7FD4"}}/>
          <h1 style={{fontSize:22,fontWeight:700,letterSpacing:-0.5}}>IoT & Akıllı Oda Yönetimi</h1>
        </div>

        {/* DASHBOARD */}
        <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12,marginBottom:24}}>
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:"16px 20px",display:"flex",alignItems:"center",gap:12}}>
            <div style={{width:40,height:40,borderRadius:8,background:"#DBEAFE",display:"flex",alignItems:"center",justifyContent:"center"}}>
              <i className="ti ti-devices" style={{fontSize:20,color:"#3B82F6"}}/>
            </div>
            <div>
              <div style={{fontSize:11,color:"#8FAAC8",fontWeight:500}}>Toplam Cihaz</div>
              <div style={{fontSize:22,fontWeight:700}}>{devices.length}</div>
            </div>
          </div>
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:"16px 20px",display:"flex",alignItems:"center",gap:12}}>
            <div style={{width:40,height:40,borderRadius:8,background:"#D1FAE5",display:"flex",alignItems:"center",justifyContent:"center"}}>
              <i className="ti ti-circle-check" style={{fontSize:20,color:"#10B981"}}/>
            </div>
            <div>
              <div style={{fontSize:11,color:"#8FAAC8",fontWeight:500}}>Online</div>
              <div style={{fontSize:22,fontWeight:700}}>{onlineCount}</div>
            </div>
          </div>
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:"16px 20px",display:"flex",alignItems:"center",gap:12}}>
            <div style={{width:40,height:40,borderRadius:8,background:"#FEE2E2",display:"flex",alignItems:"center",justifyContent:"center"}}>
              <i className="ti ti-circle-x" style={{fontSize:20,color:"#EF4444"}}/>
            </div>
            <div>
              <div style={{fontSize:11,color:"#8FAAC8",fontWeight:500}}>Offline</div>
              <div style={{fontSize:22,fontWeight:700}}>{offlineCount}</div>
            </div>
          </div>
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:"16px 20px",display:"flex",alignItems:"center",gap:12}}>
            <div style={{width:40,height:40,borderRadius:8,background:"#FEF3C7",display:"flex",alignItems:"center",justifyContent:"center"}}>
              <i className="ti ti-alert-triangle" style={{fontSize:20,color:"#F59E0B"}}/>
            </div>
            <div>
              <div style={{fontSize:11,color:"#8FAAC8",fontWeight:500}}>Hata</div>
              <div style={{fontSize:22,fontWeight:700}}>{errorCount}</div>
            </div>
          </div>
        </div>

        {/* TABS */}
        <div style={{display:"flex",gap:4,marginBottom:24,background:"#fff",borderRadius:8,padding:4,border:"1px solid #D6E4FA",width:"fit-content"}}>
          {[
            {key:"devices",icon:"ti-devices",label:"Cihazlar"},
            {key:"commands",icon:"ti-send",label:"Komutlar"},
            {key:"rules",icon:"ti-automation",label:"Kurallar"},
            {key:"environment",icon:"ti-temperature",label:"Çevre"},
          ].map(t=>(
            <button key={t.key} onClick={()=>setTab(t.key)} style={{display:"flex",alignItems:"center",gap:6,padding:"8px 16px",borderRadius:6,border:"none",background:tab===t.key?"#4A7FD4":"transparent",color:tab===t.key?"#fff":"#5A7499",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer",transition:"all .15s"}}>
              <i className={`ti ${t.icon}`} style={{fontSize:16}}/>
              {t.label}
            </button>
          ))}
        </div>

        {/* TAB: DEVICES */}
        {tab==="devices" && (
          <>
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
                <span style={{fontSize:14,fontWeight:600}}>Cihaz Envanteri</span>
                <button onClick={()=>setShowDeviceForm(true)} style={{display:"flex",alignItems:"center",gap:4,padding:"6px 14px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                  <i className="ti ti-plus" style={{fontSize:14}}/> Cihaz Ekle
                </button>
              </div>
              {devices.map(d=>(
                <div key={d.id} style={{display:"flex",alignItems:"center",gap:12,padding:"12px 20px",borderBottom:"1px solid #EEF4FF",transition:"background .15s"}} className="hover-row">
                  <div style={{width:36,height:36,borderRadius:8,background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                    <i className={`ti ${typeIcon(d.deviceType)}`} style={{fontSize:18,color:"#4A7FD4"}}/>
                  </div>
                  <div style={{flex:1,minWidth:0}}>
                    <div style={{display:"flex",alignItems:"center",gap:8}}>
                      <span style={{fontSize:13,fontWeight:600}}>{d.deviceName}</span>
                      <span style={{fontSize:10,color:"#8FAAC8",background:"#EEF4FF",padding:"2px 6px",borderRadius:4,textTransform:"uppercase",fontWeight:600}}>{d.deviceType}</span>
                    </div>
                    <div style={{fontSize:11,color:"#8FAAC8",marginTop:1}}>Oda {d.roomNumber} · {d.manufacturer} {d.model} · SN: {d.serialNumber}</div>
                  </div>
                  <span style={statusBadge(d.status)}>{d.status}</span>
                  <button onClick={()=>setShowCommand(showCommand===d.id?null:d.id)} style={{display:"flex",alignItems:"center",gap:4,padding:"6px 10px",borderRadius:6,border:"1px solid #D6E4FA",background:"transparent",color:"#4A7FD4",fontFamily:"inherit",fontSize:12,cursor:"pointer"}}>
                    <i className="ti ti-send" style={{fontSize:14}}/>
                  </button>
                  {showCommand===d.id && (
                    <div style={{position:"absolute",right:20,marginTop:120,background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:12,boxShadow:"0 4px 12px rgba(0,0,0,0.08)",zIndex:10,minWidth:200}}>
                      <div style={{fontSize:12,fontWeight:600,marginBottom:8}}>{d.deviceName} - Komut Gönder</div>
                      <select value={commandType} onChange={e=>setCommandType(e.target.value)} style={{width:"100%",padding:"6px 8px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:12,fontFamily:"inherit",marginBottom:6,background:"#fff"}}>
                        <option value="set_temperature">Sıcaklık Ayarı</option>
                        <option value="lock">Kilitle</option>
                        <option value="unlock">Kilit Aç</option>
                        <option value="light_on">Işık Aç</option>
                        <option value="light_off">Işık Kapa</option>
                        <option value="curtain_open">Perde Aç</option>
                        <option value="curtain_close">Perde Kapa</option>
                        <option value="tv_on">TV Aç</option>
                        <option value="tv_off">TV Kapa</option>
                      </select>
                      {commandType==="set_temperature" && (
                        <input type="text" value={commandValue} onChange={e=>setCommandValue(e.target.value)} placeholder="örn: 22" style={{width:"100%",padding:"6px 8px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:12,fontFamily:"inherit",marginBottom:6,background:"#fff"}} />
                      )}
                      <div style={{display:"flex",gap:4}}>
                        <button onClick={()=>setShowCommand(null)} style={{flex:1,padding:"6px",border:"1px solid #D6E4FA",borderRadius:6,background:"transparent",color:"#8FAAC8",fontFamily:"inherit",fontSize:11,cursor:"pointer"}}>İptal</button>
                        <button onClick={()=>sendCmd(d.id)} style={{flex:1,padding:"6px",border:"none",borderRadius:6,background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:11,fontWeight:600,cursor:"pointer"}}>Gönder</button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {showDeviceForm && (
              <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.4)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:50}} onClick={()=>setShowDeviceForm(false)}>
                <div style={{background:"#fff",borderRadius:12,padding:24,width:"100%",maxWidth:420,margin:16}} onClick={e=>e.stopPropagation()}>
                  <h3 style={{fontSize:16,fontWeight:700,marginBottom:16}}>Yeni Cihaz Kaydet</h3>
                  <div style={{display:"grid",gap:10}}>
                    <div>
                      <label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Cihaz Türü</label>
                      <select value={formDevice.deviceType} onChange={e=>setFormDevice({...formDevice,deviceType:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4,background:"#fff"}}>
                        <option value="thermostat">Termostat</option>
                        <option value="smart_lock">Akıllı Kilit</option>
                        <option value="light">Işık</option>
                        <option value="curtain">Perde</option>
                        <option value="tv">TV</option>
                        <option value="speaker">Hoparlör</option>
                        <option value="sensor">Sensör</option>
                      </select>
                    </div>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Cihaz Adı</label><input value={formDevice.deviceName} onChange={e=>setFormDevice({...formDevice,deviceName:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Oda No</label><input value={formDevice.roomNumber} onChange={e=>setFormDevice({...formDevice,roomNumber:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
                      <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Marka</label><input value={formDevice.manufacturer} onChange={e=>setFormDevice({...formDevice,manufacturer:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                      <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Model</label><input value={formDevice.model} onChange={e=>setFormDevice({...formDevice,model:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                    </div>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Seri No</label><input value={formDevice.serialNumber} onChange={e=>setFormDevice({...formDevice,serialNumber:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                  </div>
                  <div style={{display:"flex",gap:8,marginTop:16}}>
                    <button onClick={()=>setShowDeviceForm(false)} style={{flex:1,padding:"8px",borderRadius:8,border:"1px solid #D6E4FA",background:"transparent",color:"#5A7499",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer"}}>İptal</button>
                    <button onClick={addDevice} style={{flex:1,padding:"8px",borderRadius:8,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer"}}>Kaydet</button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* TAB: COMMANDS */}
        {tab==="commands" && (
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",gap:8}}>
              <i className="ti ti-send" style={{fontSize:16,color:"#4A7FD4"}}/>
              <span style={{fontSize:14,fontWeight:600}}>Komut Geçmişi</span>
            </div>
            {devices.slice(0,6).map(d=>(
              <div key={d.id} style={{display:"flex",alignItems:"center",gap:12,padding:"12px 20px",borderBottom:"1px solid #EEF4FF"}}>
                <div style={{width:32,height:32,borderRadius:8,background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                  <i className={`ti ${typeIcon(d.deviceType)}`} style={{fontSize:16,color:"#4A7FD4"}}/>
                </div>
                <div style={{flex:1}}>
                  <div style={{fontSize:13,fontWeight:600}}>{d.deviceName}</div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>Oda {d.roomNumber} · {d.deviceType}</div>
                </div>
                <div style={{display:"flex",gap:6}}>
                  <button onClick={()=>{setCommandType("lock"); setCommandValue(""); sendCmd(d.id)}} style={{padding:"5px 10px",borderRadius:6,border:"1px solid #D6E4FA",background:"transparent",color:"#1A2B4A",fontFamily:"inherit",fontSize:11,cursor:"pointer"}}>
                    <i className="ti ti-lock" style={{fontSize:12,marginRight:3}}/> Kilitle
                  </button>
                  <button onClick={()=>{setCommandType("unlock"); setCommandValue(""); sendCmd(d.id)}} style={{padding:"5px 10px",borderRadius:6,border:"1px solid #D6E4FA",background:"transparent",color:"#1A2B4A",fontFamily:"inherit",fontSize:11,cursor:"pointer"}}>
                    <i className="ti ti-lock-open" style={{fontSize:12,marginRight:3}}/> Aç
                  </button>
                  <select onChange={e=>e.target.value&&(()=>{setCommandType(e.target.value); setCommandValue(e.target.value==="light_on"?"on":e.target.value==="light_off"?"off":""); sendCmd(d.id)})()} style={{padding:"5px 8px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:11,fontFamily:"inherit",background:"#fff",cursor:"pointer"}}>
                    <option value="">Işık</option>
                    <option value="light_on">Aç</option>
                    <option value="light_off">Kapa</option>
                  </select>
                </div>
                <span style={statusBadge(d.status)}>{d.status}</span>
              </div>
            ))}
          </div>
        )}

        {/* TAB: RULES */}
        {tab==="rules" && (
          <>
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
                <div style={{display:"flex",alignItems:"center",gap:8}}>
                  <i className="ti ti-automation" style={{fontSize:16,color:"#4A7FD4"}}/>
                  <span style={{fontSize:14,fontWeight:600}}>Otomasyon Kuralları</span>
                </div>
                <button onClick={()=>setShowRuleForm(true)} style={{display:"flex",alignItems:"center",gap:4,padding:"6px 14px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                  <i className="ti ti-plus" style={{fontSize:14}}/> Kural Ekle
                </button>
              </div>
              {rules.map(r=>(
                <div key={r.id} style={{display:"flex",alignItems:"center",gap:12,padding:"14px 20px",borderBottom:"1px solid #EEF4FF"}}>
                  <div style={{width:36,height:36,borderRadius:8,background:r.isActive?"#D1FAE5":"#F3F4F6",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                    <i className="ti ti-automation" style={{fontSize:18,color:r.isActive?"#10B981":"#9CA3AF"}}/>
                  </div>
                  <div style={{flex:1}}>
                    <div style={{fontSize:13,fontWeight:600}}>{r.name}</div>
                    <div style={{fontSize:11,color:"#8FAAC8",marginTop:1}}>
                      Tetikleyici: {r.triggerEvent} · {r.actions.length} aksiyon
                    </div>
                    <div style={{display:"flex",gap:4,marginTop:4}}>
                      {r.actions.map((a:any,i:number)=>(
                        <span key={i} style={{fontSize:10,background:"#EEF4FF",color:"#4A7FD4",padding:"2px 6px",borderRadius:4,fontWeight:500}}>{a.commandType}</span>
                      ))}
                    </div>
                  </div>
                  <button onClick={()=>toggleRule(r.id)} style={{padding:"6px 12px",borderRadius:6,border:"none",background:r.isActive?"#10B981":"#9CA3AF",color:"#fff",fontFamily:"inherit",fontSize:11,fontWeight:600,cursor:"pointer"}}>
                    {r.isActive ? "Aktif" : "Pasif"}
                  </button>
                </div>
              ))}
            </div>

            {showRuleForm && (
              <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.4)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:50}} onClick={()=>setShowRuleForm(false)}>
                <div style={{background:"#fff",borderRadius:12,padding:24,width:"100%",maxWidth:420,margin:16}} onClick={e=>e.stopPropagation()}>
                  <h3 style={{fontSize:16,fontWeight:700,marginBottom:16}}>Yeni Otomasyon Kuralı</h3>
                  <div style={{display:"grid",gap:10}}>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Kural Adı</label><input value={formRule.name} onChange={e=>setFormRule({...formRule,name:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/></div>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Tetikleyici</label>
                      <select value={formRule.triggerEvent} onChange={e=>setFormRule({...formRule,triggerEvent:e.target.value})} style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4,background:"#fff"}}>
                        <option value="checkin">Check-in</option>
                        <option value="checkout">Check-out</option>
                        <option value="time_schedule">Zamanlama</option>
                        <option value="occupancy">Doluluk</option>
                        <option value="temperature">Sıcaklık</option>
                      </select>
                    </div>
                    <div><label style={{fontSize:11,fontWeight:600,color:"#5A7499"}}>Aksiyonlar (virgülle ayır: command_type:value)</label>
                      <input value={formRule.actions} onChange={e=>setFormRule({...formRule,actions:e.target.value})} placeholder="set_temperature:22, unlock:unlock, light_on:on" style={{width:"100%",padding:"8px 10px",border:"1px solid #D6E4FA",borderRadius:6,fontSize:13,fontFamily:"inherit",marginTop:4}}/>
                    </div>
                  </div>
                  <div style={{display:"flex",gap:8,marginTop:16}}>
                    <button onClick={()=>setShowRuleForm(false)} style={{flex:1,padding:"8px",borderRadius:8,border:"1px solid #D6E4FA",background:"transparent",color:"#5A7499",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer"}}>İptal</button>
                    <button onClick={saveRule} style={{flex:1,padding:"8px",borderRadius:8,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer"}}>Kaydet</button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* TAB: ENVIRONMENT */}
        {tab==="environment" && (
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",gap:8}}>
              <i className="ti ti-temperature" style={{fontSize:16,color:"#4A7FD4"}}/>
              <span style={{fontSize:14,fontWeight:600}}>Oda Çevre Verileri</span>
            </div>
            <div style={{overflowX:"auto"}}>
              <table style={{width:"100%",borderCollapse:"collapse"}}>
                <thead>
                  <tr style={{background:"#F8FAFF",borderBottom:"1px solid #D6E4FA"}}>
                    {["Oda","Sıcaklık","Nem","Işık","Ses","Durum","Zaman"].map(h=>(
                      <th key={h} style={{textAlign:"left",padding:"10px 16px",fontSize:12,fontWeight:600,color:"#5A7499"}}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {MOCK_ENV.map(e=>(
                    <tr key={e.id} style={{borderBottom:"1px solid #EEF4FF"}}>
                      <td style={{padding:"12px 16px",fontSize:13,fontWeight:600}}>Oda {e.roomNumber}</td>
                      <td style={{padding:"12px 16px",fontSize:13}}>
                        <span style={{display:"flex",alignItems:"center",gap:4}}>
                          <i className="ti ti-temperature" style={{fontSize:14,color:"#F59E0B"}}/> {e.temperature}°C
                        </span>
                      </td>
                      <td style={{padding:"12px 16px",fontSize:13}}>
                        <span style={{display:"flex",alignItems:"center",gap:4}}>
                          <i className="ti ti-droplet" style={{fontSize:14,color:"#3B82F6"}}/> %{e.humidity}
                        </span>
                      </td>
                      <td style={{padding:"12px 16px",fontSize:13}}>
                        <span style={{display:"flex",alignItems:"center",gap:4}}>
                          <i className="ti ti-sun" style={{fontSize:14,color:"#F59E0B"}}/> {e.lightLevel} lx
                        </span>
                      </td>
                      <td style={{padding:"12px 16px",fontSize:13}}>
                        <span style={{display:"flex",alignItems:"center",gap:4}}>
                          <i className="ti ti-volume" style={{fontSize:14,color:"#8B5CF6"}}/> {e.noiseLevel} dB
                        </span>
                      </td>
                      <td style={{padding:"12px 16px"}}>
                        <span style={{fontSize:11,padding:"3px 8px",borderRadius:12,background:e.occupancyDetected?"#D1FAE5":"#FEE2E2",color:e.occupancyDetected?"#10B981":"#EF4444",fontWeight:600}}>
                          {e.occupancyDetected ? "Dolu" : "Boş"}
                        </span>
                      </td>
                      <td style={{padding:"12px 16px",fontSize:11,color:"#8FAAC8"}}>{new Date(e.loggedAt).toLocaleString("tr-TR")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
      <style>{`.hover-row:hover { background: #F8FAFF !important; }`}</style>
    </main>
  );
}
