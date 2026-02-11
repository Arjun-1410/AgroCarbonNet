import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Animated,
  Dimensions,
  Image,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import { Audio } from 'expo-av';
import * as ImagePicker from 'expo-image-picker';
import { BarChart, PieChart } from 'react-native-gifted-charts';

const BACKEND_URL = "https://agrocarbonnet.onrender.com";
const { width } = Dimensions.get('window');

// Language configurations
const LANGUAGES = {
  en: { name: 'English', code: 'en-US', flag: 'EN', greeting: 'Hello! I am your Farmer Assistant. How can I help you today?' },
  hi: { name: 'हिंदी', code: 'hi-IN', flag: 'HI', greeting: 'नमस्ते! मैं आपका किसान सहायक हूं। आज मैं आपकी कैसे मदद कर सकता हूं?' },
  te: { name: 'తెలుగు', code: 'te-IN', flag: 'TE', greeting: 'నమస్కారం! నేను మీ రైతు సహాయకుడిని. ఈ రోజు మీకు ఎలా సహాయం చేయగలను?' },
};

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  language?: 'en' | 'hi' | 'te';
  chartData?: any;
  weatherData?: any;
  imageAnalysis?: any;
}

interface FarmContext {
  crop_type: string;
  soil_type: string;
  season: string;
  location: string;
  rainfall_mm?: number;
  irrigation_percent?: number;
}

interface WeatherData {
  current: {
    temperature_c: number;
    humidity_percent: number;
    condition: string;
    wind_speed_kmh: number;
  };
  advisories: Array<{
    type: string;
    severity: string;
    message: string;
  }>;
}

export default function FarmerVoiceAssistant() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [language, setLanguage] = useState<'en' | 'hi' | 'te'>('en');
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showFarmModal, setShowFarmModal] = useState(false);
  const [showWeatherModal, setShowWeatherModal] = useState(false);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [farmContext, setFarmContext] = useState<FarmContext>({
    crop_type: '',
    soil_type: '',
    season: '',
    location: '',
    irrigation_percent: 50,
  });
  const [activeTab, setActiveTab] = useState<'chat' | 'analysis'>('chat');
  
  const scrollViewRef = useRef<ScrollView>(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const recording = useRef<Audio.Recording | null>(null);

  // Initialize session
  useEffect(() => {
    initSession();
    return () => {
      Speech.stop();
    };
  }, []);

  const initSession = async () => {
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
    
    const welcomeContent = LANGUAGES[language].greeting;
    
    const welcomeMsg: Message = {
      id: `msg_${Date.now()}`,
      role: 'assistant',
      content: welcomeContent,
      timestamp: new Date(),
      language: language,
    };
    setMessages([welcomeMsg]);
  };

  // Pulse animation for recording
  useEffect(() => {
    if (isRecording) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.3,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isRecording]);

  const fetchWeather = async () => {
    if (!farmContext.location) {
      Alert.alert(
        language === 'hi' ? 'स्थान आवश्यक' : language === 'te' ? 'స్థానం అవసరం' : 'Location Required',
        language === 'hi' ? 'कृपया पहले खेत की जानकारी में स्थान दर्ज करें' : 
        language === 'te' ? 'దయచేసి ముందు పొలం వివరాలలో స్థానం నమోదు చేయండి' :
        'Please enter your location in farm details first'
      );
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/weather/${encodeURIComponent(farmContext.location)}?language=${language}`);
      const data = await response.json();
      if (!data.error) {
        setWeatherData(data);
        setShowWeatherModal(true);
      }
    } catch (error) {
      console.error('Weather fetch error:', error);
    }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Please allow access to photos');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.7,
      base64: true,
    });

    if (!result.canceled && result.assets[0]) {
      analyzePestImage(result.assets[0]);
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Please allow camera access');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 0.7,
      base64: true,
    });

    if (!result.canceled && result.assets[0]) {
      analyzePestImage(result.assets[0]);
    }
  };

  const analyzePestImage = async (image: ImagePicker.ImagePickerAsset) => {
    setIsLoading(true);

    // Add user message showing they uploaded an image
    const userMsg: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: language === 'hi' ? '🔍 फसल की तस्वीर का विश्लेषण करें' : 
               language === 'te' ? '🔍 పంట చిత్రాన్ని విశ్లేషించండి' :
               '🔍 Analyze crop image for pests/diseases',
      timestamp: new Date(),
      language: language,
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const formData = new FormData();
      formData.append('file', {
        uri: image.uri,
        type: 'image/jpeg',
        name: 'crop_image.jpg',
      } as any);

      const response = await fetch(
        `${BACKEND_URL}/api/analyze-pest-image?language=${language}&crop=${farmContext.crop_type}`,
        {
          method: 'POST',
          body: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const data = await response.json();

      const analysisMsg: Message = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: data.analysis || 'Unable to analyze image',
        timestamp: new Date(),
        language: language,
        imageAnalysis: data,
      };

      setMessages(prev => [...prev, analysisMsg]);
      speakText(data.analysis?.substring(0, 500) || '', language);

    } catch (error) {
      console.error('Image analysis error:', error);
      const errorMsg: Message = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: language === 'hi' ? 'तस्वीर का विश्लेषण करने में त्रुटि हुई। कृपया पुनः प्रयास करें।' :
                 language === 'te' ? 'చిత్రాన్ని విశ్లేషించడంలో లోపం. దయచేసి మళ్ళీ ప్రయత్నించండి.' :
                 'Error analyzing image. Please try again.',
        timestamp: new Date(),
        language: language,
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchChartData = async () => {
    if (!farmContext.crop_type || !farmContext.soil_type || !farmContext.season || !farmContext.location) {
      return null;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/chart-data/yield-comparison`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(farmContext),
      });
      return await response.json();
    } catch (error) {
      console.error('Chart data error:', error);
      return null;
    }
  };

const sendMessage = async () => {
  try {
    const response = await fetch("https://agrocarbonnet.onrender.com/api/");
    const data = await response.json();
    console.log("SUCCESS:", data);
    alert("Backend reachable");
  } catch (error) {
    console.log("ERROR:", error);
    alert("Backend NOT reachable");
  }
};


    console.log("Response status:", response.status);

    const data = await response.json();
    console.log("Response data:", data);

  } catch (error) {
    console.log("FULL ERROR:", error);
  }
};


    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date(),
      language: language,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    session_id: sessionId,
    message: text,
    language: language,
    farm_context: farmContext.crop_type ? farmContext : null,
  }),
});


      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      const responseLanguage = data.language as 'en' | 'hi' | 'te';
      
      if (responseLanguage && responseLanguage !== language) {
        setLanguage(responseLanguage);
      }

      // Fetch chart data if we have farm context
      let chartData = null;
      if (farmContext.crop_type && data.ml_prediction) {
        chartData = await fetchChartData();
      }

      const assistantMessage: Message = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        language: responseLanguage || language,
        chartData: chartData,
      };

      setMessages(prev => [...prev, assistantMessage]);
      speakText(data.response, responseLanguage || language);

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: language === 'hi' 
          ? 'क्षमा करें, कुछ गलत हो गया। कृपया पुनः प्रयास करें।'
          : language === 'te'
          ? 'క్షమించండి, ఏదో తప్పు జరిగింది. దయచేసి మళ్ళీ ప్రయత్నించండి.'
          : 'Sorry, something went wrong. Please try again.',
        timestamp: new Date(),
        language: language,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const speakText = async (text: string, spokenLanguage?: 'en' | 'hi' | 'te') => {
    try {
      const langToUse = spokenLanguage || language;
      const langCode = LANGUAGES[langToUse].code;
      
      setIsSpeaking(true);
      await Speech.speak(text, {
        language: langCode,
        rate: 0.85,
        pitch: 1.0,
        onDone: () => setIsSpeaking(false),
        onError: () => setIsSpeaking(false),
      });
    } catch (error) {
      console.error('Speech error:', error);
      setIsSpeaking(false);
    }
  };

  const stopSpeaking = () => {
    Speech.stop();
    setIsSpeaking(false);
  };

  const [isTranscribing, setIsTranscribing] = useState(false);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status !== 'granted') {
        Alert.alert(
          language === 'hi' ? 'अनुमति आवश्यक' : language === 'te' ? 'అనుమతి అవసరం' : 'Permission Required',
          language === 'hi' ? 'माइक्रोफ़ोन की अनुमति आवश्यक है' : 
          language === 'te' ? 'మైక్రోఫోన్ అనుమతి అవసరం' : 'Microphone permission is required'
        );
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording: newRecording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      
      recording.current = newRecording;
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = async () => {
    try {
      setIsRecording(false);
      
      if (!recording.current) {
        return;
      }

      // Stop recording and get the URI
      await recording.current.stopAndUnloadAsync();
      const uri = recording.current.getURI();
      recording.current = null;

      if (!uri) {
        console.error('No recording URI');
        return;
      }

      // Show transcribing state
      setIsTranscribing(true);
      setInputText(
        language === 'hi' ? '🎙️ आवाज पहचान रहा है...' :
        language === 'te' ? '🎙️ వాయిస్ గుర్తిస్తోంది...' :
        '🎙️ Recognizing speech...'
      );

      try {
        // Create form data with the audio file
        const formData = new FormData();
        formData.append('file', {
          uri: uri,
          type: 'audio/m4a',
          name: 'recording.m4a',
        } as any);

        // Send to speech-to-text API
        const response = await fetch(`${BACKEND_URL}/api/speech-to-text?language=${language}`, {
          method: 'POST',
          body: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const data = await response.json();

        if (data.success && data.text) {
          // Set the transcribed text in the input
          setInputText(data.text);
          
          // Update language if detected differently
          if (data.detected_language && data.detected_language !== language) {
            setLanguage(data.detected_language as 'en' | 'hi' | 'te');
          }

          // Show success feedback
          const feedbackMsg = language === 'hi' ? '✓ आवाज पहचान सफल' :
                             language === 'te' ? '✓ వాయిస్ గుర్తింపు విజయవంతం' :
                             '✓ Voice recognized successfully';
          
          // Optionally auto-send the message
          // Uncomment the next line to auto-send after voice recognition:
          // await sendMessage(data.text);
          
        } else {
          setInputText('');
          Alert.alert(
            language === 'hi' ? 'पहचान विफल' : language === 'te' ? 'గుర్తింపు విఫలమైంది' : 'Recognition Failed',
            language === 'hi' ? 'कृपया फिर से बोलें या टाइप करें' :
            language === 'te' ? 'దయచేసి మళ్ళీ మాట్లాడండి లేదా టైప్ చేయండి' :
            'Please speak again or type your question'
          );
        }
      } catch (error) {
        console.error('Speech-to-text error:', error);
        setInputText('');
        Alert.alert(
          language === 'hi' ? 'त्रुटि' : language === 'te' ? 'లోపం' : 'Error',
          language === 'hi' ? 'आवाज पहचान में त्रुटि। कृपया टाइप करें।' :
          language === 'te' ? 'వాయిస్ గుర్తింపులో లోపం. దయచేసి టైప్ చేయండి.' :
          'Voice recognition error. Please type your question.'
        );
      } finally {
        setIsTranscribing(false);
      }
      
    } catch (error) {
      console.error('Failed to stop recording:', error);
      setIsTranscribing(false);
    }
  };

  const changeLanguage = (lang: 'en' | 'hi' | 'te') => {
    setLanguage(lang);
    setShowLanguageModal(false);
    
    const langMsg: Message = {
      id: `msg_${Date.now()}`,
      role: 'assistant',
      content: LANGUAGES[lang].greeting,
      timestamp: new Date(),
      language: lang,
    };
    setMessages(prev => [...prev, langMsg]);
    speakText(LANGUAGES[lang].greeting, lang);
  };

  const renderChart = (chartData: any) => {
    if (!chartData || !chartData.data) return null;

    const barData = chartData.data.labels.map((label: string, index: number) => ({
      value: chartData.data.values[index],
      label: label.length > 10 ? label.substring(0, 10) + '...' : label,
      frontColor: chartData.data.colors[index],
    }));

    return (
      <View style={styles.chartContainer}>
        <Text style={styles.chartTitle}>{chartData.title}</Text>
        <BarChart
          data={barData}
          barWidth={40}
          spacing={20}
          roundedTop
          roundedBottom
          hideRules
          xAxisThickness={1}
          yAxisThickness={1}
          yAxisTextStyle={{ fontSize: 10 }}
          xAxisLabelTextStyle={{ fontSize: 8, width: 50 }}
          noOfSections={4}
          maxValue={Math.max(...chartData.data.values) * 1.2}
          width={width - 100}
          height={150}
        />
        <Text style={styles.chartUnit}>Unit: {chartData.unit}</Text>
        {chartData.analysis && (
          <Text style={styles.chartAnalysis}>{chartData.analysis}</Text>
        )}
      </View>
    );
  };

  const renderMessage = (message: Message) => {
    const isUser = message.role === 'user';
    const msgLanguage = message.language || language;
    
    return (
      <View key={message.id}>
        <View
          style={[
            styles.messageContainer,
            isUser ? styles.userMessage : styles.assistantMessage,
          ]}
        >
          {!isUser && (
            <View style={styles.avatarContainer}>
              <Ionicons name="leaf" size={20} color="#2E7D32" />
            </View>
          )}
          <View style={[styles.messageBubble, isUser ? styles.userBubble : styles.assistantBubble]}>
            <Text style={[styles.messageText, isUser && styles.userMessageText]}>
              {message.content}
            </Text>
          </View>
          {!isUser && (
            <TouchableOpacity
              style={styles.speakButton}
              onPress={() => isSpeaking ? stopSpeaking() : speakText(message.content, msgLanguage)}
            >
              <Ionicons
                name={isSpeaking ? "stop-circle" : "volume-high"}
                size={20}
                color="#2E7D32"
              />
            </TouchableOpacity>
          )}
        </View>
        {message.chartData && renderChart(message.chartData)}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Ionicons name="leaf" size={28} color="#2E7D32" />
          <Text style={styles.headerTitle}>
            {language === 'hi' ? 'किसान सहायक' : language === 'te' ? 'రైతు సహాయకుడు' : 'Farmer Assistant'}
          </Text>
        </View>
        <View style={styles.headerRight}>
          <TouchableOpacity style={styles.headerButton} onPress={fetchWeather}>
            <Ionicons name="cloud-outline" size={22} color="#2E7D32" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.headerButton} onPress={() => setShowFarmModal(true)}>
            <Ionicons name="settings-outline" size={22} color="#2E7D32" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.languageButton} onPress={() => setShowLanguageModal(true)}>
            <Text style={styles.languageText}>{LANGUAGES[language].flag}</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Quick Actions Bar */}
      <View style={styles.quickActions}>
        <TouchableOpacity style={styles.quickActionBtn} onPress={takePhoto}>
          <Ionicons name="camera" size={18} color="#fff" />
          <Text style={styles.quickActionText}>
            {language === 'hi' ? 'फोटो' : language === 'te' ? 'ఫోటో' : 'Photo'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickActionBtn} onPress={pickImage}>
          <Ionicons name="image" size={18} color="#fff" />
          <Text style={styles.quickActionText}>
            {language === 'hi' ? 'गैलरी' : language === 'te' ? 'గ్యాలరీ' : 'Gallery'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickActionBtn} onPress={fetchWeather}>
          <Ionicons name="rainy" size={18} color="#fff" />
          <Text style={styles.quickActionText}>
            {language === 'hi' ? 'मौसम' : language === 'te' ? 'వాతావరణం' : 'Weather'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
      >
        {messages.map(renderMessage)}
        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#2E7D32" />
            <Text style={styles.loadingText}>
              {language === 'hi' ? 'सोच रहा हूं...' : language === 'te' ? 'ఆలోచిస్తున్నాను...' : 'Thinking...'}
            </Text>
          </View>
        )}
      </ScrollView>

      {/* Input Area */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        {/* Voice Mode Indicator */}
        {(isRecording || isTranscribing) && (
          <View style={styles.voiceModeBar}>
            <Ionicons 
              name={isRecording ? "mic" : "hourglass"} 
              size={18} 
              color="#fff" 
            />
            <Text style={styles.voiceModeText}>
              {isRecording 
                ? (language === 'hi' ? '🔴 बोलिए...' : language === 'te' ? '🔴 మాట్లాడండి...' : '🔴 Listening...')
                : (language === 'hi' ? '⏳ पहचान रहा है...' : language === 'te' ? '⏳ గుర్తిస్తోంది...' : '⏳ Transcribing...')
              }
            </Text>
          </View>
        )}
        
        <View style={styles.inputContainer}>
          <Animated.View style={[styles.micButtonContainer, { transform: [{ scale: pulseAnim }] }]}>
            <TouchableOpacity
              style={[
                styles.micButton, 
                isRecording && styles.micButtonActive,
                isTranscribing && styles.micButtonTranscribing
              ]}
              onPressIn={startRecording}
              onPressOut={stopRecording}
              disabled={isTranscribing}
            >
              {isTranscribing ? (
                <ActivityIndicator size="small" color="#2E7D32" />
              ) : (
                <Ionicons
                  name={isRecording ? "mic" : "mic-outline"}
                  size={24}
                  color={isRecording ? "#fff" : "#2E7D32"}
                />
              )}
            </TouchableOpacity>
          </Animated.View>
          
          <TextInput
            style={styles.textInput}
            value={inputText}
            onChangeText={setInputText}
            placeholder={
              language === 'hi' ? 'बोलें या टाइप करें...' 
              : language === 'te' ? 'మాట్లాడండి లేదా టైప్ చేయండి...'
              : 'Speak or type here...'
            }
            placeholderTextColor="#999"
            multiline
            maxLength={500}
            editable={!isTranscribing}
          />
          
          <TouchableOpacity
            style={[styles.sendButton, (!inputText.trim() || isTranscribing) && styles.sendButtonDisabled]}
            onPress={() => sendMessage(inputText)}
            disabled={!inputText.trim() || isLoading || isTranscribing}
          >
            <Ionicons name="send" size={20} color="#fff" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>

      {/* Language Selection Modal */}
      {showLanguageModal && (
        <View style={styles.modalOverlay}>
          <View style={styles.modal}>
            <Text style={styles.modalTitle}>Select Language / भाषा चुनें / భాష ఎంచుకోండి</Text>
            {Object.entries(LANGUAGES).map(([key, lang]) => (
              <TouchableOpacity
                key={key}
                style={[styles.languageOption, language === key && styles.languageOptionActive]}
                onPress={() => changeLanguage(key as 'en' | 'hi' | 'te')}
              >
                <Text style={[styles.languageOptionText, language === key && styles.languageOptionTextActive]}>
                  {lang.name}
                </Text>
                {language === key && <Ionicons name="checkmark" size={20} color="#2E7D32" />}
              </TouchableOpacity>
            ))}
            <TouchableOpacity style={styles.modalCloseButton} onPress={() => setShowLanguageModal(false)}>
              <Text style={styles.modalCloseText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Weather Modal */}
      {showWeatherModal && weatherData && (
        <View style={styles.modalOverlay}>
          <View style={styles.weatherModal}>
            <View style={styles.weatherHeader}>
              <Ionicons name="partly-sunny" size={40} color="#FF9800" />
              <View style={styles.weatherTemp}>
                <Text style={styles.weatherTempText}>{weatherData.current.temperature_c}°C</Text>
                <Text style={styles.weatherCondition}>{weatherData.current.condition}</Text>
              </View>
            </View>
            
            <View style={styles.weatherDetails}>
              <View style={styles.weatherDetailItem}>
                <Ionicons name="water" size={20} color="#2196F3" />
                <Text style={styles.weatherDetailText}>{weatherData.current.humidity_percent}%</Text>
              </View>
              <View style={styles.weatherDetailItem}>
                <Ionicons name="speedometer" size={20} color="#4CAF50" />
                <Text style={styles.weatherDetailText}>{weatherData.current.wind_speed_kmh} km/h</Text>
              </View>
            </View>

            <Text style={styles.advisoryTitle}>
              {language === 'hi' ? 'कृषि सलाह' : language === 'te' ? 'వ్యవసాయ సలహా' : 'Agricultural Advisory'}
            </Text>
            
            {weatherData.advisories?.slice(0, 3).map((advisory, index) => (
              <View key={index} style={[styles.advisoryItem, 
                advisory.severity === 'high' ? styles.advisoryHigh : 
                advisory.severity === 'medium' ? styles.advisoryMedium : styles.advisoryLow
              ]}>
                <Ionicons 
                  name={advisory.severity === 'high' ? 'warning' : 'information-circle'} 
                  size={18} 
                  color={advisory.severity === 'high' ? '#F44336' : advisory.severity === 'medium' ? '#FF9800' : '#4CAF50'} 
                />
                <Text style={styles.advisoryText}>{advisory.message}</Text>
              </View>
            ))}

            <TouchableOpacity style={styles.modalCloseButton} onPress={() => setShowWeatherModal(false)}>
              <Text style={styles.modalCloseText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Farm Context Modal */}
      {showFarmModal && (
        <View style={styles.modalOverlay}>
          <ScrollView style={styles.farmModal}>
            <Text style={styles.modalTitle}>
              {language === 'hi' ? 'खेत की जानकारी' : language === 'te' ? 'పొలం వివరాలు' : 'Farm Details'}
            </Text>
            <Text style={styles.modalSubtitle}>
              {language === 'hi' ? 'बेहतर सलाह के लिए जानकारी दें' 
              : language === 'te' ? 'మెరుగైన సలహా కోసం వివరాలు ఇవ్వండి'
              : 'Provide details for better advice'}
            </Text>

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'फसल का प्रकार' : language === 'te' ? 'పంట రకం' : 'Crop Type'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.crop_type}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, crop_type: text }))}
              placeholder="e.g., Rice, Wheat, Cotton, Tomato"
              placeholderTextColor="#999"
            />

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'मिट्टी का प्रकार' : language === 'te' ? 'మట్టి రకం' : 'Soil Type'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.soil_type}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, soil_type: text }))}
              placeholder="e.g., Alluvial, Black, Red, Loamy"
              placeholderTextColor="#999"
            />

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'मौसम' : language === 'te' ? 'సీజన్' : 'Season'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.season}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, season: text }))}
              placeholder="e.g., Kharif, Rabi, Zaid"
              placeholderTextColor="#999"
            />

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'स्थान' : language === 'te' ? 'స్థానం' : 'Location'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.location}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, location: text }))}
              placeholder="e.g., Guntur, Andhra Pradesh"
              placeholderTextColor="#999"
            />

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'वर्षा (मिमी)' : language === 'te' ? 'వర్షపాతం (మిమీ)' : 'Rainfall (mm)'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.rainfall_mm?.toString() || ''}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, rainfall_mm: parseFloat(text) || undefined }))}
              placeholder="e.g., 800"
              placeholderTextColor="#999"
              keyboardType="numeric"
            />

            <Text style={styles.inputLabel}>
              {language === 'hi' ? 'सिंचाई (%)' : language === 'te' ? 'నీటిపారుదల (%)' : 'Irrigation (%)'}
            </Text>
            <TextInput
              style={styles.modalInput}
              value={farmContext.irrigation_percent?.toString() || ''}
              onChangeText={(text) => setFarmContext(prev => ({ ...prev, irrigation_percent: parseFloat(text) || undefined }))}
              placeholder="e.g., 70"
              placeholderTextColor="#999"
              keyboardType="numeric"
            />

            <TouchableOpacity style={styles.saveButton} onPress={() => setShowFarmModal(false)}>
              <Text style={styles.saveButtonText}>
                {language === 'hi' ? 'सहेजें' : language === 'te' ? 'సేవ్ చేయండి' : 'Save'}
              </Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.modalCloseButton} onPress={() => setShowFarmModal(false)}>
              <Text style={styles.modalCloseText}>Close</Text>
            </TouchableOpacity>
          </ScrollView>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5DC',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#2E7D32',
    marginLeft: 8,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerButton: {
    padding: 8,
  },
  languageButton: {
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  languageText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E7D32',
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 10,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  quickActionBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2E7D32',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 6,
  },
  quickActionText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
    paddingBottom: 24,
  },
  messageContainer: {
    flexDirection: 'row',
    marginBottom: 16,
    alignItems: 'flex-start',
  },
  userMessage: {
    justifyContent: 'flex-end',
  },
  assistantMessage: {
    justifyContent: 'flex-start',
  },
  avatarContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#E8F5E9',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  messageBubble: {
    maxWidth: '70%',
    padding: 12,
    borderRadius: 16,
  },
  userBubble: {
    backgroundColor: '#2E7D32',
    borderBottomRightRadius: 4,
  },
  assistantBubble: {
    backgroundColor: '#fff',
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  messageText: {
    fontSize: 15,
    lineHeight: 22,
    color: '#333',
  },
  userMessageText: {
    color: '#fff',
  },
  speakButton: {
    padding: 8,
    marginLeft: 4,
  },
  chartContainer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    marginLeft: 44,
  },
  chartTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
    textAlign: 'center',
  },
  chartUnit: {
    fontSize: 11,
    color: '#666',
    textAlign: 'center',
    marginTop: 8,
  },
  chartAnalysis: {
    fontSize: 12,
    color: '#2E7D32',
    textAlign: 'center',
    marginTop: 8,
    fontStyle: 'italic',
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
  },
  loadingText: {
    marginLeft: 8,
    color: '#666',
    fontSize: 14,
  },
  voiceModeBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2E7D32',
    paddingVertical: 8,
    paddingHorizontal: 16,
    gap: 8,
  },
  voiceModeText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
  },
  micButtonContainer: {
    marginRight: 8,
  },
  micButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#E8F5E9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  micButtonActive: {
    backgroundColor: '#F44336',
  },
  micButtonTranscribing: {
    backgroundColor: '#FFF3E0',
    borderWidth: 2,
    borderColor: '#FF9800',
  },
  textInput: {
    flex: 1,
    minHeight: 44,
    maxHeight: 100,
    backgroundColor: '#F5F5F5',
    borderRadius: 22,
    paddingHorizontal: 16,
    paddingVertical: 10,
    fontSize: 15,
    color: '#333',
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#2E7D32',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 8,
  },
  sendButtonDisabled: {
    backgroundColor: '#A5D6A7',
  },
  modalOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modal: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    width: '100%',
    maxWidth: 340,
  },
  farmModal: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    width: '100%',
    maxWidth: 340,
    maxHeight: '80%',
  },
  weatherModal: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    width: '100%',
    maxWidth: 340,
  },
  weatherHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  weatherTemp: {
    marginLeft: 16,
  },
  weatherTempText: {
    fontSize: 36,
    fontWeight: '700',
    color: '#333',
  },
  weatherCondition: {
    fontSize: 14,
    color: '#666',
  },
  weatherDetails: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
    paddingVertical: 12,
    backgroundColor: '#F5F5F5',
    borderRadius: 12,
  },
  weatherDetailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  weatherDetailText: {
    fontSize: 14,
    color: '#333',
  },
  advisoryTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 12,
  },
  advisoryItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    gap: 8,
  },
  advisoryHigh: {
    backgroundColor: '#FFEBEE',
  },
  advisoryMedium: {
    backgroundColor: '#FFF3E0',
  },
  advisoryLow: {
    backgroundColor: '#E8F5E9',
  },
  advisoryText: {
    flex: 1,
    fontSize: 13,
    color: '#333',
    lineHeight: 18,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#2E7D32',
    textAlign: 'center',
    marginBottom: 8,
  },
  modalSubtitle: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  languageOption: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    marginBottom: 8,
    backgroundColor: '#F5F5F5',
  },
  languageOptionActive: {
    backgroundColor: '#E8F5E9',
    borderWidth: 1,
    borderColor: '#2E7D32',
  },
  languageOptionText: {
    fontSize: 16,
    color: '#333',
  },
  languageOptionTextActive: {
    color: '#2E7D32',
    fontWeight: '600',
  },
  modalCloseButton: {
    marginTop: 16,
    padding: 12,
    alignItems: 'center',
  },
  modalCloseText: {
    color: '#666',
    fontSize: 14,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 6,
    marginTop: 12,
  },
  modalInput: {
    backgroundColor: '#F5F5F5',
    borderRadius: 12,
    padding: 12,
    fontSize: 15,
    color: '#333',
  },
  saveButton: {
    backgroundColor: '#2E7D32',
    borderRadius: 12,
    padding: 14,
    alignItems: 'center',
    marginTop: 20,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
