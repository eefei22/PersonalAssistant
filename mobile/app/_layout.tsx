import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: '#0d0d0d' },
        headerTintColor: '#00ff41',
        headerTitleStyle: { fontFamily: 'monospace', fontSize: 16 },
        contentStyle: { backgroundColor: '#0d0d0d' },
      }}
    >
      <Stack.Screen name="index" options={{ title: '> personal_assistant' }} />
    </Stack>
  );
}
