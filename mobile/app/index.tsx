import { useCallback, useEffect, useRef, useState } from 'react';
import { FlatList, Keyboard, KeyboardEvent, StyleSheet, Text, View, SafeAreaView, Platform } from 'react-native';

import ChatInput from '../components/ChatInput';
import MessageBubble from '../components/MessageBubble';
import { sendMessage } from '../services/api';

const uid = () => Math.random().toString(36).slice(2) + Date.now().toString(36);

interface Message {
  id: string;
  text: string;
  isUser: boolean;
}

const SESSION_ID = uid();

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [keyboardHeight, setKeyboardHeight] = useState(0);
  const flatListRef = useRef<FlatList<Message>>(null);

  useEffect(() => {
    const show = Keyboard.addListener('keyboardDidShow', (e: KeyboardEvent) => {
      setKeyboardHeight(e.endCoordinates.height);
    });
    const hide = Keyboard.addListener('keyboardDidHide', () => {
      setKeyboardHeight(0);
    });
    return () => { show.remove(); hide.remove(); };
  }, []);

  const handleSend = useCallback(async (text: string) => {
    const userMsg: Message = { id: uid(), text, isUser: true };
    setMessages((prev) => [...prev, userMsg]);
    setThinking(true);
    setError(null);

    try {
      const res = await sendMessage(text, SESSION_ID);
      const assistantMsg: Message = { id: uid(), text: res.reply, isUser: false };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Something went wrong';
      setError(msg);
    } finally {
      setThinking(false);
    }
  }, []);

  useEffect(() => {
    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }, [messages, thinking]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={[styles.inner, { paddingBottom: keyboardHeight + 18 }]}>
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <MessageBubble text={item.text} isUser={item.isUser} />}
          contentContainerStyle={styles.list}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyText}>Ask me to log an expense or task!</Text>
            </View>
          }
        />

        {thinking && (
          <View style={styles.thinkingRow}>
            <Text style={styles.thinkingText}>Thinking...</Text>
          </View>
        )}

        {error && (
          <View style={styles.errorRow}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}

        <ChatInput onSend={handleSend} disabled={thinking} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0d0d0d',
  },
  inner: {
    flex: 1,
  },
  list: {
    flexGrow: 1,
    paddingVertical: 8,
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 200,
  },
  emptyText: {
    color: '#444',
    fontSize: 14,
    fontFamily: 'monospace',
  },
  thinkingRow: {
    paddingHorizontal: 16,
    paddingBottom: 4,
  },
  thinkingText: {
    color: '#555',
    fontSize: 13,
    fontFamily: 'monospace',
    fontStyle: 'italic',
  },
  errorRow: {
    paddingHorizontal: 16,
    paddingBottom: 4,
  },
  errorText: {
    color: '#ff4444',
    fontSize: 13,
    fontFamily: 'monospace',
  },
});
