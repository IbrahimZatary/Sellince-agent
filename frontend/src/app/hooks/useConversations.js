import { useCallback, useEffect, useState } from 'react';
import { getConversation, getConversations } from '../../services/api/conversations.api';

export const STATUS_LABELS = {
  open: 'In progress',
  closed: 'Closed',
};

export function statusLabel(status) {
  return STATUS_LABELS[status] || status;
}

export function useConversations() {
  const [conversations, setConversations] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const [selectedId, setSelectedId] = useState(null);
  const [detail, setDetail] = useState(null);
  const [detailStatus, setDetailStatus] = useState('idle');

  const load = useCallback(async () => {
    setStatus('loading');
    setError('');
    try {
      const list = await getConversations();
      setConversations(list);
      setStatus('ready');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load conversations');
      setStatus('error');
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const openConversation = useCallback(async (id) => {
    setSelectedId(id);
    setDetailStatus('loading');
    setDetail(null);
    try {
      const thread = await getConversation(id);
      setDetail(thread);
      setDetailStatus('ready');
    } catch (err) {
      setDetailStatus('error');
    }
  }, []);

  return { conversations, status, error, retry: load, selectedId, openConversation, detail, detailStatus };
}