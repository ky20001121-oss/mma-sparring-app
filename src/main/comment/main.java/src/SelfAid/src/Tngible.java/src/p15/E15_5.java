package p15;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class E15_5 {
    public static void main(String[] args) {
        
        // ① 現在の日時を取得する（これだけでOK！）
        LocalDate now = LocalDate.now();
        
        // ② 100日後を計算する（Calendarに変換しなくていい！）
        LocalDate future = now.plusDays(100);
        
        // ③ 指定した形式で表示する（SimpleDateFormatの代わり）
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("西暦yyyy年MM月dd日");
        
        System.out.println("現在： " + now.format(fmt));
        System.out.println("100日後： " + future.format(fmt));
        
    }
}
    

