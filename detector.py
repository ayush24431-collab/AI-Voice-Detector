import librosa
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class VoiceDetector:
    """AI Voice Detection System - ULTRA STRICT VERSION"""
    
    def __init__(self):
        self.supported_languages = ['Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu']
        self.version = "ULTRA_STRICT_2.0"
        print(f"✅ Detector initialized: {self.version}")
    
    def analyze(self, audio_file, language):
        """Analyze audio with ULTRA STRICT detection"""
        print(f"\n{'='*60}")
        print(f"🎙️  Analyzing: {audio_file}")
        print(f"🌍 Language: {language}")
        print(f"{'='*60}")
        
        try:
            y, sr = librosa.load(audio_file, sr=16000, duration=30)
            features = self.extract_features(y, sr)
            classification, confidence, explanation = self.classify_ultra_strict(features)
            
            return {
                "status": "success",
                "language": language,
                "classification": classification,
                "confidenceScore": confidence,
                "explanation": explanation
            }
        except Exception as e:
            return {"status": "error", "message": f"Analysis failed: {str(e)}"}
    
    def extract_features(self, y, sr):
        """Extract audio features"""
        features = {}
        
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features['zcr_var'] = float(np.var(zcr))
        
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features['spectral_centroid_std'] = float(np.std(spectral_centroids))
        
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_std'] = float(np.std(mfccs))
        
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if pitch_values:
            features['pitch_std'] = float(np.std(pitch_values))
            features['pitch_range'] = float(np.max(pitch_values) - np.min(pitch_values))
        else:
            features['pitch_std'] = 0
            features['pitch_range'] = 0
        
        rms = librosa.feature.rms(y=y)[0]
        features['energy_std'] = float(np.std(rms))
        
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        features['spectral_contrast_std'] = float(np.std(spectral_contrast))
        
        return features
    
    def classify_ultra_strict(self, features):
        """ULTRA STRICT Classification - Threshold: 0.35"""
        ai_score = 0.0
        indicators = []
        
        print(f"\n🔍 ULTRA STRICT ANALYSIS:")
        print(f"   Pitch Std: {features['pitch_std']:.2f} (trigger if <80)")
        print(f"   Spectral Std: {features['spectral_centroid_std']:.2f} (trigger if <300)")
        print(f"   ZCR Var: {features['zcr_var']:.6f} (trigger if <0.003)")
        print(f"   MFCC Std: {features['mfcc_std']:.2f} (trigger if <15)")
        print(f"   Energy Std: {features['energy_std']:.6f} (trigger if <0.035)")
        print(f"   Pitch Range: {features['pitch_range']:.2f} (trigger if <120)")
        
        # Check 1: Pitch (ULTRA STRICT: <80)
        if features['pitch_std'] < 80:
            if features['pitch_std'] < 40:
                ai_score += 0.35
                indicators.append("extremely consistent pitch")
                print(f"   ❌ Pitch: SEVERE (+0.35)")
            elif features['pitch_std'] < 60:
                ai_score += 0.25
                indicators.append("very consistent pitch")
                print(f"   ⚠️  Pitch: HIGH (+0.25)")
            else:
                ai_score += 0.15
                indicators.append("consistent pitch")
                print(f"   ⚠️  Pitch: MODERATE (+0.15)")
        else:
            print(f"   ✅ Pitch: PASS")
        
        # Check 2: Spectral (ULTRA STRICT: <300)
        if features['spectral_centroid_std'] < 300:
            if features['spectral_centroid_std'] < 150:
                ai_score += 0.30
                indicators.append("extremely uniform spectra")
                print(f"   ❌ Spectral: SEVERE (+0.30)")
            elif features['spectral_centroid_std'] < 225:
                ai_score += 0.20
                indicators.append("very uniform spectra")
                print(f"   ⚠️  Spectral: HIGH (+0.20)")
            else:
                ai_score += 0.12
                indicators.append("uniform spectra")
                print(f"   ⚠️  Spectral: MODERATE (+0.12)")
        else:
            print(f"   ✅ Spectral: PASS")
        
        # Check 3: Speech Rhythm (<0.003)
        if features['zcr_var'] < 0.003:
            if features['zcr_var'] < 0.001:
                ai_score += 0.25
                indicators.append("extremely robotic rhythm")
                print(f"   ❌ Rhythm: SEVERE (+0.25)")
            else:
                ai_score += 0.15
                indicators.append("robotic rhythm")
                print(f"   ⚠️  Rhythm: MODERATE (+0.15)")
        else:
            print(f"   ✅ Rhythm: PASS")
        
        # Check 4: Voice Timbre (<15)
        if features['mfcc_std'] < 15:
            if features['mfcc_std'] < 8:
                ai_score += 0.30
                indicators.append("extremely artificial timbre")
                print(f"   ❌ Timbre: SEVERE (+0.30)")
            elif features['mfcc_std'] < 12:
                ai_score += 0.20
                indicators.append("very artificial timbre")
                print(f"   ⚠️  Timbre: HIGH (+0.20)")
            else:
                ai_score += 0.12
                indicators.append("artificial timbre")
                print(f"   ⚠️  Timbre: MODERATE (+0.12)")
        else:
            print(f"   ✅ Timbre: PASS")
        
        # Check 5: Energy (<0.035)
        if features['energy_std'] < 0.035:
            if features['energy_std'] < 0.02:
                ai_score += 0.20
                indicators.append("extremely constant energy")
                print(f"   ❌ Energy: SEVERE (+0.20)")
            else:
                ai_score += 0.12
                indicators.append("constant energy")
                print(f"   ⚠️  Energy: MODERATE (+0.12)")
        else:
            print(f"   ✅ Energy: PASS")
        
        # Check 6: Pitch Range (<120)
        if features['pitch_range'] < 120:
            if features['pitch_range'] < 60:
                ai_score += 0.18
                indicators.append("extremely limited pitch range")
                print(f"   ❌ Range: SEVERE (+0.18)")
            else:
                ai_score += 0.10
                indicators.append("limited pitch range")
                print(f"   ⚠️  Range: MODERATE (+0.10)")
        else:
            print(f"   ✅ Range: PASS")
        
        # Check 7: Spectral Texture (<2.5)
        if features['spectral_contrast_std'] < 2.5:
            if features['spectral_contrast_std'] < 1.5:
                ai_score += 0.15
                indicators.append("very smooth texture")
                print(f"   ❌ Texture: HIGH (+0.15)")
            else:
                ai_score += 0.08
                indicators.append("smooth texture")
                print(f"   ⚠️  Texture: MODERATE (+0.08)")
        else:
            print(f"   ✅ Texture: PASS")
        
        print(f"\n📊 TOTAL AI SCORE: {ai_score:.3f}")
        print(f"🎯 THRESHOLD: 0.35")
        print(f"📋 Indicators Found: {len(indicators)}")
        
        threshold = 0.35
        
        if ai_score > threshold:
            classification = "AI_GENERATED"
            confidence = round(min(ai_score, 1.0), 2)
            explanation = f"AI characteristics detected: {', '.join(indicators[:3]) if indicators else 'processed patterns'}"
            print(f"✅ RESULT: AI_GENERATED (confidence: {confidence})\n")
        else:
            classification = "HUMAN"
            confidence = round(1 - ai_score, 2)
            explanation = "Natural human speech patterns with expected variations in pitch, energy, and spectral characteristics"
            print(f"✅ RESULT: HUMAN (confidence: {confidence})\n")
        
        return classification, confidence, explanation

detector = VoiceDetector()