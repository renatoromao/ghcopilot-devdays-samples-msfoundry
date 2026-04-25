import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:5000';

export interface ChatMessage {
    id: number | string;
    text: string;
    sender: string;
    timestamp?: string;
}

export interface FoundryStatus {
    configured: boolean;
    endpoint: string | null;
    agent_id: string | null;
    model_deployment: string | null;
}

export interface AgentInfo {
    id: string;
    name: string;
    description?: string;
    model?: string | null;
    mode?: 'foundry' | 'local';
}

export interface ChatResponse {
    messages: ChatMessage[];
    status: FoundryStatus;
}

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' },
});

export const getHealth = async (): Promise<{ status: string; foundry: FoundryStatus }> => {
    const response = await apiClient.get('/api/health');
    return response.data;
};

export const initializeAgent = async (): Promise<{ agent: AgentInfo; status: FoundryStatus }> => {
    const response = await apiClient.post('/api/agents', {});
    return response.data;
};

export const sendMessage = async (message: string): Promise<ChatResponse> => {
    const response = await apiClient.post('/api/chat/send', { message });
    return response.data;
};

export const fetchMessages = async (): Promise<ChatResponse> => {
    const response = await apiClient.get('/api/chat/history');
    return response.data;
};

export const resetChat = async (): Promise<ChatResponse> => {
    const response = await apiClient.post('/api/chat/reset', {});
    return response.data;
};
