import React from 'react';
import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';

// 1. IMPORT DATA - Ensure this file is in app/(tabs)/
import seriesData from './doorables_master_hub.json';

const GITHUB_BASE_URL = "https://raw.githubusercontent.com/noahvolpini/Doorables-Assets/main/";

export default function HomeScreen() {
  const router = useRouter();

  const renderItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.card}
      onPress={() => router.push({
        pathname: '/characters',
        params: { 
          series: item.series_name, 
          url: item.live_data_url // MATCHED TO YOUR JSON KEY
        }
      })}
    >
      <Image 
        source={{ uri: `${GITHUB_BASE_URL}${item.id}.png` }} 
        style={styles.icon}
        defaultSource={require('../../assets/images/favicon.png')}
      />
      
      <View style={styles.textContainer}>
        <Text style={styles.cardText}>{item.series_name}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Doorables Project Hub</Text>
      
      <FlatList
        data={seriesData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id} // MATCHED TO YOUR JSON KEY
        numColumns={2}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f2f5', paddingTop: 60 },
  header: { fontSize: 28, fontWeight: '800', textAlign: 'center', marginBottom: 20, color: '#1a1a1a' },
  list: { paddingHorizontal: 10, paddingBottom: 20 },
  card: {
    flex: 1,
    margin: 8,
    backgroundColor: '#fff',
    borderRadius: 15,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    alignItems: 'center',
    height: 160,
  },
  icon: { width: '100%', height: 100, resizeMode: 'contain', backgroundColor: '#fff', marginTop: 5 },
  textContainer: { padding: 10, justifyContent: 'center', flex: 1 },
  cardText: { fontSize: 16, fontWeight: 'bold', color: '#333', textAlign: 'center' },
});