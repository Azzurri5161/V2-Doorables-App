import React, { useState, useEffect, memo } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet, TextInput, Image, Platform } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface DoorableCharacter {
  id: string;
  name: string;
  code: string;
  rarity: string;
  subText?: string;
}

const getImageUrl = (name: string, series: string) => {
  if (!name || name === 'Unknown' || name.includes('Character')) return null;
  const cleanName = name.trim().replace(/\s+/g, '_').replace(/[()]/g, '');
  const cleanSeries = series.replace(/\s+/g, '').replace('0', ''); 
  return `https://disney-doorables.fandom.com/wiki/Special:FilePath/${cleanSeries}_${cleanName}.png`;
};

const CharacterCard = memo(({ item, seriesName }: { item: DoorableCharacter, seriesName: string }) => {
  const imageUrl = getImageUrl(item.name, seriesName);
  
  return (
    <View style={styles.card}>
      {imageUrl ? (
        <Image 
          source={{ uri: imageUrl }} 
          style={styles.charImage}
          resizeMode="contain"
        />
      ) : (
        <View style={[styles.charImage, { backgroundColor: '#E5E5EA', justifyContent: 'center', alignItems: 'center' }]}>
          <Text style={{ fontSize: 10, color: '#8E8E93' }}>No Pic</Text>
        </View>
      )}
      <View style={styles.leftContent}>
        <Text style={styles.name}>{item.name}</Text>
        {item.subText ? <Text style={styles.subText}>{item.subText}</Text> : null}
      </View>
      <View style={styles.rightContent}>
        <Text style={styles.code}>#{item.code}</Text>
        <Text style={styles.rarity}>{item.rarity}</Text>
      </View>
    </View>
  );
});

export default function CharactersScreen({ route }: any) {
  // Web fallback: if route.params is missing, use empty strings
  const params = route?.params || {};
  const { csvUrl = '', seriesName = 'Characters' } = params;
  
  const [characters, setCharacters] = useState<DoorableCharacter[]>([]);
  const [filteredCharacters, setFilteredCharacters] = useState<DoorableCharacter[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (csvUrl) fetchCharacterData(csvUrl);
  }, [csvUrl]);

  const fetchCharacterData = async (url: string) => {
    setLoading(true);
    const cacheKey = `cache_${url}`;

    try {
      // AsyncStorage check (Safe for Web)
      const cachedData = await AsyncStorage.getItem(cacheKey);
      if (cachedData) {
        processRawData(cachedData, url);
        if (Platform.OS !== 'web') setLoading(false); 
      }

      const response = await axios.get(url);
      const freshData = response.data;

      if (freshData !== cachedData) {
        await AsyncStorage.setItem(cacheKey, freshData);
        processRawData(freshData, url);
      }
    } catch (error) {
      console.error("Fetch Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const processRawData = (rawData: string, url: string) => {
    if (!rawData) return;
    const rows = rawData.split('\n');
    const isGithubClean = url.includes('raw.githubusercontent.com');
    
    let headerIndex = 0;
    if (!isGithubClean) {
      const BLACKLIST = ['home', 'share your codes', 'welcome', 'navigation', 'click here'];
      for (let i = 0; i < Math.min(rows.length, 30); i++) {
        const lowerRow = rows[i]?.toLowerCase() || '';
        if (BLACKLIST.some(word => lowerRow.includes(word))) continue;
        if ((lowerRow.includes('character') || lowerRow.includes('name')) && (lowerRow.includes('code') || lowerRow.includes('no.'))) {
          headerIndex = i;
          break;
        }
      }
    }

    const dataRows = rows.slice(headerIndex + 1);
    const parsedData = dataRows
      .filter((row: string) => row.trim() !== '' && row.includes(','))
      .map((row: string, index: number) => {
        const cols = row.split(',').map(c => c.trim());

        if (url.includes('Village_Peeks_CLEAN')) {
          return { id: `vp-${index}`, name: cols[1], code: cols[2], rarity: cols[3], subText: cols[0] };
        }
        if (url.includes('Mega_Specials_CLEAN')) {
          return { id: `ms-${index}`, name: cols[2], code: cols[3], rarity: cols[4], subText: `${cols[0]} - ${cols[1]}` };
        }

        const isMulti = url.includes('gid=583329007') || url.includes('gid=1566419762') || url.includes('gid=1864196160') || url.includes('gid=1279867451') || url.includes('gid=1335729580');

        if (isMulti) {
          return {
            id: `multi-${index}`,
            name: cols[1] || cols[3] || 'Unknown',
            code: cols[0] || 'N/A',
            rarity: 'Common',
            subText: cols[2] ? `Pack-mate: ${cols[2]}` : ''
          };
        }

        return {
          id: `std-${index}`,
          name: cols[7] || cols[0] || 'Unknown',
          code: cols[2] || cols[4] || 'N/A',
          rarity: cols[12] || cols[1] || 'Common'
        };
      });

    setCharacters(parsedData);
    setFilteredCharacters(parsedData);
  };

  const handleSearch = (text: string) => {
    setSearchQuery(text);
    const query = text.toLowerCase();
    const filtered = characters.filter(char => 
      char.name?.toLowerCase().includes(query) || 
      char.code?.toLowerCase().includes(query) ||
      char.subText?.toLowerCase().includes(query)
    );
    setFilteredCharacters(filtered);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>{seriesName}</Text>
      <TextInput
        style={styles.searchBar}
        placeholder="Search name or code..."
        value={searchQuery}
        onChangeText={handleSearch}
      />
      {loading && characters.length === 0 ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color="#007AFF" />
        </View>
      ) : (
        <FlatList
          data={filteredCharacters}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <CharacterCard item={item} seriesName={seriesName} />}
          contentContainerStyle={styles.listContainer}
          ListEmptyComponent={<Text style={styles.emptyText}>No characters found.</Text>}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F2F2F7' },
  headerTitle: { fontSize: 24, fontWeight: 'bold', padding: 20, paddingBottom: 10, color: '#1C1C1E' },
  searchBar: {
    height: 45,
    backgroundColor: '#FFF',
    marginHorizontal: 15,
    marginBottom: 15,
    borderRadius: 10,
    paddingHorizontal: 15,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  listContainer: { paddingHorizontal: 15, paddingBottom: 30 },
  card: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 12,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
  },
  charImage: { width: 60, height: 60, borderRadius: 8, marginRight: 12 },
  leftContent: { flex: 1 },
  rightContent: { alignItems: 'flex-end' },
  name: { fontSize: 17, fontWeight: '600', color: '#1C1C1E' },
  subText: { fontSize: 13, color: '#8E8E93', marginTop: 2 },
  code: { fontSize: 15, fontWeight: '700', color: '#007AFF' },
  rarity: { fontSize: 12, color: '#8E8E93', marginTop: 4 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { textAlign: 'center', marginTop: 50, color: '#8E8E93' },
});