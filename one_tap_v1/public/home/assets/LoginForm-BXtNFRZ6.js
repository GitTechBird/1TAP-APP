var ie=Object.defineProperty,le=Object.defineProperties;var ce=Object.getOwnPropertyDescriptors;var F=Object.getOwnPropertySymbols;var O=Object.prototype.hasOwnProperty,$=Object.prototype.propertyIsEnumerable;var Z=(t,s,r)=>s in t?ie(t,s,{enumerable:!0,configurable:!0,writable:!0,value:r}):t[s]=r,g=(t,s)=>{for(var r in s||(s={}))O.call(s,r)&&Z(t,r,s[r]);if(F)for(var r of F(s))$.call(s,r)&&Z(t,r,s[r]);return t},M=(t,s)=>le(t,ce(s));var T=(t,s)=>{var r={};for(var n in t)O.call(t,n)&&s.indexOf(n)<0&&(r[n]=t[n]);if(t!=null&&F)for(var n of F(t))s.indexOf(n)<0&&$.call(t,n)&&(r[n]=t[n]);return r};var G=(t,s,r)=>new Promise((n,c)=>{var u=i=>{try{d(r.next(i))}catch(x){c(x)}},m=i=>{try{d(r.throw(i))}catch(x){c(x)}},d=i=>i.done?n(i.value):Promise.resolve(i.value).then(u,m);d((r=r.apply(t,s)).next())});import{j as e,c as z,k as P,f as de,G as he,u as ue,a as me,R as xe,b as pe,d as ge,e as fe,t as je,r as a,g as be,F as l,B as o,h as ye,I as A,l as U,S as J,H as ve,T as E,i as q,m as Q,n as Ce,o as we,p as C,q as ke,s as Se,v as Fe,L as Pe,w as De}from"./index-6G_JhQkf.js";var R=t=>e.jsx(z.circle,g({cx:50,cy:50,r:42,fill:"transparent"},t));R.displayName="Circle";function Ie(t,s,r){return(t-s)*100/(r-s)}var Te=P({"0%":{strokeDasharray:"1, 400",strokeDashoffset:"0"},"50%":{strokeDasharray:"400, 400",strokeDashoffset:"-100"},"100%":{strokeDasharray:"400, 400",strokeDashoffset:"-260"}}),Ae=P({"0%":{transform:"rotate(0deg)"},"100%":{transform:"rotate(360deg)"}});P({"0%":{left:"-40%"},"100%":{left:"100%"}});P({from:{backgroundPosition:"1rem 0"},to:{backgroundPosition:"0 0"}});function Ee(t){const{value:s=0,min:r,max:n,valueText:c,getValueText:u,isIndeterminate:m,role:d="progressbar"}=t,i=Ie(s,r,n);return{bind:{"data-indeterminate":m?"":void 0,"aria-valuemax":n,"aria-valuemin":r,"aria-valuenow":m?void 0:s,"aria-valuetext":(()=>{if(s!=null)return typeof u=="function"?u(s,i):c})(),role:d},percent:i,value:s}}var X=t=>{const c=t,{size:s,isIndeterminate:r}=c,n=T(c,["size","isIndeterminate"]);return e.jsx(z.svg,g({viewBox:"0 0 100 100",__css:{width:s,height:s,animation:r?`${Ae} 2s linear infinite`:void 0}},n))};X.displayName="Shape";var K=de((t,s)=>{var r;const S=t,{size:n="48px",max:c=100,min:u=0,valueText:m,getValueText:d,value:i,capIsRound:x,children:_,thickness:w="10px",color:L="#0078d4",trackColor:B="#edebe9",isIndeterminate:p}=S,f=T(S,["size","max","min","valueText","getValueText","value","capIsRound","children","thickness","color","trackColor","isIndeterminate"]),j=Ee({min:u,max:c,value:i,valueText:m,getValueText:d,isIndeterminate:p}),b=p?void 0:((r=j.percent)!=null?r:0)*2.64,y=b==null?void 0:`${b} ${264-b}`,D=p?{css:{animation:`${Te} 1.5s linear infinite`}}:{strokeDashoffset:66,strokeDasharray:y,transitionProperty:"stroke-dasharray, stroke",transitionDuration:"0.6s",transitionTimingFunction:"ease"},k={display:"inline-block",position:"relative",verticalAlign:"middle",fontSize:n};return e.jsxs(z.div,M(g(g({ref:s,className:"chakra-progress"},j.bind),f),{__css:k,children:[e.jsxs(X,{size:n,isIndeterminate:p,children:[e.jsx(R,{stroke:B,strokeWidth:w,className:"chakra-progress__track"}),e.jsx(R,g({stroke:L,strokeWidth:w,className:"chakra-progress__indicator",strokeLinecap:x?"round":void 0,opacity:j.value===0&&!p?0:void 0},D))]}),_]}))});K.displayName="CircularProgress";function Re(t){return he({tag:"svg",attr:{viewBox:"0 0 256 256",fill:"currentColor"},child:[{tag:"path",attr:{d:"M128,28A100,100,0,1,0,228,128,100.11,100.11,0,0,0,128,28Zm0,192a92,92,0,1,1,92-92A92.1,92.1,0,0,1,128,220Zm36-108a36,36,0,1,0-59.55,27.22L92.57,169A8,8,0,0,0,100,180h56a8,8,0,0,0,7.43-11l-11.88-29.82A36.11,36.11,0,0,0,164,112Zm-21,27.42L156,172H100l13-32.58a4,4,0,0,0-1.37-4.72,28,28,0,1,1,32.78,0A4,4,0,0,0,143,139.42Z"},child:[]}]})(t)}const ze="/assets/one_tap_v1/home/assets/Icon%20WHITE-2XuD39RM.png";function He(){const t=ue();let[s,r]=me();console.log("ChannelRedirectNew",s.get("redirect-to")),xe.createRef();const{response:n,error:c,loading:u,fetchData:m}=pe();ge();const d=fe(),{currentUser:i,isValidating:x,isLoading:_,login:w,logout:L,updateCurrentUser:B,getUserCookie:p}=je(),[f,j]=a.useState(!1),b=()=>j(!f),[y,D]=a.useState(""),[k,S]=a.useState(""),[_e,Y]=a.useState(""),[ee,H]=a.useState(!1),[te,N]=a.useState(!1);a.useState(!1),a.useState(!1),a.useState(!1);const[I]=be("(max-width: 767px)"),[se,W]=a.useState(!1);a.useState(!1),a.useState("flase"),a.useState("false");const re=v=>G(this,null,function*(){v.preventDefault(),H(!0);try{const h=yield w({username:y,password:k});console.log("loginResponse",h);const V=decodeURIComponent(s.get("redirect-to"));h&&h.verification&&h.verification.token_delivery?d(`/otpPage?redirect-to=${V}`,{state:{loginResponse:h,email:y,password:k,path:"Login"}}):h.message==="Logged In"&&(d(`/authuser/${encodeURIComponent(y)}?redirect-to=${V}`),t({title:"login successfully.",status:"success",duration:2e3,isClosable:!0}))}catch(h){console.error("handleSubmite",h),Y(h.message),t({title:"Invalid credentials. Please check your email and password.",status:"error",duration:2e3,isClosable:!0})}finally{H(!1)}}),ne=()=>{N(!0)},oe=()=>{N(!1)},ae=()=>{W(!0)};return a.useEffect(()=>{console.log("API response",n)},[n]),e.jsxs(l,{id:"login",width:"full",align:"center",justifyContent:"center",height:"100vh",flexDirection:{base:"column",md:"row"},overflow:"hidden",children:[e.jsx(o,{display:{base:"none",md:"flex"},justifyContent:"center",flexBasis:{base:"auto",md:"50%"},bg:"#BFE4FE",minHeight:"100%",alignItems:"center",overflow:"hidden",children:e.jsxs(o,{children:[e.jsxs(o,{textAlign:"center",boxSize:"md",children:[e.jsxs(ye.Carousel,{showThumbs:!1,children:[e.jsx("div",{children:e.jsx("img",{src:"https://media.istockphoto.com/id/1392016982/photo/mixed-group-of-business-people-sitting-around-a-table-and-talking.jpg?s=1024x1024&w=is&k=20&c=BJSTan1XQ50Bg3JpA0ZVOPiyniTybeuPDFATtZrD0E8=",alt:"Dan Abramov",style:{borderRadius:"7px",borderWidth:"1px"}})}),e.jsx("div",{children:e.jsx("img",{src:"https://media.istockphoto.com/id/1392016982/photo/mixed-group-of-business-people-sitting-around-a-table-and-talking.jpg?s=1024x1024&w=is&k=20&c=BJSTan1XQ50Bg3JpA0ZVOPiyniTybeuPDFATtZrD0E8=",alt:"Dan Abramov",style:{borderRadius:"7px",borderWidth:"1px"}})})]}),e.jsx(l,{justifyContent:"center",children:e.jsx(o,{fontSize:"25",fontWeight:"bold",children:"Start building our Own Company."})}),e.jsx(l,{justifyContent:"center",children:e.jsx(o,{fontSize:"md",children:"Create an account With 1TaP and Leave on us to set up your company at the dream of land Dubai."})})]}),e.jsx(l,{justifyContent:"center",mt:"4",children:e.jsx(A,{src:U,alt:"Dan Abramov",h:"35"})}),e.jsx(l,{justifyContent:"center",mt:"4",children:e.jsx(o,{children:"Privacy Policy | Terms & Conditons | Help"})})]})}),e.jsx(o,{flex:1,justifyContent:"center",alignItems:"center",mt:{base:"3",md:"0"},overflowY:"auto",children:e.jsxs(o,{p:10,mt:"4",children:[e.jsx(J,{below:"md",children:e.jsx(l,{justifyContent:"center",alignItems:"center",m:"2",children:e.jsx(A,{src:U,alt:"1Tap Logo",h:"35"})})}),e.jsx(o,{textAlign:"center",children:e.jsx(ve,{fontSize:"2xl",children:"Welcome"})}),e.jsxs(o,{className:I?"width-768":"white",children:[e.jsx(o,{textAlign:"center",mt:5,children:e.jsxs(l,{direction:"row",justifyContent:"center",alignItems:"flex-end",p:1,gap:1,children:[e.jsx(o,{as:"span",mr:2,mb:"1",children:e.jsx(Re,{})}),e.jsx(E,{children:"Please enter your login Details"})]})}),e.jsx(o,{my:4,textAlign:"left",children:e.jsxs("form",{onSubmit:re,children:[e.jsx(q,{isRequired:!0,mx:"auto",w:{base:"90%",md:"70%",sm:"60%"},children:e.jsx(Q,{type:"text",placeholder:"Email ID or Phone Number",size:"md",onChange:v=>D(v.currentTarget.value),border:"2px",borderColor:"#1E69D7",p:"2",textAlign:"center",_placeholder:{fontSize:"sm"},bg:I?"#FFFFFF":"transparent"})}),e.jsx(q,{isRequired:!0,mt:8,mx:"auto",w:{base:"90%",md:"70%",sm:"60%"},children:e.jsxs(Ce,{children:[e.jsx(Q,{type:f?"text":"password",placeholder:"Password",onChange:v=>S(v.currentTarget.value),border:"2px",borderColor:"#1E69D7",p:"2",textAlign:"center",_placeholder:{fontSize:"sm"},bg:I?"#FFFFFF":"transparent"}),e.jsx(we,{width:"4.5rem",children:e.jsx(C,{h:"1.75rem",size:"sm",onClick:b,children:f?"Hide":"Show"})})]})}),se?e.jsx(ke,{onSuccess:W}):e.jsx(l,{flexDirection:{base:"column",md:"row"},alignItems:"center",justifyContent:"center",mt:{base:4,md:6},children:e.jsx(o,{fontSize:"sm",borderBottom:"1px solid black",onClick:ae,cursor:"pointer",children:"Forgot password"})}),e.jsx(l,{justifyContent:"center",mt:{base:4,md:6},children:e.jsx(C,{mt:5,width:"60",bg:"#267FEA",type:"submit",color:"#FFFFFF",children:ee?e.jsx(K,{isIndeterminate:!0,size:"24px"}):"Sign In"})}),e.jsxs(l,{justifyContent:"center",mt:"7",children:[e.jsxs(E,{color:"#CCE0E9",mr:"2",children:["-----"," "]}),e.jsxs(o,{children:[" ",e.jsx("b",{children:"Other ways to Sign up"})," "]})," ",e.jsxs(E,{color:"#CCE0E9",ml:"2",children:[" ","-----"]})]}),e.jsxs(l,{justifyContent:"center",children:[e.jsx(C,{mt:4,width:"32",mr:4,fontSize:"17px",border:"2px",borderColor:"#1E69D7",leftIcon:e.jsx(Se,{}),children:"Google"}),e.jsx(C,{mt:4,width:"30",border:"2px",borderColor:"#1E69D7",fontSize:"16px",leftIcon:e.jsx(Fe,{}),children:"Facebook"})]}),e.jsxs(l,{justifyContent:"center",mt:"8",children:[e.jsxs(o,{mr:1,children:[" ","Don’t have an account?"]}),e.jsx(o,{children:e.jsx(Pe,{to:"/registration",style:{fontWeight:"bold"},children:"Create an account"})})]}),e.jsx(J,{below:"md",children:e.jsx(l,{justifyContent:"center",alignItems:"center",m:"7",children:e.jsx(o,{fontSize:"sm",children:"Privacy Policy | Terms & Conditons | Help"})})}),e.jsx(o,{position:"absolute",top:"90%",right:"5",children:e.jsx(C,{width:"27px",height:"27px",boxShadow:"white",onClick:ne,bg:"#34314C",children:e.jsx(o,{children:e.jsx(De,{isOpen:te,onClose:oe,children:e.jsx(A,{src:ze,alt:"Help Icon",borderRadius:"full",maxWidth:"460%"})})})})})]})})]})]})})]})}export{He as default};
