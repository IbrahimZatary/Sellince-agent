import { useEffect, useRef, useState } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { getCustomers } from '../../services/api/customers.api';
import { sendChatMessage } from '../../services/api/agent.api';

const OFFER_SUGGESTIONS = [
  'My data is running out, what are my options?',
  'Can you recommend a better plan for me?',
  'My contract is ending soon, what should I do?',
  'I need more speed for my home internet',
];

export default function AgentChat() {
  const [customers, setCustomers] = useState([]);
  const [customersStatus, setCustomersStatus] = useState('loading');
  const [selectedId, setSelectedId] = useState(null);
  const [thread, setThread] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const list = await getCustomers();
        if (cancelled) return;
        setCustomers(list);
        if (list.length > 0) setSelectedId(list[0].id);
        setCustomersStatus('ready');
      } catch (err) {
        if (cancelled) return;
        setCustomersStatus('error');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [thread, sending]);

  const selectedCustomer = customers.find((customer) => customer.id === selectedId);

  const handleSend = async (textOverride) => {
    const message = (textOverride ?? input).trim();
    if (!message || !selectedId || sending) return;
    setThread((t) => [...t, { role: 'user', text: message }]);
    setInput('');
    setSending(true);
    setError('');
    try {
      const reply = await sendChatMessage(selectedId, message);
      setThread((t) => [
        ...t,
        { role: 'agent', text: reply.response },
        ...(reply.offer ? [{ role: 'offer', offer: reply.offer }] : []),
        ...(reply.action === 'show_offer'
          ? [{ role: 'agent', text: 'I have sent you an offer — take a look below.', subtle: true }]
          : []),
      ]);
    } catch (err) {
      setError(err.response?.data?.message || 'The agent could not reply. Please try again.');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)] min-h-[32rem]">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-main)]">AI Agent</h1>
          <p className="text-[var(--color-text-secondary)] mt-1">
            Chat with a customer through your AI agent
          </p>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-card)]">
        {/* Customer context */}
        <aside className="w-80 shrink-0 border-r border-[var(--color-border)] flex flex-col">
          <div className="px-4 py-3 border-b border-[var(--color-border)]">
            <h2 className="text-sm font-medium text-[var(--color-text-secondary)]">
              Customer context
            </h2>
          </div>

          {customersStatus === 'loading' && (
            <div className="p-4 space-y-2 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 rounded-lg bg-[var(--color-border)]/40" />
              ))}
            </div>
          )}

          {customersStatus === 'error' && (
            <div className="p-4 text-center">
              <p className="text-sm text-red-600">Failed to load customers.</p>
            </div>
          )}

          {customersStatus === 'ready' && (
            <>
              <div className="px-4 py-3 border-b border-[var(--color-border)]">
                <select
                  value={selectedId ?? ''}
                  onChange={(event) => {
                    setSelectedId(Number(event.target.value));
                    setThread([]);
                    setError('');
                  }}
                  className="w-full px-3 py-2 rounded-md border border-[var(--color-border)] bg-white text-sm text-[var(--color-text-main)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-orange)]/40"
                >
                  {customers.map((customer) => (
                    <option key={customer.id} value={customer.id}>
                      {customer.name}
                    </option>
                  ))}
                </select>
              </div>

              {selectedCustomer ? (
                <div className="px-4 py-4 space-y-2 text-sm border-b border-[var(--color-border)]">
                  <p className="font-medium text-[var(--color-text-main)]">{selectedCustomer.name}</p>
                  <p className="text-[var(--color-text-secondary)]">{selectedCustomer.phone}</p>
                  <p className="text-[var(--color-text-secondary)]">{selectedCustomer.current_plan}</p>
                  {selectedCustomer.service_type ? (
                    <p className="text-[var(--color-text-secondary)]">{selectedCustomer.service_type}</p>
                  ) : null}
                  {selectedCustomer.segment ? (
                    <span className="inline-flex px-2 py-0.5 rounded-full text-xs font-medium bg-[var(--color-brand-orange-light)] text-[var(--color-brand-orange)]">
                      {selectedCustomer.segment}
                    </span>
                  ) : null}
                </div>
              ) : null}

              <div className="px-4 py-4">
                <h3 className="text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                  Try asking
                </h3>
                <div className="space-y-2">
                  {OFFER_SUGGESTIONS.map((suggestion) => (
                    <button
                      key={suggestion}
                      onClick={() => handleSend(suggestion)}
                      disabled={sending}
                      className="w-full text-left text-xs px-3 py-2 rounded-lg border border-[var(--color-border)] text-[var(--color-text-muted)] hover:border-[var(--color-brand-orange)] hover:text-[var(--color-brand-orange)] transition-colors disabled:opacity-50"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}
        </aside>

        {/* Chat thread */}
        <section className="flex-1 flex flex-col min-h-0">
          <div className="flex-1 overflow-y-auto px-6 py-5 space-y-4">
            {thread.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="h-12 w-12 rounded-full bg-[var(--color-brand-orange-light)] text-[var(--color-brand-orange)] flex items-center justify-center mb-3">
                  <Bot className="h-6 w-6" />
                </div>
                <p className="text-lg font-medium text-[var(--color-text-main)]">
                  {customers.length === 0
                    ? 'No customers to chat with yet'
                    : 'Start the conversation'}
                </p>
                <p className="text-sm text-[var(--color-text-muted)] mt-1 max-w-sm">
                  {customers.length === 0
                    ? 'Seed the database to give customers for your agent to serve.'
                    : 'Pick a customer on the left, then send a message or use a suggestion.'}
                </p>
              </div>
            )}

            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            {thread.map((entry, index) => {
              if (entry.role === 'offer') {
                return (
                  <div key={index} className="flex justify-start">
                    <div className="max-w-[75%] rounded-xl border border-[var(--color-brand-orange)] bg-[var(--color-brand-orange-light)] px-4 py-3">
                      <p className="text-xs font-medium text-[var(--color-brand-orange)] mb-1 inline-flex items-center">
                        <Sparkles className="h-3.5 w-3.5 mr-1" /> Offer sent to customer
                      </p>
                      <p className="font-semibold text-[var(--color-text-main)]">
                        {entry.offer.product}
                      </p>
                      {entry.offer.price ? (
                        <p className="text-sm text-[var(--color-text-main)] mt-0.5">
                          {entry.offer.price}
                        </p>
                      ) : null}
                      {entry.offer.description ? (
                        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
                          {entry.offer.description}
                        </p>
                      ) : null}
                    </div>
                  </div>
                );
              }

              const isUser = entry.role === 'user';
              return (
                <div key={index} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                  <div
                    className={`max-w-[75%] px-4 py-2.5 rounded-xl text-sm ${
                      isUser
                        ? 'bg-[var(--color-brand-orange)] text-white rounded-br-sm'
                        : 'bg-gray-100 text-[var(--color-text-main)] rounded-bl-sm'
                    } ${entry.subtle ? 'text-[var(--color-text-muted)] opacity-80' : ''}`}
                  >
                    <div className="flex items-center gap-1.5 mb-1 text-[11px] font-medium uppercase tracking-wide">
                      {isUser ? <User className="h-3 w-3" /> : <Bot className="h-3 w-3" />}
                      {isUser ? 'You' : 'AI Agent'}
                    </div>
                    <p>{entry.text}</p>
                  </div>
                </div>
              );
            })}

            {sending && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-[var(--color-text-secondary)] px-4 py-2.5 rounded-xl rounded-bl-sm flex items-center gap-1">
                  <span className="h-2 w-2 bg-[var(--color-text-muted)] rounded-full animate-bounce" />
                  <span className="h-2 w-2 bg-[var(--color-text-muted)] rounded-full animate-bounce [animation-delay:150ms]" />
                  <span className="h-2 w-2 bg-[var(--color-text-muted)] rounded-full animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <form
            onSubmit={(event) => {
              event.preventDefault();
              handleSend();
            }}
            className="border-t border-[var(--color-border)] px-6 py-4"
          >
            <div className="flex items-center gap-3">
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder={
                  selectedCustomer
                    ? `Message ${selectedCustomer.name} via the agent…`
                    : 'Select a customer to start'
                }
                disabled={!selectedCustomer || sending}
                className="flex-1 px-4 py-2.5 rounded-lg border border-[var(--color-border)] bg-white text-sm text-[var(--color-text-main)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-orange)]/40 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!selectedCustomer || sending || !input.trim()}
                className="px-4 py-2.5 rounded-lg bg-[var(--color-brand-orange)] text-white text-sm hover:opacity-90 disabled:opacity-40 inline-flex items-center gap-2"
              >
                <Send className="h-4 w-4" />
                Send
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  );
}