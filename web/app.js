const $ = id => document.getElementById(id);
async function api(path, data) {
  const response = await fetch(path, data === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || '요청에 실패했습니다.');
  return result;
}
function bubble(text, role='agent') {
  const node = document.createElement('div'); node.className = `bubble ${role}`; node.textContent = text;
  $('messages').append(node); $('messages').scrollTop = $('messages').scrollHeight; return node;
}
async function chat(message) {
  bubble(message, 'user'); $('send').disabled = true;
  try {
    const result = await api('/api/chat', {message});
    const node = bubble(result.answer + '\n\n' + result.steps.map((step,i)=>`${i+1}. ${step}`).join('\n'));
    const button = document.createElement('button'); button.textContent = '미해결 · 티켓 접수'; node.append(button);
    button.onclick = async () => {
      button.disabled = true;
      try { const ticket = await api('/api/tickets', {title:message,priority:'보통'}); button.textContent = '접수 완료'; bubble(`티켓 IT-${String(ticket.id).padStart(4,'0')}을 접수했습니다. 분류: ${ticket.category}\n오른쪽 지원 티켓에서 진행 상황을 확인할 수 있습니다.`); await refresh(); }
      catch(error) {button.disabled=false; bubble(error.message);}
    };
    $('messages').scrollTop = $('messages').scrollHeight;
  } catch(error) {bubble(error.message);} finally {$('send').disabled=false;}
}
$('chat-form').onsubmit = event => {event.preventDefault();const value=$('message').value.trim();if(value){$('message').value='';chat(value);}};
document.querySelectorAll('[data-query]').forEach(button=>button.onclick=()=>chat(button.dataset.query));
async function refresh() {
  try {
    const tickets = await api('/api/tickets'); $('total').textContent=tickets.length; $('open').textContent=tickets.filter(t=>t.status!=='해결').length; $('done').textContent=tickets.filter(t=>t.status==='해결').length;
    $('tickets').replaceChildren();
    if(!tickets.length){const node=document.createElement('div');node.className='empty';node.textContent='아직 접수된 티켓이 없어요.\n챗봇에서 문제를 상담하고 티켓을 접수해 보세요.';$('tickets').append(node);}
    for(const ticket of tickets){
      const node=document.createElement('article');node.className='ticket';
      const top=document.createElement('div');top.className='ticket-top';top.textContent=`IT-${String(ticket.id).padStart(4,'0')} · ${ticket.category}`;
      const title=document.createElement('h3');title.textContent=ticket.title;
      const bottom=document.createElement('div');bottom.className='ticket-bottom';const time=document.createElement('span');time.textContent=new Date(ticket.created_at).toLocaleString('ko-KR');
      const select=document.createElement('select');select.setAttribute('aria-label',`티켓 ${ticket.id} 상태`);
      for(const status of ['접수','처리 중','해결']){const option=document.createElement('option');option.textContent=status;option.selected=status===ticket.status;select.append(option);}
      select.onchange=async()=>{select.disabled=true;try{await api(`/api/tickets/${ticket.id}`,{status:select.value});await refresh();}catch(error){select.value=ticket.status;select.disabled=false;bubble(error.message);}};
      bottom.append(time,select);node.append(top,title,bottom);$('tickets').append(node);
    }
  }catch(error){$('tickets').textContent=error.message;}
}
$('refresh').onclick=refresh;refresh();
