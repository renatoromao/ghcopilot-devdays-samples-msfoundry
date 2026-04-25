import React, { useEffect, useRef, useState } from 'react';
import {
    AgentInfo,
    ChatMessage,
    FoundryStatus,
    fetchMessages,
    resetChat,
    sendMessage,
} from '../services/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

interface ChatWindowProps {
    agent: AgentInfo;
    status: FoundryStatus | null;
    onStatus?: (status: FoundryStatus) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ agent, status, onStatus }) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [sending, setSending] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const scrollRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const load = async () => {
            try {
                const data = await fetchMessages();
                setMessages(data.messages || []);
                if (onStatus && data.status) onStatus(data.status);
            } catch (currentError: any) {
                console.error('Failed to load history', currentError);
            }
        };
        load();
    }, [onStatus]);

    useEffect(() => {
        const node = scrollRef.current;
        if (node) node.scrollTop = node.scrollHeight;
    }, [messages, sending]);

    const handleSend = async (text: string) => {
        setSending(true);
        setError(null);
        try {
            const data = await sendMessage(text);
            setMessages(data.messages || []);
            if (onStatus && data.status) onStatus(data.status);
        } catch (currentError: any) {
            const detail = currentError?.response?.data?.error || currentError?.message;
            setError(detail || 'Unable to send message.');
        } finally {
            setSending(false);
        }
    };

    const handleReset = async () => {
        try {
            const data = await resetChat();
            setMessages(data.messages || []);
            setError(null);
        } catch (currentError: any) {
            const detail = currentError?.response?.data?.error || currentError?.message;
            setError(detail || 'Unable to reset chat.');
        }
    };

    return (
        <section className="chat-card">
            <header className="chat-header">
                <div>
                    <h2>{agent.name || 'Foundry agent'}</h2>
                    <p className="chat-subtitle">
                        {agent.mode === 'foundry'
                            ? `Model: ${agent.model || 'configured in Foundry'}`
                            : 'Running in local echo mode'}
                        {status?.agent_id ? ` · ${status.agent_id}` : ''}
                    </p>
                </div>
                <button type="button" className="ghost-button" onClick={handleReset}>
                    New conversation
                </button>
            </header>

            <div className="chat-scroll" ref={scrollRef}>
                {messages.length === 0 && !sending && (
                    <div className="chat-empty">
                        <h3>Start chatting with your Foundry agent</h3>
                        <p>Ask anything — the conversation runs against your live project thread.</p>
                    </div>
                )}
                <MessageList messages={messages} />
                {sending && (
                    <div className="message assistant typing">
                        <span className="dot" />
                        <span className="dot" />
                        <span className="dot" />
                    </div>
                )}
            </div>

            {error && <div className="chat-error">{error}</div>}

            <MessageInput onSend={handleSend} disabled={sending} />
        </section>
    );
};

export default ChatWindow;
