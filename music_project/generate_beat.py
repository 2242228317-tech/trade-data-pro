#!/usr/bin/env python3
"""
AI创业说唱 - 伴奏生成器
使用Python + mido库生成MIDI伴奏
"""

from mido import Message, MidiFile, MidiTrack, MetaMessage
import os

def create_boom_bap_beat(filename="ai_startup_beat.mid"):
    """创建一个Boom Bap风格的伴奏"""
    
    mid = MidiFile()
    
    # === 轨道1: 鼓组 (Drums) ===
    drum_track = MidiTrack()
    mid.tracks.append(drum_track)
    drum_track.append(MetaMessage('track_name', name='Drums', time=0))
    
    # 设置BPM = 85
    drum_track.append(MetaMessage('set_tempo', tempo=705882, time=0))  # 85 BPM
    
    # 鼓组音符定义 (General MIDI)
    KICK = 36      # 底鼓
    SNARE = 38     # 军鼓
    HIHAT_CLOSED = 42  # 闭镲
    HIHAT_OPEN = 46    # 开镲
    
    # 4小节鼓组循环
    for bar in range(8):  # 8小节
        # 第1拍: Kick + Hat
        drum_track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=9))
        drum_track.append(Message('note_on', note=HIHAT_CLOSED, velocity=80, time=0, channel=9))
        drum_track.append(Message('note_off', note=KICK, velocity=0, time=480, channel=9))
        drum_track.append(Message('note_off', note=HIHAT_CLOSED, velocity=0, time=0, channel=9))
        
        # 第2拍: Snare + Hat
        drum_track.append(Message('note_on', note=SNARE, velocity=90, time=0, channel=9))
        drum_track.append(Message('note_on', note=HIHAT_CLOSED, velocity=80, time=0, channel=9))
        drum_track.append(Message('note_off', note=SNARE, velocity=0, time=480, channel=9))
        drum_track.append(Message('note_off', note=HIHAT_CLOSED, velocity=0, time=0, channel=9))
        
        # 第3拍: Kick + Hat
        drum_track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=9))
        drum_track.append(Message('note_on', note=HIHAT_CLOSED, velocity=80, time=0, channel=9))
        drum_track.append(Message('note_off', note=KICK, velocity=0, time=480, channel=9))
        drum_track.append(Message('note_off', note=HIHAT_CLOSED, velocity=0, time=0, channel=9))
        
        # 第4拍: Snare + Open Hat (加重)
        drum_track.append(Message('note_on', note=SNARE, velocity=100, time=0, channel=9))
        drum_track.append(Message('note_on', note=HIHAT_OPEN, velocity=90, time=0, channel=9))
        drum_track.append(Message('note_off', note=SNARE, velocity=0, time=480, channel=9))
        drum_track.append(Message('note_off', note=HIHAT_OPEN, velocity=0, time=0, channel=9))
    
    # === 轨道2: 贝斯 (Bass) ===
    bass_track = MidiTrack()
    mid.tracks.append(bass_track)
    bass_track.append(MetaMessage('track_name', name='Bass', time=0))
    
    # 设置乐器: 合成贝斯 (Acoustic Bass = 32)
    bass_track.append(Message('program_change', program=32, time=0, channel=1))
    
    # 低音循环: C - G - A - F (适合说唱的小调)
    bass_notes = [36, 43, 45, 41]  # C2, G2, A2, F2
    
    for bar in range(8):
        note = bass_notes[bar % 4]
        # 每小节演奏根音
        bass_track.append(Message('note_on', note=note, velocity=80, time=0, channel=1))
        bass_track.append(Message('note_off', note=note, velocity=0, time=1920, channel=1))
    
    # === 轨道3: 合成器铺底 (Synth Pad) ===
    pad_track = MidiTrack()
    mid.tracks.append(pad_track)
    pad_track.append(MetaMessage('track_name', name='Pad', time=0))
    
    # 设置乐器: 合成铺底 (Pad = 91)
    pad_track.append(Message('program_change', program=91, time=0, channel=2))
    
    # 和弦进行
    chords = [
        [48, 52, 55],  # C minor
        [43, 47, 50],  # G major
        [45, 48, 52],  # A minor
        [41, 45, 48],  # F major
    ]
    
    for bar in range(8):
        chord = chords[bar % 4]
        # 演奏和弦
        for note in chord:
            pad_track.append(Message('note_on', note=note, velocity=60, time=0, channel=2))
        # 持续一小节
        for note in chord:
            pad_track.append(Message('note_off', note=note, velocity=0, time=1920, channel=2))
    
    # === 轨道4: 钢琴旋律 (Piano) ===
    piano_track = MidiTrack()
    mid.tracks.append(piano_track)
    piano_track.append(MetaMessage('track_name', name='Piano', time=0))
    
    # 设置乐器: 原声钢琴 (Acoustic Grand Piano = 0)
    piano_track.append(Message('program_change', program=0, time=0, channel=3))
    
    # 简单的旋律动机
    melody = [60, 62, 64, 62, 60, 58, 60, 62]  # C-D-E-D-C-Bb-C-D
    
    for bar in range(8):
        for note in melody:
            piano_track.append(Message('note_on', note=note, velocity=70, time=0, channel=3))
            piano_track.append(Message('note_off', note=note, velocity=0, time=240, channel=3))
    
    # 保存文件
    mid.save(filename)
    print(f"[OK] 伴奏已生成: {filename}")
    print(f"[INFO] 8小节, 85 BPM, Boom Bap风格")
    print(f"[INFO] 包含: 鼓组, 贝斯, 合成铺底, 钢琴旋律")
    return filename

def create_simple_kick_snare(filename="simple_beat.mid"):
    """简化版：只有底鼓和军鼓"""
    
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    track.append(MetaMessage('set_tempo', tempo=705882, time=0))
    
    KICK = 36
    SNARE = 38
    
    for _ in range(16):  # 16小节
        # Kick
        track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=9))
        track.append(Message('note_off', note=KICK, velocity=0, time=480, channel=9))
        # Snare
        track.append(Message('note_on', note=SNARE, velocity=90, time=0, channel=9))
        track.append(Message('note_off', note=SNARE, velocity=0, time=480, channel=9))
        # Kick
        track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=9))
        track.append(Message('note_off', note=KICK, velocity=0, time=480, channel=9))
        # Snare (加重)
        track.append(Message('note_on', note=SNARE, velocity=100, time=0, channel=9))
        track.append(Message('note_off', note=SNARE, velocity=0, time=480, channel=9))
    
    mid.save(filename)
    print(f"[OK] 简化节拍已生成: {filename}")
    return filename

if __name__ == "__main__":
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 生成完整伴奏
    create_boom_bap_beat("output/ai_startup_beat.mid")
    
    # 生成简化节拍
    create_simple_kick_snare("output/simple_beat.mid")
    
    print("\n[USAGE] 使用说明:")
    print("1. 安装mido: pip install mido")
    print("2. 安装 fluidsynth 或 timidity 播放MIDI")
    print("3. 用DAW软件(如LMMS/Cakewalk)导入.mid文件")
    print("4. 替换音源为更好的鼓组和乐器")
