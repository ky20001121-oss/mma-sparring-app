import streamlit as st
from datetime import date
import os
from collections import Counter
import sqlite3
import pandas as pd

# タイトル
st.title("格闘技スパーリング記録アプリ")

# データベース接続とテーブル作成
conn = sqlite3.connect('mma_records.db')  # データベースファイルに接続
conn.execute('''CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY,
    practice_date TEXT,
    opponent_name TEXT,
    result TEXT,
    concentration INTEGER,
    meal TEXT,
    opponent_style TEXT,
    opponent_build TEXT,
    previous_day TEXT,
    memo TEXT
)''')  # テーブルが存在しなければ作成
conn.commit()  # 変更を保存

# データの読み込み
cursor = conn.execute('SELECT * FROM records')
rows = cursor.fetchall()
st.session_state.records = []
for row in rows:
    record = {
        "練習日": date.fromisoformat(row[1]),  # TEXTからdate型に変換
        "対戦相手": row[2],
        "結果": row[3],
        "集中度": row[4],
        "食事": row[5],
        "相手のスタイル": row[6],
        "相手の体格": row[7],
        "前日の過ごし方": row[8],
        "メモ": row[9]
    }
    st.session_state.records.append(record)
conn.close()  # 接続を閉じる

# 入力フォーム
st.header("新しい記録を入力")

practice_date = st.date_input("練習日", value=date.today())
opponent_name = st.text_input("対戦相手の名前")
result = st.selectbox("スパーリングの結果", ["一本勝ち", "一本負け", "判定勝ち", "判定負け", "引き分け"])
concentration = st.slider("集中度", min_value=1, max_value=5, value=3)
meal = st.selectbox("直前の食事", ["食べた", "食べてない", "軽く食べた"])
opponent_style = st.selectbox("相手のスタイル", ["ストライカー", "グラップラー", "レスラー"])
opponent_build = st.selectbox("相手の体格", ["大きい", "同じくらい", "小さい"])
previous_day = st.selectbox("前日の過ごし方", ["しっかり休憩", "筋トレした", "夜更かしした"])
memo = st.text_area("メモ")

# 保存ボタン
if st.button("保存"):
    new_record = {
        "練習日": practice_date,
        "対戦相手": opponent_name,
        "結果": result,
        "集中度": concentration,
        "食事": meal,
        "相手のスタイル": opponent_style,
        "相手の体格": opponent_build,
        "前日の過ごし方": previous_day,
        "メモ": memo
    }
    st.session_state.records.append(new_record)
    
    # データベースに保存
    conn = sqlite3.connect('mma_records.db')  # データベースに接続
    conn.execute('INSERT INTO records VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
        practice_date.isoformat(),  # dateをTEXTに変換
        opponent_name,
        result,
        concentration,
        meal,
        opponent_style,
        opponent_build,
        previous_day,
        memo
    ))
    conn.commit()  # 変更を保存
    conn.close()  # 接続を閉じる
    
    st.success("記録が保存されました！")

# 記録リストの表示
st.header("記録リスト")
if st.session_state.records:
    for i, record in enumerate(st.session_state.records):
        st.subheader(f"記録 {i+1}")
        st.write(f"練習日: {record['練習日']}")
        st.write(f"対戦相手: {record['対戦相手']}")
        st.write(f"結果: {record['結果']}")
        st.write(f"集中度: {record['集中度']}")
        st.write(f"食事: {record['食事']}")
        st.write(f"相手のスタイル: {record['相手のスタイル']}")
        st.write(f"相手の体格: {record['相手の体格']}")
        st.write(f"前日の過ごし方: {record['前日の過ごし方']}")
        st.write(f"メモ: {record['メモ']}")
        st.divider()
else:
    st.write("まだ記録がありません。")

# データ分析
st.header("データ分析")
if st.session_state.records:
    records = st.session_state.records
    
    # 勝敗カウント
    wins = sum(1 for r in records if '勝ち' in r['結果'])
    losses = sum(1 for r in records if '負け' in r['結果'])
    draws = sum(1 for r in records if '引き分け' in r['結果'])
    
    st.subheader("勝敗統計")
    st.write(f"総試合数: {len(records)}")
    st.write(f"勝ち: {wins}, 負け: {losses}, 引き分け: {draws}")
    
    # 集中度の平均
    avg_concentration = sum(r['集中度'] for r in records) / len(records)
    st.subheader("集中度")
    st.write(f"平均集中度: {avg_concentration:.2f}")
    
    # 食事ごとの勝率
    st.subheader("食事ごとの勝率")
    meal_stats = {}
    for r in records:
        meal = r['食事']
        if meal not in meal_stats:
            meal_stats[meal] = {'total': 0, 'wins': 0}
        meal_stats[meal]['total'] += 1
        if '勝ち' in r['結果']:
            meal_stats[meal]['wins'] += 1
    
    for meal, stats in meal_stats.items():
        win_rate = stats['wins'] / stats['total'] * 100 if stats['total'] > 0 else 0
        st.write(f"{meal}: 試合数 {stats['total']}, 勝率 {win_rate:.1f}%")
    
    # 苦手分析
    st.header("苦手分析")
    
    # 天敵スタイル
    st.subheader("天敵スタイル")
    lost_matches = [r for r in records if '負け' in r['結果']]
    if lost_matches:
        enemy_combinations = [(r['相手のスタイル'], r['相手の体格']) for r in lost_matches]
        most_common = Counter(enemy_combinations).most_common(1)
        if most_common:
            style, build = most_common[0][0]
            count = most_common[0][1]
            st.write(f"最も負けた組み合わせ: {style} × {build} (負け数: {count})")
    else:
        st.write("負けた試合がありません。")
    
    # コンディション分析
    st.subheader("コンディション分析")
    high_concentration = [r for r in records if r['集中度'] >= 4]
    low_concentration = [r for r in records if r['集中度'] <= 2]
    
    if high_concentration:
        st.write("**高集中度時 (4-5)**")
        high_meal = Counter(r['食事'] for r in high_concentration)
        high_previous = Counter(r['前日の過ごし方'] for r in high_concentration)
        st.write(f"食事: {dict(high_meal)}")
        st.write(f"前日の過ごし方: {dict(high_previous)}")
    
    if low_concentration:
        st.write("**低集中度時 (1-2)**")
        low_meal = Counter(r['食事'] for r in low_concentration)
        low_previous = Counter(r['前日の過ごし方'] for r in low_concentration)
        st.write(f"食事: {dict(low_meal)}")
        st.write(f"前日の過ごし方: {dict(low_previous)}")
    
    if not high_concentration and not low_concentration:
        st.write("集中度のデータが不足しています。")
    
    # 成功分析
    st.header("成功分析")
    successful_matches = [r for r in records if '勝ち' in r['結果']]
    if successful_matches:
        # 食事の影響
        st.subheader("食事の影響")
        meal_counter = Counter(r['食事'] for r in successful_matches)
        most_common_meal = meal_counter.most_common(1)[0][0] if meal_counter else "なし"
        st.write(f"上手くいった日に最も多かった食事: {most_common_meal}")
        
        # 前日の過ごし方
        st.subheader("前日の過ごし方")
        previous_counter = Counter(r['前日の過ごし方'] for r in successful_matches)
        most_common_previous = previous_counter.most_common(1)[0][0] if previous_counter else "なし"
        st.write(f"上手くいった日に共通する前日の過ごし方: {most_common_previous}")
        
        # 集中度の相関
        st.subheader("集中度の相関")
        successful_avg_concentration = sum(r['集中度'] for r in successful_matches) / len(successful_matches)
        other_matches = [r for r in records if '勝ち' not in r['結果']]
        if other_matches:
            other_avg_concentration = sum(r['集中度'] for r in other_matches) / len(other_matches)
            st.write(f"上手くいった日の平均集中度: {successful_avg_concentration:.2f}")
            st.write(f"その他の日の平均集中度: {other_avg_concentration:.2f}")
        else:
            st.write(f"上手くいった日の平均集中度: {successful_avg_concentration:.2f}")
            st.write("その他の日のデータがありません。")
        
        # データの可視化
        st.subheader("データの可視化")
        # 食事の円グラフ
        meal_df = pd.DataFrame(list(meal_counter.items()), columns=['食事', '回数'])
        st.bar_chart(meal_df.set_index('食事'))
        
        # 前日の過ごし方の棒グラフ
        previous_df = pd.DataFrame(list(previous_counter.items()), columns=['前日の過ごし方', '回数'])
        st.bar_chart(previous_df.set_index('前日の過ごし方'))
    else:
        st.write("成功した試合がありません。")
    
    # あなたの必勝パターン
    st.header("あなたの必勝パターン")
    if successful_matches:
        # 最も多い組み合わせを特定
        pattern_counter = Counter((r['前日の過ごし方'], r['食事'], r['集中度']) for r in successful_matches)
        if pattern_counter:
            most_common_pattern = pattern_counter.most_common(1)[0][0]
            previous, meal, conc = most_common_pattern
            st.write(f"前日に{previous}して、当日に{meal}を食べ、集中度が{conc}以上の時に、最も高いパフォーマンスを発揮しています。")
        else:
            st.write("パターンを特定できませんでした。")
    else:
        st.write("成功した試合がありません。")
else:
    st.write("データがありません。")