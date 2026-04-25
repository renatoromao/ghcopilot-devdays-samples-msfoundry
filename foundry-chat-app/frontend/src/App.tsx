import React, { useEffect, useState } from 'react';
import ChatWindow from './components/ChatWindow';
import { AgentInfo, FoundryStatus, getHealth, initializeAgent } from './services/api';
import './App.css';

const App: React.FC = () => {
    const [agent, setAgent] = useState<AgentInfo | null>(null);
    const [status, setStatus] = useState<FoundryStatus | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const bootstrap = async () => {
            try {
                const health = await getHealth();
                setStatus(health.foundry);
                const result = await initializeAgent();
                setAgent(result.agent);
                setStatus(result.status);
            } catch (currentError: any) {
                console.error('Failed to initialize agent', currentError);
                const detail = currentError?.response?.data?.error || currentError?.message;
                setError(detail || 'Unable to initialize the chat agent.');
            } finally {
                setLoading(false);
            }
        };

        bootstrap();
    }, []);

    const isFoundry = status?.configured ?? false;

    return (
        <div className="app-shell">
            <div className="app-background" />
            <header className="app-header">
                <div className="app-brand">
                    <span className="app-logo">✦</span>
                    <div>
                        <h1>Foundry Chat</h1>
                        <p>Microsoft Foundry agent playground</p>
                    </div>
                </div>
                <div className={`status-pill ${isFoundry ? 'status-online' : 'status-local'}`}>
                    <span className="status-dot" />
                    {isFoundry ? 'Connected to Foundry' : 'Local mode (no Foundry config)'}
                </div>
            </header>

            <main className="app-main">
                {loading && <div className="card placeholder">Connecting to your Foundry project…</div>}

                {!loading && error && (
                    <div className="card error">
                        <h2>We couldn’t reach the agent</h2>
                        <p>{error}</p>
                        <p className="muted">
                            Set <code>AZURE_AI_PROJECT_ENDPOINT</code> and either <code>FOUNDRY_AGENT_ID</code> or
                            <code> FOUNDRY_MODEL_DEPLOYMENT</code> in <code>.env</code>, then run <code>az login</code>.
                        </p>
                    </div>
                )}

                {!loading && !error && agent && (
                    <ChatWindow agent={agent} status={status} onStatus={setStatus} />
                )}
            </main>
        </div>
    );
};

export default App;
