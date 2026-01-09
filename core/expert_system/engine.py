import json
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_kb():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'data', 'knowledge_base.json')
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Database tidak ditemukan di: {json_path}")
        
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_score(val1, val2):
    try:
        return (float(val1 or 0) + float(val2 or 0)) / 2
    except (ValueError, TypeError):
        return 0.5

def get_expert_analysis(form_data):
    kb = load_kb()
    experts = kb.get('experts', {})
    theories = kb.get('theories', {})
    
    scores = {
        'visual_learning': calculate_score(form_data.get('s1'), form_data.get('s2')),
        'auditory_learning': calculate_score(form_data.get('s3'), form_data.get('s4')),
        'read_write_learning': calculate_score(form_data.get('s5'), form_data.get('s6')),
        'kinesthetic_learning': calculate_score(form_data.get('s7'), form_data.get('s8'))
    }
    
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    primary_key, primary_val = sorted_scores[0]
    secondary_key, secondary_val = sorted_scores[1]
    
    is_multimodal = (primary_val - secondary_val) < 0.1
    dom_sensorik = primary_key

    deep_val = calculate_score(form_data.get('p1'), form_data.get('p2'))
    sprint_val = calculate_score(form_data.get('p3'), form_data.get('p4'))
    dom_psikologis = 'deep_worker' if deep_val >= sprint_val else 'sprint_learner'
    
    solitary_val = calculate_score(form_data.get('so1'), form_data.get('so2'))
    social_val = calculate_score(form_data.get('so3'), form_data.get('so4'))
    dom_sosial = 'solitary_learner' if solitary_val >= social_val else 'social_learner'
    
    seq_val = calculate_score(form_data.get('k1'), form_data.get('k2'))
    global_val = calculate_score(form_data.get('k3'), form_data.get('k4'))
    dom_kognitif = 'sequential_learner' if seq_val >= global_val else 'global_learner'

    personality_path = []
    
    if dom_sosial == 'solitary_learner':
        personality_path.append("Siapin zona fokus. Cari tempat yang sepi, pakai headset anti-berisik, atau masuk ke ruangan tertutup biar nggak keganggu.")
    else:
        personality_path.append("Environment: Cari 'Accountability Partner' atau tempat umum agar tetap termotivasi.")

    strategy_msg = ""
    if dom_psikologis == 'deep_worker':
        if 'visual' in dom_sensorik:
            strategy_msg = "Deep Work: Blok waktu 90 menit untuk menggambar Mind Map raksasa."
        elif 'auditory' in dom_sensorik:
            strategy_msg = "Deep Work: Dengarkan materi panjang tanpa jeda, lalu rekam ulang pemahamanmu."
        elif 'kinesthetic' in dom_sensorik:
            strategy_msg = "Deep Work: Bangun simulasi atau model fisik sampai prototype selesai."
        else:
            strategy_msg = "Deep Work: Baca buku teks mendalam dan tulis ulang menjadi jurnal terstruktur."
    else: 
        base_sprint = "Sprint 25:5 (Pomodoro). "
        if 'visual' in dom_sensorik:
            strategy_msg = base_sprint + "Gunakan flashcards bergambar untuk hafalan cepat."
        elif 'kinesthetic' in dom_sensorik:
            strategy_msg = base_sprint + "Lakukan aktivitas fisik ringan sambil menghafal poin kunci."
        else:
            strategy_msg = base_sprint + "Baca ringkasan cepat lalu tes diri sendiri."
            
    personality_path.append(strategy_msg)

    if dom_kognitif == 'global_learner':
        personality_path.append("Processing: Skim seluruh materi untuk paham 'Big Picture' dulu baru masuk ke detail.")
    else:
        personality_path.append("Processing: Ikuti silabus secara linear. Pastikan bab 1 paham 100% sebelum ke bab 2.")

    if is_multimodal:
        formatted_sec = secondary_key.replace('_learning', '').replace('_', ' ').capitalize()
        personality_path.append(f"Hybrid Note: Gabungkan metode utama dengan metode {formatted_sec} untuk retensi terbaik.")

    final_data_pakar = []
    keys_to_fetch = [dom_sensorik, dom_psikologis, dom_kognitif]
    
    for key in keys_to_fetch:
        if key in theories:
            theory_item = theories[key].copy()
            expert_id = theory_item.get('expert_id')
            if expert_id and expert_id in experts:
                theory_item['pakar'] = experts[expert_id]
            final_data_pakar.append(theory_item)

    def format_label(txt):
        return txt.replace('_learning', '').replace('_', ' ').capitalize()
    
    descriptions = {
        "Visual": "Model pembelajaran visual adalah pendekatan belajar yang mengandalkan penglihatan (mata) sebagai indra utama untuk memahami materi, di mana informasi paling efektif diterima melalui gambar, grafik, diagram, warna, video, dan tulisan yang terstruktur visual seperti mind map atau catatan berwarna, karena individu cenderung lebih mudah menyerap konsep yang disajikan secara visual daripada teks panjang atau instruksi verbal saja.",
        "Auditory": "Model pembelajaran auditori adalah pendekatan belajar yang mengandalkan pendengaran (telinga) sebagai indra utama untuk memahami materi, di mana individu lebih efektif menyerap informasi melalui mendengarkan penjelasan verbal, diskusi, ceramah, rekaman audio, atau musik, sehingga mereka cenderung lebih mudah mengingat konsep yang disampaikan secara lisan dibandingkan dengan membaca teks atau melihat gambar.",
        "Read write": "Model pembelajaran baca-tulis adalah pendekatan belajar yang mengandalkan teks tertulis sebagai media utama untuk memahami materi, di mana individu lebih efektif menyerap informasi melalui membaca buku, artikel, catatan, dan menulis ulang konsep dalam bentuk tulisan, sehingga mereka cenderung lebih mudah mengingat dan memahami materi yang disajikan secara tertulis dibandingkan dengan metode visual atau auditori.",
        "kinesthetic": "Model pembelajaran kinestetik adalah pendekatan belajar yang mengandalkan pengalaman fisik dan gerakan tubuh sebagai cara utama untuk memahami materi, di mana individu lebih efektif menyerap informasi melalui aktivitas langsung, praktik, eksperimen, atau simulasi, sehingga mereka cenderung lebih mudah mengingat konsep yang dipelajari melalui tindakan fisik dibandingkan dengan metode visual atau auditori."
}

    primary_label = format_label(dom_sensorik)

    return {
        "profile": {
            "primary": primary_label,
            "description": descriptions.get(primary_label, ""),
            "secondary": format_label(secondary_key) if is_multimodal else None,
            "psikologis": format_label(dom_psikologis),
            "sosial": format_label(dom_sosial),
            "kognitif": format_label(dom_kognitif),
            "confidence": int(primary_val * 100),
            "is_multimodal": is_multimodal,
            "personality_path": personality_path,
            "scores": {k.replace('_learning', ''): v for k, v in scores.items()}
        },
        "data_pakar": final_data_pakar
    }