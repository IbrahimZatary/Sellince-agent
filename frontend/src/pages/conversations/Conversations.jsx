import { useConversations, statusLabel } from '../../app/hooks/useConversations';

function relativeTime(iso) {
  const seconds = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 1000));
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hrs ago`;
  return `${Math.floor(seconds / 86400)} days ago`;
}

function formatTime(iso) {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function StatusChip({ status }) {
  const isOpen = status === 'open';
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
        isOpen ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'
      }`}
    >
      {isOpen ? <span className="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1.5" /> : null}
      {statusLabel(status)}
    </span>
  );
}

function EmptyState({ title, message }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-6">
      <p className="text-lg font-medium text-[var(--color-text-main)]">{title}</p>
      <p className="text-sm text-[var(--color-text-muted)] mt-1 max-w-xs">{message}</p>
    </div>
  );
}

export default function Conversations() {
  const {
    conversations,
    status,
    error,
    retry,
    selectedId,
    openConversation,
    detail,
    detailStatus,
  } = useConversations();

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)] min-h-[32rem]">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-main)]">Conversations</h1>
          <p className="text-[var(--color-text-secondary)] mt-1">
            Customer conversations handled by your AI agent
          </p>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-card)]">
        {/* Conversation list */}
        <aside className="w-80 shrink-0 border-r border-[var(--color-border)] flex flex-col min-h-0">
          <div className="px-4 py-3 border-b border-[var(--color-border)]">
            <h2 className="text-sm font-medium text-[var(--color-text-secondary)]">
              Inbox
              <span className="ml-2 px-2 py-0.5 rounded-full bg-[var(--color-brand-orange-light)] text-[var(--color-brand-orange)] text-xs font-semibold">
                {status === 'ready' ? conversations.length : '…'}
              </span>
            </h2>
          </div>

          <div className="flex-1 overflow-y-auto">
            {status === 'loading' && (
              <div className="p-4 space-y-3 animate-pulse">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-20 rounded-lg bg-[var(--color-border)]/40" />
                ))}
              </div>
            )}

            {status === 'error' && (
              <div className="p-6 text-center">
                <p className="text-red-600 text-sm">{error}</p>
                <button
                  onClick={retry}
                  className="mt-3 px-3 py-1.5 rounded-md bg-[var(--color-brand-orange)] text-white text-xs hover:opacity-90"
                >
                  Try again
                </button>
              </div>
            )}

            {status === 'ready' && conversations.length === 0 && (
              <p className="px-4 py-8 text-sm text-[var(--color-text-muted)] text-center">
                No conversations yet. Seed the database or wait for your agent to engage customers.
              </p>
            )}

            {status === 'ready' &&
              conversations.map((conversation) => {
                const active = conversation.id === selectedId;
                return (
                  <button
                    key={conversation.id}
                    onClick={() => openConversation(conversation.id)}
                    className={`w-full text-left px-4 py-3 border-b border-[var(--color-border)] transition-colors ${
                      active ? 'bg-[var(--color-brand-orange-light)]' : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium text-[var(--color-text-main)] truncate">
                        {conversation.customer.name}
                      </span>
                      <span className="text-xs text-[var(--color-text-muted)] whitespace-nowrap">
                        {relativeTime(conversation.last_activity_at)}
                      </span>
                    </div>
                    <p className="text-sm text-[var(--color-text-secondary)] truncate mt-0.5">
                      {conversation.last_message?.text || 'No messages yet'}
                    </p>
                    <div className="flex items-center justify-between mt-1.5">
                      <StatusChip status={conversation.status} />
                      {conversation.offer ? (
                        <span className="text-xs text-[var(--color-brand-orange)]">
                          {conversation.offer.product_name}
                        </span>
                      ) : null}
                    </div>
                  </button>
                );
              })}
          </div>
        </aside>

        {/* Detail pane */}
        <section className="flex-1 flex flex-col min-h-0">
          {!selectedId ? (
            <EmptyState
              title="Select a conversation"
              message="Choose a conversation from the inbox to read the full thread and any offer the agent made."
            />
          ) : (
            <>
              {/* Detail header */}
              <div className="px-5 py-4 border-b border-[var(--color-border)] flex items-start justify-between gap-4">
                {detail ? (
                  <>
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="text-lg font-semibold text-[var(--color-text-main)]">
                          {detail.customer.name}
                        </h2>
                        <StatusChip status={detail.status} />
                      </div>
                      <p className="text-sm text-[var(--color-text-secondary)] mt-0.5">
                        {detail.customer.phone} · {detail.customer.plan}
                        {detail.customer.service_type ? ` · ${detail.customer.service_type}` : ''}
                      </p>
                      <p className="text-xs text-[var(--color-text-muted)] mt-0.5">
                        Started {formatTime(detail.started_at)}
                      </p>
                    </div>
                  </>
                ) : (
                  <div className="h-12 w-48 rounded bg-[var(--color-border)]/40 animate-pulse" />
                )}
              </div>

              {/* Offer banner */}
              {detail?.offer && (
                <div className="mx-5 mt-4 px-4 py-3 rounded-lg border border-dashed border-[var(--color-brand-orange)] bg-[var(--color-brand-orange-light)] flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-[var(--color-text-main)]">
                      {detail.offer.product_name}
                    </p>
                    <p className="text-xs text-[var(--color-text-secondary)]">
                      {detail.offer.price} EGP · {detail.offer.status}
                    </p>
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-white text-[var(--color-brand-orange)] border border-[var(--color-brand-orange)]/30">
                    Offer
                  </span>
                </div>
              )}

              {/* Thread */}
              <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
                {detailStatus === 'loading' && (
                  <div className="space-y-2 animate-pulse">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="h-10 rounded-lg bg-[var(--color-border)]/40" />
                    ))}
                  </div>
                )}
                {detailStatus === 'error' && (
                  <p className="text-sm text-red-600">Failed to load this conversation.</p>
                )}
                {detail?.messages.map((message) => {
                  const isAgent = message.sender === 'agent';
                  return (
                    <div
                      key={message.id}
                      className={`flex ${isAgent ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[75%] px-4 py-2 rounded-xl text-sm ${
                          isAgent
                            ? 'bg-[var(--color-brand-orange)] text-white rounded-br-sm'
                            : 'bg-gray-100 text-[var(--color-text-main)] rounded-bl-sm'
                        }`}
                      >
                        <p>{message.text}</p>
                        <p
                          className={`text-[11px] mt-1 ${
                            isAgent ? 'text-white/70' : 'text-[var(--color-text-muted)]'
                          }`}
                        >
                          {isAgent ? 'AI Agent' : 'Customer'} · {formatTime(message.sent_at)}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </section>
      </div>
    </div>
  );
}