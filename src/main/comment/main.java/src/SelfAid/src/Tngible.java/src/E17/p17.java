package E17;

import java.io.IOException;

public class p17 {
    public static void main(String[] args) {

        // --- 【前半：Null（空っぽ）のチェック】 ---
        String s = null;
        try {
            // 中身がないのに長さを数えようとする
            System.out.println(s.length()); 
        } catch (NullPointerException e) {
            // 「ヌルポ」が起きた時の専用窓口
            System.out.println("NullPointerExceptionが発生しました");
            System.out.println("例外の内容：" + e.getMessage());
            e.printStackTrace(); // 履歴を表示
            System.out.println("スタックトレースの要素数：" + e.getStackTrace().length);
        }

        // --- 【後半：数字変換のチェック】 ---
        try {
            // 漢字の「三」を数字にしようとする
            int num = Integer.parseInt("三  ");
            System.out.println("変換した数値：" + num);
        } catch (NumberFormatException e) {
            // 「数字じゃないよ」エラーが起きた時の専用窓口
            System.out.println("NumberFormatExceptionが発生しました");
            System.out.println("例外の内容：" + e.getMessage());
            e.printStackTrace(); // 履歴を表示
            System.out.println("スタックトレースの要素数：" + e.getStackTrace().length);
        }
    }
}