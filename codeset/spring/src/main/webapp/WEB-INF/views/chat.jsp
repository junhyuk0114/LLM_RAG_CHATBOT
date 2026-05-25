<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주식 RAG 챗봇</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        .bubble table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 13px; }
        .bubble th, .bubble td { border: 1px solid #dadce0; padding: 6px 10px; text-align: left; }
        .bubble th { background: #f1f3f4; font-weight: bold; }
        .bubble p { margin: 4px 0; }
        .bubble ul, .bubble ol { padding-left: 20px; margin: 4px 0; }
        .bubble strong { font-weight: bold; }
        .bubble code { background: #f1f3f4; padding: 1px 5px; border-radius: 3px; font-size: 13px; }
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Malgun Gothic', sans-serif;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        #chat-wrap {
            width: 720px;
            height: 85vh;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        #chat-header {
            background: #1a73e8;
            color: #fff;
            padding: 18px 24px;
            font-size: 17px;
            font-weight: bold;
            letter-spacing: -0.3px;
        }

        #chat-header span {
            font-size: 13px;
            font-weight: normal;
            opacity: 0.85;
            margin-left: 8px;
        }

        #chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .msg-row {
            display: flex;
            flex-direction: column;
        }

        .msg-row.user { align-items: flex-end; }
        .msg-row.assistant { align-items: flex-start; }

        .bubble {
            max-width: 75%;
            padding: 11px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .user .bubble {
            background: #1a73e8;
            color: #fff;
            border-bottom-right-radius: 4px;
        }

        .assistant .bubble {
            background: #f1f3f4;
            color: #202124;
            border-bottom-left-radius: 4px;
        }

        .sources {
            font-size: 11px;
            color: #888;
            margin-top: 5px;
            max-width: 75%;
        }

        .loading .bubble {
            color: #888;
            font-style: italic;
        }

        #input-area {
            display: flex;
            gap: 10px;
            padding: 14px 20px;
            border-top: 1px solid #e8eaed;
            background: #fff;
        }

        #question-input {
            flex: 1;
            padding: 11px 16px;
            border: 1px solid #dadce0;
            border-radius: 24px;
            font-size: 14px;
            outline: none;
            font-family: inherit;
        }

        #question-input:focus { border-color: #1a73e8; }

        #send-btn {
            padding: 11px 22px;
            background: #1a73e8;
            color: #fff;
            border: none;
            border-radius: 24px;
            font-size: 14px;
            cursor: pointer;
            font-family: inherit;
        }

        #send-btn:disabled {
            background: #9aa0a6;
            cursor: not-allowed;
        }
    </style>
</head>
<body>

<div id="chat-wrap">
    <div id="chat-header">
        주식 RAG 챗봇 <span>초보 투자자를 위한 기업 공시 · 주식 용어 안내</span>
    </div>
    <div id="chat-box">
        <div class="msg-row assistant">
            <div class="bubble">안녕하세요! 주식 용어나 기업 공시(DART)에 대해 궁금한 점을 질문해 주세요.</div>
        </div>
    </div>
    <div id="input-area">
        <input type="text" id="question-input" placeholder="예: PER이 뭔가요? / 삼성전자 최근 실적은?" maxlength="300" />
        <button id="send-btn">전송</button>
    </div>
</div>

<script>
    const ctxPath = '${pageContext.request.contextPath}';
    const sessionId = 'sess-' + Date.now() + '-' + Math.random().toString(36).slice(2, 7);

    const chatBox   = document.getElementById('chat-box');
    const input     = document.getElementById('question-input');
    const sendBtn   = document.getElementById('send-btn');

    function appendMsg(role, text, sources) {
        const row = document.createElement('div');
        row.className = 'msg-row ' + role;

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        if (role === 'assistant') {
            bubble.innerHTML = marked.parse(text);
        } else {
            bubble.textContent = text;
        }
        row.appendChild(bubble);

        if (sources && sources.length > 0) {
            const src = document.createElement('div');
            src.className = 'sources';
            src.textContent = '출처: ' + sources.map(s => s.corp_name + ' ' + s.report_type).join(' | ');
            row.appendChild(src);
        }

        chatBox.appendChild(row);
        chatBox.scrollTop = chatBox.scrollHeight;
        return row;
    }

    function sendMessage() {
        const question = input.value.trim();
        if (!question) return;

        appendMsg('user', question, null);
        input.value = '';
        input.disabled = true;
        sendBtn.disabled = true;

        const loadingRow = appendMsg('loading', '답변을 생성하는 중입니다...', null);

        fetch(ctxPath + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question, sessionId: sessionId })
        })
        .then(res => res.json())
        .then(data => {
            chatBox.removeChild(loadingRow);
            appendMsg('assistant', data.answer, data.sources);
        })
        .catch(() => {
            chatBox.removeChild(loadingRow);
            appendMsg('assistant', '오류가 발생했습니다. 잠시 후 다시 시도해주세요.', null);
        })
        .finally(() => {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });
</script>

</body>
</html>
