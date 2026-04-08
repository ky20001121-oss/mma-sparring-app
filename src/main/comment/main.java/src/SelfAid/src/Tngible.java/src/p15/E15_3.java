package p15;

import java.text.SimpleDateFormat; // スタンプ（書式）の道具
import java.util.Calendar;         // 計算機付きカレンダーの道具
import java.util.Date;             // 日付の写真データ


public class E15_3 {
    public static void main(String[] args) {
        
        // ① 現在の日時を「写真」として撮る
        Date now = new Date();
        System.out.println("今の写真（Date）：" + now);

        // ② 写真を「計算機付きカレンダー」の中にセットする
        Calendar c = Calendar.getInstance();
        c.setTime(now);
        System.out.println("カレンダーに読み込み完了！");

        // ③ 今日の「日」が何日か、数字で取り出す
        int day = c.get(Calendar.DAY_OF_MONTH);
        System.out.println("取り出した『日』の数値：" + day);

        // ④ その数字に100を足して、カレンダーにセットし直す
        // ★ここが魔法！月や年も自動で繰り上がります
        c.set(Calendar.DAY_OF_MONTH, day + 100);
        System.out.println("カレンダー上で100日進めました...");

        // ⑤ 計算が終わったカレンダーから、また「写真（Date）」に戻す
        Date future = c.getTime();
        System.out.println("100日後の写真（Date）：" + future);

        // ⑥ 「西暦...」という形のスタンプを用意して、画面に表示！
        SimpleDateFormat f = new SimpleDateFormat("西暦yyyy年MM月dd日");
        System.out.println("【最終結果】： " + f.format(future));
        
    }
}