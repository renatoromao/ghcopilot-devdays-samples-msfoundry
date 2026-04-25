import React from 'react';
import { ChatMessage } from '../services/api';

interface MessageListProps {
    messages: ChatMessage[];
}

const formatTime = (timestamp?: string): string => {
    if (!timestamp) return '';
    const parsed = new Date(timestamp);
    if (Number.isNaN(parsed.getTime())) return '';
    return parsed.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
    return (
        <div className="message-list">
            {messages.map((message) => {
                const role = message.sender === 'user' ? 'user' : 'assistant';
                return (
                    <div key={message.id} className={`message ${role}`}>
                        <div className="message-bubble">
                            <p>{message.text}</p>
                        </div>
                        <span className="message-meta">
                            {role === 'user' ? 'You' : 'Agent'}
                            {message.timestamp ? ` · ${formatTime(message.timestamp)}` : ''}
                        </span>
                    </div>
                );
            })}
        </div>
    );
};

export default MessageList;
