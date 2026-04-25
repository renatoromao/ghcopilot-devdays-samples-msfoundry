import React, { useState } from 'react';

interface MessageInputProps {
    onSend: (message: string) => void | Promise<void>;
    disabled?: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSend, disabled }) => {
    const [message, setMessage] = useState('');

    const submit = async () => {
        const trimmed = message.trim();
        if (!trimmed || disabled) return;
        setMessage('');
        await onSend(trimmed);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        submit();
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submit();
        }
    };

    return (
        <form className="message-input" onSubmit={handleSubmit}>
            <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message your Foundry agent…  (Enter to send, Shift+Enter for newline)"
                rows={1}
                disabled={disabled}
            />
            <button type="submit" className="send-button" disabled={disabled || !message.trim()}>
                <span aria-hidden>➤</span>
                <span className="sr-only">Send</span>
            </button>
        </form>
    );
};

export default MessageInput;
