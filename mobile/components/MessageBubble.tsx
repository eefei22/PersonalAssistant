import { StyleSheet, Text, View } from 'react-native';

interface Props {
  text: string;
  isUser: boolean;
}

export default function MessageBubble({ text, isUser }: Props) {
  return (
    <View style={[styles.row, isUser ? styles.rowRight : styles.rowLeft]}>
      <View style={[styles.bubble, isUser ? styles.userBubble : styles.assistantBubble]}>
        <Text style={isUser ? styles.userText : styles.assistantText}>{text}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    paddingHorizontal: 12,
    paddingVertical: 4,
  },
  rowRight: {
    alignItems: 'flex-end',
  },
  rowLeft: {
    alignItems: 'flex-start',
  },
  bubble: {
    maxWidth: '80%',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 4,
  },
  userBubble: {
    backgroundColor: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#00ff41',
  },
  assistantBubble: {
    backgroundColor: '#0d0d0d',
    borderWidth: 1,
    borderColor: '#333',
  },
  userText: {
    color: '#00ff41',
    fontSize: 14,
    fontFamily: 'monospace',
  },
  assistantText: {
    color: '#c0c0c0',
    fontSize: 14,
    fontFamily: 'monospace',
  },
});
