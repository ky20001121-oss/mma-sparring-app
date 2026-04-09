import streamlit as st
from datetime import date
import os
from collections import Counter
import sqlite3
import pandas as pd
import plotly.express as px
from supabase import create_client

st.set_page_config(page_title="格闘技スパーリング記録アプリ", layout="wide")

# Page configuration
st.title("格闘技スパーリング記録アプリ")

SUPABASE_TABLE = "records"


def create_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None
    # 改行コードを除去してクリーンなAPIキーにする
    url = url.strip()
    key = key.strip()
    return create_client(url, key)


supabase_client = create_supabase_client()


# SQLite テーブル作成
def init_db():
    conn = sqlite3.connect('mma_records.db')
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
        memo TEXT,
        fatigue TEXT,
        opponent_weight TEXT,
        own_weight TEXT
    )''')
    
    cursor = conn.execute("PRAGMA table_info(records)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'fatigue' not in columns:
        conn.execute('ALTER TABLE records ADD COLUMN fatigue TEXT')
    if 'opponent_weight' not in columns:
        conn.execute('ALTER TABLE records ADD COLUMN opponent_weight TEXT')
    if 'own_weight' not in columns:
        conn.execute('ALTER TABLE records ADD COLUMN own_weight TEXT')
    
    conn.commit()
    conn.close()


# SQLite からデータ読み込み
def load_records_sqlite():
    conn = sqlite3.connect('mma_records.db')
    cursor = conn.execute('SELECT * FROM records')
    rows = cursor.fetchall()
    records = []
    for row in rows:
        record = {
            "id": row[0],
            "練習日": date.fromisoformat(row[1]),
            "対戦相手": row[2],
            "結果": row[3],
            "集中度": row[4],
            "食事": row[5],
            "相手のスタイル": row[6],
            "相手の体格": row[7],
            "前日の過ごし方": row[8],
            "メモ": row[9],
            "当日の疲労度": row[10] if len(row) > 10 else "",
            "相手の体重": row[11] if len(row) > 11 else "",
            "自分の体重": row[12] if len(row) > 12 else ""
        }
        records.append(record)
    conn.close()
    return records


# Supabase からデータ読み込み
def load_records_supabase():
    if not supabase_client:
        return []
    try:
        response = supabase_client.table(SUPABASE_TABLE).select('*').order('practice_date').execute()
        records = []
        for row in response.data:
            record = {
                "id": row.get('id'),
                "練習日": date.fromisoformat(row.get('practice_date')) if row.get('practice_date') else date.today(),
                "対戦相手": row.get('opponent_name', ''),
                "結果": row.get('result', ''),
                "集中度": row.get('concentration', 3),
                "食事": row.get('meal', ''),
                "相手のスタイル": row.get('opponent_style', ''),
                "相手の体格": row.get('opponent_build', ''),
                "前日の過ごし方": row.get('previous_day', ''),
                "メモ": row.get('memo', ''),
                "当日の疲労度": row.get('fatigue', ''),
                "相手の体重": row.get('opponent_weight', ''),
                "自分の体重": row.get('own_weight', '')
            }
            records.append(record)
        return records
    except Exception as e:
        raise RuntimeError(f"Supabase読み込みエラー: {e}")


# データベース読み込み
def load_records():
    if supabase_client:
        try:
            return load_records_supabase()
        except Exception as e:
            st.warning(f"Supabase読み込みエラーのためSQLiteを使用します: {e}")
    return load_records_sqlite()


# Supabase にデータを保存
def insert_record_supabase(record):
    try:
        response = supabase_client.table(SUPABASE_TABLE).insert(record).execute()
        return response
    except Exception as e:
        raise RuntimeError(f"Supabase保存エラー: {e}")


# SQLite にデータを保存
def insert_record_sqlite(record):
    conn = sqlite3.connect('mma_records.db')
    conn.execute(
        'INSERT INTO records (practice_date, opponent_name, result, concentration, meal, opponent_style, opponent_build, previous_day, memo, fatigue, opponent_weight, own_weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            record['practice_date'],
            record['opponent_name'],
            record['result'],
            record['concentration'],
            record['meal'],
            record['opponent_style'],
            record['opponent_build'],
            record['previous_day'],
            record['memo'],
            record['fatigue'],
            record['opponent_weight'],
            record['own_weight']
        )
    )
    conn.commit()
    conn.close()


# データ保存
def save_record(record):
    if supabase_client:
        try:
            insert_record_supabase(record)
            return
        except Exception as e:
            st.warning(f"Supabase保存エラーのためSQLiteに保存します: {e}")
    insert_record_sqlite(record)


# Supabase で更新
def update_record_supabase(record_id, record):
    try:
        response = supabase_client.table(SUPABASE_TABLE).update(record).eq('id', record_id).execute()
        return response
    except Exception as e:
        raise RuntimeError(f"Supabase更新エラー: {e}")


# SQLite で更新
def update_record_sqlite(record_id, record):
    conn = sqlite3.connect('mma_records.db')
    conn.execute(
        '''UPDATE records SET practice_date = ?, opponent_name = ?, result = ?, concentration = ?, meal = ?, opponent_style = ?, opponent_build = ?, opponent_weight = ?, own_weight = ?, previous_day = ?, fatigue = ?, memo = ? WHERE id = ?''',
        (
            record['practice_date'],
            record['opponent_name'],
            record['result'],
            record['concentration'],
            record['meal'],
            record['opponent_style'],
            record['opponent_build'],
            record['opponent_weight'],
            record['own_weight'],
            record['previous_day'],
            record['fatigue'],
            record['memo'],
            record_id
        )
    )
    conn.commit()
    conn.close()


def update_record(record_id, record):
    if supabase_client:
        try:
            update_record_supabase(record_id, record)
            return
        except Exception as e:
            st.warning(f"Supabase更新エラーのためSQLiteを更新します: {e}")
    update_record_sqlite(record_id, record)


# Supabase で削除
def delete_record_supabase(record_id):
    try:
        response = supabase_client.table(SUPABASE_TABLE).delete().eq('id', record_id).execute()
        return response
    except Exception as e:
        raise RuntimeError(f"Supabase削除エラー: {e}")


# SQLite で削除
def delete_record_sqlite(record_id):
    conn = sqlite3.connect('mma_records.db')
    conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()


def delete_record(record_id):
    if supabase_client:
        try:
            delete_record_supabase(record_id)
            return
        except Exception as e:
            st.warning(f"Supabase削除エラーのためSQLiteを削除します: {e}")
    delete_record_sqlite(record_id)


# Supabase への移行
def migrate_sqlite_to_supabase():
    if not supabase_client:
        return
    try:
        # 既存データをチェック
        response = supabase_client.table(SUPABASE_TABLE).select('id').limit(1).execute()
        if response.data:
            return
        sqlite_records = load_records_sqlite()
        if not sqlite_records:
            return
        payload = []
        for record in sqlite_records:
            payload.append({
                'practice_date': record['練習日'].isoformat(),
                'opponent_name': record['対戦相手'],
                'result': record['結果'],
                'concentration': record['集中度'],
                'meal': record['食事'],
                'opponent_style': record['相手のスタイル'],
                'opponent_build': record['相手の体格'],
                'previous_day': record['前日の過ごし方'],
                'memo': record['メモ'],
                'fatigue': record['当日の疲労度'],
                'opponent_weight': record['相手の体重'],
                'own_weight': record['自分の体重']
            })
        supabase_client.table(SUPABASE_TABLE).insert(payload).execute()
        st.success('SQLiteの記録をSupabaseに移行しました。')
    except Exception as e:
        st.warning(f"Supabase移行中にエラーが発生しました: {e}")


# 初期化
init_db()
if supabase_client:
    migrate_sqlite_to_supabase()

# ページ選択
page = st.sidebar.radio("ナビゲーション", ["📝 記録する", "📋 記録一覧", "📊 グラフ"])

if page == "📝 記録する":
    st.header("新しい記録を入力")
    
    with st.form("record_form"):
        practice_date = st.date_input("練習日", value=date.today())
        opponent_name = st.text_input("対戦相手の名前")
        result = st.text_input("スパーリングの結果")
        concentration = st.slider("集中度", min_value=1, max_value=5, value=3)
        meal = st.text_input("直前の食事")
        opponent_style = st.text_input("相手のスタイル")
        opponent_build = st.text_input("相手の体格")
        opponent_weight = st.text_input("相手の体重")
        own_weight = st.text_input("当日の自分の体重")
        previous_day = st.text_input("前日の過ごし方")
        fatigue = st.text_input("当日の疲労度")
        memo = st.text_area("メモ")
        
        submitted = st.form_submit_button("保存")
        
        if submitted:
            if opponent_name:
                record = {
                    'practice_date': practice_date.isoformat(),
                    'opponent_name': opponent_name,
                    'result': result,
                    'concentration': concentration,
                    'meal': meal,
                    'opponent_style': opponent_style,
                    'opponent_build': opponent_build,
                    'opponent_weight': opponent_weight,
                    'own_weight': own_weight,
                    'previous_day': previous_day,
                    'fatigue': fatigue,
                    'memo': memo
                }
                save_record(record)
                st.success("記録が保存されました！")
            else:
                st.error("対戦相手の名前を入力してください")

elif page == "📋 記録一覧":
    st.header("これまでの記録")
    
    records = load_records()
    
    if records:
        for record in records:
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**練習日**: {record['練習日']}")
                    st.write(f"**対戦相手**: {record['対戦相手']}")
                    st.write(f"**相手の体重**: {record['相手の体重']}")
                    st.write(f"**自分の体重**: {record['自分の体重']}")
                    st.write(f"**結果**: {record['結果']}")
                with col2:
                    st.write(f"**集中度**: {record['集中度']}")
                    st.write(f"**食事**: {record['食事']}")
                    st.write(f"**相手のスタイル**: {record['相手のスタイル']}")
                    st.write(f"**相手の体格**: {record['相手の体格']}")
                    st.write(f"**前日の過ごし方**: {record['前日の過ごし方']}")
                    st.write(f"**当日の疲労度**: {record['当日の疲労度']}")
                st.write(f"**メモ**: {record['メモ']}")
                
                edit_expander = st.expander("編集する")
                with edit_expander:
                    with st.form(f"edit_form_{record['id']}"):
                        edit_date = st.date_input("練習日", value=record['練習日'], key=f"edit_date_{record['id']}")
                        edit_opponent_name = st.text_input("対戦相手の名前", value=record['対戦相手'], key=f"edit_opponent_name_{record['id']}")
                        edit_result = st.text_input("スパーリングの結果", value=record['結果'], key=f"edit_result_{record['id']}")
                        edit_concentration = st.slider("集中度", min_value=1, max_value=5, value=record['集中度'], key=f"edit_concentration_{record['id']}")
                        edit_meal = st.text_input("直前の食事", value=record['食事'], key=f"edit_meal_{record['id']}")
                        edit_opponent_style = st.text_input("相手のスタイル", value=record['相手のスタイル'], key=f"edit_opponent_style_{record['id']}")
                        edit_opponent_build = st.text_input("相手の体格", value=record['相手の体格'], key=f"edit_opponent_build_{record['id']}")
                        edit_opponent_weight = st.text_input("相手の体重", value=record['相手の体重'], key=f"edit_opponent_weight_{record['id']}")
                        edit_own_weight = st.text_input("当日の自分の体重", value=record['自分の体重'], key=f"edit_own_weight_{record['id']}")
                        edit_previous_day = st.text_input("前日の過ごし方", value=record['前日の過ごし方'], key=f"edit_previous_day_{record['id']}")
                        edit_fatigue = st.text_input("当日の疲労度", value=record['当日の疲労度'], key=f"edit_fatigue_{record['id']}")
                        edit_memo = st.text_area("メモ", value=record['メモ'], key=f"edit_memo_{record['id']}")
                        updated = st.form_submit_button("更新", use_container_width=True, key=f"update_{record['id']}")
                        if updated:
                            if edit_opponent_name:
                                updated_record = {
                                    'practice_date': edit_date.isoformat(),
                                    'opponent_name': edit_opponent_name,
                                    'result': edit_result,
                                    'concentration': edit_concentration,
                                    'meal': edit_meal,
                                    'opponent_style': edit_opponent_style,
                                    'opponent_build': edit_opponent_build,
                                    'opponent_weight': edit_opponent_weight,
                                    'own_weight': edit_own_weight,
                                    'previous_day': edit_previous_day,
                                    'fatigue': edit_fatigue,
                                    'memo': edit_memo
                                }
                                update_record(record['id'], updated_record)
                                st.success("記録が更新されました！")
                                st.experimental_rerun()
                            else:
                                st.error("対戦相手の名前を入力してください")
                
                delete_col, _ = st.columns([1, 4])
                with delete_col:
                    if st.button("削除", key=f"delete_{record['id']}"):
                        delete_record(record['id'])
                        st.success("記録を削除しました。")
                        st.experimental_rerun()
    else:
        st.write("まだ記録がありません.")

elif page == "📊 グラフ":
    st.header("データ分析")
    
    records = load_records()
    
    if records:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            wins = sum(1 for r in records if '勝ち' in r['結果'])
            st.metric("総勝ち数", wins)
        
        with col2:
            losses = sum(1 for r in records if '負け' in r['結果'])
            st.metric("総負け数", losses)
        
        with col3:
            draws = sum(1 for r in records if '引き分け' in r['結果'])
            st.metric("総引き分け数", draws)
        
        st.divider()
        
        # 集中度の平均
        avg_concentration = sum(r['集中度'] for r in records) / len(records)
        st.metric("集中度の平均", f"{avg_concentration:.1f}")
        
        # 対戦相手の統計
        st.subheader("対戦相手別の記録")
        opponent_counts = Counter(r['対戦相手'] for r in records)
        df_opponents = pd.DataFrame(opponent_counts.items(), columns=['対戦相手', '回数'])
        fig_opponents = px.bar(df_opponents, x='回数', y='対戦相手', orientation='h', labels={'回数': '試合数', '対戦相手': '対戦相手'})
        fig_opponents.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_opponents, use_container_width=True)
        
        # 集中度の分布
        st.subheader("集中度の分布")
        concentration_counts = Counter(r['集中度'] for r in records)
        df_concentration = pd.DataFrame(concentration_counts.items(), columns=['集中度', '回数']).sort_values('集中度')
        df_concentration['集中度'] = df_concentration['集中度'].astype(str)
        fig_concentration = px.bar(df_concentration, x='集中度', y='回数', labels={'回数': '試合数', '集中度': '集中度'})
        fig_concentration.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_concentration, use_container_width=True)
    else:
        st.write("表示するデータがありません。")
    
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