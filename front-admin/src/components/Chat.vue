<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

// 채팅 ID (임시 하드코딩)
const chatId = 'sample_chat_id';
// 사용자 ID (임시 하드코딩)
const userId = 'sample_user_id';

// 백엔드 API 기본 URL (환경 변수 사용)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'; // 기본값 설정

// Axios 기본 URL 설정
axios.defaults.baseURL = API_BASE_URL;

// 메시지 목록
const messages = ref([]);
const newMessage = ref('');

// 통신 방식 선택 ('rest' 또는 'websocket')
const communicationMode = ref('rest'); // 기본값

// WebSocket 관련
let ws = null;
const wsStatus = ref('Disconnected');

// 메시지 구조 정의
const createMessage = (text, isBot = false) => ({
  text,
  isBot,
});

// 채팅 내역 불러오기 (RESTful)
const fetchChatHistory = async () => {
  try {
    const response = await axios.get(`/api/v1/users/${userId}/chats/${chatId}`);
    messages.value = response.data.map(msg => createMessage(msg.answer, true)); // 챗봇 답변만 저장되므로 isBot: true
  } catch (error) {
    console.error('Failed to fetch chat history:', error);
  }
};

// 메시지 전송 (RESTful)
const sendRestMessage = async () => {
  if (!newMessage.value.trim()) return;

  const userMessage = newMessage.value;
  messages.value.push(createMessage(userMessage));
  newMessage.value = '';

  try {
    const response = await axios.post(`/api/v1/users/${userId}/chats/${chatId}`, { message: userMessage });
    messages.value.push(createMessage(response.data.answer, true));
  } catch (error) {
    console.error('Failed to send REST message:', error);
    messages.value.push(createMessage('메시지 전송 실패', true));
  }
};

// WebSocket 연결
const connectWebSocket = () => {
  // WebSocket URL은 백엔드 주소에 맞게 수정 필요
  // const wsUrl = `ws://localhost:8000/ws/v1/chats/${productId}`;
  const wsUrl = API_BASE_URL.replace('http', 'ws') + `/ws/v1/users/${userId}/chats/${chatId}`;
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    wsStatus.value = 'Connected';
    console.log('WebSocket Connected');
    // 연결 시 채팅 내역 불러오기 (WebSocket으로도 가능하지만 여기서는 REST 사용 예시)
     fetchChatHistory();
  };

  ws.onmessage = (event) => {
    const botAnswer = event.data;
    messages.value.push(createMessage(botAnswer, true));
  };

  ws.onerror = (error) => {
    wsStatus.value = 'Error';
    console.error('WebSocket Error:', error);
    // 오류 발생 시 연결 재시도 로직 추가 가능
  };

  ws.onclose = () => {
    wsStatus.value = 'Disconnected';
    console.log('WebSocket Disconnected');
    // 연결 종료 시 재연결 로직 추가 가능
  };
};

// 메시지 전송 (WebSocket)
const sendWebSocketMessage = () => {
  if (!newMessage.value.trim() || ws?.readyState !== WebSocket.OPEN) return;

  const userMessage = newMessage.value;
  messages.value.push(createMessage(userMessage));
  newMessage.value = '';

  ws.send(userMessage);
};

// 메시지 전송 핸들러 (모드에 따라 분기)
const sendMessage = () => {
  if (communicationMode.value === 'rest') {
    sendRestMessage();
  } else {
    sendWebSocketMessage();
  }
};

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  // 초기에는 REST로 내역만 불러오거나, 바로 WebSocket 연결 선택 가능
   fetchChatHistory();
  // WebSocket 모드를 기본으로 사용하려면 아래 주석 해제
  // connectWebSocket();
});

// 컴포넌트 언마운트 시 WebSocket 연결 해제
onUnmounted(() => {
  if (ws) {
    ws.close();
  }
});

</script>

<template>
  <div class="chat-container">
    <h2>제품 채팅 ({{ chatId }})</h2>

    <!-- 통신 모드 선택 -->
    <div>
      <label>
        <input type="radio" value="rest" v-model="communicationMode"> RESTful API
      </label>
      <label>
        <input type="radio" value="websocket" v-model="communicationMode"> WebSocket (Status: {{ wsStatus }})
      </label>
      <button v-if="communicationMode === 'websocket' && wsStatus !== 'Connected'" @click="connectWebSocket">Connect WS</button>
      <button v-if="communicationMode === 'websocket' && wsStatus === 'Connected'" @click="ws.close()">Disconnect WS</button>
    </div>

    <!-- 메시지 목록 -->
    <div class="messages-list">
      <div v-for="(msg, index) in messages" :key="index" :class="{'message': true, 'bot-message': msg.isBot, 'user-message': !msg.isBot}">
        <div class="message-bubble">{{ msg.text }}</div>
      </div>
    </div>

    <!-- 메시지 입력 -->
    <div class="message-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="메시지를 입력하세요..."
        :disabled="communicationMode === 'websocket' && wsStatus !== 'Connected'"
      />
      <button @click="sendMessage" :disabled="communicationMode === 'websocket' && wsStatus !== 'Connected'">전송</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px; /* 예시 높이 */
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  width: 400px; /* 예시 너비 */
  margin: 20px auto;
}

.messages-list {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 10px;
  padding-right: 5px;
}

.message {
  margin-bottom: 8px;
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.bot-message {
  justify-content: flex-start;
}

.message-bubble {
  padding: 8px 12px;
  border-radius: 15px;
  max-width: 70%;
  word-break: break-word;
}

.user-message .message-bubble {
  background-color: #007bff;
  color: white;
}

.bot-message .message-bubble {
  background-color: #e9e9eb;
  color: #333;
}

.message-input {
  display: flex;
}

.message-input input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 5px;
}

.message-input button {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message-input button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

</style> 